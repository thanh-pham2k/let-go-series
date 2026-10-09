from pathlib import Path
from urllib.parse import quote
import re,json,hashlib
ROOT=Path(__file__).resolve().parent
doc=ROOT.parent/'Review 1-2(3).md'
original=doc.read_text(encoding='utf-8')
backup=ROOT/'references/challenge-original.md'
if not backup.exists():backup.write_text(original,encoding='utf-8')
text=original
changes=[('- go\n','- come here\n'),('**go**','**come here**'),('- [ ] đi\n','- [ ] lại đây\n'),('11. go →','11. come here →'),('11. đi →','11. lại đây →'),('| go |','| come here |'),('🧻','🖼️ hộp băng keo')]
counts={}
for old,new in changes:
    counts[old]=text.count(old);text=text.replace(old,new)
text=re.sub(r'\*\*Coverage:.*?\*\*','**Phạm vi đối chiếu:** đã rà hai trang PDF: sáu cặp nhận biết và năm đồ dùng/câu mẫu. Câu trắc nghiệm bổ sung không xác nhận đáp án bài nghe gốc; audio chưa được nghe độc lập.',text)
def link(label,name):return f'[{label}]({quote(ROOT.name+"/"+name,safe="/")})'
block=f'''<!-- review-package-status -->
## Bộ Review chuẩn

Hai mục CD1_36–37 theo đúng marker PDF; không chia sáu cặp lựa chọn thành track mới. Trang School Supplies giữ đủ paper, scissors, glue, paint, tape và câu “I have paper.”; cảnh câu mẫu cùng trang không có marker audio riêng.

- {link('Preview','preview.html')} · {link('Contact sheet','preview.jpg')}.
- {link('Metadata','review.regenerated.metadata')} · {link('Câu hỏi theo trang','questions.md')}.

Đối chiếu PDF trang1, cặp6a: bé đi về phía cô giáo tương ứng Come here, nên sửa go/đi thành come here/lại đây trong bài luyện. Thay emoji giấy vệ sinh bằng mô tả hộp băng keo cho tape. Các bài luyện khác được giữ nguyên; xem bản gốc lưu tại references/challenge-original.md để đối chiếu. Không tự đặt đáp án Listen and circle khi chưa nghe.
<!-- /review-package-status -->

'''
text=re.sub(r'<!-- review-package-status -->.*?<!-- /review-package-status -->\s*','',text,flags=re.S)
first,rest=text.split('\n',1);text=first+'\n\n'+block+rest.lstrip('\n')
text=re.sub(r'<!-- challenge-audio-notes -->.*?<!-- /challenge-audio-notes -->\s*','',text,flags=re.S)
notes='''
<!-- challenge-audio-notes -->
# Audio clip riêng cần bổ sung

Chủ dự án tự cung cấp. Tất cả ô dưới đây **chưa hoàn thành**, tên file chỉ là gợi ý, chưa có file audio riêng tương ứng. CD1_36/37 có sẵn cho trang học chính, không mặc định thay các clip ngẫu nhiên của Challenge. Mỗi nội dung thu một clip dùng chung cho các bài liệt kê; không thu lặp cho từng câu. Chọn ngẫu nhiên đúng tập lựa chọn của câu hiện tại.

| Đã có | File gợi ý | Nội dung đọc | Mức / bài dùng chung |
|---|---|---|---|
'''
for word in ['car','train','bicycle','ball','green','red','purple','yellow','paper','scissors','glue','paint','tape']:
    use='Challenge 1.4; 2.1' if word in ['car','train','bicycle','ball'] else 'Challenge 1.4; 2.2' if word in ['green','red','purple','yellow'] else 'Challenge 1.4; 2.4'
    notes+=f'| ☐ | `r12_{word}.mp3` | {word} | Cần thiết — {use}; tùy chọn làm mẫu phát âm ở bài tự nói |\n'
for slug,utterance in [('stand_up','Stand up.'),('sit_down','Sit down.'),('come_here','Come here.'),('turn_around','Turn around.')]:
    notes+=f'| ☐ | `r12_{slug}.mp3` | {utterance} | Cần thiết — Challenge 2.3; 5.4, dùng chung mỗi lệnh |\n'
notes+='| ☐ | `r12_i_have_paper.mp3` | I have paper. | Cần thiết — Challenge 2.5; 3.5. Tùy chọn làm mẫu ở 3.4; 4; 5.6–8 |\n'
notes+='''
Bài nhìn hình, điền, dịch và tự nói không bắt buộc clip riêng. Giọng Boss, hướng dẫn tiếng Việt và câu mẫu bổ sung là tùy chọn. Challenge 5.5 hiện hướng dẫn người lớn **chỉ hình** để bé tự nói, nên không bắt buộc audio dù tiêu đề có “Nghe”. Không thêm câu “I have scissors/glue/paint/tape” như nội dung PDF bắt buộc: nguồn chỉ in “I have paper.” Không có hội thoại hai lượt trong Review này cần thu thêm.

<!-- /challenge-audio-notes -->
'''
doc.write_text(text.rstrip()+'\n'+notes,encoding='utf-8')
(ROOT/'challenge-changes.json').write_text(json.dumps({'source_original_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'replacements':counts,'preserved_challenges':list(range(1,6)),'audio_clips_required':18,'audio_created':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('Challenge preserved; source-confirmed come-here/tape corrections; 18 pending shared audio clips.')
