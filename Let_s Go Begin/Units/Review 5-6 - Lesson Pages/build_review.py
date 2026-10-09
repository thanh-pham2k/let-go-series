"""Review 5-6 only. Source scripts and other packages remain read-only."""
from pathlib import Path
from urllib.parse import quote,unquote
import json,re,hashlib,zipfile,argparse,shutil
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
UNITS=ROOT.parent
CD=UNITS.parent/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD2'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
def link(label,target):return f'[{label}]({quote(target,safe="/")})'
def init():
    mapping=read(UNITS.parent/'lets_go_audio_mapping.metadata')
    found=[]
    def visit(v):
        if isinstance(v,dict):
            if v.get('source_pdf')=='Review 5-6.pdf' and isinstance(v.get('audio'),dict):found.append(v)
            else:
                for x in v.values():visit(x)
        elif isinstance(v,list):
            for x in v:visit(x)
    visit(mapping)
    assert [(r['audio']['disc'],r['audio']['track']) for r in found]==[('CD2',35),('CD2',36)]
    write(ROOT/'source.mapping.json',found)
    items=[]
    questions=[('Ở lựa chọn 1a của hình Listen and circle, có bao nhiêu con mèo?', [('A','2'),('B','3'),('C','4')],'B'),('Từ nào chỉ hình thời tiết có lá bay, khăn bay và cây nghiêng?', [('A','cloudy'),('B','windy'),('C','rainy')],'B')]
    contents=[
      {'pairs':[{'number':1,'a':'3 orange/yellow striped cats','b':'4 orange/yellow striped cats'},{'number':2,'a':'2 brown rabbits','b':'5 brown rabbits'},{'number':3,'a':'one white ice cream cone','b':'one yellow layered chocolate cake slice on blue plate'},{'number':4,'a':'one bread slice','b':'one pink/yellow/blue bowl of white rice'},{'number':5,'a':'one boy skipping','b':'same boy jumping with both feet off ground'},{'number':6,'a':'3 children in a line','b':'same 3 children in a circle'}],'printed_text':['Units 5-6 Listen and Review','A. Listen and circle.','CD2 35','1.','2.','3.','4.','5.','6.','a','b','54'],'source_answers':'Unknown; no original listening selections inferred or circled.'},
      {'printed_text':['The Weather','A. Say these.','CD2 36','1. sunny','2. cloudy','3. windy','4. rainy','5. snowy',"It's sunny.",'55'],'weather_semantics':{'sunny':'orange sun blue sky upright green trees','cloudy':'gray/purple clouds; no wind or precipitation','windy':'flying leaves, scarf/hair in wind, bending trees; no rain or snow','rainy':'visible diagonal raindrops','snowy':'falling snow, snow piled on trees/ground/ledge; purple sweater girl shivering'},'same_page_activity':'Large sunny window scene and printed sentence retained using CD2_36 page audio context; no additional audio marker or invented track.'}
    ]
    for i,r in enumerate(found):
        t=f"CD2_{r['audio']['track']}";q,choices,answer=questions[i]
        audio=f"Track{r['audio']['track']}.mp3";assert (CD/audio).exists();shutil.copy2(CD/audio,ROOT/'audio'/audio)
        items.append({'track':t,'audio_key':r['audio']['audio_key'],'exercise':r['exercise']+'. '+r['exercise_title'],'pdf_page':r['pdf_page'],'book_page':r['book_page'],'source_pdf':'../Review 5-6.pdf','source_reference':f'references/{t}.png','source_page':f"source-pages/page-{i+1}.png",'audio_file':'audio/'+audio,'output':{'png':f'pages/png/{t}.png','webp':f'pages/webp/{t}.webp'},'canvas':{'size':[1200,1200],'background':'#FFFFFF'},'layers':[],'question':{'id':'R5-6-'+t,'prompt':q,'choices':[{'id':k,'text':v} for k,v in choices],'correct_choice_id':answer,'show_after_audio':True,'render_in_lesson_image':False},'lesson_specs':contents[i],'adaptation_notes':['One full source page per audio item; no new sub-tracks.','Original choices remain unmarked. Quiz is supplementary visual recognition, not an answer key to original MP3.','Layout may be compacted to fit a square canvas; original order and semantic counts retained.'],'status':'pending_generation'})
    write(ROOT/'manifest.json',{'schema_version':'2.0','review':'5-6','topic':'Listen and Review / The Weather','source_pdf':'../Review 5-6.pdf','source_item_count':2,'image_count':2,'image_fit':'contain','coordinate_system':'pixel boxes [x,y,width,height], top-left origin; crop boxes [left,top,right,bottom]','items':items})
    original=UNITS/'Review 5-6(2).md'
    if not (ROOT/'assets/challenge.original.md').exists():shutil.copy2(original,ROOT/'assets/challenge.original.md')
    template=(UNITS/'Unit 2 - Colors - Lesson Pages/preview.html').read_text(encoding='utf-8')
    template=re.sub(r'const manifest=.*?;\s*\nconst pages=', 'const manifest=/*MANIFEST_JSON*/;\nconst pages=',template,flags=re.S)
    template=template.replace('Unit 2 · Colors','Review 5–6 · Animals, Food & Weather').replace('17 bài nghe','2 bài nghe')
    (ROOT/'preview.template.html').write_text(template,encoding='utf-8')
    print('Initialized 2 exact Review mappings, source specs, questions, copied CD2 audio and private preview template.')
def render_page(p):
    out=Image.new('RGB',tuple(p['canvas']['size']),p['canvas']['background']);draw=ImageDraw.Draw(out)
    for l in p['layers']:
        x,y,w,h=l['box'];assert min(x,y)>=0 and x+w<=1200 and y+h<=1200
        if l['type']=='image':
            with Image.open(ROOT/l['asset']) as im:im=ImageOps.contain(im.convert('RGB'),(w,h),Image.Resampling.LANCZOS);out.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
        elif l['type']=='rect':draw.rectangle((x,y,x+w-1,y+h-1),fill=l['fill'])
        elif l['type']=='text':
            f=font(l['font_size'],l.get('bold',False));bb=draw.multiline_textbbox((0,0),l['text'],font=f);assert bb[2]-bb[0]<=w and bb[3]-bb[1]<=h
            draw.multiline_text((x,y-bb[1]),l['text'],font=f,fill=l.get('color','#25334A'))
        else:raise ValueError(l['type'])
    return out
def import_batch(boxes,note):
    assert note and len(boxes)==2
    m=read(ROOT/'manifest.json');j=read(ROOT/'assets/batches/batch1.json')
    with Image.open(ROOT/'assets/batches/batch1.png') as im:
        for p,box in zip(m['items'],boxes):
            assert 0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height
            name=f"assets/{p['track']}-lesson.png";im.crop(box).convert('RGB').save(ROOT/name)
            p.update(layers=[{'type':'image','asset':name,'box':[0,0,1200,1200]}],source_crop_box=box,generation_batch='batch1',status='reviewed',visual_review=note)
        j.update(status='reviewed',sheet_size=list(im.size),crop_boxes=boxes,visual_review=note,sha256=sha(ROOT/'assets/batches/batch1.png'))
    write(ROOT/'manifest.json',m);write(ROOT/'assets/batches/batch1.json',j)
def render():
    m=read(ROOT/'manifest.json');assert all(p['status']=='reviewed' for p in m['items'])
    sheet=Image.new('RGB',(1200,640),'#EDF2F7');d=ImageDraw.Draw(sheet)
    for i,p in enumerate(m['items']):
        im=render_page(p);im.save(ROOT/p['output']['png']);im.save(ROOT/p['output']['webp'],quality=93,method=6)
        thumb=ImageOps.contain(im,(580,580),Image.Resampling.LANCZOS);sheet.paste(thumb,(i*600+10,45));d.text((i*600+15,12),p['track'],font=font(23,True),fill='#25334A')
    sheet.save(ROOT/'preview.jpg',quality=95)
    print('Rendered 2/2 at 1200x1200, contain, separate PNG/WebP and contact sheet.')
def questions(m,prefix=''):
    lines=['# Review 5–6 — Câu hỏi theo trang','', 'Bộ chuẩn gồm **2 mục audio**, mỗi mục có một ảnh PNG/WebP 1200×1200 và đúng một câu trắc nghiệm bổ sung.','',link('Preview',prefix+'preview.html')+' · '+link('Metadata',prefix+'review.regenerated.metadata')+' · '+link('Contact sheet',prefix+'preview.jpg'),'', 'Câu hỏi hiện sau audio hoặc khi bấm ôn tập; phản hồi sau lựa chọn. Không phải đáp án cho các cặp Listen and circle của bài nghe gốc. MP3 chỉ đối chiếu byte, chưa nghe/transcribe độc lập.','']
    for p in m['items']:
        q=p['question'];lines += [f"## {p['track']} — {p['exercise']}",'',f"Trang PDF {p['pdf_page']}, trang sách {p['book_page']}. Mã câu hỏi: {q['id']}.",'',link('Ảnh WebP',prefix+p['output']['webp'])+' · '+link('Ảnh PNG',prefix+p['output']['png'])+' · '+link('Audio CD2',prefix+p['audio_file']),'','**Câu hỏi:** '+q['prompt'],'']+[f"- {c['id']}. {c['text']}" for c in q['choices']]+['']
    lines+=['## Đáp án câu hỏi bổ sung','','| Track | Đáp án |','|---|---|']
    for p in m['items']:
        q=p['question'];c=next(c for c in q['choices'] if c['id']==q['correct_choice_id']);lines.append(f"| {p['track']} | {c['id']}. {c['text']} |")
    return '\n'.join(lines)+'\n'
def docs():
    m=read(ROOT/'manifest.json');assert all(p['status']=='reviewed' for p in m['items'])
    metadata={'format_version':'2.0','review':'5-6','topic':m['topic'],'item_count':2,'uniform_size':[1200,1200],'items':[{'track':p['track'],'exercise':p['exercise'],'page':p['pdf_page'],'book_page':p['book_page'],'image':p['output']['webp'],'audio_file':p['audio_file'],'size':[1200,1200],'question':p['question'],'adaptation_notes':p['adaptation_notes']} for p in m['items']]}
    write(ROOT/'review.regenerated.metadata',metadata)
    payload=json.dumps(m,ensure_ascii=False).replace('<','\\u003c')
    (ROOT/'preview.html').write_text((ROOT/'preview.template.html').read_text(encoding='utf-8').replace('/*MANIFEST_JSON*/',payload),encoding='utf-8')
    (ROOT/'questions.md').write_text(questions(m),encoding='utf-8')
    (UNITS/'Review 5-6 - Cau hoi theo trang.md').write_text(questions(m,ROOT.name+'/'),encoding='utf-8')
    (ROOT/'README.md').write_text('''# Review 5–6 — Animals, Food, Actions & The Weather

Đủ **2/2 mục CD2_35–CD2_36**, mỗi mục gồm PNG/WebP **1200×1200**, MP3 CD2 và đúng một câu trắc nghiệm riêng. Ảnh được regenerate bằng **built-in image_gen**; không dùng fallback hoặc ảnh nguồn thay minh họa.

- [Preview học và làm bài](preview.html) · [Contact sheet](preview.jpg)
- [Metadata](review.regenerated.metadata) · [Câu hỏi](questions.md)
- [Manifest dựng trang](manifest.json) · [Generation log](generation.json) · [Validation](validation.json)
- [Nguồn trang 54](source-pages/page-1.png) · [Nguồn trang 55](source-pages/page-2.png)

Ảnh chuẩn: pages/webp; PNG tương ứng: pages/png. assets giữ ảnh sinh/crop để dựng lại; assets/batches lưu prompt, refs, tool, source-output và log sửa. references/source-pages giữ nguồn đối chiếu. Layout được nén/điều chỉnh cho canvas vuông, contain giữ tỷ lệ; box cắt theo gutter thực tế nằm trong manifest.

CD2_35 giữ 6 cặp a/b: 3/4 mèo, 2/5 thỏ, kem/bánh, bánh mì/cơm, skip/jump, 3 trẻ xếp hàng/vòng tròn. Không khoanh lựa chọn hoặc suy ra đáp án audio. Các tên động vật/món ăn/hành động dùng trong tài liệu bổ sung để mô tả hình; không thêm nhãn từ mới lên bài nghe nguồn.

CD2_36 giữ sunny, cloudy, windy, rainy, snowy và cảnh/câu **It's sunny.**; cloudy không có dấu gió, windy có khăn/lá/cây chuyển động, rainy có giọt mưa, snowy có tuyết. Cảnh luyện câu cùng trang không có marker audio riêng; giữ chung trang CD2_36, không bịa track hoặc clip riêng.

Đã xem đủ 2 trang nguồn và mọi ảnh sau cắt/contact sheet. MP3 kiểm tra đồng nhất từng byte với CD2 nguồn; **chưa nghe/transcribe độc lập**. Vì vậy không có đáp án cho bài Listen and circle gốc. Câu trắc nghiệm bổ sung hỏi nhận biết hình, không kiểm thứ tự trong MP3.

Bài Challenge được giữ trong Review 5-6(2).md; đã sửa tên nguồn từ Review 5-6(2) thành Review 5-6.pdf, giới hạn khẳng định coverage và bổ sung checklist audio bắt buộc/tùy chọn. Không tạo audio Challenge; chủ dự án tự thu.

Dựng lại: `python build_review.py render`, `python build_review.py docs`, `node check_preview.cjs`, `python build_review.py validate`. Chỉ thực hiện trong thư mục Review này.
''',encoding='utf-8')
    doc=UNITS/'Review 5-6(2).md';text=doc.read_text(encoding='utf-8-sig')
    for marker in ['lesson-package-status','challenge-audio-notes']:
        text=re.sub(r'<!-- '+marker+r' -->.*?<!-- /'+marker+r' -->\s*','',text,flags=re.S)
    text=text.replace('PDF **Review 5-6(2)**','PDF **Review 5-6.pdf**')
    text=re.sub(r'\*\*Coverage:.*?\*\*','**Phạm vi đối chiếu:** bài luyện bao gồm các nhóm từ/hình của hai trang nguồn. Bài nghe CD2_35 chưa có đáp án được xác nhận bằng nghe; audio Challenge chưa có file. Bảng trên ghi nội dung bài luyện, không chứng minh kiểm chứng âm thanh.',text)
    block='<!-- lesson-package-status -->\n## Bộ Review chuẩn\n\nĐã có **2/2 mục CD2_35–CD2_36**, PNG/WebP1200×1200, MP3 và một câu trắc nghiệm bổ sung mỗi mục.\n\n'+link('Preview',ROOT.name+'/preview.html')+' · '+link('Metadata',ROOT.name+'/review.regenerated.metadata')+' · '+link('Câu hỏi theo trang','Review 5-6 - Cau hoi theo trang.md')+'\n\nNguồn chuẩn là **Review 5-6.pdf**, trang sách54–55. Đã sửa tên PDF sai trong chú thích cũ; giữ các bài luyện người dùng. Các số lượng trong bài luyện là biến thể luyện số ít/số nhiều; hình nguồn có 3/4 mèo và 2/5 thỏ. Câu Weather in trong nguồn chỉ là **It\'s sunny.**; không suy ra câu khác đã in hoặc đã có clip.\n\nMP3 chỉ kiểm byte với CD2 nguồn, chưa nghe/transcribe độc lập. Cảnh sunny luyện câu dùng chung trang CD2_36, không có audio marker riêng. Không thêm track cho từng cặp lựa chọn.\n<!-- /lesson-package-status -->\n\n'
    first,rest=text.split('\n',1);text=first+'\n\n'+block+rest.lstrip('\n')
    mandatory=['cat','rabbit','ice cream','cake','bread','rice','sunny','cloudy','windy','rainy','snowy',"It's sunny.",'skip','jump','make a line','make a circle']
    optional=['cats','rabbits']
    notes='\n\n<!-- challenge-audio-notes -->\n# Audio clip Challenge cần chủ dự án bổ sung\n\nTất cả file dưới đây **chưa có/chưa hoàn thành**; tên file là gợi ý. Audio CD dài không mặc định thay cho clip từ/câu ngắn. Clip trùng nội dung được dùng chung; không thu lặp cho mỗi câu.\n\n| Đã có | Mức | Tên file gợi ý | Nội dung cần đọc | Nơi dùng chung |\n|---|---|---|---|---|\n'
    for v in mandatory+optional:
        slug=re.sub('[^a-z0-9]+','_',v.lower()).strip('_');level='Cần thiết cho chế độ nghe tự động' if v in mandatory else 'Tùy chọn'
        use='Challenge 1.4; 2.1; 5.7' if v in mandatory[:6] else 'Challenge 1.4; 2.2/2.3; 5.7' if v in mandatory[6:11] else 'Challenge 2.3.6; 3.5; tùy chọn cho 5.8' if v=="It's sunny." else 'Challenge 2.4; 5.6' if v in mandatory[12:] else 'Recall 3.2 / Final Boss 5.1 nếu thêm chế độ nghe số nhiều'
        notes+=f'| ☐ | {level} | `r56_{slug}.mp3` | {v} | {use} |\n'
    notes+='\n- Người lớn có thể đọc thay clip khi luyện trực tiếp. Bài nhìn hình, ghép từ, dịch/viết không bắt buộc audio. Giọng Boss riêng hoặc bản đọc toàn hướng dẫn là tùy chọn.\n- Challenge 1.4/5.7 chọn ngẫu nhiên đúng một clip trong kho11 từ đã liệt kê; không tự gán đáp án bài nghe CD2_35.\n- Ảnh emoji trong Challenge là gợi ý, chưa phải asset/clip riêng. Để phân biệt windy/cloudy, dùng tranh Weather chuẩn có lá/khăn bay và cây nghiêng cho windy.\n- Nếu nối clip hành động, skip/jump/make a line/make a circle là lệnh do chủ dự án thu riêng; trang54 minh họa hành động, không in các nhãn này.\n<!-- /challenge-audio-notes -->\n'
    doc.write_text(text.rstrip()+notes,encoding='utf-8')
    write(ROOT/'generation.json',{'tool':'built-in image_gen','batch_count':1,'tracks':['CD2_35','CD2_36'],'jobs':[read(p) for p in sorted((ROOT/'assets/batches').glob('*.json'))]})
    if not (ROOT/'validation.json').exists():write(ROOT/'validation.json',{'result':'pending_validation','review':'5-6','note':'Technical/export checks not yet complete.'})
    print('Metadata, preview, questions, README and both external Markdown docs updated.')
def validate():
    m=read(ROOT/'manifest.json');assert [p['track'] for p in m['items']]==['CD2_35','CD2_36']
    md=read(ROOT/'review.regenerated.metadata');assert md['item_count']==2
    checks=[]
    for p,item in zip(m['items'],md['items']):
        assert p['status']=='reviewed' and p['visual_review']
        q=p['question'];assert isinstance(q,dict) and q['show_after_audio'] is True and q['render_in_lesson_image'] is False
        ids=[c['id'] for c in q['choices']];assert len(ids)==len(set(ids)) and q['correct_choice_id'] in ids
        assert item['track']==p['track'] and item['image']==p['output']['webp'] and item['audio_file']==p['audio_file'] and item['question']==q
        expected=render_page(p)
        for fmt in ['png','webp']:
            with Image.open(ROOT/p['output'][fmt]) as im:
                assert im.size==(1200,1200)
                if fmt=='png':assert im.convert('RGB').tobytes()==expected.tobytes()
                im.load()
        audio=ROOT/p['audio_file'];assert audio.read_bytes()==(CD/audio.name).read_bytes()
        assert (ROOT/p['source_reference']).exists() and (ROOT/p['source_page']).exists()
        checks.append({'track':p['track'],'result':'pass','size':[1200,1200],'png_sha256':sha(ROOT/p['output']['png']),'webp_sha256':sha(ROOT/p['output']['webp']),'audio_sha256':sha(audio),'visual_review':p['visual_review']})
    for doc in [ROOT/'README.md',ROOT/'questions.md',UNITS/'Review 5-6(2).md',UNITS/'Review 5-6 - Cau hoi theo trang.md']:
        for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):assert (doc.parent/unquote(target)).exists(),(doc,target)
    orig=(ROOT/'assets/challenge.original.md').read_text(encoding='utf-8-sig');new=(UNITS/'Review 5-6(2).md').read_text(encoding='utf-8')
    old_body=orig.split('# Challenge 1',1)[1].split('# Coverage Check',1)[0]
    new_body=new.split('# Challenge 1',1)[1].split('# Coverage Check',1)[0];assert old_body==new_body,'User Challenge exercises changed unexpectedly'
    assert 'Coverage: toàn bộ' not in new
    job=read(ROOT/'assets/batches/batch1.json');assert job['tool']=='built-in image_gen' and job['status']=='reviewed' and job['source_output'] and job['prompt'] and job['refs']
    assert all(Path(x).exists() for x in job['refs'])
    preview_check=read(ROOT/'preview.checks.json');assert preview_check['result']=='pass' and preview_check['item_count']==2
    browser_check=read(ROOT/'browser.checks.json');assert browser_check['result']=='pass' and browser_check['item_count']==2 and not browser_check['page_errors']
    report={'result':'pass','review':'5-6','item_count':2,'source_page_count':2,'uniform_size':[1200,1200],'checks':checks,'audio_validation':'Byte-for-byte identity with source CD2 MP3; no independent listening/transcription.','source_listening_answers':'Unknown, original a/b selections remain unmarked.','visual_validation':'All source/final images and contact sheet inspected; technical checks alone do not prove illustration semantics.','preview_validation':preview_check,'challenge_preservation':'Challenge 1-5 body identical to original; source-name and coverage notes corrected; clip checklist added.','challenge_audio':'No Challenge audio generated; unchecked mandatory/optional recording pool in external Markdown.'}
    report['browser_validation']=browser_check
    report['visual_audit']=read(ROOT/'visual.audit.json')
    write(ROOT/'validation.json',report)
    write(ROOT/'generation.json',{'tool':'built-in image_gen','batch_count':1,'tracks':['CD2_35','CD2_36'],'source_pdf_sha256':sha(UNITS/'Review 5-6.pdf'),'jobs':[read(p) for p in sorted((ROOT/'assets/batches').glob('*.json'))],'final_images':{p['track']:p['output'] for p in m['items']},'visual_evidence':[p['visual_review'] for p in m['items']]})
    dest=UNITS/'Review_5-6_regenerated.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for f in ROOT.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts:z.write(f,f.relative_to(ROOT))
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for p in m['items']:
            for path in [p['output']['png'],p['output']['webp'],p['audio_file']]:assert z.read(path)==(ROOT/path).read_bytes()
        for path in ['manifest.json','review.regenerated.metadata','preview.html','preview.jpg','questions.md','README.md','generation.json','validation.json','browser.checks.json','visual.audit.json']:assert path in z.namelist()
        report_in_zip=json.loads(z.read('validation.json'));assert report_in_zip==report
    print('PASS: 2/2 Review items, exact mapping, 1200 PNG/WebP, PNG render equality, CD2 bytes, questions, all links, preserved Challenge body, preview checks and ZIP CRC/contents.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['init','import','render','docs','validate']);ap.add_argument('--boxes');ap.add_argument('--note');a=ap.parse_args()
    if a.action=='import':import_batch(json.loads(a.boxes),a.note)
    else:globals()[a.action]()
