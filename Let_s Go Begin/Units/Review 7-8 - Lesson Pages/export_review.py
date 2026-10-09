from pathlib import Path
from urllib.parse import quote,unquote
import json,re,hashlib,zipfile
from PIL import Image
from render_review import render
ROOT=Path(__file__).resolve().parent
UNITS=ROOT.parent
def save(name,d):(ROOT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def link(label,target):return '['+label+']('+quote(target,safe='/')+')'
def questions(m,prefix=''):
 lines=['# Review 7–8 – Câu hỏi theo trang','', 'Ba mục audio riêng, mỗi mục có một PNG/WebP1200×1200, một MP3 nguồn và đúng một câu trắc nghiệm bổ sung.','',
 '- '+link('Preview',prefix+'preview.html')+' · '+link('Contact sheet',prefix+'preview.jpg')+'.',
 '- '+link('Metadata',prefix+'review.regenerated.metadata')+'.',
 '- Câu hỏi bổ sung nhận biết nội dung nhìn thấy, không phải đáp án suy đoán của bài Listen and circle gốc.',
 '- MP3 đã đối chiếu từng byte với CD2 nguồn; chưa nghe/transcribe độc lập.','']
 for p in m['items']:
  q=p['question'];lines += ['## '+p['track']+' – '+p['exercise'],'',
   '- Trang PDF '+str(p['pdf_page'])+' / trang sách '+str(p['book_page'])+'.',
   '- Ảnh: '+link(p['track']+'.webp',prefix+p['output']['webp'])+' · '+link('PNG',prefix+p['output']['png'])+'.',
   '- Audio: '+link(Path(p['audio_file']).name,prefix+p['audio_file'])+'.',
   '- Mã câu hỏi: '+q['id']+'.','',q['prompt'],'']
  lines += ['- '+c['id']+'. '+c['text'] for c in q['choices']]+['']
 lines+=['## Đáp án','', '| Track | Đáp án |','|---|---|']
 for p in m['items']:
  q=p['question'];c=next(c for c in q['choices'] if c['id']==q['correct_choice_id']);lines+=['| '+p['track']+' | '+c['id']+'. '+c['text']+' |']
 return '\n'.join(lines)+'\n'
def update_challenge():
 doc=UNITS/'Review 7-8(2).md';text=doc.read_text(encoding='utf-8-sig')
 for name in ['review-package-status','review-source-audit','review-challenge-audio']:
  text=re.sub('<!-- '+name+' -->.*?<!-- /'+name+' -->\\n*','',text,flags=re.S)
 text=text.replace('PDF **Review 7-8(2)**','PDF chuẩn **Review 7-8.pdf**')
 text=re.sub(r'\*\*Coverage:.*?\*\*','**Phạm vi:** bảng cũ liệt kê nội dung đã đưa vào Challenge; không chứng minh đầy đủ mọi lựa chọn hình hay nội dung lời nói trong MP3. Đối chiếu nguồn và phần bổ sung ở dưới.',text,flags=re.S)
 folder=ROOT.name+'/'
 status='<!-- review-package-status -->\n## Bộ Review chính\n\nĐủ3 mục CD2_70–CD2_72 theo đúng mapping Review7–8; không thêm track cho từng cặp hình. Hai trang nguồn được adapt riêng thành3 ảnh học.\n\n- '+link('Preview học/nghe/ôn tập',folder+'preview.html')+' · '+link('Xem3 ảnh',folder+'preview.jpg')+'.\n- '+link('Metadata',folder+'review.regenerated.metadata')+' · '+link('Câu hỏi theo trang','Review 7-8 - Cau hoi theo trang.md')+'.\n\nẢnh PNG/WebP1200×1200; mỗi mục một câu trắc nghiệm riêng sau nghe hoặc bấm ôn tập. Audio CD2 trùng byte với nguồn; chưa nghe/transcribe độc lập. Các Challenge dưới đây giữ bài luyện cũ; người lớn có thể đọc trực tiếp. Clip ngắn cho chạy tự động chưa có và do chủ dự án bổ sung.\n<!-- /review-package-status -->\n\n'
 first,rest=text.split('\n',1);text=first+'\n\n'+status+rest.lstrip('\n')
 audit='''\n<!-- review-source-audit -->
## Đối chiếu nguồn và phần bổ sung

- Sửa tên nguồn từ Review7–8(2) sang **Review 7-8.pdf**; tên Markdown (2) là bản bài luyện, không phải tên PDF chuẩn.
- Sáu cặp a/b CD2_70 giữ nguyên thứ tự. Không khoanh đáp án bài nghe gốc khi chưa nghe. Những cụm hành động trong Challenge là cách gọi hình để luyện, không phải bản chép track70.
- Cặp1b có bạn nhỏ gập đầu gối và đặt hai tay lên đầu gối; giữ khác biệt với wink ở1a (một mắt đóng, một mắt mở).
- Cặp2a chạm tới ngón chân giày; cặp2b hai tay còn cách giày. Không biến hai hình thành cùng động tác hay bỏ khác biệt làm được/chưa làm được.
- Cặp5a là **giậm chân** và5b là **vỗ tay**. Bài luyện cũ chưa có hai động tác này; hình chuẩn đã giữ cả hai. dance thuộc4b, không thay cho5a.
- Sunday1, Monday2, Tuesday3, Wednesday4, Thursday5, Friday6, Saturday7 là thứ tự thẻ ngày trong PDF; phần bài luyện cũ đúng thứ tự này.
- CD2_71 giữ câu **It's Monday.** và lịch tháng có ngày1 ở cộtMonday; số thẻ ngày và ngày trong lịch tháng là hai hệ số khác nhau.
- CD2_72 có lịch hai hàng1–7 và8–14. PDF không in lời hát; không bổ sung lời hát hay tuyên bố đã chép lời audio.

### Nhận biết bổ sung từ hình nguồn (không có track riêng)

1. So sánh cặp1: hình nào wink, hình nào đặt hai tay lên đầu gối?
2. So sánh cặp2: hình nào chạm được tới ngón chân giày? Hình nào còn khoảng cách?
3. Ghép cặp5 với hai cụm: `Stamp your feet.` / `Clap your hands.`
4. Nhìn lịch CD2_72: đọc bảy tên ngày và chỉ vị trí các số1–14.

Đây là luyện nhìn/nói theo hình, không phải đáp án đã kiểm chứng của bài nghe gốc. Không mặc định clip CD2_70 nói các cụm bổ sung này theo một thứ tự cụ thể.
<!-- /review-source-audit -->
'''
 audio='\n<!-- review-challenge-audio -->\n## Audio clip riêng cần bổ sung cho Challenge\n\n**Chủ dự án tự thu; tất cả dòng chưa có file và chưa hoàn thành.** Clip dùng chung cho các câu trùng, không thu lại mỗi lần. Bắt buộc chỉ khi chạy bài nghe Challenge tự động; người lớn đọc trực tiếp vẫn dùng được. MP3 track70–72 không tự thay thế các clip ngắn nếu chưa chọn/kiểm đúng đoạn.\n\n| Đã có | Mức cần | Tên gợi ý | Nội dung cần đọc | Dùng chung ở |\n|---|---|---|---|---|\n'
 actions=['wink','touch your toes','ride a bicycle','fly a kite','swim','dance','point to the board','stand up']
 days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
 for value in actions+days+["It's Monday."]:
  slug=re.sub(r'[^a-z0-9]+','_',value.lower()).strip('_')
  if value in actions:
   where='C1 §3; C5 §5; '+('C2 §2 (câu lệnh classroom)' if value in actions[-2:] else 'C2 §1 (nghe chọn hình)')
  elif value in days:where='C1 §4; C2 §3; C5 §6; cùng một clip cho mọi lần tên ngày lặp lại'
  else:where='C2 §4; C3 §5; dùng mẫu tùy chọn cho C5 §7–8'
  audio+='| ☐ | Bắt buộc cho nghe tự động | `r7_8_'+slug+'.mp3` | '+value+' | '+where+' |\n'
 for v in ['Stamp your feet.','Clap your hands.']:
  slug=re.sub(r'[^a-z0-9]+','_',v.lower()).strip('_')
  audio+='| ☐ | Tùy chọn | `r7_8_'+slug+'.mp3` | '+v+' | Phần nhận biết bổ sung cặp5; hiện là luyện nhìn/nói, có thể thêm phát mẫu |\n'
 audio+='\nĐọc `Point to the board.` và `Stand up.` thành câu lệnh đầy đủ; dùng chung với pool action tương ứng. Bản đọc đủ bảy tên ngày liên tiếp, mẫu câu cho phần tự nói và giọng Boss riêng là tùy chọn. Không thu lời hát mới khi chưa có bản chép xác nhận; bài hát chính dùng '+link('Track72.mp3',folder+'audio/Track72.mp3')+' đã có. Nếu thêm hội thoại, lưu rõ câu cần đọc và câu nào dùng lại clip cũ.\n<!-- /review-challenge-audio -->\n'
 text=text.rstrip()+'\n'+audit+audio
 original=(ROOT/'references/challenge-original.md').read_text(encoding='utf-8-sig')
 def body(s):return s[s.index('# Challenge 1'):s.index('# Coverage Check')]
 assert body(text)==body(original),'Existing Challenge exercises changed'
 doc.write_text(text,encoding='utf-8')
 packaged=text.replace(quote(folder,safe='/'),'').replace(quote('Review 7-8 - Cau hoi theo trang.md',safe='/'),'questions.md')
 (ROOT/'challenge.md').write_text(packaged,encoding='utf-8')
 return doc
def main():
 m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
 assert len(m['items'])==3 and all(p['status']=='reviewed' for p in m['items'])
 checks=[]
 for p in m['items']:
  expected=render(p)
  q=p['question'];assert q['correct_choice_id'] in [c['id'] for c in q['choices']]
  assert len({c['id'] for c in q['choices']})==len(q['choices'])==3
  assert q['show_after_audio'] and not q['render_in_lesson_image']
  assert (ROOT/p['audio_file']).read_bytes()==Path(p['audio_source']).read_bytes()
  for ext in ['png','webp']:
   with Image.open(ROOT/p['output'][ext]) as im:
    assert im.size==(1200,1200)
    if ext=='png':assert im.convert('RGB').tobytes()==expected.tobytes()
  checks.append({'track':p['track'],'result':'pass','size':[1200,1200],'png_sha256':hashlib.sha256((ROOT/p['output']['png']).read_bytes()).hexdigest(),'audio_sha256':hashlib.sha256((ROOT/p['audio_file']).read_bytes()).hexdigest(),'visual_review':p['visual_review']})
 metadata={'format_version':'2.0','review':'7-8','item_count':3,'uniform_size':[1200,1200],'items':[{'track':p['track'],'exercise':p['exercise'],'pdf_page':p['pdf_page'],'book_page':p['book_page'],'image':p['output']['webp'],'audio_file':p['audio_file'],'size':[1200,1200],'question':p['question'],'adaptation_notes':p['adaptation_notes']} for p in m['items']]}
 save('review.regenerated.metadata',metadata)
 template=(ROOT/'preview.template.html').read_text(encoding='utf-8')
 assert '/*MANIFEST_JSON*/' in template
 html=template.replace('/*MANIFEST_JSON*/',json.dumps(m,ensure_ascii=False).replace('<','\\u003c'))
 (ROOT/'preview.html').write_text(html,encoding='utf-8')
 (ROOT/'questions.md').write_text(questions(m),encoding='utf-8')
 external=UNITS/'Review 7-8 - Cau hoi theo trang.md';external.write_text(questions(m,ROOT.name+'/'),encoding='utf-8')
 doc=update_challenge()
 readme='''# Review 7–8 – Bộ bài học chuẩn

Đủ3/3 mục audio từ **Review 7-8.pdf**: CD2_70 (trang72), CD2_71 và CD2_72 (trang73). Cả Listen and Review và Days of the Week được adapt; không tạo track mới cho từng cặp hình.

- [Preview](preview.html) · [Contact sheet](preview.jpg)
- [Metadata](review.regenerated.metadata) · [Câu hỏi](questions.md)
- [Challenge và checklist audio](challenge.md)
- [Validation](validation.json) · [Đối chiếu trực quan](visual-review.json)
- [Generation và log prompt](generation.json)

Ảnh chuẩn cho app ở **pages/webp**, PNG tương ứng ở **pages/png**. Tất cả1200×1200, contain giữ tỷ lệ, không kéo méo. assets giữ ảnh regenerate từ built-in image_gen; assets/batches giữ sheet, prompt, reference và log sửa. references/source.pdf, source-pages và references/CD2_*.png giữ nguồn đối chiếu; chúng không thay cho ảnh học regenerate.

## Nội dung và điều chỉnh

- CD2_70 giữ6 nhóm và12 hình lựa chọn a/b: wink/đặt tay lên gối; chạm được/chưa chạm tới ngón chân; đi xe đạp/thả diều; bơi/nhảy múa; giậm chân/vỗ tay; chỉ bảng/đứng lên. Không khoanh đáp án gốc hay suy ra lời MP3 từ hình.
- CD2_71 giữ7 thẻ Sunday1–Saturday7, đúng màu số, câu It's Monday. và lịch tháng: ngày1 trong cộtMonday, khác với Sunday=1 của thẻ. Tái bố trí để vừa một ảnh học, giữ nghĩa người nói/chỉ.
- CD2_72 là ảnh riêng cho Let's sing cùng trang73, giữ lịch hai hàng1–7/8–14, đủ7 tên ngày và bạn nhỏ áo xanh chỉWednesday. Không có lời hát in trong PDF; không tự thêm.
- Mỗi mục có đúng một câu trắc nghiệm nhận biết hình/chữ; câu hỏi/đáp án không nằm trên ảnh học, hiện khi audio kết thúc hoặc bấm ôn tập.

Audio trùng từng byte với Track70–72.mp3 của CD2 nguồn; **chưa nghe/transcribe độc lập**. Đáp án6 cặp nghe gốc chưa xác định. Clip ngắn cho Challenge chưa có; người dùng tự bổ sung theo checklist bắt buộc/tùy chọn và dùng chung. Bài luyện cũ được giữ nguyên; sửa tên nguồn và bỏ khẳng định coverage toàn bộ, bổ sung các khác biệt hình còn thiếu.

Tái dựng trong thư mục Review: `python render_review.py` (dựng từ layers), `python export_review.py`, `node check_preview.cjs`, `python validate_package.py`. Không chạy scripts chung của Unit cho Review. Các bản sau dựng cần xem lại nếu thay đổi asset/layers. Xem ảnh PNG riêng ở kích thước đầy đủ khi cần đọc bảng lịch nhỏ.
'''
 (ROOT/'README.md').write_text(readme,encoding='utf-8')
 save('validation.json',{'result':'technical_pass_pending_preview_check','review':'7-8','item_count':3,'uniform_size':[1200,1200],'checks':checks,'visual_content_review':json.loads((ROOT/'visual-review.json').read_text(encoding='utf-8')),'source_pdf_pages':2,'audio_validation':'Byte-for-byte comparison with CD2 source MP3s; not independently listened/transcribed.','challenge_exercises_preserved':True})
 generation=json.loads((ROOT/'generation.json').read_text(encoding='utf-8'));generation['status']='visually_reviewed';save('generation.json',generation)
 for f in [ROOT/'questions.md',ROOT/'README.md',ROOT/'challenge.md',external,doc]:
  for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
   assert (f.parent/unquote(target)).exists(),(f,target)
 print('Exported metadata,3 questions, independent preview and preserved Challenge docs; technical checks pass. Run preview validation then package.')
if __name__=='__main__':main()

