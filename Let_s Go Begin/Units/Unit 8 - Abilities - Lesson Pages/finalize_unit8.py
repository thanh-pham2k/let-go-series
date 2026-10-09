"""Finalize Unit8 documentation and audit without writing other units."""
from pathlib import Path
from urllib.parse import unquote
import json,re,zipfile,hashlib
from PIL import Image
R=Path(__file__).resolve().parent
U=R.parent
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
m=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
m['visual_review_scope']='All16 final1200x1200 PNGs and contact sheet viewed against source pages; CD2_68 rechecked after lowercase-y repair.'
if 'Lowercase y added' not in m['items'][14]['visual_review']:
 m['items'][14]['visual_review']+=' Lowercase y added by built-in repair and final PNG rechecked; all six X/x Y/y Z/z glyphs present.'
write(R/'manifest.json',m)
report=json.loads((R/'validation.json').read_text(encoding='utf-8'))
for check,p in zip(report['checks'],m['items']):check['visual_review']=p['visual_review']
report['visual_audit']={'result':'pass','final_pngs_viewed':[p['track'] for p in m['items']],'contact_sheet_viewed':True,'source_pages_viewed':list(range(1,9)),'lyrics_lines':14,'alphabet_glyphs':52,'game_spaces':14,'game_circle_children':5,'game_line_children':4,'ahead_spaces':2,'back_spaces':3,'quiz_not_in_images':True}
report['limitations']=['Source MP3 byte identity checked; speech not independently listened/transcribed.','Challenge clips not created; project owner must supply them.']
write(R/'validation.json',report)
readme=(R/'README.md').read_text(encoding='utf-8').split('## Đối chiếu và điều chỉnh cụ thể')[0].rstrip()+'\n'
readme+='''
## Đối chiếu và điều chỉnh cụ thể

- CD2_54: sắp lại thành các khung hội thoại để chỉ rõ người nói; giữ bốn câu gốc.
- CD2_55: bỏ chữ viết tay trên bản scan; giữ hai chỗ trống chưa điền và dấu chấm gốc.
- CD2_58 dùng hai lệnh ở D cùng trang65; CD2_60 dùng bốn hình/từ ở A cùng trang66.
- CD2_62 dùng hai câu và bốn cặp hình suy nghĩ cùng trang67; CD2_64 dùng bốn hình/từ cùng trang68; CD2_66 dùng hội thoại và tám hình cùng trang69. Đây là các mục nguồn chỉ có tiêu đề; không thêm lời chant chưa in.
- CD2_67 sắp52 glyph thành nhiều hàng để đọc rõ, vẫn đúng thứ tự và màu X/Y/Z.
- CD2_68 giữ hoạt động Find the letters, cả X/x Y/y Z/z, không khoanh đáp án.
- CD2_69 giữ14 ô liên tục, **Move ahead2 spaces** và **Move back3 spaces** đúng PDF. Hình Make a circle có5 trẻ; Make a line có4 trẻ.
- Bố cục minh họa được vẽ lại, không phải bản sao pixel của scan. Những lần sinh có sai nội dung được ghi trong job; chỉ selected_regions được đưa vào trang cuối.

Đã xem riêng cả16 PNG sau cắt và contact sheet. lesson_specs.json lưu chữ bắt buộc; manifest ghi box cắt thực tế. Các cặp sửa được sinh trái/phải, trang sửa đơn dùng toàn ảnh; mọi trang contain trên canvas1200×1200, không kéo méo.

Để dựng lại từ batch đã chọn: chạy assemble_unit8.py trong thư mục này, rồi lệnh render/export ở root. Không chỉnh script chung.
'''
(R/'README.md').write_text(readme,encoding='utf-8')
doc=U/'Unit 8 - Abilities(2).md'
text=doc.read_text(encoding='utf-8')
note='''<!-- source-discrepancies -->
### Lưu ý đối chiếu PDF

PDF trang71 in **Move ahead2 spaces**; một số bài luyện cũ bên dưới dùng **Move ahead3 spaces**. Giữ nội dung người dùng đã sửa như biến thể luyện thêm, không xem số3 là trích nguyên nguồn. Bảng trò chơi chuẩn CD2_69 dùng số2.
Câu **What can you do?** có trong bài luyện cũ nhưng không thấy in trên8 trang PDF này; giữ như phần mở rộng, không khẳng định là câu nguồn.
<!-- /source-discrepancies -->

'''
if '<!-- source-discrepancies -->' not in text:
 text=text.replace('# Nội dung cần nắm',note+'# Nội dung cần nắm',1)
# Add type/use to automatically produced pool without changing old exercises.
required={'ride_a_bicycle':'Challenge1§2,2§2; chọn ngẫu nhiên trong nhóm','sing_a_song':'Challenge1§2; chọn ngẫu nhiên trong nhóm','fly_a_kite':'Challenge1§2,2§2','bounce_a_ball':'Challenge1§2','swim':'Challenge1§2,2§2','smile':'Challenge1§2','wink':'Challenge1§2','dance':'Challenge1§2,2§2','let_s_play':'Challenge2§1.1','ok_let_s_play_ball':'Challenge2§1.2','ok_let_s_play_tag':'Challenge2§1.3','ok_let_s_jump_rope':'Challenge2§1.4','point_to_the_board':'Challenge2§1.5,§4;5§7','go_to_the_board':'Challenge2§1.6,§4;5§7','can_you_swim':'Challenge2§1.7,§3.2;3§4','can_you_dance':'Challenge2§1.8,§3.1;3§4','yes_i_can':'Challenge2§1.9','no_i_can_t':'Challenge2§1.10','can_you_jump':'Challenge2§3.3','i_can_fly_a_kite':'Challenge3§4','i_can_t_fly_a_kite':'Challenge3§4','jump':'Challenge2§4;5§7','stand_up':'Challenge2§4;5§7','make_a_circle':'Challenge2§4;5§7','sit_down':'Challenge2§4;5§7','walk':'Challenge2§4;5§7','skip':'Challenge2§4;5§7','make_a_line':'Challenge2§4;5§7','run':'Challenge2§4;5§7','stop':'Challenge2§4;5§7','move_ahead_3_spaces':'Challenge5§7 biến thể luyện thêm số3; không phải số PDF','move_back_3_spaces':'Challenge5§7'}
text=text.replace('| Đã có | Tên file gợi ý | Nội dung cần đọc |','| Đã có | Tên file gợi ý | Nội dung cần đọc | Mức cần | Dùng chung cho |').replace('|---|---|---|\n| ☐ |','|---|---|---|---|---|\n| ☐ |')
def row(match):
 filename,value=match.groups();slug=filename[3:-4]
 return '| ☐ | `'+filename+'` | '+value+' | '+('Bắt buộc khi chạy nghe tự động' if slug in required else 'Tùy chọn')+' | '+required.get(slug,'Luyện nói/đọc; không có yêu cầu nghe riêng')+' |'
text=re.sub(r'^\| ☐ \| `(u8_[^`]+\.mp3)` \| ([^\n|]+?) \|$',row,text,flags=re.M)
extra='''
## Bổ sung sau rà checklist tự động

Bảng trên phân loại31 clip bắt buộc cho các bài nghe hiện có và12 clip tùy chọn. Một câu trùng giữa nhiều bài dùng cùng file; nhóm nghe từ ngẫu nhiên phải chọn clip thuộc đúng bốn lựa chọn của từng câu. Không lấy đoạn CD dài làm clip ngắn mặc định. Tất cả vẫn chưa có file.

| Đã có | File gợi ý | Nội dung | Mức cần / phạm vi |
|---|---|---|---|
| ☐ | `u8_move_ahead_2_spaces.mp3` | Move ahead2 spaces. | Bắt buộc nếu tự động đọc ô trò chơi chuẩn; số2 theo PDF |
| ☐ | `u8_fox.mp3` | fox | Tùy chọn; phonics tự nói/ghép từ |
| ☐ | `u8_yarn.mp3` | yarn | Tùy chọn; phonics tự nói/ghép từ |
| ☐ | `u8_zebra.mp3` | zebra | Tùy chọn; phonics tự nói/ghép từ |
| ☐ | `u8_alphabet_upper_lower.mp3` | A–Z rồi a–z | Tùy chọn; đọc chữ, không tự thêm lời hát |
| ☐ | `u8_dialogue_play_ball.mp3` | Let's play. / OK. Let's play ball. | Tùy chọn; hai lượt cho Challenge5§9.1 |
| ☐ | `u8_dialogue_dance_yes.mp3` | Can you dance? / Yes, I can. | Tùy chọn; hai lượt cho Challenge5§9.2 |
| ☐ | `u8_dialogue_swim_no.mp3` | Can you swim? / No, I can't. | Tùy chọn; hai lượt cho Challenge5§9.3 |
| ☐ | `u8_dialogue_jump_yes.mp3` | Can you jump? / Yes, I can. | Tùy chọn; hai lượt cho Challenge5§9.4 |

Các bài điền, nhìn hình, sắp xếp chữ và tự nói không bắt buộc bản thu nếu giao diện không thêm chức năng nghe. Giọng Boss riêng là tùy chọn. Checklist này rà theo yêu cầu nghe trong Markdown; chưa có xác nhận nội dung bản thu.
'''
if '## Bổ sung sau rà checklist tự động' not in text:
 text=text.replace('<!-- /challenge-audio-notes -->',extra+'\n<!-- /challenge-audio-notes -->')
# derive honest pool counts instead of hard-coding
text=text.replace('31 clip bắt buộc','%d clip bắt buộc'%len(required)).replace('12 clip tùy chọn','%d clip tùy chọn'%(43-len(required)))
for before,after in [('ahead2','ahead 2'),('back3','back 3'),('ahead3','ahead 3'),('có5','có 5'),('có4','có 4'),('số2','số 2'),('số3','số 3'),('trang71','trang 71'),('trên8','trên 8')]:
 text=text.replace(before,after)
 readme=readme.replace(before,after)
doc.write_text(text,encoding='utf-8')
(R/'README.md').write_text(readme,encoding='utf-8')
# Provenance for superseded attempts; preserve reference assets and truthful status.
for path in (R/'assets/batches').glob('*.json'):
 job=json.loads(path.read_text(encoding='utf-8'))
 if 'selected_regions' not in job:
  job['status']='superseded_not_used'
 job.setdefault('result_file',path.stem+'.png' if (path.with_suffix('.png')).exists() else None)
 write(path,job)
# Audit mapping16 items recursively and all referenced resources.
mapping=json.loads((U.parent/'lets_go_audio_mapping.metadata').read_text(encoding='utf-8'))
found={}
def walk(v):
 if isinstance(v,dict):
  if v.get('unit')==8 and isinstance(v.get('audio'),dict):found[v['audio']['audio_key']]=v
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(mapping)
assert len(m['items'])==16
for p in m['items']:
 ref=found[p['audio_key']]
 assert ref['pdf_page']==p['unit_pdf_page'] and ref['book_page']==p['book_page']
 q=p['question'];assert len(set(c['id'] for c in q['choices']))==len(q['choices'])
 assert q['correct_choice_id'] in [c['id'] for c in q['choices']]
 assert q['show_after_audio'] and not q['render_in_lesson_image']
 for fmt in ['png','webp']:
  with Image.open(R/p['output'][fmt]) as im:assert im.size==(1200,1200)
for file in [R/'README.md',R/'questions.md',doc,U/'Unit 8 - Abilities - Cau hoi theo trang.md']:
 for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
  assert (file.parent/unquote(target)).exists(),(file,target)
report['mapping_validation']='16 printed track keys/pages verified against read-only overall mapping.'
report['markdown_links']='All links in README/questions and both external Markdown files exist.'
report['preview_runtime_validation']='Node VM mock DOM passed:16 options/image-audio paths/3 choices each,ended reveal,feedback,reset,navigation bounds; no independent browser/audio playback audit.'
write(R/'validation.json',report)
preview=(R/'preview.html').read_text(encoding='utf-8')
preview=re.sub(r'const manifest=.*?;\nconst pages=',lambda _: 'const manifest='+json.dumps(m,ensure_ascii=False).replace('<','\\u003c')+';\nconst pages=',preview,flags=re.S)
(R/'preview.html').write_text(preview,encoding='utf-8')
dest=U/'Unit_8_Abilities_regenerated.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for path in R.rglob('*'):
  if path.is_file() and '__pycache__' not in path.parts:z.write(path,path.relative_to(R))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for p in m['items']:
  assert z.read(p['output']['png'])==(R/p['output']['png']).read_bytes()
 assert json.loads(z.read('validation.json'))['item_count']==16
print('Final audit pass:16 tracks,32 images,16 quizzes,source audio/mapping,Markdown links,ZIP CRC and entries.')
print('Required challenge pool:',len(required),'optional:',43-len(required),'plus conditional game2 clip and optional phonics/dialogues.')

