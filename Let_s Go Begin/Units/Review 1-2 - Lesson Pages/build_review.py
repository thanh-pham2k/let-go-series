from pathlib import Path
from urllib.parse import quote,unquote
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,re,hashlib,shutil,zipfile,argparse
ROOT=Path(__file__).resolve().parent
BOOK=ROOT.parent.parent
def dump(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def render(item):
    canvas=Image.new('RGB',(1200,1200),'white')
    for l in item['layers']:
        x,y,w,h=l['box']
        if l['type']=='image':
            im=ImageOps.contain(Image.open(ROOT/l['asset']).convert('RGB'),(w,h),Image.Resampling.LANCZOS)
            canvas.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
        else:
            f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',l['font_size'])
            ImageDraw.Draw(canvas).text((x,y),l['text'],font=f,fill='#25334a')
    return canvas
def link(label,path):return f'[{label}]({quote(path,safe="/")})'
def questions(m,prefix=''):
    text='# Review 1–2 – Câu hỏi theo trang\n\nHai mục audio; mỗi mục có một câu trắc nghiệm bổ sung, hiện sau khi nghe hoặc bấm ôn tập. Các câu này hỏi nội dung nhìn thấy, không phải đáp án bài nghe Listen and circle.\n\n'
    text+=link('Preview',prefix+'preview.html')+' · '+link('Metadata',prefix+'review.regenerated.metadata')+'\n\n'
    for p in m['items']:
        q=p['question']
        text+=f"## {p['track']} – {p['exercise']}\n\nTrang PDF {p['pdf_page']}, trang sách {p['book_page']}.\n\n"
        text+=link('Ảnh WebP',prefix+p['output']['webp'])+' · '+link('PNG',prefix+p['output']['png'])+' · '+link('Audio',prefix+p['audio_file'])+'\n\n'+q['prompt']+'\n\n'
        text+='\n'.join(f"- {c['id']}. {c['text']}" for c in q['choices'])+'\n\n'
    text+='## Đáp án câu bổ sung\n\n| Track | Đáp án |\n|---|---|\n'
    for p in m['items']:
        q=p['question'];c=next(c for c in q['choices'] if c['id']==q['correct_choice_id'])
        text+=f"| {p['track']} | {c['id']}. {c['text']} |\n"
    return text+'\nAudio đã so sánh từng byte với CD1 nguồn, chưa nghe/transcribe độc lập. Không xác định đáp án sáu cặp Listen and circle.\n'
def build(split):
    sheet=Image.open(ROOT/'assets/batches/batch1.png').convert('RGB');w,h=sheet.size
    assert 0<split<w
    boxes=[(0,0,split,h),(split,0,w,h)]
    items=[]
    for n,box in zip([36,37],boxes):
        track=f'CD1_{n}';asset=f'assets/{track}-lesson.png'
        sheet.crop(box).save(ROOT/asset)
        source=BOOK/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD1'/f'Track{n}.mp3'
        shutil.copyfile(source,ROOT/'audio'/source.name)
        q=({'prompt':'Ở cặp 3, mảng màu bên trái (a) là màu nào?','choices':[{'id':'A','text':'green'},{'id':'B','text':'red'},{'id':'C','text':'purple'}],'correct_choice_id':'A'} if n==36 else {'prompt':'Cô giáo cầm tờ giấy và nói câu nào trong hình?','choices':[{'id':'A','text':'I have glue.'},{'id':'B','text':'I have paper.'},{'id':'C','text':'I have tape.'}],'correct_choice_id':'B'})
        q.update(id=f'R1-2-{track}',show_after_audio=True,render_in_lesson_image=False)
        p={'track':track,'audio_key':f'CD1-{n}','exercise':'A. Listen and circle.' if n==36 else 'A. Say these.','pdf_page':n-35,'unit_pdf_page':n-35,'book_page':n-18,'source_reference':f'references/{track}.png','source_page':f'source-pages/page-{n-35}.png','audio_file':f'audio/Track{n}.mp3','output':{'png':f'pages/png/{track}.png','webp':f'pages/webp/{track}.webp'},'canvas':{'size':[1200,1200],'background':'#FFFFFF'},'layers':[{'type':'image','asset':asset,'box':[0,0,1200,1200]}],'source_crop_box':list(box),'question':q,'status':'awaiting_final_visual_review','adaptation_notes':(['Six source pairs retained without selecting answers; no separate tracks per pair.','Pair6 depicts Come here / Turn around; Go corrected in Challenge document.'] if n==36 else ['Five school supplies and teacher model I have paper. retained.','Bottom model scene has no separate audio marker; included with CD1_37, independent MP3 speech coverage not audited.'])}
        im=render(p);im.save(ROOT/p['output']['png']);im.save(ROOT/p['output']['webp'],quality=92,method=6)
        items.append(p)
    m={'schema_version':'2.0','review':'1-2','topic':'Listen and Review / School Supplies','source_pdf':'Review 1-2.pdf','source_pdf_sha256':sha(ROOT.parent/'Review 1-2.pdf'),'source_item_count':2,'image_count':2,'image_fit':'contain','coordinate_system':'pixel boxes [x,y,width,height]','items':items}
    dump(ROOT/'manifest.json',m)
    job=json.loads((ROOT/'assets/batches/batch1.json').read_text(encoding='utf-8'));job.update(sheet_size=[w,h],split_x=split,sha256=sha(ROOT/'assets/batches/batch1.png'));dump(ROOT/'assets/batches/batch1.json',job)
    contact=Image.new('RGB',(1200,640),'#edf3f8');d=ImageDraw.Draw(contact)
    for i,p in enumerate(items):
        im=ImageOps.contain(Image.open(ROOT/p['output']['png']),(590,590));contact.paste(im,(i*600+5,40));d.text((i*600+20,10),p['track'],font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',22),fill='#25334a')
    contact.save(ROOT/'preview.jpg',quality=94)
    print('Rendered two pages; awaiting visual review.')
def export():
    m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    assert all(p['status']=='reviewed' for p in m['items'])
    metadata={'format_version':'2.0','review':'1-2','item_count':2,'uniform_size':[1200,1200],'items':[{'track':p['track'],'exercise':p['exercise'],'pdf_page':p['pdf_page'],'book_page':p['book_page'],'image':p['output']['webp'],'audio_file':p['audio_file'],'size':[1200,1200],'question':p['question'],'adaptation_notes':p['adaptation_notes']} for p in m['items']]}
    dump(ROOT/'review.regenerated.metadata',metadata)
    template=(ROOT.parent/'Unit 2 - Colors - Lesson Pages/preview.html').read_text(encoding='utf-8')
    template=re.sub(r'const manifest=.*?;\s*const pages=',lambda _: 'const manifest='+json.dumps(m,ensure_ascii=False).replace('<','\\u003c')+';\nconst pages=',template,flags=re.S)
    template=template.replace('Unit 2 · Colors','Review 1–2 · School Supplies').replace('17 bài nghe','2 bài nghe')
    template=template.replace('<p id="caption" class="note"></p>','<p id="caption" class="note"></p><p class="note">Chưa xác định đáp án bài nghe Listen and circle. Câu ôn tập bổ sung hỏi nội dung nhìn thấy trong hình.</p>')
    (ROOT/'preview.html').write_text(template,encoding='utf-8')
    (ROOT/'questions.md').write_text(questions(m),encoding='utf-8')
    (ROOT.parent/'Review 1-2 - Cau hoi theo trang.md').write_text(questions(m,ROOT.name+'/'),encoding='utf-8')
    (ROOT/'README.md').write_text('''# Review 1–2 – Bộ bài học chuẩn

Hai trang CD1_36–37, PNG/WebP **1200 × 1200**, contain giữ tỷ lệ. Minh họa mới bằng built-in image_gen; không dùng ảnh nguồn làm ảnh học.

- [Preview](preview.html) · [Contact sheet](preview.jpg)
- [Metadata](review.regenerated.metadata) · [Câu hỏi](questions.md)
- [Validation](validation.json) · [Generation](generation.json)

Ảnh chuẩn: pages/webp; PNG tương ứng: pages/png. references/source-pages chỉ dùng đối chiếu PDF. assets giữ minh họa và batch gốc để dựng lại.

CD1_36 giữ sáu cặp theo thứ tự: car/train, bicycle/ball, green/red, purple/yellow, stand up/sit down, come here/turn around; mỗi cặp giữ a bên trái, b bên phải, không khoanh đáp án. CD1_37 giữ năm đồ dùng 1 paper, 2 scissors, 3 glue, 4 paint, 5 tape và câu cô giáo “I have paper.” ở cùng trang. Cảnh câu mẫu không có track riêng; giữ cùng trang, không khẳng định audio đọc câu này.

Điều chỉnh: bố cục nguồn được chuyển thành canvas vuông; style cartoon sáng/soft shading theo Unit3; sửa “go/đi” trong bài luyện thành “come here/lại đây” theo hình6 và nội dung Unit2. Tape dùng mô tả hộp băng keo thay emoji giấy vệ sinh dễ gây hiểu sai. Câu bổ sung kiểm nhận biết hình/câu mẫu, không phải đáp án bài nghe gốc.

Audio copy đúng từng byte từ CD1 nguồn. Chưa nghe/transcribe độc lập; không suy đoán đáp án Listen and circle. Audio Challenge riêng chưa có, chủ dự án tự cung cấp theo checklist. Preview hiện câu hỏi sau audio ended hoặc bấm ôn tập, chỉ phản hồi đáp án sau khi chọn.

Dựng lại: python build_review.py --build --split-x SPLIT (đọc split_x trong batch1.json). Lệnh này đặt lại trạng thái chờ duyệt; chỉ --export sau khi xem lại ảnh và ghi reviewed cùng bằng chứng vào manifest.
''',encoding='utf-8')
    checks=[]
    for p in m['items']:
        q=p['question'];assert len(q['choices'])==3 and q['correct_choice_id'] in [c['id'] for c in q['choices']]
        assert q['show_after_audio'] and not q['render_in_lesson_image']
        expected=render(p)
        for fmt in ['png','webp']:
            with Image.open(ROOT/p['output'][fmt]) as im:
                assert im.size==(1200,1200)
                if fmt=='png':assert im.convert('RGB').tobytes()==expected.tobytes()
        source=BOOK/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD1'/Path(p['audio_file']).name
        assert source.read_bytes()==(ROOT/p['audio_file']).read_bytes()
        checks.append({'track':p['track'],'size':[1200,1200],'png_sha256':sha(ROOT/p['output']['png']),'audio_sha256':sha(source),'visual_review':p['visual_review']})
    dump(ROOT/'validation.json',{'result':'pass','item_count':2,'checks':checks,'audio_validation':'Byte identity only; not independently listened/transcribed. Original listening answers not inferred.','preview_validation':'See runtime-check.json','source_coverage':'Both complete PDF pages adapted, including unmarked teacher sentence scene.'})
    dump(ROOT/'generation.json',{'tool':'built-in image_gen','jobs':['assets/batches/batch1.json'],'tracks':['CD1_36','CD1_37'],'final_pages_reviewed':True})
    for f in [ROOT/'README.md',ROOT/'questions.md',ROOT.parent/'Review 1-2 - Cau hoi theo trang.md',ROOT.parent/'Review 1-2(3).md']:
        for t in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
            assert (f.parent/unquote(t)).exists(),(f,t)
    dest=ROOT.parent/'Review_1-2_regenerated.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for f in ROOT.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts:z.write(f,f.relative_to(ROOT))
        for f in [ROOT.parent/'Review 1-2(3).md',ROOT.parent/'Review 1-2 - Cau hoi theo trang.md']:
            content=f.read_text(encoding='utf-8').replace(quote(ROOT.name,safe='/')+'/', '../')
            z.writestr('external-docs/'+f.name,content)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for p in m['items']:
            for f in [p['output']['png'],p['output']['webp'],p['audio_file']]: assert z.read(f)==(ROOT/f).read_bytes()
        import posixpath
        for name in z.namelist():
            if name.endswith('.md'):
                for t in re.findall(r'\]\(([^)]+)\)',z.read(name).decode('utf-8')):
                    assert posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(t))) in z.namelist(),(name,t)
    print('PASS: 2 PNG/WebP, audio identity, metadata/questions/links/PNG rebuild/ZIP verified.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--split-x',type=int);ap.add_argument('--export',action='store_true');a=ap.parse_args()
    if a.build:build(a.split_x)
    if a.export:export()
