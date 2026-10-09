"""Import reviewed ImageGen sheets and validate/export a complete unit."""
from pathlib import Path
from urllib.parse import quote,unquote
import argparse,json,re,hashlib,zipfile,sys,importlib.util
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parent
UNITS=ROOT/'Let_s Go Begin/Units'
CANVAS=(1200,1200)
spec=importlib.util.spec_from_file_location('lesson_render',UNITS/'Unit 1 - Toys - Lesson Pages/render.py')
render=importlib.util.module_from_spec(spec);spec.loader.exec_module(render)

def font(size,bold=False):return render.font(size,bold)
def filelink(label,path):return f'[{label}]({quote(path,safe="/")})'

def separator(im,axis):
    # Pick the continuous neutral gutter closest to the middle. Fall back to center.
    w,h=im.size;extent=h if axis=='y' else w
    candidates=[]
    for n in range(int(extent*.46),int(extent*.54)):
        pixels=[im.getpixel((x,n)) for x in range(w)] if axis=='y' else [im.getpixel((n,y)) for y in range(h)]
        neutral=sum(max(p)-min(p)<=3 and min(p)>=205 for p in pixels)/len(pixels)
        gray=sum(max(p)-min(p)<=3 and 205<=min(p)<=248 for p in pixels)/len(pixels)
        if neutral>.985:candidates.append((gray,-abs(n-extent/2),n))
    return max(candidates)[2] if candidates else extent//2

def import_batch(folder,batchid,note,split_x=None,split_y=None):
    manifest_path=folder/'manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    job_path=folder/'assets/batches'/f'{batchid}.json'
    job=json.loads(job_path.read_text(encoding='utf-8'))
    source=folder/'assets/batches'/f'{batchid}.png'
    with Image.open(source) as img:
        sheet=img.convert('RGB');w,h=sheet.size
        x=split_x or separator(sheet,'x');y=split_y or separator(sheet,'y')
        count=len(job['tracks'])
        if count==1:boxes=[(0,0,w,h)]
        elif count==2:boxes=[(1,1,x-1,h-1),(x+1,1,w-1,h-1)]
        else:boxes=[(1,1,x-1,y-1),(x+1,1,w-1,y-1),(1,y+1,x-1,h-1),(x+1,y+1,w-1,h-1)][:count]
        for track,box in zip(job['tracks'],boxes):
            page=next(p for p in manifest['items'] if p['track']==track)
            crop=sheet.crop(box)
            name=f'assets/{track}-lesson.png'
            crop.save(folder/name)
            page['layers']=[{'type':'image','asset':name,'box':[0,0,*CANVAS]}]
            if manifest['unit']==3 and track=='CD1_43':
                # Source header's classroom-language example was omitted by ImageGen.
                page['layers'] += [
                    {'type':'rect','box':[40,126,600,43],'fill':'#FFFFFF'},
                    {'type':'text','text':'Draw a circle.','box':[60,130,560,35],
                     'font_size':30,'align':'left','bold':False,'color':'#25334A'}]
            page['canvas']['size']=list(CANVAS)
            page['status']='reviewed'
            page['visual_review']=note
            page['generation_batch']=batchid
            page['source_crop_box']=list(box)
    job.update({'status':'reviewed','visual_review':note,'sheet_size':[w,h],'split':[x,y],'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    job_path.write_text(json.dumps(job,ensure_ascii=False,indent=2),encoding='utf-8')
    for b in manifest.get('batches',[]):
        if b['tracks']==job['tracks']:b['status']='reviewed'
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(batchid,job['tracks'],'sheet',w,h,'split',x,y)

def render_all(folder):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));render.ROOT=folder
    ready=[p for p in manifest['items'] if p['status']=='reviewed']
    for p in ready:
        im=render.render_page(p)
        render.save_image(im,folder/p['output']['png'])
        render.save_image(im,folder/p['output']['webp'],quality=90,method=6)
    thumbs=Image.new('RGB',(1200,((len(manifest['items'])+3)//4)*330),'#EDF2F7')
    d=ImageDraw.Draw(thumbs)
    for i,p in enumerate(manifest['items']):
        x=(i%4)*300;y=(i//4)*330
        d.text((x+10,y+7),p['track'],font=font(18,True),fill='#25334A')
        if p in ready:
            im=ImageOps.contain(Image.open(folder/p['output']['webp']),(290,290))
            thumbs.paste(im,(x+5,y+30))
        else:d.text((x+15,y+65),'Pending generation',font=font(18),fill='#777777')
    render.save_image(thumbs,folder/'preview.jpg',quality=92)
    print('Rendered',len(ready),'/',len(manifest['items']))

def questions_markdown(manifest,prefix=''):
    lines=[f"# Unit {manifest['unit']} – {manifest['topic']}: Câu hỏi theo trang",'',
        f"Bộ chuẩn gồm {len(manifest['items'])} trang, mỗi trang có ảnh có chữ, audio và đúng một câu trắc nghiệm. Ảnh đều 1200 × 1200, giữ tỷ lệ nội dung.",'',
        '- '+filelink('Preview học và làm bài',prefix+'preview.html')+' · '+filelink('Xem cả bộ',prefix+'preview.jpg')+'.',
        '- '+filelink('Metadata nối ảnh/audio/câu hỏi',prefix+'unit.regenerated.metadata')+'.',
        '- Hiện câu hỏi sau khi nghe, phản hồi đáp án sau khi bé chọn.',
        '- Audio khớp file CD nguồn; chưa nghe/transcribe đối chiếu độc lập.','']
    if manifest['unit']==6:
        lines+=['**Lưu ý nguồn:** hai nhãn CD1 32 và CD1 34 in trong PDF được chuẩn hóa thành CD2_32 và CD2_34 theo mapping tổng và thư mục audio Unit 6; cần nghe xác nhận nội dung khi kiểm tra audio.','']
    for p in manifest['items']:
        q=p['question'];lines += [f"## {p['track']} – {p['exercise']}",'',f"- **Mã câu hỏi:** {q['id']}.",
            f"- **Trang PDF:** {p['unit_pdf_page']} (trang sách {p['book_page']}).",
            '- **Ảnh chuẩn:** '+filelink(p['track']+'.webp',prefix+p['output']['webp'])+'.',
            '- **Audio:** '+filelink(Path(p['audio_file']).name,prefix+p['audio_file'])+'.','',
            '**Câu hỏi:** '+q['prompt'],'']
        lines += [f"- {c['id']}. {c['text']}" for c in q['choices']]+['']
    lines+=['## Đáp án','', '| Track | Đáp án |','|---|---|']
    for p in manifest['items']:
        q=p['question'];answer=next(c for c in q['choices'] if c['id']==q['correct_choice_id'])
        lines.append(f"| {p['track']} | {answer['id']}. {answer['text']} |")
    return '\n'.join(lines)+'\n'

def export(folder):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));render.ROOT=folder
    assert all(p['status']=='reviewed' for p in manifest['items']),'Some pages still pending'
    assert len({p['track'] for p in manifest['items']})==manifest['source_item_count']
    checks=[]
    for p in manifest['items']:
        q=p['question'];assert q['correct_choice_id'] in [c['id'] for c in q['choices']]
        source_audio=UNITS.parent/f"Oxford - Let_s Go Begin Student_s Book 3rd Edition {p['track'].split('_')[0]}"/Path(p['audio_file']).name
        assert (folder/p['audio_file']).read_bytes()==source_audio.read_bytes()
        assert (folder/p['source_reference']).exists()
        expected=render.render_page(p)
        for fmt in ['png','webp']:
            with Image.open(folder/p['output'][fmt]) as im:
                assert im.size==CANVAS
                if fmt=='png':assert im.convert('RGB').tobytes()==expected.tobytes()
        checks.append({'track':p['track'],'size':list(CANVAS),'status':'pass','png_sha256':hashlib.sha256((folder/p['output']['png']).read_bytes()).hexdigest(),'visual_review':p['visual_review']})
    metadata={'format_version':'2.0','unit':manifest['unit'],'topic':manifest['topic'],'item_count':len(manifest['items']),'uniform_size':list(CANVAS),
        'items':[{'track':p['track'],'exercise':p['exercise'],'page':p['unit_pdf_page'],'book_page':p['book_page'],'image':p['output']['webp'],'audio_file':p['audio_file'],'size':list(CANVAS),'question':p['question']} for p in manifest['items']]}
    (folder/'unit.regenerated.metadata').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    template=(UNITS/'Unit 1 - Toys - Lesson Pages/preview.template.html').read_text(encoding='utf-8')
    template=template.replace('Unit 1 · Toys',f"Unit {manifest['unit']} · {manifest['topic']}").replace('17 bài nghe',f"{len(manifest['items'])} bài nghe")
    payload=json.dumps(manifest,ensure_ascii=False).replace('<','\\u003c')
    (folder/'preview.html').write_text(template.replace('/*MANIFEST_JSON*/',payload),encoding='utf-8')
    (folder/'questions.md').write_text(questions_markdown(manifest),encoding='utf-8')
    external=UNITS/f"Unit {manifest['unit']} - {manifest['topic']} - Cau hoi theo trang.md"
    external.write_text(questions_markdown(manifest,folder.name+'/'),encoding='utf-8')
    readme=f"""# Unit {manifest['unit']} – {manifest['topic']}: Bộ bài học chuẩn

Đủ {len(manifest['items'])} ảnh + audio + câu trắc nghiệm. Ảnh PNG/WebP đều **1200 × 1200**, giữ tỷ lệ minh họa và chữ. Regenerate bằng **image_gen tích hợp**, theo nhóm nhiều trang rồi cắt riêng; không dùng fallback.

- [Preview học và làm bài](preview.html)
- [Xem cả bộ](preview.jpg)
- [Metadata tích hợp](unit.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Báo cáo kiểm tra](validation.json)

Ảnh chuẩn dùng cho app: pages/webp. Bản PNG tương ứng: pages/png. assets giữ lớp ảnh phục vụ dựng lại; references và source-pages giữ nguồn PDF đối chiếu. assets/batches lưu prompt, ảnh ghép và đánh giá từng batch; không dùng ảnh ghép làm trang học.

Giữ chữ bài học, số chỉ hình, câu thoại và chỗ trống; câu trắc nghiệm nằm riêng. Các mục chỉ có tiêu đề được bổ sung bằng nội dung của mục cùng trang. Nên hỗ trợ phóng to để đọc lời bài hát trên điện thoại.

Audio khớp file CD nguồn, chưa nghe/transcribe độc lập. Tài liệu Challenge luyện thêm có checklist audio riêng do chủ dự án tự bổ sung.

Dựng lại từ thư mục gốc repo: python build_lesson_unit.py --unit {manifest['unit']} --render --export
"""
    (folder/'README.md').write_text(readme,encoding='utf-8')
    report={'result':'pass','unit':manifest['unit'],'item_count':len(checks),'uniform_size':list(CANVAS),'checks':checks,'audio_validation':'Byte-for-byte identity with source CD MP3; speech not independently audited.'}
    (folder/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    for f in [external,folder/'README.md',folder/'questions.md']:
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):assert (f.parent/unquote(target)).exists(),(f,target)
    dest=UNITS/f"Unit_{manifest['unit']}_{manifest['topic'].replace(' ','_')}_regenerated.zip"
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for path in folder.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:z.write(path,path.relative_to(folder))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    print('PASS',manifest['unit'],len(checks),'tracks, uniform 1200x1200, questions/audio/links/PNG/ZIP verified')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--import-batch');ap.add_argument('--note');ap.add_argument('--split-x',type=int);ap.add_argument('--split-y',type=int);ap.add_argument('--render',action='store_true');ap.add_argument('--export',action='store_true')
    args=ap.parse_args();folder=next(UNITS.glob(f'Unit {args.unit} - * - Lesson Pages'))
    if args.import_batch:
        assert args.note,'Reviewed content note required'
        import_batch(folder,args.import_batch,args.note,args.split_x,args.split_y)
    if args.render:render_all(folder)
    if args.export:export(folder)
