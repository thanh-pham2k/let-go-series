from pathlib import Path
import json,re,zipfile,hashlib
from urllib.parse import unquote
from PIL import Image
F=Path(__file__).resolve().parent
U=F.parent
m=json.loads((F/'manifest.json').read_text(encoding='utf-8'))
assert len(m['items'])==18 and all(p['status']=='reviewed' for p in m['items'])
doc=U/'Unit 5 - Animals(2).md'
s=doc.read_text(encoding='utf-8')
extra='''
## Phân loại clip và đối chiếu bài nghe

Các clip dưới đây chưa được cung cấp. Checkbox trong kho bản thu chỉ là danh sách cần chuẩn bị; câu trùng dùng chung clip.

- **Bắt buộc để tự động chạy bài nghe:** Challenge 1 mục 3.1–3.4 cần chọn clip từ đúng trong lựa chọn từng câu; dùng kho dog/dogs, cat/cats, bird/birds, cow/cows, rabbit/rabbits, duck/ducks. Không mặc định một đáp án cho câu ngẫu nhiên.
- **Bắt buộc:** Challenge 2 mục 1.1–1.8 cần Here you are.; Thank you.; Jump.; Skip.; Let's count the cats.; How many ducks?; How many cows?; How many cars?. Mục 2 dùng dogs, cat, birds, rabbits. Mục 3 dùng How many ducks?, How many cows?, How many cars?, Here you are.. Mục 4 dùng Jump./Skip. ngẫu nhiên.
- **Bắt buộc:** Challenge 3 mục 4 dùng Let's count the cats.; 3 ducks.; 8 cows.; 8 cars..
- **Bắt buộc:** Challenge 5 các mục Commands, kể cả Commands — Nghe và làm, dùng chung Jump./Skip.. Mẫu Mini Conversation có thể dùng kho câu để phát lượt người lớn: Here you are.; Let's count the cats.; How many ducks?; How many cows?; How many cars?. Khi người lớn trực tiếp đọc thì không cần clip để thực hành.
- **Tùy chọn:** bài nhìn hình, ghép từ, viết, tự nói; moon/nest/octopus/peach; bảng chữ cái A–Z/a–z; Thank you, thank you!; Let's count.; 1 train, 2 trains, 3 trains.; bản hội thoại đủ hai lượt và giọng Boss. Kho từ/câu hỗ trợ luyện phát âm có thể thu sau.
- **Clip dùng chung:** Here you are./Thank you. dùng ở Challenge 2 và hội thoại Challenge 5; các câu hỏi How many… dùng ở Challenge 2/5; Let's count the cats. dùng ở Challenge 2/3/5; Jump./Skip. dùng ở mọi mục nghe lệnh. Câu trả lời 3 ducks./8 cows./8 cars. dùng ở Challenge 3 và mẫu hội thoại nếu cần phát đáp án.

Không có audio Challenge mới được tạo trong lần hoàn thiện này. Audio CD chính chỉ được kiểm tra khớp byte với nguồn, chưa nghe hoặc chép lời độc lập.
'''
marker='<!-- challenge-audio-classification -->'
if marker not in s:s+='\n'+marker+'\n'+extra+'\n<!-- /challenge-audio-classification -->\n'
words=['dog','dogs','cat','cats','bird','birds','cow','cows','rabbit','rabbits','duck','ducks']
s+='\n## Clip từ đơn còn thiếu trong checklist tự động\n\n| Đã có | Tên file gợi ý | Nội dung | Dùng |\n|---|---|---|---|\n'
for w in words:s+=f'| ☐ | `u5_{w}.mp3` | {w} | Bắt buộc: Challenge 1 nghe chọn từ; dùng chung Challenge 2 khi phù hợp. |\n'
s+='\nCác bản thu chữ M m — moon… trong kho là tùy chọn; có thể thu thêm moon/nest/octopus/peach riêng để dùng chung cho luyện phát âm.\n'
s=s.replace('---\n\n---','---')
doc.write_text(s,encoding='utf-8')
r=F/'README.md'
s=r.read_text(encoding='utf-8')
s+='''
## Điều chỉnh và đối chiếu nguồn

Nguồn đối chiếu: ../Unit 5 - Animals.pdf; references/CD2_02.png–CD2_19.png và source-pages/page-01.png–page-08.png. Minh họa được vẽ lại bằng built-in image_gen. Một số nhóm được giãn hoặc sắp theo hàng để đếm rõ; giữ số nhóm, số lượng, màu và chữ học. CD2_06/08/12/14 dùng nội dung bài tương ứng cùng trang nguồn thay cho crop chỉ có tiêu đề. CD2_10/15 chỉ giữ nội dung in trong PDF, không thêm lời hát. CD2_15 sửa lựa chọn “Gà” thành “Chim” theo nhóm birds trong nguồn. CD2_16 chia bảng chữ thành hàng để đủ 26 cặp; M–P giữ màu nhấn. Câu hỏi và đáp án nằm trong metadata, không ghép lên ảnh.

Đường chia batch được lưu trong manifest; mỗi crop được contain trên canvas vuông, không kéo méo. Kiểm tra nội dung trực quan được ghi riêng cho từng track; kiểm tra kỹ thuật không thay cho đếm vật hoặc so chữ. Audio chưa được nghe/transcribe độc lập; clip Challenge còn chờ chủ dự án bổ sung.
'''
r.write_text(s,encoding='utf-8')
checks=[]
for p in m['items']:
 for fmt in ['png','webp']:
  with Image.open(F/p['output'][fmt]) as im:assert im.size==(1200,1200)
 q=p['question'];assert len(q['choices'])==3 and q['correct_choice_id'] in [c['id'] for c in q['choices']]
 assert q['show_after_audio'] and not q['render_in_lesson_image']
 checks.append(p['track'])
for f in [F/'README.md',F/'questions.md',doc,U/'Unit 5 - Animals - Cau hoi theo trang.md']:
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):assert (f.parent/unquote(link)).exists(),(f,link)
report=json.loads((F/'validation.json').read_text(encoding='utf-8'))
report['visual_validation']='All 18 final cropped PNG pages inspected against source; detailed per-track reviews in manifest.'
report['challenge_audio']='Missing; owner to supply mandatory listening clips. Optional and shared clips documented.'
(F/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
zpath=U/'Unit_5_Animals_regenerated.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in F.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(F))
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for p in m['items']:
  for key in ['png','webp']:assert z.read(p['output'][key])==(F/p['output'][key]).read_bytes()
  assert z.read(p['audio_file'])==(F/p['audio_file']).read_bytes()
print('Final audit PASS:',len(checks),'tracks; links, canvas, quiz flags, ZIP CRC/content; Challenge audio explicitly pending.')
