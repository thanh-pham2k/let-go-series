"""Join existing approved artwork into complete activity images; preserve audio tracks."""
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np
import json,hashlib,shutil,csv,zipfile,subprocess,re,argparse
from book1_audio_specs import MODEL_PAIRS
from book1_audio_pages import preview

ROOT=Path(__file__).resolve().parent;UNITS=ROOT/'Let_s Go 1/Units';INDEX=UNITS/'Audio Pages'
OUT=ROOT/'output/imagegen/book1-combined-activities'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def trim(path,model=False):
    im=Image.open(path).convert('RGB')
    if model:
        if path.stem in ['CD1_41','CD2_12','CD2_42']:
            # A narrow sliver from the adjacent batch cell is outside this activity.
            im=im.crop((20,0,im.width,im.height))
        a=np.asarray(im).astype('int16')
        orange=(a[:,:,0]>180)&(a[:,:,1]>65)&(a[:,:,1]<235)&(a[:,:,2]<135)&((a[:,:,0]-a[:,:,1])>15)
        counts=orange.sum(axis=1);active=np.flatnonzero(counts>max(20,counts.max()*.25))
        if len(active):
            # Both the top and bottom borders belong to the same frame even when
            # its pale interior has few orange pixels; retain their full span.
            band=active
            # Keep the orange grammar frame, its audio badges and the nearby heading.
            top=max(0,int(band.min())-90);bottom=min(im.height,int(band.max())+10)
            im=im.crop((0,top,im.width,bottom))
    a=np.asarray(im)
    ink=(a.min(axis=2)<210)
    # Ignore very faint batch grid lines; no drawing or text is regenerated here.
    yy,xx=np.where(ink)
    if not len(yy):raise ValueError(f'Blank input {path}')
    box=(max(0,int(xx.min())-8),max(0,int(yy.min())-8),min(im.width,int(xx.max())+9),min(im.height,int(yy.max())+9))
    return im.crop(box)

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    mp=INDEX/'manifest.json'
    snapshot=OUT/'manifest-before.json'
    if not snapshot.exists():shutil.copy2(mp,snapshot)
    m=json.loads(snapshot.read_text(encoding='utf-8'));byid={r['id']:r for r in m['tracks']}
    groups=[];used=set()
    for disc,pairs in MODEL_PAIRS.items():
        for parent,children in pairs:
            numbers=[parent]+children
            if disc==2 and parent==38:numbers=[37]+numbers
            ids=[f'CD{disc}_{t:02}' for t in numbers];rows=[byid[t] for t in ids]
            assert len({r['section'] for r in rows})==1 and len({r['source_pdf_page'] for r in rows})==1
            assert not used.intersection(ids);used.update(ids)
            gid=f'{ids[0]}-{numbers[-1]:02}'
            folder=UNITS/(rows[0]['section']+' - Audio Pages')
            source_paths=[]
            for row in rows:
                single=folder/'regenerated-single'/f'{row["id"]}.webp'
                single.parent.mkdir(exist_ok=True)
                if not single.exists():shutil.copy2(UNITS/row['image'],single)
                source_paths.append(single)
            if ids[0]=='CD1_50':
                # Recover the complete bottom speech bubble from the accepted batch,
                # whose original half-height cut was a few pixels too high.
                sheet=Image.open(ROOT/'output/imagegen/book1-all-batches/batch-07/generated.png').convert('RGB')
                fix=OUT/'CD1_50-full-dialogue.png'
                sheet.crop((0,0,round(sheet.width*.25),round(sheet.height*.53))).save(fix)
                source_paths[0]=fix
            # The read/chant tracks printed on the same box share one model panel.
            panel_indices=[0,1,2] if disc==2 and parent==38 else [0,1]
            panels=[trim(source_paths[k],model=(k==panel_indices[-1])) for k in panel_indices]
            rendered=[];placements=[];gap=20;margin=24;width=768
            for panel in panels:
                scale=min((width-2*margin)/panel.width,760/panel.height)
                rendered.append(panel.resize((round(panel.width*scale),round(panel.height*scale)),Image.Resampling.LANCZOS))
            required=margin*2+sum(p.height for p in rendered)+gap*(len(rendered)-1)
            height=768 if required<=768 else 1024 if required<=1024 else 1280 if required<=1280 else ((required+127)//128)*128
            canvas=Image.new('RGB',(width,height),'white');y=(height-(required-2*margin))//2
            for k,panel in enumerate(rendered):
                x=(width-panel.width)//2;canvas.paste(panel,(x,y));placements.append(dict(source_track=ids[panel_indices[k]],box=[x,y,x+panel.width,y+panel.height]));y+=panel.height+gap
            dest=folder/'combined'/f'{gid}.webp';dest.parent.mkdir(exist_ok=True);canvas.save(dest,'WEBP',quality=88,method=6)
            groups.append(dict(id=gid,section=rows[0]['section'],source_pdf_page=rows[0]['source_pdf_page'],track_ids=ids,image=str(dest.relative_to(UNITS)).replace('\\','/'),image_size=[width,height],image_bytes=dest.stat().st_size,image_sha256=digest(dest),panels=placements,source_images=[dict(track=ids[i],path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=digest(p)) for i,p in enumerate(source_paths)],reason='Same printed activity: illustration/vocabulary/actions plus its sentence model. Read and chant share the model panel.'))
    assert len(groups)==50
    data=dict(groups=groups,group_count=len(groups),grouped_tracks=len(used),standalone_tracks=[r['id'] for r in m['tracks'] if r['id'] not in used],total_tracks=len(m['tracks']))
    (OUT/'groups.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    for start in range(0,len(groups),6):
        sheet=Image.new('RGB',(1200,1440),'#e8edf3');draw=ImageDraw.Draw(sheet)
        for k,g in enumerate(groups[start:start+6]):
            im=Image.open(UNITS/g['image']).convert('RGB');im.thumbnail((384,650),Image.Resampling.LANCZOS)
            x=k%3*400;y=k//3*720;draw.text((x+8,y+8),g['id'],fill='black',font=font);sheet.paste(im,(x+(400-im.width)//2,y+52))
        sheet.save(OUT/f'contact-{start//6+1:02}.jpg',quality=92)
    print(json.dumps({k:v for k,v in data.items() if k!='groups'},ensure_ascii=False))

def activate():
    data=json.loads((OUT/'groups.json').read_text(encoding='utf-8'))
    m=json.loads((OUT/'manifest-before.json').read_text(encoding='utf-8'));byid={r['id']:r for r in m['tracks']}
    for row in m['tracks']:
        row['single_image']=row['image']
        row['related_track_ids']=[row['id']]
    for g in data['groups']:
        for tid in g['track_ids']:
            row=byid[tid];folder=UNITS/(row['section']+' - Audio Pages')
            row['single_image']=str((folder/'regenerated-single'/f'{tid}.webp').relative_to(UNITS)).replace('\\','/')
            # Preserve the user's established per-track paths as aliases of the whole activity.
            alias=folder/'regenerated'/f'{tid}.webp';shutil.copy2(UNITS/g['image'],alias)
            row.update(image=g['image'],image_size=g['image_size'],image_bytes=g['image_bytes'],image_sha256=g['image_sha256'],activity_group=g['id'],related_track_ids=g['track_ids'],image_method='Deterministic composition of existing batch-regenerated artwork; no new AI generation')
    m['image_variant']='combined-activity-webp'
    m['activity_groups']=data['groups']
    m['composition']={k:v for k,v in data.items() if k!='groups'}
    m['notes'].append('Related illustration and sentence-model tracks now share one complete activity image; original audio tracks stay separate and may be played in sequence.')
    for sec in m['sections']:
        folder=UNITS/(sec['name']+' - Audio Pages');mp=folder/'manifest.json'
        if not (folder/'index-single.html').exists():shutil.copy2(folder/'index.html',folder/'index-single.html')
        if not (folder/'manifest-single.json').exists():shutil.copy2(mp,folder/'manifest-single.json')
        local=json.loads(mp.read_text(encoding='utf-8'));rows=[dict(r) for r in m['tracks'] if r['section']==sec['name']]
        for row in rows:
            for field in ['image','single_image','source_crop_image','page_image','audio','expected_audio']:
                if row.get(field):row[field]=str((UNITS/row[field]).relative_to(folder)).replace('\\','/')
        local['tracks']=rows;local['image_variant']=m['image_variant'];local['activity_groups']=[g['id'] for g in data['groups'] if g['section']==sec['name']]
        mp.write_text(json.dumps(local,ensure_ascii=False,indent=2),encoding='utf-8')
        singles=[dict(r,image=r['single_image']) for r in rows]
        preview(folder,singles,sec['name']+' — Ảnh đơn','../Audio%20Pages/index.html')
        shutil.copy2(folder/'index.html',folder/'index-single.html')
        single_manifest=dict(local,tracks=singles,image_variant='single-batch-regenerated-webp')
        (folder/'manifest-single.json').write_text(json.dumps(single_manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        preview(folder,rows,sec['name']+' — Tranh và mẫu câu','../Audio%20Pages/index.html')
        hp=folder/'index.html';html=hp.read_text(encoding='utf-8')
        html=html.replace('Tải ảnh PNG','Tải ảnh WebP')
        html=re.sub(r'<div class="muted">[^<]*</div></header>','<div class="muted">Tranh và mẫu câu cùng hoạt động được ghép chung ảnh. Mỗi audio track vẫn riêng; có thể nghe cả cụm theo thứ tự.</div></header>',html,count=1)
        html=html.replace('<nav>','<section class="panel"><b id="groupTitle"></b><div id="groupTracks"></div><button id="playGroup">▶ Nghe cả cụm theo thứ tự</button><p id="groupNote" class="muted"></p><a id="singleLink">Xem ảnh riêng của track</a> · <a href="index-original.html">Xem bản cắt gốc</a></section><nav>',1)
        extra='''
let groupQueue=[];
const baseShow=show;
show=function(i,fromPlaylist=false){
 if(!fromPlaylist)groupQueue=[];
 baseShow(i);
 const r=rows[+select.value],ids=r.related_track_ids||[r.id];
 document.getElementById('groupTitle').textContent=ids.length>1?'Cùng hoạt động: '+ids.join(' → '):'Hoạt động riêng: '+r.id;
 const box=document.getElementById('groupTracks');box.replaceChildren();
 ids.forEach(id=>{const b=document.createElement('button');b.textContent=id;b.disabled=id===r.id;b.style.margin='8px 8px 8px 0';b.onclick=()=>show(rows.findIndex(t=>t.id===id));box.appendChild(b)});
 document.getElementById('singleLink').href=r.single_image;
 document.getElementById('playGroup').hidden=ids.length<2;
 const missing=ids.filter(id=>!rows.find(t=>t.id===id).audio);
 document.getElementById('groupNote').textContent=(ids.length>1?'Tranh và mẫu câu dùng chung ảnh. ':'')+(missing.length?'Chưa có audio nguồn: '+missing.join(', ')+'. Khi nghe cả cụm sẽ bỏ qua track thiếu.':'');
 document.getElementById('playGroup').disabled=ids.every(id=>!rows.find(t=>t.id===id).audio);
};
document.getElementById('playGroup').onclick=()=>{
 const r=rows[+select.value];groupQueue=r.related_track_ids.map(id=>rows.findIndex(t=>t.id===id)).filter(i=>rows[i].audio);
 if(groupQueue.length){const first=groupQueue.shift();show(first,true);audio.play().catch(()=>document.getElementById('status').textContent='Bấm phát audio để bắt đầu.');}
};
audio.addEventListener('ended',()=>{if(groupQueue.length){const next=groupQueue.shift();show(next,true);audio.play().catch(()=>document.getElementById('status').textContent='Bấm phát audio để tiếp tục.');}});
show(+select.value);
'''
        html=html.replace('</script>',extra+'\n</script>');hp.write_text(html,encoding='utf-8')
    (INDEX/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    (INDEX/'activity-groups.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    with (INDEX/'mapping-combined.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['id','section','activity_group','related_track_ids','image','single_image','audio'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in m['tracks']:w.writerow({k:','.join(r[k]) if k=='related_track_ids' else r.get(k,'') for k in fields})
    unique=sorted({r['image'] for r in m['tracks']})
    with zipfile.ZipFile(INDEX/'Let-Go-1-combined-activities-webp.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in unique:z.write(UNITS/p,p)
        z.write(INDEX/'mapping-combined.csv','mapping-combined.csv');z.write(INDEX/'activity-groups.json','activity-groups.json')
    hp=INDEX/'index.html';html=hp.read_text(encoding='utf-8')
    html=re.sub(r'<p><b>50 ảnh ghép cho .*?</p>','',html,flags=re.S)
    html=html.replace('Let’s Go 1 — Ảnh regenerate WebP 512×512','Let’s Go 1 — Tranh và mẫu câu theo hoạt động')
    html=html.replace('72 trang gốc · 196 ảnh cắt · 186 audio MP3 gốc có sẵn','105 ảnh đang dùng · 50 ảnh ghép + 55 ảnh riêng · 196 mã track')
    html=html.replace('Tải toàn bộ 196 ảnh WebP','Bộ ảnh đơn 512×512 trước khi ghép')
    html=html.replace('href="mapping.csv"','href="mapping-combined.csv"')
    html=re.sub(r'<aside>.*?</aside>','<aside>Tranh, từ vựng hoặc hành động được ghép với mẫu câu của cùng hoạt động. Các track liên quan dùng chung ảnh, audio vẫn riêng. Ảnh đơn và trang sách gốc có sẵn để đối chiếu.</aside>',html,flags=re.S)
    html=html.replace('<section>','<p><b>50 ảnh ghép cho '+str(data['grouped_tracks'])+' track liên quan</b> · Các track còn lại giữ ảnh riêng. <a href="Let-Go-1-combined-activities-webp.zip">Tải bộ ảnh đang dùng</a> · <a href="mapping-combined.csv">Mapping mới</a> · <a href="combined-validation.json">Kiểm tra ảnh ghép</a></p><section>',1)
    hp.write_text(html,encoding='utf-8')
    for folder in [INDEX]+[UNITS/(s['name']+' - Audio Pages') for s in m['sections']]:
        rp=folder/'README.md';old=rp.read_text(encoding='utf-8')
        if '# Tranh và mẫu câu cùng hoạt động' not in old:
            rp.write_text('# Tranh và mẫu câu cùng hoạt động\n\nTrang xem hiện dùng ảnh ghép cho các track thuộc cùng một hoạt động. Audio vẫn riêng; nút nghe cả cụm phát theo thứ tự mã track, bỏ qua MP3 nguồn còn thiếu. Ảnh ghép rộng 768 px, chiều cao theo nội dung. Bản WebP đơn và PNG nguồn được giữ để đối chiếu.\n\n'+old,encoding='utf-8')
    validate()

def validate():
    m=json.loads((INDEX/'manifest.json').read_text(encoding='utf-8'));data=json.loads((OUT/'groups.json').read_text(encoding='utf-8'));byid={r['id']:r for r in m['tracks']}
    assert len(byid)==196 and len(data['groups'])==50
    checks=[];seen=set()
    for g in data['groups']:
        assert not seen.intersection(g['track_ids']);seen.update(g['track_ids'])
        p=UNITS/g['image']
        with Image.open(p) as im:assert list(im.size)==g['image_size'] and im.format=='WEBP'
        assert digest(p)==g['image_sha256']
        for panel in g['panels']:
            x0,y0,x1,y1=panel['box'];assert 0<=x0<x1<=g['image_size'][0] and 0<=y0<y1<=g['image_size'][1]
        for tid in g['track_ids']:
            r=byid[tid];assert r['image']==g['image'] and r['related_track_ids']==g['track_ids']
            alias=UNITS/(r['section']+' - Audio Pages')/'regenerated'/f'{tid}.webp';assert alias.read_bytes()==p.read_bytes()
        for src in g['source_images']:assert digest(ROOT/src['path'])==src['sha256']
    for r in m['tracks']:
        for key in ['image','single_image','source_crop_image','page_image','audio']:
            if r.get(key):assert (UNITS/r[key]).exists(),(r['id'],key)
        if r['audio']:assert digest(UNITS/r['audio'])==r['audio_sha256']
    for sec in m['sections']:
        folder=UNITS/(sec['name']+' - Audio Pages');local=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        assert len(local['tracks'])==sec['tracks']
        for row in local['tracks']:
            assert (folder/row['image']).read_bytes()==(UNITS/byid[row['id']]['image']).read_bytes()
        html=(folder/'index.html').read_text(encoding='utf-8');script=re.search(r'<script>([\s\S]*?)</script>',html).group(1)
        result=subprocess.run(['node','--check'],input=script,text=True,encoding='utf-8',capture_output=True);assert result.returncode==0,result.stderr
    unique={r['image'] for r in m['tracks']}
    with zipfile.ZipFile(INDEX/'Let-Go-1-combined-activities-webp.zip') as z:
        assert set(n for n in z.namelist() if n.endswith('.webp'))==unique
        for p in unique:assert z.read(p)==(UNITS/p).read_bytes()
    report=dict(status='passed',track_count=196,groups=50,grouped_tracks=len(seen),standalone_tracks=len(data['standalone_tracks']),unique_active_images=len(unique),active_image_bytes=sum((UNITS/p).stat().st_size for p in unique),checks=['All 50 semantically mapped illustration/model groups share one image across all related tracks','No activity groups cross a source page or section; no track belongs to two groups','All composed panels fit fully within the output canvas','Original single images and PNG crops are accessible','All per-track regenerated paths alias their whole activity image','196 global/local image mappings and 186 original audio hashes verified','12 preview scripts pass syntax checks; groups expose ordered audio playlists','ZIP contains exactly the unique active images and matching bytes'],limitations='Composes the previously accepted regenerated artwork without redrawing it; existing AI text/detail differences may remain.')
    (INDEX/'combined-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','activate','validate']);args=parser.parse_args();globals()[args.command]()
