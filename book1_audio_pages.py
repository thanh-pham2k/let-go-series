"""Extract original PDF page and track regions. No generative image editing."""
from pathlib import Path
import json,hashlib,re,shutil,subprocess
import csv,html
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw,ImageFont
import pymupdf as fitz

ROOT=Path(__file__).parent
UNITS=ROOT/'Let_s Go 1/Units'
INDEX=UNITS/'Audio Pages'
INDEX.mkdir(exist_ok=True)
SOURCE=ROOT/'Let_s Go 1/Oxford - Lets Go 1 Students Book 3 Edition.pdf'
SECTIONS=json.loads((UNITS/'source-manifest.json').read_text(encoding='utf-8'))['sections']

def prepare():
    doc=fitz.open(SOURCE)
    for sec in SECTIONS:
        dest=UNITS/(sec['name']+' - Audio Pages')
        for sub in ['pages','tracks','audio']: (dest/sub).mkdir(parents=True,exist_ok=True)
        thumbs=[]
        for i in range(sec['start'],sec['end']+1):
            path=dest/'pages'/f'PDF-{i:03}.png'
            if not path.exists():doc[i-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(path)
            im=Image.open(path).convert('RGB');im.thumbnail((600,790))
            thumbs.append((i,im.copy()))
        sheet=Image.new('RGB',(2400,840*((len(thumbs)+3)//4)),'#eeeeee');draw=ImageDraw.Draw(sheet)
        for k,(i,im) in enumerate(thumbs):
            x=k%4*600;y=k//4*840;sheet.paste(im,(x,y));draw.text((x+12,y+795),f'PDF {i} / printed {i-1}',fill='black',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22))
        sheet.save(INDEX/(sec['name']+' - source-contact.jpg'),quality=94)
    print('Prepared 72 source page PNGs and 12 contact sheets.')

def audio_info(path):
    result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,sample_rate,channels','-of','json',str(path)],capture_output=True,text=True,check=True)
    info=json.loads(result.stdout)
    return dict(duration_seconds=float(info['format']['duration']),streams=info['streams'])

def preview(folder,rows,title,back):
    data=json.dumps(rows,ensure_ascii=False).replace('</','<\\/')
    template='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f6fa;color:#182433;font:16px/1.5 system-ui,sans-serif}header{background:#fff;border-bottom:1px solid #d9e0ea;padding:18px 24px}main{max-width:1040px;margin:auto;padding:20px}h1{font-size:23px;margin:5px 0}a{color:#155bb0}nav{display:flex;gap:10px;align-items:center;flex-wrap:wrap}select{flex:1;min-width:240px}select,button{font:inherit;padding:9px;border:1px solid #c4cfde;border-radius:8px;background:white}button{cursor:pointer}button:disabled{opacity:.35;cursor:default}.panel{padding:18px;background:white;border:1px solid #d9e0ea;border-radius:12px;margin-top:16px}#image{display:block;max-width:100%;height:auto;margin:12px auto 0}audio{width:100%;margin-top:12px}.muted{color:#526379;font-size:14px}details img{max-width:100%;height:auto}#meta{margin:8px 0}#status{color:#b02a2a}
</style><header><a href="__BACK__">← Danh mục Let’s Go 1</a><h1>__TITLE__</h1><div class="muted">Mỗi ảnh cắt tương ứng 1 audio track gốc. Ảnh chỉ chứa hoạt động của track đã chọn. Track đọc và chant cùng một khung trong sách dùng chung khung đó.</div></header><main>
<nav><button id="prev" aria-label="Track trước">← Trước</button><select id="choose" aria-label="Chọn audio track"></select><button id="next" aria-label="Track sau">Tiếp →</button></nav>
<section class="panel"><strong id="label"></strong><div id="meta" class="muted"></div><audio id="audio" controls preload="metadata"></audio><div id="status" role="status"></div><img id="image" alt=""><p><a id="download" download>Tải ảnh PNG</a> · <a id="downloadAudio" download>Tải audio MP3</a></p></section>
<details class="panel"><summary>Trang gốc để đối chiếu (có nhiều track)</summary><p class="muted" id="sourceLabel"></p><img id="source" alt="Trang sách gốc đầy đủ" loading="lazy"></details>
</main><script>
const rows=__DATA__,select=document.getElementById('choose'),audio=document.getElementById('audio');
rows.forEach((r,i)=>{const o=document.createElement('option');o.value=i;o.textContent=r.id+' — '+r.activity;select.appendChild(o)});
function show(i){i=Math.max(0,Math.min(rows.length-1,i));select.value=i;const r=rows[i];audio.pause();if(r.audio){audio.src=r.audio;audio.hidden=false}else{audio.removeAttribute('src');audio.load();audio.hidden=true}document.getElementById('image').src=r.image;document.getElementById('image').alt=r.id+' — '+r.activity;document.getElementById('source').src=r.page_image;document.getElementById('label').textContent=r.id+' — '+r.activity;document.getElementById('meta').textContent='Trang PDF gốc '+r.source_pdf_page+' · Trang in '+r.printed_page+' · Trang trong PDF Unit '+r.section_page+' · '+(r.duration_seconds===null?'Thiếu MP3 nguồn':r.duration_seconds.toFixed(1)+' giây');document.getElementById('sourceLabel').textContent='Trang PDF '+r.source_pdf_page+' — '+r.section;document.getElementById('download').href=r.image;document.getElementById('downloadAudio').href=r.audio||'#';document.getElementById('downloadAudio').hidden=!r.audio;document.getElementById('status').textContent=r.audio?'':'Thiếu file MP3 gốc cho '+r.id+'. Ảnh đã cắt theo đúng ký hiệu track trong sách.';document.getElementById('prev').disabled=i===0;document.getElementById('next').disabled=i===rows.length-1;history.replaceState(null,'','#'+r.id)}
select.addEventListener('change',()=>show(+select.value));document.getElementById('prev').onclick=()=>show(+select.value-1);document.getElementById('next').onclick=()=>show(+select.value+1);audio.addEventListener('error',()=>document.getElementById('status').textContent='Không tải được audio. Kiểm tra file MP3 trong thư mục audio.');const initial=rows.findIndex(r=>r.id===location.hash.slice(1));show(initial<0?0:initial);
</script></html>'''
    (folder/'index.html').write_text(template.replace('__TITLE__',html.escape(title)).replace('__BACK__',back).replace('__DATA__',data),encoding='utf-8')

def build():
    from book1_audio_specs import SPECS
    audio_sources={}
    for disc in [1,2]:
        source_folder=next((ROOT/'Let_s Go 1').glob(f'*Students Book*CD{disc}'))
        for path in source_folder.glob('*.mp3'):
            audio_sources[(disc,int(path.name.split(' ')[0]))]=path
    allrows=[];bysection={s['name']:[] for s in SECTIONS}
    for spec in SPECS:
        d=spec['disc'];t=spec['track'];page=spec['source_pdf_page'];id=f'CD{d}_{t:02}'
        sec=next(s for s in SECTIONS if s['start']<=page<=s['end']);folder=UNITS/(sec['name']+' - Audio Pages')
        image_path=folder/'tracks'/(id+'.png');page_path=folder/'pages'/f'PDF-{page:03}.png'
        with Image.open(page_path) as im:
            w,h=im.size;x0,y0,x1,y1=spec['crop_normalized'];box=[round(x0*w),round(y0*h),round(x1*w),round(y1*h)]
            assert 0<=box[0]<box[2]<=w and 0<=box[1]<box[3]<=h
            crop=im.crop(box)
            # Source-region clipping: remove only the neighbouring section that
            # overlaps the song illustration in the original two-column layout.
            for ex in spec.get('exclude_normalized',[]):
                eb=[round(ex[0]*w)-box[0],round(ex[1]*h)-box[1],round(ex[2]*w)-box[0],round(ex[3]*h)-box[1]]
                ImageDraw.Draw(crop).rectangle(eb,fill='white')
            same=False
            if image_path.exists():
                with Image.open(image_path) as old:same=old.size==crop.size and old.tobytes()==crop.tobytes()
            if not same:crop.save(image_path,compress_level=6)
            image_size=list(crop.size)
        src=audio_sources.get((d,t));target=folder/'audio'/(id+'.mp3')
        if src and (not target.exists() or hashlib.sha256(target.read_bytes()).digest()!=hashlib.sha256(src.read_bytes()).digest()):shutil.copy2(src,target)
        row=dict(**spec,id=id,section=sec['name'],printed_page=page-1,section_page=page-sec['start']+1,source_pdf=str(SOURCE.relative_to(ROOT)).replace('\\','/'),source_section_pdf=sec['pdf'],image='tracks/'+image_path.name,page_image='pages/'+page_path.name,audio='audio/'+target.name if src else None,expected_audio='audio/'+target.name,audio_status='available' if src else 'missing_source',source_audio=str(src.relative_to(ROOT)).replace('\\','/') if src else None,audio_sha256=hashlib.sha256(src.read_bytes()).hexdigest() if src else None,image_size=image_size,source_page_size=[w,h],crop_pixels=box,alignment_method='Printed CD/track symbol on source page; original numbered CD file when available; each crop isolates its own printed activity')
        bysection[sec['name']].append(row)
        grow=dict(row);grow['image']=str(image_path.relative_to(INDEX.parent)).replace('\\','/');grow['audio']=str(target.relative_to(INDEX.parent)).replace('\\','/') if src else None;grow['expected_audio']=str(target.relative_to(INDEX.parent)).replace('\\','/');grow['page_image']=str(page_path.relative_to(INDEX.parent)).replace('\\','/');allrows.append(grow)
    with ThreadPoolExecutor(max_workers=6) as pool:
        infos=list(pool.map(lambda r:audio_info(UNITS/r['audio']) if r['audio'] else dict(duration_seconds=None,streams=[]),allrows))
    for row,info in zip(allrows,infos):
        row.update(info)
        local=next(r for r in bysection[row['section']] if r['id']==row['id']);local.update(info)
    for sec in SECTIONS:
        name=sec['name'];folder=UNITS/(name+' - Audio Pages');rows=bysection[name]
        manifest=dict(section=name,source_pdf_pages=[sec['start'],sec['end']],page_count=sec['end']-sec['start']+1,track_count=len(rows),audio_available=sum(bool(r['audio']) for r in rows),missing_audio=[r['id'] for r in rows if not r['audio']],tracks=rows)
        (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        preview(folder,rows,name,'../Audio%20Pages/index.html')
        lines=[f'# {name} — Trang và ảnh theo audio','',f'- {manifest["page_count"]} ảnh trang đầy đủ trong `pages/`.',f'- {len(rows)} ảnh cắt trong `tracks/`; {manifest["audio_available"]} MP3 nguồn trong `audio/`. Mỗi ảnh gắn một mã track.','- [Mở preview ảnh và audio](index.html) · [Mapping JSON](manifest.json).','- Audio thiếu nguồn: '+(', '.join(manifest['missing_audio']) or 'không có')+'.','', '| Track | Trang PDF gốc | Trang in | Mục | Ảnh | Audio |','|---|---:|---:|---|---|---|']
        lines.extend(f'| {r["id"]} | {r["source_pdf_page"]} | {r["printed_page"]} | {r["activity"]} | [PNG]({r["image"]}) | '+(f'[MP3]({r["audio"]})' if r['audio'] else '**Thiếu file nguồn**')+' |' for r in rows)
        (folder/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        # QA contact sheets contain all final crops, labelled by exact track id.
        for batch in range((len(rows)+7)//8):
            chunk=rows[batch*8:(batch+1)*8];sheet=Image.new('RGB',(2000,1740),'#e7ebf0');draw=ImageDraw.Draw(sheet)
            for k,r in enumerate(chunk):
                with Image.open(folder/r['image']) as im:
                    im.thumbnail((480,790));x=k%4*500;y=k//4*870;sheet.paste(im,(x+(500-im.width)//2,y+46))
                    draw.text((x+10,y+8),r['id']+f' / PDF {r["source_pdf_page"]}',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23),fill='#102238')
            sheet.save(INDEX/(name+f' - crops-{batch+1}.jpg'),quality=92)
    intro=[]
    for d in [1,2]:
        src=audio_sources[(d,1)];intro.append(dict(disc=d,track=1,source_audio=str(src.relative_to(ROOT)).replace('\\','/'),reason='Disc introduction/credits; no printed activity icon in PDF pages 3–74; excluded from lesson crops.'))
    report=dict(source_pdf=str(SOURCE.relative_to(ROOT)).replace('\\','/'),source_pdf_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),page_count=72,track_count=len(allrows),audio_available=sum(bool(r['audio']) for r in allrows),missing_audio=[r['id'] for r in allrows if not r['audio']],sections=[dict(name=s['name'],pages=s['end']-s['start']+1,tracks=len(bysection[s['name']])) for s in SECTIONS],tracks=allrows,excluded_intro_tracks=intro,notes=['Image crops are extracted from the original PDF render without redrawing or altering text.','Each printed track has a distinct image file. Available MP3s are byte-identical copies; missing source audio is explicitly flagged, never replaced by another track.','Only tracks printed on the same activity share a crop; separate activities are isolated.','Unnumbered activities remain on full-page images; no invented audio tracks are assigned.'])
    (INDEX/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    with (INDEX/'mapping.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        fields=['id','disc','track','section','source_pdf_page','printed_page','section_page','activity','kind','image','audio','audio_status','expected_audio','page_image','duration_seconds','source_audio','audio_sha256']
        writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(allrows)
    from urllib.parse import quote
    cards=''.join(f'<article><h2>{html.escape(s["name"])}</h2><p>{s["end"]-s["start"]+1} trang · {len(bysection[s["name"]])} ảnh–audio</p><a href="../{quote(s["name"]+" - Audio Pages")}/index.html">Mở ảnh và nghe audio →</a></article>' for s in SECTIONS)
    (INDEX/'index.html').write_text('<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Let’s Go 1 — Ảnh và audio</title><style>body{background:#f2f5fa;color:#17283e;font:16px/1.6 system-ui;margin:0}main{max-width:1120px;margin:auto;padding:30px}h1{font-size:30px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px}article{background:white;border:1px solid #d6dfeb;border-radius:14px;padding:20px}h2{font-size:20px;margin-top:0}a{color:#155bb0}aside{padding:18px;border-left:4px solid #326ac0;background:white;margin:24px 0}</style><main><h1>Let’s Go 1 — Ảnh theo audio track</h1><p><b>72 trang gốc · 196 ảnh cắt · 186 audio MP3 gốc có sẵn</b></p><aside>CD1_02–CD1_99 và CD2_02–CD2_99. Mỗi ảnh gắn một track cùng mã. Nguồn thiếu CD1_31–CD1_40 (10 MP3); các ảnh này vẫn được cắt đầy đủ và ghi rõ thiếu audio. Track 01 của mỗi CD là phần giới thiệu, không gán vào bài học. Chỉ các track cùng ký hiệu trên một khung bài được dùng chung khung đó. Hoạt động không có ký hiệu audio vẫn được giữ trong ảnh trang đầy đủ.</aside><section>'+cards+'</section><p><a href="mapping.csv">Mapping CSV</a> · <a href="manifest.json">Manifest JSON</a> · <a href="validation.json">Báo cáo kiểm tra</a></p></main></html>',encoding='utf-8')
    lines=['# Let’s Go 1 — Trang và ảnh theo audio','', '**72 ảnh trang đầy đủ; 196 ảnh cắt theo mã track; 186 MP3 gốc có sẵn.**','', '- [Mở preview toàn bộ sách](index.html).','- [Mapping CSV](mapping.csv) · [Manifest JSON](manifest.json) · [Kiểm tra](validation.json).','', '## Quy ước','', '- `pages/PDF-003.png` là trang PDF gốc 3 (trang in 2); số trang được ghi rõ trong metadata.', '- `tracks/CD1_02.png` ghép đúng `audio/CD1_02.mp3`. Không ghép theo thứ tự đọc tên file trên Windows.', '- **Nguồn thiếu CD1_31–CD1_40 (10 MP3).** Vẫn cắt đủ ảnh theo ký hiệu trong sách; manifest và preview đánh dấu thiếu nguồn. Không thay bằng track khác.', '- Tách riêng từng hoạt động theo ký hiệu track; chỉ track đọc và chant trên cùng khung được dùng chung khung.', '- Track 01 của mỗi CD là phần giới thiệu; không có vùng bài học tương ứng trong phạm vi được tách.', '- Hoạt động không có ký hiệu audio được giữ ở ảnh trang đầy đủ. Không tự tạo track.', '- Ảnh được cắt trực tiếp từ trang scan, giữ nguyên chữ và hình. Chất lượng và phần mất mép nếu có của bản scan gốc được giữ nguyên.','', '## Các phần','', '| Phần | Trang | Ảnh–audio | Preview |','|---|---:|---:|---|']
    lines.extend(f'| {s["name"]} | {s["end"]-s["start"]+1} | {len(bysection[s["name"]])} | [Mở](../{quote(s["name"]+" - Audio Pages")}/index.html) |' for s in SECTIONS)
    (INDEX/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Built {len(allrows)} track images, {report["audio_available"]} original MP3s, {len(report["missing_audio"])} missing MP3s, 72 full pages, 12 section previews.',flush=True)

if __name__=='__main__':
    prepare()
    import sys
    if '--build' in sys.argv:build()
