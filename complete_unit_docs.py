"""Link completed lesson packages and preserve additional exercise audio notes."""
from pathlib import Path
from urllib.parse import quote,unquote
import argparse,json,re
ROOT=Path(__file__).resolve().parent/'Let_s Go Begin/Units'

def run(unit):
    folder=next(ROOT.glob(f'Unit {unit} - * - Lesson Pages'))
    m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    assert all(p['status']=='reviewed' for p in m['items'])
    doc=next(p for p in ROOT.glob(f'Unit {unit} - *(*).md') if 'Cau hoi' not in p.name)
    text=doc.read_text(encoding='utf-8-sig')
    start='<!-- lesson-package-status -->';end='<!-- /lesson-package-status -->'
    if start in text:text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n*','',text,flags=re.S)
    def link(label,name):return f'[{label}]({quote(folder.name+"/"+name,safe="/")})'
    block=f'''{start}
## Bộ bài học chính và tài nguyên luyện thêm

Đã có đủ **{len(m['items'])} trang học chính**, mỗi trang gồm ảnh có chữ → audio → một câu trắc nghiệm. PNG/WebP đều **1200 × 1200**.

- {link('Preview học và làm bài','preview.html')} · {link('Xem cả bộ ảnh','preview.jpg')}.
- {link('Metadata tích hợp','unit.regenerated.metadata')}.
- [{doc.stem.split('(')[0].strip()} – Câu hỏi theo trang]({quote('Unit '+str(unit)+' - '+m['topic']+' - Cau hoi theo trang.md',safe='/')}).

Các Challenge bên dưới là bài luyện thêm, giữ nguyên nội dung. Ký hiệu 🖼️ là hướng dẫn chọn hình, chưa phải asset riêng gắn cho từng câu. Người lớn có thể đọc phần nghe; để chạy tự động cần audio clip riêng. Chủ dự án sẽ tự bổ sung audio theo checklist cuối file. Audio CD nguồn đã kiểm tra file, chưa nghe/transcribe độc lập.
{end}

'''
    lines=text.splitlines(keepends=True);text=lines[0]+'\n'+block+''.join(lines[1:]).lstrip('\n')
    # Do not retain a blanket coverage claim as if the extra exercises were audited.
    text=re.sub(r'\*\*Coverage: 100%.*?\*\*','**Phạm vi:** xem bảng đối chiếu nội dung bên trên; bộ trang học chính và Challenge luyện thêm được quản lý riêng.',text)
    notes_start='<!-- challenge-audio-notes -->';notes_end='<!-- /challenge-audio-notes -->'
    if notes_start in text:text=re.sub(re.escape(notes_start)+r'.*?'+re.escape(notes_end)+r'\n*','',text,flags=re.S)
    front=text.split('# Challenge',1)[0]
    # Source coverage vocabulary and model sentences form a reusable recording pool.
    candidates=[]
    for row in front.splitlines():
        if row.startswith('- ') and not '](' in row:
            value=row[2:].strip().strip('*`')
            if re.fullmatch(r"[A-Za-z0-9 ,.!?'’—–-]+",value) and any(c.isalpha() for c in value):candidates.append(value)
        if row.startswith('`'):
            candidates+=re.findall(r'`([A-Za-z][A-Za-z -]+)`',row)
    # Explicit English utterances in listening tasks supplement the reusable pool.
    for value in re.findall(r'(?:Nghe:|Nghe|Người lớn đọc:)\s*(?:\*\*|[“"])([A-Za-z][A-Za-z0-9 ,.!?\'’-]+)',text):candidates.append(value.rstrip('*'))
    clips=[]
    for v in candidates:
        if v not in clips and v not in ['A–Z / a–z']:clips.append(v)
    notes=f'''\n---\n\n{notes_start}
# Ghi chú audio cần bổ sung cho Challenge – Unit {unit}

**Người bổ sung:** chủ dự án tự chuẩn bị. Các file dưới đây là tên gợi ý, chưa có audio tương ứng và chưa đánh dấu hoàn thành. Audio theo track của bài học chính đã có, không thay thế mặc định các clip ngắn này.

Đây là kho bản thu theo từ vựng/câu mẫu để tái sử dụng giữa các Challenge. Mỗi dòng thu một clip; câu trùng dùng chung một file. Các mục không có bài nghe riêng có thể thu sau. Với mục chọn từ ngẫu nhiên, ứng dụng phải chọn một từ có trong các lựa chọn của câu đó; không tự mặc định đáp án nếu chưa chọn clip.

| Đã có | Tên file gợi ý | Nội dung cần đọc |
|---|---|---|
'''
    for i,v in enumerate(clips,1):
        slug=re.sub(r'[^a-z0-9]+','_',v.lower()).strip('_')
        notes+=f'| ☐ | `u{unit}_{slug}.mp3` | {v} |\n'
    notes+='\nNếu thu hội thoại, đọc đủ hai lượt hỏi/đáp theo bài và lưu clip riêng. Giọng Boss khác giọng bài học là tùy chọn. Khi có file, bổ sung đường dẫn thực tế và nối đúng câu luyện tập; không đánh dấu chỉ vì file được liệt kê.\n'+notes_end+'\n'
    doc.write_text(text.rstrip()+'\n'+notes,encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):assert (doc.parent/unquote(target)).exists(),target
    print('Updated',doc.name,'audio note pool:',len(clips))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);run(ap.parse_args().unit)
