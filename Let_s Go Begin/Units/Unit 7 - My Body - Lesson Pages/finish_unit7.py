from pathlib import Path
from urllib.parse import unquote
import json,re,zipfile,hashlib
ROOT=Path(__file__).resolve().parent
UNITS=ROOT.parent
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
doc=UNITS/'Unit 7 - My Body(2).md'
text=doc.read_text(encoding='utf-8-sig')
start='<!-- unit7-audio-audit -->';end='<!-- /unit7-audio-audit -->'
text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n*','',text,flags=re.S)
notes='\n'+start+'\n## Phân loại clip và đối chiếu bài nghe Challenge\n\nTất cả clip bổ sung dưới đây **chưa có**. Một bản thu dùng chung cho các mục được liệt kê; bắt buộc chỉ khi chạy bài nghe tự động. Người lớn đọc trực tiếp vẫn dùng được. Không dùng nguyên track CD để thay clip ngắn mà chưa chọn đúng đoạn.\n\n| Đã có | Ưu tiên | Clip dùng chung | Nội dung | Nơi dùng |\n|---|---|---|---|---|\n'
body=['head','shoulders','knees','toes','eyes','ears','mouth','nose']
models=["Oops! I'm sorry.","That's OK.","I can touch my head.","What can you do?","I can touch my nose.","I can touch my eyes.","Stamp your feet.","Clap your hands.","I can touch the red circle."]
for v in body+models:
 slug=re.sub(r'[^a-z0-9]+','_',v.lower()).strip('_')
 if v in body:where='C1 §2 chọn từ ngẫu nhiên trong lựa chọn; C2 §2 dùng head/eyes/ears/nose'
 elif v in models[:2]:where='C2 §1, §3; C5 §9 tình huống 1 nếu phát mẫu'
 elif v=="What can you do?":where='C2 §1, §3 (dùng chung hai lần); C5 §9 nếu phát mẫu'
 elif v in models[6:8]:where='C2 §1, §4; C5 §7'
 elif v in models[2:6]:where='C2 §1; C3 §4; C5 §9 nếu phát mẫu'
 else:where='C2 §1.9; C5 §9 tình huống 4 nếu phát mẫu'
 notes+=f'| ☐ | Bắt buộc cho nghe tự động | `u7_{slug}.mp3` | {v} | {where} |\n'
for v in ['umbrella','violin','watch','A to Z / a to z']:
 slug=re.sub(r'[^a-z0-9]+','_',v.lower()).strip('_')
 notes+=f'| ☐ | Tùy chọn | `u7_{slug}.mp3` | {v} | C1 §4, C4 §4, C5 §8: bài nhìn/đọc/nói, không bắt buộc phát mẫu |\n'
notes+='\n**Hội thoại hai lượt tùy chọn:** có thể ghép các clip dùng chung hoặc thu nguyên cặp Oops!/That’s OK.; What can you do?/I can touch my head.; What can you do?/I can touch my eyes.; What can you do?/I can touch my nose. Không bỏ clip câu hỏi dùng chung. Giọng Boss khác là tùy chọn.\n\nKho tự động ở trên là danh sách ứng viên; bảng phân loại này xác định yêu cầu thực tế. Không đánh dấu hoàn thành khi chỉ có tên gợi ý.\n'+end+'\n'
text=text.rstrip()+'\n'+notes
doc.write_text(text,encoding='utf-8')
original=(ROOT/'references/challenge-original.md').read_text(encoding='utf-8-sig')
# Exercise body must remain unchanged; generated status and audio notes are outside this span.
def exercises(t):return t[t.index('# Challenge 1'):t.index('# Coverage Check')]
assert exercises(original)==exercises(text),'Challenge exercises changed'
readme=ROOT/'README.md'
r=readme.read_text(encoding='utf-8')
r+='\n## Điều chỉnh có nguồn đối chiếu\n\n'
for p in m['items']:
 if p.get('adaptation_notes'):r+='- '+p['track']+': '+p['adaptation_notes']+'\n'
r+='\nĐã xem từng PNG sau cắt và contact sheet; kiểm tra từ, nhãn, số thứ tự, vị trí chạm và câu thoại với 8 trang PDF nguồn. Mặt đồng hồ là minh họa cho watch, không phải bài đọc giờ. references/lesson-crops giữ vùng bài học đã chọn; lesson_specs.json và manifest lưu đặc tả. Bản thu Challenge cần bổ sung, xem bảng bắt buộc/tùy chọn ở tài liệu bên ngoài.\n'
readme.write_text(r,encoding='utf-8')
meta=ROOT/'unit.regenerated.metadata'
data=json.loads(meta.read_text(encoding='utf-8'))
for p,it in zip(m['items'],data['items']):
 if p.get('adaptation_notes'):it['adaptation_notes']=p['adaptation_notes']
meta.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
# Keep practice hidden until audio ends; resets when switching tracks.
preview=ROOT/'preview.html'
html=preview.read_text(encoding='utf-8')
html=html.replace("audio.src=p.audio_file;","audio.src=p.audio_file;document.getElementById('review').disabled=true;")
html=html.replace("function review(){","function review(){document.getElementById('review').disabled=false;")
preview.write_text(html,encoding='utf-8')
for file in [doc,UNITS/'Unit 7 - My Body - Cau hoi theo trang.md',ROOT/'README.md',ROOT/'questions.md']:
 for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
  assert (file.parent/unquote(target)).exists(),(file,target)
report=ROOT/'validation.json';d=json.loads(report.read_text(encoding='utf-8'))
d['visual_content_review']={'result':'pass','source_pdf_pages':8,'all_final_pages_viewed':17,'checks':['Exact eight source lyric lines in CD2_39','Two blanks retained in CD2_38','Body labels and numbered actions compared with source','All 26 upper/lowercase alphabet pairs and Uu/Vv/Ww search glyphs','Final source game object colors, counts and speaker roles','No cropped lesson text or gutter intrusion']}
d['challenge_exercises_preserved']=True
d['challenge_audio_status']='Additional short clips not created; mandatory/optional/shared checklist added.'
report.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
dest=UNITS/'Unit_7_My_Body_regenerated.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for path in ROOT.rglob('*'):
  if path.is_file() and '__pycache__' not in path.parts:z.write(path,path.relative_to(ROOT))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for p in m['items']:
  for fmt in ['png','webp']:
   assert z.read(p['output'][fmt])==(ROOT/p['output'][fmt]).read_bytes()
print('Challenge body unchanged; Markdown links valid; adaptations documented; updated ZIP opens and matches all 34 images.')

