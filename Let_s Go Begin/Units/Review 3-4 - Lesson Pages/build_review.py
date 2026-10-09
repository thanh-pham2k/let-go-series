"""Review3-4 only. Import reviewed built-in sheets, render contain, export and audit."""
from pathlib import Path
from urllib.parse import quote,unquote
import argparse,json,hashlib,re,zipfile
from PIL import Image,ImageDraw,ImageFont,ImageOps
F=Path(__file__).resolve().parent
U=F.parent
CANVAS=(1200,1200)
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def link(label,target):return f'[{label}]({quote(target,safe="/")})'
def render(p):
 out=Image.new('RGB',CANVAS,'white')
 for layer in p['layers']:
  x,y,w,h=layer['box'];assert x>=0 and y>=0 and x+w<=1200 and y+h<=1200
  if layer['type']=='image':
   im=ImageOps.contain(Image.open(F/layer['asset']).convert('RGB'),(w,h),Image.Resampling.LANCZOS)
   out.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
  else:raise ValueError('Only generated raster layers configured in this review')
 return out

def import_batch(batch,split,note):
 m=read(F/'manifest.json');j=read(F/'assets/batches'/f'{batch}.json')
 assert note and split and len(j['tracks'])==2
 source=F/'assets/batches'/f'{batch}.png';im=Image.open(source).convert('RGB');w,h=im.size
 assert 0<split<w
 boxes=[(1,1,split-1,h-1),(split+1,1,w-1,h-1)]
 for t,b in zip(j['tracks'],boxes):
  p=next(p for p in m['items'] if p['track']==t);asset=f'assets/{t}-lesson.png'
  im.crop(b).save(F/asset)
  p.update(layers=[{'type':'image','asset':asset,'box':[0,0,1200,1200]}],status='reviewed_batch',visual_review=note,source_crop_box=list(b),generation_batch=batch)
 j.update(status='reviewed_batch',visual_review=note,split_x=split,sheet_size=[w,h],sha256=hashlib.sha256(source.read_bytes()).hexdigest())
 write(F/'assets/batches'/f'{batch}.json',j);write(F/'manifest.json',m)

def render_all():
 m=read(F/'manifest.json');sheet=Image.new('RGB',(1200,650),'#EDF2F7');d=ImageDraw.Draw(sheet)
 font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',24)
 for i,p in enumerate(m['items']):
  assert p['layers'];im=render(p)
  im.save(F/p['output']['png']);im.save(F/p['output']['webp'],quality=92,method=6)
  thumb=ImageOps.contain(im,(580,580));sheet.paste(thumb,(i*600+(600-thumb.width)//2,50));d.text((i*600+15,10),p['track'],font=font,fill='#25334A')
 sheet.save(F/'preview.jpg',quality=94)
 print('Rendered2 canvases1200x1200 + contact sheet')

def questions(m,prefix=''):
 lines=['# Review 3–4: Câu hỏi theo trang','', 'Hai mục theo mapping PDF, mỗi mục có một câu trắc nghiệm bổ sung sau nghe. Câu hỏi nhận biết hình/câu mẫu; không phải đáp án bài Listen and circle gốc.','',link('Preview',prefix+'preview.html')+' · '+link('Metadata',prefix+'review.regenerated.metadata'),'','Audio khớp byte với CD1 nguồn; chưa nghe/transcribe độc lập.']
 for p in m['items']:
  q=p['question'];lines += ['',f"## {p['track']} – {p['exercise']}",'',f"Trang PDF {p['pdf_page']}, trang sách {p['book_page']}.",'',link('Ảnh WebP',prefix+p['output']['webp'])+' · '+link('PNG',prefix+p['output']['png'])+' · '+link('Audio',prefix+p['audio_file']),'',q['prompt'],'']
  lines += [f"- {c['id']}. {c['text']}" for c in q['choices']]
 lines+=['','## Đáp án trắc nghiệm bổ sung','','| Track | Đáp án |','|---|---|']
 for p in m['items']:
  q=p['question'];c=next(c for c in q['choices'] if c['id']==q['correct_choice_id']);lines.append(f"| {p['track']} | {c['id']}. {c['text']} |")
 return '\n'.join(lines)+'\n'

def docs(m):
 (F/'questions.md').write_text(questions(m),encoding='utf-8')
 (U/'Review 3-4 - Cau hoi theo trang.md').write_text(questions(m,F.name+'/'),encoding='utf-8')
 readme='''# Review 3–4: Bộ bài học chuẩn

Đủ2 mục CD1_71 và CD1_72, adapt toàn bộ2 trang PDF36–37. Minh họa regenerate bằng built-in image_gen, theo batch2 ô rồi cắt theo gutter thực tế; ảnh chuẩn pages/webp và PNG tương ứng pages/png đều1200×1200, contain giữ tỷ lệ.

- [Preview nghe và làm bài](preview.html)
- [Contact sheet](preview.jpg)
- [Metadata](review.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Validation](validation.json)
- [Generation log và prompt](generation.json)
- [PDF đối chiếu](references/source.pdf)

CD1_71 giữ nguyên6 cặp a/b: circle/square; star/heart;4 tam giác/5 hình tròn;6 hình thoi/7 oval;walk/run;go/stop. Các số trong hình3 là nhãn từng vật, đã đối chiếu số lượng thực tế. Square có cạnh bằng nhau; oval có chiều ngang dài hơn chiều cao. Bài circle chưa chọn đáp án; chưa suy ra đáp án bài nghe gốc.

CD1_72 giữ4 lệnh và nghĩa lấy/cất, mở/đóng, màu quần áo/đồ dùng. Câu Please take out your pencil. và tranh giáo viên ở cuối trang được giữ cùng ảnh72; không có marker audio riêng, không bịa thêm track hoặc khẳng định câu đó được đọc trong MP3.

Bố cục được giãn để đọc/đếm rõ; typography và phong cách được vẽ lại. Không thêm lời hát, không tô đáp án bài gốc, câu trắc nghiệm bổ sung và đáp án nằm riêng trong metadata. Trắc nghiệm hiện khi audio kết thúc hoặc bấm Ôn tập; phản hồi sau chọn.

Audio copy đúng từng byte từ CD1 Track71/72.mp3. Chưa nghe/transcribe độc lập. Clip Challenge riêng chưa có, chủ dự án tự bổ sung theo checklist ở Markdown ngoài thư mục. Challenge cũ được giữ; không phát hiện mâu thuẫn nội dung cần thay đổi sau đối chiếu PDF. Bỏ khẳng định coverage tuyệt đối để phân biệt việc đối chiếu nội dung với kiểm chứng audio.

## Bằng chứng kiểm tra preview

[Kiểm tra Edge headless](browser-validation.json), [kiểm tra JavaScript](preview-validation.json) và [tài nguyên HTTP](http-validation.json) ghi kết quả. Hai ảnh chụp preview-browser-1.png/2.png đã được xem trực quan: không cắt chữ hay hình. Edge tải cả2 ảnh và giải mã metadata MP3 với thời lượng62.906667s/66.8s; chọn/chuyển bài, câu hỏi ban đầu ẩn, sự kiện ended và nút Ôn tập hiện câu hỏi, phản hồi đúng/sai đều pass. Sự kiện ended được mô phỏng để kiểm UI; chưa nghe/transcribe lời audio độc lập. Công cụ trình duyệt tích hợp lỗi khởi tạo, nên kiểm bằng Edge headless riêng. Profile kiểm thử .browser-check được giữ cục bộ và loại khỏi ZIP.

references/source-pages giữ ảnh nguồn chỉ để đối chiếu; assets giữ minh họa dựng lại; assets/batches giữ prompt/tool/reference/source-output. Không dùng ảnh nguồn làm ảnh học. build_review.py là helper riêng, không sửa script Unit chung. Chạy lại: python build_review.py --render --export (giữ dấu kiểm trực quan đã ghi trong manifest).
'''
 (F/'README.md').write_text(readme,encoding='utf-8')
 original=(F/'references/challenge-original.md').read_text(encoding='utf-8-sig')
 body=re.sub(r'\*\*Coverage:.*?\*\*','**Phạm vi đối chiếu:** nội dung được rà với cả2 trang PDF. Audio CD và clip Challenge chưa được nghe/transcribe độc lập; không khẳng định coverage audio100%.',original,flags=re.S)
 block='''<!-- review-package-status -->
## Bộ trang học chuẩn

Đủ2 mục CD1_71/72 với ảnh chữ → audio → một câu trắc nghiệm bổ sung. Trang36 giữ6 cặp lựa chọn đúng thứ tự a/b và chưa khoanh đáp án; trang37 giữ4 lệnh cùng cảnh giáo viên nói Please take out your pencil.. Cảnh cuối không có track riêng.

'''+link('Preview',F.name+'/preview.html')+' · '+link('Metadata',F.name+'/review.regenerated.metadata')+' · '+link('Câu hỏi theo trang','Review 3-4 - Cau hoi theo trang.md')+'''

Đối chiếu PDF không phát hiện lỗi từ/câu cần sửa trong các Challenge đã có. Giữ nguyên bài luyện; chỉ thay khẳng định coverage tuyệt đối bằng phạm vi và giới hạn kiểm chứng. Câu hỏi bổ sung không phải answer key cho bài nghe gốc.
<!-- /review-package-status -->
'''
 first,rest=body.split('\n',1);body=first+'\n\n'+block+'\n'+rest.lstrip('\n')
 notes=['','---','','<!-- challenge-audio-notes -->','# Audio riêng cần bổ sung cho Challenge','','Chủ dự án tự thu. Tên dưới đây là gợi ý, chưa có file và tất cả để chưa hoàn thành. CD1 Track71/72 không tự thay cho các clip ngắn. Người lớn đọc trực tiếp vẫn dùng được bài luyện.','','**Cần thiết để tự động chạy phần nghe:** Challenge1 mục4; Challenge2 mục1–4; Challenge3 mục5; Challenge5 mục6. Câu trùng dùng chung một clip. Chọn clip ngẫu nhiên phải chọn trong đúng danh sách lựa chọn, không mặc định đáp án.','','| Đã có | File gợi ý | Nội dung cần đọc | Dùng chung |','|---|---|---|---|']
 groups=[(['circle','square','star','heart','triangle','diamond','oval'],'Challenge1.4; Challenge2.1 theo các lựa chọn'),(['one','two','three','four','five','six','seven'],'Challenge2.2: số1–7'),(['walk','run','go','stop'],'Challenge1.4; Challenge2.4; Challenge5.6'),(['Take out your pencil.','Put away your pencil.','Open your book.','Close your book.'],'Challenge2.3/2.4; Challenge3.5; Challenge5.6'),(['Please take out your pencil.'],'Challenge2.3.5; câu mẫu lịch sự')]
 for values,use in groups:
  for value in values:
   slug=re.sub('[^a-z0-9]+','_',value.lower()).strip('_');notes.append(f'| ☐ | `r34_{slug}.mp3` | {value} | {use} |')
 notes+=['','**Tùy chọn:** clip phát âm pencil/book; giọng Boss; bản hội thoại giáo viên–học sinh; hướng dẫn cho phần nhìn hình, điền, dịch, ghép từ và tự nói. Các mục này không bắt buộc audio riêng. Không tạo audio trong lần hoàn thiện này.','', '**Clip dùng chung:** bốn classroom commands dùng lại ở Challenge2,3,5; Please take out your pencil. là clip riêng với Please; walk/run/go/stop dùng chung phần nghe hành động. one–seven dùng cho số lượng, không thay bằng âm đọc nhãn a/b.','<!-- /challenge-audio-notes -->','']
 (U/'Review 3-4(2).md').write_text(body+'\n'+'\n'.join(notes),encoding='utf-8')
 # Proof that all original Challenge exercises remain byte-equivalent as text.
 original_challenge=original.split('# Challenge 1',1)[1].split('# Coverage Check',1)[0]
 updated=(U/'Review 3-4(2).md').read_text(encoding='utf-8').split('# Challenge 1',1)[1].split('# Coverage Check',1)[0]
 assert updated==original_challenge
 return hashlib.sha256(original_challenge.encode()).hexdigest()

def export():
 m=read(F/'manifest.json');assert len(m['items'])==2
 assert {p['track'] for p in m['items']}=={'CD1_71','CD1_72'}
 checks=[]
 for p in m['items']:
  assert p['status']=='reviewed' and p.get('final_crop_review')
  q=p['question'];assert len(q['choices'])==3 and len({c['id'] for c in q['choices']})==3 and q['correct_choice_id'] in [c['id'] for c in q['choices']]
  assert q['show_after_audio'] and not q['render_in_lesson_image']
  source=U.parent/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD1'/Path(p['audio_file']).name
  assert source.read_bytes()==(F/p['audio_file']).read_bytes()
  expected=render(p)
  for key in ['png','webp']:
   im=Image.open(F/p['output'][key]);assert im.size==CANVAS
   if key=='png':assert im.convert('RGB').tobytes()==expected.tobytes()
  checks.append({'track':p['track'],'size':list(CANVAS),'png_sha256':hashlib.sha256((F/p['output']['png']).read_bytes()).hexdigest(),'audio_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_reference':p['source_reference'],'visual_review':p['visual_review'],'final_crop_review':p['final_crop_review'],'result':'pass'})
 metadata={'format_version':'2.0','review':'3-4','item_count':2,'uniform_size':list(CANVAS),'items':[{'track':p['track'],'exercise':p['exercise'],'pdf_page':p['pdf_page'],'book_page':p['book_page'],'image':p['output']['webp'],'audio_file':p['audio_file'],'size':list(CANVAS),'question':p['question'],'adaptation_notes':p['adaptation_notes']} for p in m['items']],'non_audio_activities':m['non_audio_activities']}
 write(F/'review.regenerated.metadata',metadata)
 template=(U/'Unit 2 - Colors - Lesson Pages/preview.html').read_text(encoding='utf-8')
 template=re.sub(r'const manifest=.*?;\s*const pages=', 'const manifest='+json.dumps(m,ensure_ascii=False).replace('<','\\u003c')+';\nconst pages=',template,flags=re.S)
 template=template.replace('Unit 2 · Colors','Review 3–4').replace('17 bài nghe','2 bài nghe')
 (F/'preview.html').write_text(template,encoding='utf-8')
 preserved=docs(m)
 jobs=[read(p) for p in sorted((F/'assets/batches').glob('*.json'))]
 write(F/'generation.json',{'tool_policy':'built-in image_gen only','jobs':jobs,'source_pdf':'references/source.pdf','visual_source_pages':['source-pages/page-1.png','source-pages/page-2.png'],'original_answer_key':'Not inferred; listening not independently audited.'})
 write(F/'validation.json',{'result':'pass','review':'3-4','item_count':2,'checks':checks,'audio_validation':'Byte-for-byte source identity; not independently listened/transcribed.','challenge_audio':'Missing; owner to provide. Required/optional/shared clips documented.','challenge_exercise_sha256_unchanged':preserved,'original_listening_answers':'Not inferred or marked.','source_coverage':'Both full pages; all six a/b pairs and four commands plus bottom Please scene visually inspected.'})
 report=read(F/'validation.json')
 report['preview_validation']={name:read(F/name) for name in ['browser-validation.json','preview-validation.json','http-validation.json'] if (F/name).exists()}
 report['browser_screenshot_review']='Both screenshots visually inspected: complete page imagery, readable text, controls and quiz feedback; no clipping.'
 write(F/'validation.json',report)
 for f in [F/'README.md',F/'questions.md',U/'Review 3-4(2).md',U/'Review 3-4 - Cau hoi theo trang.md']:
  for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
   assert (f.parent/unquote(target)).exists(),(f,target)
 package()
 print('PASS2/2:PNG/WebP1200x1200,exact audio,quiz flags/answers,links,PNG rebuild,Challenge preservation,ZIP CRC/content')

def package():
 dest=U/'Review_3-4_regenerated.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
  for p in F.rglob('*'):
   if p.is_file() and '__pycache__' not in p.parts and '.browser-check' not in p.parts:z.write(p,p.relative_to(F))
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  for p in read(F/'manifest.json')['items']:
   for item in [p['output']['png'],p['output']['webp'],p['audio_file']]:assert z.read(item)==(F/item).read_bytes()
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--import-batch');ap.add_argument('--split-x',type=int);ap.add_argument('--note');ap.add_argument('--render',action='store_true');ap.add_argument('--export',action='store_true');ap.add_argument('--package',action='store_true');a=ap.parse_args()
 if a.import_batch:import_batch(a.import_batch,a.split_x,a.note)
 if a.render:render_all()
 if a.export:export()
 if a.package:package()
