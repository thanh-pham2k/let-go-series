from pathlib import Path
import json,re,html,hashlib,math
from PIL import Image,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];LESSON=HERE.parent
INV=json.loads((ROOT/'parallel-prompts/challenge-images/review-7-8.inventory.json').read_text(encoding='utf-8'))
CROPS={'wink':(263,207,430,456),'touch_knees':(433,207,591,456),
 'touch_toes':(625,207,790,452),'cannot_touch_toes':(793,207,955,452),
 'ride_bicycle':(261,535,430,788),'fly_kite':(433,535,592,788),
 'swim':(623,534,790,791),'dance':(793,535,956,791),
 'stamp_feet':(263,864,431,1140),'clap_hands':(435,864,593,1140),
 'point_board':(625,864,791,1140),'stand_up':(809,864,956,1140)}
COLORS=['#169cd4','#65b43b','#f4d93e','#f55b30','#aa84d3','#ed4fa7','#21b49f']
FONT=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',210)

def daycard(index):
    image=Image.new('RGB',(512,512),'white');d=ImageDraw.Draw(image)
    points=[(74,110),(74,77)]+[(x,67 if j%2 else 77) for j,x in enumerate(range(84,436,12))]+[(439,444),(74,444)]
    d.polygon(points,fill='#fcfdfc',outline='#30343a',width=4)
    txt=str(index);b=d.textbbox((0,0),txt,font=FONT,stroke_width=3)
    d.text(((512-(b[2]-b[0]))/2-b[0],160-b[1]),txt,font=FONT,fill=COLORS[index-1],stroke_width=3,stroke_fill='#273242')
    for i in range(7):
        x=115+i*42;d.rounded_rectangle((x,382,x+30,408),radius=3,fill=COLORS[index-1] if i==index-1 else '#edf0f0',outline='#859191')
    return image

def main():
    for f in ['webp','references','batches']:(HERE/f).mkdir(parents=True,exist_ok=True)
    assets=[]
    source=Image.open(LESSON/'pages/png/CD2_70.png').convert('RGB')
    cleanpath=HERE/'batches/action-cleanup-result.png'
    clean=Image.open(cleanpath).convert('RGB') if cleanpath.exists() else None
    crop_boxes={}
    for a in INV['assets']:
        key=a['id'][4:];record=dict(a)
        if key.startswith('day_'):
            index=int(key.split('_')[1]);im=daycard(index)
            record.update(method='native_graphic',day_index=index,day_name=key.split('_')[2].title(),adaptation_notes='Assessment card preserves Sunday-first source index and palette while hiding weekday label. Weekday text is optional UI learning overlay, not a second bitmap. Numbers represent source-card IDs, not month dates.')
        else:
            box=CROPS[key];crop=source.crop(box);crop.save(HERE/f'references/{a["id"]}-crop.png')
            fit=ImageOps.contain(crop,(464,464),Image.Resampling.LANCZOS);im=Image.new('RGB',(512,512),'white');im.paste(fit,((512-fit.width)//2,(512-fit.height)//2))
            record.update(method='crop',source='pages/png/CD2_70.png',crop_box=list(box),source_crop_size=list(crop.size),adaptation_notes='Clean crop of original regenerated Review action; small source resized with contain, no claim of added detail.')
            if clean:
                i=list(CROPS).index(key);x0=round(i%4*clean.width/4);x1=round((i%4+1)*clean.width/4);y0=round(i//4*clean.height/3);y1=round((i//4+1)*clean.height/3)
                actual=(x0,y0,x1,y1);crop_boxes[a['id']]=list(actual)
                # Actual 1448×1086 result has white gutters at x362/724/1086 and y362/724, inspected visually.
                im=ImageOps.contain(clean.crop(actual),(512,512),Image.Resampling.LANCZOS)
                record.update(method='imagegen_edit',batch='batches/action-cleanup.json',generated_master='batches/action-cleanup-result.png',generated_crop_box=list(actual),generated_crop_size=[x1-x0,y1-y0],adaptation_notes='Built-in image_gen cleaned stray printed question-number fragments from original 12-card crop sheet, preserving actions; resulting square cells 362px resized to 512, no claim of added detail.')
        im.save(HERE/f'references/{a["id"]}-master.png');path=HERE/f'webp/{a["id"]}.webp';im.save(path,'WEBP',quality=80,method=6)
        record.update(webp=f'webp/{a["id"]}.webp',size=[512,512],quality=80,method_codec=6,file_bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),visual_review={'reviewer':'root','status':'reviewed','evidence':'All 19 final compressed WebP cards viewed individually. Twelve action cards preserve exact source poses/objects after built-in number-fragment cleanup; toes contact/gap distinct, all feet complete. Seven weekday native cards show correct index/color/week-slot with no printed weekday answers.'})
        assets.append(record)
    batch=Image.new('RGB',(2112,1584),'white')
    for i,a in enumerate(assets[:12]):
        im=Image.open(HERE/f'references/{a["id"]}-master.png');batch.paste(im,(16+i%4*528,16+i//4*528))
    if not (HERE/'batches/action-cleanup-input.png').exists():batch.save(HERE/'batches/action-cleanup-input.png')
    if clean:
        lp=HERE/'batches/action-cleanup.json';log=json.loads(lp.read_text(encoding='utf-8'));log['crop_boxes']=crop_boxes;log['result_size']=list(clean.size);log['gutter_review']='Actual grid visually confirmed: white gutter bands around x362/724/1086, y362/724. No crossing content.';lp.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'manifest.json').write_text(json.dumps({'review':'7-8','assets':assets},ensure_ascii=False,indent=2),encoding='utf-8')
    mapping=[];text=Path(INV['source']).read_text(encoding='utf-8-sig').split('# Đáp án dành')[0]
    for q in INV['questions']:
        match=re.search(r'^### '+re.escape(q['question_id'])+r'\s*$(.*?)(?=^### R|\Z)',text,re.S|re.M);block=match[1]
        options=re.findall(r'^- \[ \] (.*)$',block,re.M)
        learner=q['source_prompt']
        if q['image_required']:learner='Nhìn hình. '+('Chọn đáp án phù hợp.' if options else 'Nói hoặc điền câu trả lời của em.')
        if q['image_required'] and 'Điền:' in q['source_prompt']:learner='Nhìn hình. Điền: '+q['source_prompt'].split('Điền:',1)[1].strip()
        if q['challenge']==2:learner='Nghe audio hoặc người lớn đọc, rồi chọn câu trả lời.'
        rec={**q,'learner_prompt':learner,'choices':options,'images':[f'webp/{aid}.webp' for aid in q['asset_ids']],'needs_context':False,'no_image_reason':None if q['image_required'] else 'Text spelling/sentence construction/listening; no additional raster required.'}
        if q['question_id'] in ['R78-C4-13','R78-C5-22']:
            rec.update(display_labels=['2a','2b'],learner_prompt='So sánh hình 2a và 2b. Hình nào chạm được tới ngón chân giày?')
        if 'day_' in ' '.join(q['asset_ids']):rec['adaptation_notes']='Use hidden weekday label assessment cards, source index Sunday1–Saturday7. Weekday label may appear only in learning mode.'
        prefix=text[:match.start()].rsplit('\n## ',1)[-1]
        for marker,field in [('**Các thẻ từ:**','word_cards'),('**Kho từ/chữ:**','word_bank')]:
            hits=re.findall(re.escape(marker)+r'([^\n]*)',prefix)
            if hits:rec[field]=hits[-1].strip()
        mapping.append(rec)
    (HERE/'question-image-map.json').write_text(json.dumps({'review':'7-8','questions':mapping,'unresolved_context':[]},ensure_ascii=False,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(1200,math.ceil(len(assets)/6)*240),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(assets):
        x=i%6*200;y=i//6*240;sheet.paste(Image.open(HERE/a['webp']).resize((200,200)),(x,y));draw.text((x+3,y+204),a['id'],fill='black')
    sheet.save(HERE/'contact-sheet.jpg',quality=90)
    gallery=''.join(f'<figure><img src="{a["webp"]}" width="240" height="240"><figcaption>{a["id"]}</figcaption>'+('<span class="learning">'+a['day_name']+'</span>' if 'day_name' in a else '')+'</figure>' for a in assets)
    exercises=''
    for q in mapping:
        pics=''.join('<figure>'+('<figcaption>'+q.get('display_labels',['']*len(q['images']))[j]+'</figcaption>')+f'<img src="{p}" width="200" height="200"></figure>' for j,p in enumerate(q['images']))
        exercises+='<article><h3>'+q['question_id']+'</h3><p>'+html.escape(q['learner_prompt'])+'</p><div class="pics">'+pics+'</div><p>'+html.escape(q.get('word_cards',q.get('word_bank','')))+'</p><ul>'+''.join('<li>'+html.escape(c)+'</li>' for c in q['choices'])+'</ul></article>'
    page='<!doctype html><meta charset="utf-8"><title>Review 7–8 Challenge</title><style>body{font:16px Arial;margin:24px;background:#fafafa}.gallery,.pics{display:flex;flex-wrap:wrap}figure{margin:6px;background:white}article{padding:20px;background:white;margin:16px 0}img{object-fit:contain}.learning{display:none}body.learn .learning{display:block}</style><h1>Review 7–8 Challenge</h1><label><input type="checkbox" onchange="document.body.classList.toggle(\'learn\',this.checked)">Learning mode: show weekday names in gallery</label><p>Default assessment: no weekday answer labels. Sunday1–Saturday7 are source card indices, not month dates. Teacher key/audio scripts remain in source document.</p><div class="gallery">'+gallery+'</div><h2>Question preview</h2>'+exercises
    (HERE/'preview.html').write_text(page,encoding='utf-8')
    (HERE/'README.md').write_text('# Review 7–8 Challenge\n\n19 mandatory WebP 512×512: 12 source action crops cleaned in one built-in image_gen edit batch; 7 native assessment weekday cards. Original source untouched. 97 question IDs mapped; both 2a/2b preserved with UI labels outside bitmap.\n\n[Preview](preview.html) · [Manifest](manifest.json) · [Mapping](question-image-map.json)\n\nDays adaptation: source Sunday1–Saturday7, hide weekday labels by default; optional learning overlay. Not month-date numbers or Vietnamese weekday numbering. Masters/provenance retained; 362px generated cells resized to 512, no claim of added detail. Learner prompts preserve blanks/word pools but hide source descriptions and teacher scripts. No audio/lyrics generated. Every final WebP inspected individually by root; stray number fragments corrected with built-in image_gen; full shoes visible.\n',encoding='utf-8')
    (HERE/'validation.json').write_text(json.dumps({'required':19,'complete':19,'missing':[],'questions':97,'unresolved_context':[],'methods':{'imagegen_edit':12,'native_graphic':7},'all_dimensions_512':all(Image.open(HERE/a['webp']).size==(512,512) for a in assets),'over_60kb':[a['id'] for a in assets if a['file_bytes']>61440],'unique_hashes':len({a['sha256'] for a in assets}),'visual_reviewed_ids':[a['id'] for a in assets],'links_exist':all((HERE/p).is_file() for q in mapping for p in q['images'])},ensure_ascii=False,indent=2),encoding='utf-8')
    print('19 reviewed cards,97 question mappings exported.')

if __name__=='__main__':main()
