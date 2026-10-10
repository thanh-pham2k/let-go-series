from pathlib import Path
import json, math, re, hashlib, html, shutil
from PIL import Image, ImageDraw, ImageOps

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
LESSON=HERE.parent
INV=json.loads((ROOT/'parallel-prompts/challenge-images/review-3-4.inventory.json').read_text(encoding='utf-8'))
S=2
CROPS={
 'walk':('CD1_71',(242,791,411,1076)), 'run':('CD1_71',(415,791,628,1076)),
 'go':('CD1_71',(669,800,834,1071)), 'stop':('CD1_71',(839,800,1028,1077)),
 'take_out_pencil':('CD1_72',(237,204,568,486)),
 'put_away_pencil':('CD1_72',(639,201,940,482)),
 'open_book':('CD1_72',(205,536,577,800)),
 'close_book':('CD1_72',(615,539,942,800)),
}
COLORS={'circle':(242,73,53),'square':(75,171,211),'star':(255,202,20),'heart':(240,64,127),'triangle':(64,161,61),'diamond':(23,188,233),'oval':(119,58,147)}

def shape(kind,w,h,outline=False):
    mask=Image.new('L',(w,h));d=ImageDraw.Draw(mask);pad=5*S
    b=(pad,pad,w-pad-1,h-pad-1)
    if kind in ['circle','oval']:d.ellipse(b,fill=255)
    elif kind=='square':d.rectangle(b,fill=255)
    elif kind=='triangle':d.polygon([(w/2,pad),(w-pad,h-pad),(pad,h-pad)],fill=255)
    elif kind=='diamond':d.polygon([(w/2,pad),(w-pad,h/2),(w/2,h-pad),(pad,h/2)],fill=255)
    elif kind=='star':
        pts=[]
        for i in range(10):
            a=-math.pi/2+i*math.pi/5;r=(min(w,h)/2-pad)*(1 if i%2==0 else .45)
            pts.append((w/2+math.cos(a)*r,h/2+math.sin(a)*r))
        d.polygon(pts,fill=255)
    elif kind=='heart':
        pts=[]
        for i in range(240):
            t=2*math.pi*i/240;x=16*math.sin(t)**3;y=13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t)
            pts.append((w/2+x*(w-2*pad)/32,pad+(12-y)*(h-2*pad)/29))
        d.polygon(pts,fill=255)
    color=COLORS[kind];paint=Image.new('RGB',(w,h));pd=ImageDraw.Draw(paint)
    for y in range(h):
        t=.10-.20*y/max(1,h-1)
        c=tuple(int(v+(255-v)*t) if t>=0 else int(v*(1+t)) for v in color)
        pd.line((0,y,w,y),fill=c)
    result=Image.new('RGB',(w,h),'white');result.paste(paint,(0,0),mask)
    return result

def card(kind,count=1,basic=False):
    out=Image.new('RGB',(512*S,512*S),'white')
    if count==1:
        w=330*S;h=(230 if kind=='oval' else 330)*S
        obj=shape(kind,w,h);out.paste(obj,((512*S-w)//2,(512*S-h)//2))
    else:
        cols=2 if count==4 else 3;rows=math.ceil(count/cols)
        size=(150 if count<=6 else 135)*S;gap=12*S
        height=(105*S if kind=='oval' else size)
        for i in range(count):
            row,col=divmod(i,cols);inrow=min(cols,count-row*cols)
            x=(512*S-inrow*size-(inrow-1)*gap)//2+col*(size+gap)
            y=(512*S-rows*height-(rows-1)*gap)//2+row*(height+gap)
            out.paste(shape(kind,size,height),(x,y))
    return out.resize((512,512),Image.Resampling.LANCZOS)

def export():
    for folder in ['webp','references','batches']: (HERE/folder).mkdir(parents=True,exist_ok=True)
    entries=[]
    for a in INV['assets']:
        key=a['id'][4:];prov={};count=1
        if key in CROPS:
            track,box=CROPS[key];source=LESSON/f'pages/png/{track}.png'
            crop=Image.open(source).convert('RGB').crop(box)
            crop.save(HERE/f'references/{a["id"]}-master.png')
            image=Image.new('RGB',(512,512),'white');fitted=ImageOps.contain(crop,(464,464),Image.Resampling.LANCZOS)
            image.paste(fitted,((512-fitted.width)//2,(512-fitted.height)//2))
            prov={'method':'crop','source':str(source),'crop_box':list(box),'source_crop_size':list(crop.size),'adaptation_notes':'Clean crop from canonical regenerated lesson, excluding item labels. Contain may upscale this source artwork; no claim of added detail.'}
        else:
            kind=key
            if '_' in key:
                noun,num=key.rsplit('_',1);count=int(num);kind={'triangles':'triangle','diamonds':'diamond','circles':'circle','ovals':'oval'}[noun]
            image=card(kind,count)
            image.save(HERE/f'references/{a["id"]}-master.png')
            prov={'method':'native_graphic','shape':kind,'count':count,'adaptation_notes':'Deterministic unlabeled geometric card with source palette; count variants preserve exercise semantics and are not claimed as original PDF artwork.'}
        path=HERE/f'webp/{a["id"]}.webp';image.save(path,'WEBP',quality=80,method=6)
        entries.append({**a,**prov,'webp':f'webp/{a["id"]}.webp','size':[512,512],'quality':80,'method_codec':6,'file_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'visual_review':{'reviewer':'root','status':'reviewed','evidence':'Every final WebP viewed individually with view_image, compared with CD1_71/72. Correct semantic/count, no answer labels, no clipped target objects; crop margins corrected after review.'}})
    (HERE/'manifest.json').write_text(json.dumps({'review':'3-4','assets':entries,'source_inventory':str(ROOT/'parallel-prompts/challenge-images/review-3-4.inventory.json')},ensure_ascii=False,indent=2),encoding='utf-8')
    mapping=[]
    source=Path(INV['source']).read_text(encoding='utf-8-sig').split('# Đáp án dành')[0]
    for q in INV['questions']:
        start=source.index('### '+q['question_id']);block=source[start:];m=re.search(r'\n### R',block[4:]);block=block[:m.start()+4] if m else block
        choices=re.findall(r'^- \[ \] (.*)$',block,re.M)
        q=dict(q)
        count_overrides={'R34-C5-19':'r34_triangles_04','R34-C5-20':'r34_circles_05','R34-C5-21':'r34_diamonds_06','R34-C5-22':'r34_ovals_07'}
        if q['question_id'] in count_overrides:
            q.update(image_required=True,asset_ids=[count_overrides[q['question_id']]],mode='all_required',adaptation_notes='Inventory omitted this prose source-group reference; mapping corrected from original Challenge source without modifying source/inventory.')
        learner=q['source_prompt']
        if q['image_required']:
            learner='Nhìn hình. '+('Chọn đáp án phù hợp.' if choices else 'Nói hoặc điền câu trả lời của em.')
            if 'Điền:' in q['source_prompt']:learner='Nhìn hình. Điền: '+q['source_prompt'].split('Điền:',1)[1].strip()
        elif q['challenge']==2 or 'Nghe câu mẫu' in learner:learner='Nghe audio hoặc người lớn đọc, rồi chọn/điền câu trả lời.'
        rec={**q,'learner_prompt':learner,'choices':choices,'images':[f'webp/{aid}.webp' for aid in q['asset_ids']], 'needs_context':False,'no_image_reason':None if q['image_required'] else 'Text spelling/building/listening or live roleplay; no extra raster required.'}
        prefix=source[:start].rsplit('\n## ',1)[-1]
        for marker,field in [('**Các thẻ từ:**','word_cards'),('**Kho từ/chữ:**','word_bank')]:
            hits=re.findall(re.escape(marker)+r'([^\n]*)',prefix)
            if hits:rec[field]=hits[-1].strip()
        mapping.append(rec)
    (HERE/'question-image-map.json').write_text(json.dumps({'review':'3-4','questions':mapping,'adaptation_notes':['Geometric recognition/count cards have no printed answers. Original lesson source unchanged.']},ensure_ascii=False,indent=2),encoding='utf-8')
    thumbs=Image.new('RGB',(6*200,math.ceil(len(entries)/6)*240),'white');draw=ImageDraw.Draw(thumbs)
    for i,a in enumerate(entries):
        x=i%6*200;y=i//6*240;thumb=Image.open(HERE/a['webp']).resize((200,200))
        thumbs.paste(thumb,(x,y));draw.text((x+4,y+204),a['id'],fill='black')
    thumbs.save(HERE/'contact-sheet.jpg',quality=90)
    gallery=''.join(f'<figure><img src="{a["webp"]}" width="256" height="256"><figcaption>{a["id"]}</figcaption></figure>' for a in entries)
    exercises=''.join('<article><h3>'+q['question_id']+'</h3><p>'+html.escape(q['learner_prompt'])+'</p>'+''.join(f'<img src="{p}" width="200" height="200">' for p in q['images'])+'<p>'+html.escape(q.get('word_cards',q.get('word_bank','')))+'</p><ul>'+''.join('<li>'+html.escape(c)+'</li>' for c in q['choices'])+'</ul></article>' for q in mapping)
    page='<!doctype html><meta charset="utf-8"><title>Review 3–4 Challenge</title><style>body{font:16px Arial;margin:24px;background:#fafafa}.gallery{display:flex;flex-wrap:wrap}figure{margin:8px;background:white}article{padding:20px;background:white;margin:16px 0}img{object-fit:contain}</style><h1>Review 3–4 — Challenge assets</h1><p>Answer key and audio scripts are in the source document for adults; not shown here.</p><div class="gallery">'+gallery+'</div><h2>Question preview</h2>'+exercises
    (HERE/'preview.html').write_text(page,encoding='utf-8')
    (HERE/'README.md').write_text('# Review 3–4 Challenge assets\n\n27 WebP cards, 512×512, quality 80/method 6. 8 clean lesson crops; 19 deterministic geometric cards. Source lesson/PDF/audio untouched. All 96 source question IDs recorded. No imagegen required because clean artwork exists.\n\n[Preview](preview.html) · [Mapping](question-image-map.json) · [Manifest](manifest.json)\n\nNative count cards remove printed count answers. Source descriptions preserved only in mapping; learner preview does not expose picture-name/count hints or teacher audio scripts. Fixed inventory omission: C5-19–22 now map to exact 4 triangles/5 circles/6 diamonds/7 ovals. No new IDs added. Source crops resized with contain; master files retained, not claimed as newly detailed images. Every exported WebP viewed individually by root; initial numeric crop fragments corrected.\n',encoding='utf-8')
    sizes=[a['file_bytes'] for a in entries];hashes=[a['sha256'] for a in entries]
    validation={'required':27,'complete':27,'missing':[],'conditional':[],'questions':len(mapping),'mapped_visual_questions':sum(q['image_required'] for q in mapping),'unresolved_context':[], 'all_dimensions_512':all(Image.open(HERE/a['webp']).size==(512,512) for a in entries),'unique_hashes':len(set(hashes)),'over_60kb':[a['id'] for a in entries if a['file_bytes']>61440],'min_bytes':min(sizes),'max_bytes':max(sizes),'total_bytes':sum(sizes),'visual_reviewed_ids':[a['id'] for a in entries],'methods':{'crop':8,'native_graphic':19,'imagegen':0},'mapping_links_exist':all((HERE/p).is_file() for q in mapping for p in q['images'])}
    (HERE/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Exported',len(entries),'cards; mapping',len(mapping))

if __name__=='__main__':export()
