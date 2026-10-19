from pathlib import Path
import json
from urllib.parse import quote
from series_extract import ROOT,BOOKS

def build_index():
    report=json.loads((ROOT/'audit/series/validation.json').read_text(encoding='utf-8'))
    rows=[]
    for n in range(1,7):
        outdir=BOOKS[n].parent/'Units';manifest=json.loads((outdir/'source-manifest.json').read_text(encoding='utf-8'))
        stats=report['books'][n-1]
        lines=[f'# let-go-series-{n} — Tài liệu đã tách','',
        f'Nguồn: `{BOOKS[n].name}`. Dùng số trang **PDF, tính từ 1**, đúng các mốc được yêu cầu.','',
        f'- {len(manifest["sections"])} phần PDF; 72 trang nội dung.',
        f'- {stats["lesson_questions"]:,} câu hỏi theo trang; mỗi trang ít nhất {stats["min_questions_per_page"]} câu.',
        '- 8 file Challenge; mỗi file gồm 5 nhóm Recognition → Recall → Comprehension → Production.',
        '- Mỗi file câu hỏi và Challenge có đáp án cuối file. Bài nghe Challenge kèm kịch bản để người lớn đọc hoặc thu âm.',
        '- Ảnh dùng trực tiếp từ PDF nguồn. Không có ảnh/audio mới; không suy đoán đáp án bài nghe gốc.', '']
        if n in [2,4]:
            lines.extend(['**Ranh giới theo yêu cầu:** Unit 6 bắt đầu bằng hai trang cuối Unit 5 trong sách gốc. Giữ nguyên phạm vi, ghi chú ngay trên từng trang liên quan. Challenge Unit 5 chỉ dùng trang trong phạm vi Unit 5 đã tách; Challenge Unit 6 dùng phạm vi Unit 6 đã tách.',''])
        if n<3:lines.extend(['**Review:** Trang thứ hai trong mỗi phạm vi Review là mục Let’s Learn About (số đếm/cơ thể/ngày/cảm xúc ở sách 1; số đếm/tháng/mùa/giờ ở sách 2), được giữ chung theo yêu cầu.',''])
        lines.extend(['| Phần | Trang PDF gốc | Trang in trên sách | PDF | Câu hỏi theo trang | Challenge |','|---|---:|---:|---|---|---|'])
        for sec in manifest['sections']:
            name=sec['name'];pdf=quote(name+'.pdf');md=quote(name+' - Cau hoi theo trang.md');ch=quote(name+' - Challenge.md')
            challenge=f'[5 Challenge]({ch})' if sec['kind']=='Unit' else '—'
            lines.append(f'| {name} | {sec["start"]}–{sec["end"]} | {sec["printed_start"]}–{sec["printed_end"]} | [Mở PDF]({pdf}) | [Làm bài]({md}) | {challenge} |')
        lines.extend(['','## Ghi chú biên soạn','',
        'Câu hỏi được tạo từ từ vựng, mẫu câu, hình và bài đọc trong phạm vi tương ứng. Câu luyện có thể thay từ trong cùng khung của bài; không phải bản chép nguyên văn. Câu cá nhân có thể trả lời bằng thông tin thật trong phạm vi mẫu câu. Với bài đọc tiếp nối ở trang sau, câu hỏi ghi rõ trang cần đọc.','',
        'Câu trả lời mở có đáp án gợi ý. Khi ghép lại câu hỏi từ câu trả lời, chấp nhận các câu phù hợp khác trong phạm vi trang. Phần nói chấm theo đúng ý, đúng từ và mẫu câu; không yêu cầu giống hệt dấu câu.','',
        '## Kiểm tra','',
        '- Kiểm tra đủ trang, không trùng phạm vi, số trang trong file tách, mã câu hỏi/đáp án và liên kết nội bộ.',
        '- Render tất cả trang PDF tách và so sánh với trang nguồn: nội dung hiển thị khớp.',
        '- Nội dung nhận dạng chữ đã được đối chiếu với các ảnh trang nguồn được chọn, gồm các bảng từ và trang khó nhận dạng. Không coi đây là biên tập độc lập lần hai từng câu.',
        '- [Manifest nguồn](source-manifest.json) · [Số câu theo trang](content-validation.json).',''])
        (outdir/'README.md').write_text('\n'.join(lines),encoding='utf-8')
        path=quote((outdir/'README.md').relative_to(ROOT).as_posix())
        rows.append(f'| let-go-series-{n} | [Mở danh mục sách {n}]({path}) | {stats["pdf_sections"]} | {stats["lesson_questions"]:,} | 8 × 5 |')
    lines=['# Let’s Go Series 1–6 — Nội dung theo trang và Challenge','',
    f'Đã tách **88 PDF**, biên soạn câu hỏi cho **432 trang** trong **88 file Markdown**, và **48 file Challenge** gồm **240 nhóm Challenge**.','',
    f'Tổng cộng **{report["total_lesson_questions"]:,} câu hỏi theo trang** (ít nhất 12 câu/trang) và **{report["total_challenge_questions"]:,} mục luyện Challenge**. Các dạng luyện gồm nhận biết, nghe người lớn đọc, điền từ, sắp xếp câu, hỏi–đáp và nói theo tình huống của bài.','',
    '| Sách | Danh mục tài liệu | PDF | Câu hỏi theo trang | Challenge |','|---|---|---:|---:|---:|',*rows,'',
    '## Cách sử dụng','',
    '1. Mở danh mục sách và chọn Unit/Review/Read.',
    '2. Mở PDF và file câu hỏi theo trang cạnh nhau. Mỗi trang ghi cả số trang PDF gốc, số in trong sách và số trong file tách.',
    '3. Sau khi học Unit, dùng file Challenge theo 5 nhóm như mẫu Toys. Đáp án và kịch bản câu nghe ở cuối file.',
    '4. Với câu hỏi cá nhân và phần nói, đáp án là gợi ý; chấp nhận cách diễn đạt đúng trong phạm vi bài.','',
    '## Quy ước phạm vi','',
    '- Các khoảng trang dùng **số trang PDF, tính từ 1**. Không dịch chuyển ranh giới theo số in trên sách.',
    '- **Sách 2:** Unit 5 giữ PDF 41–46; Unit 6 giữ PDF 47–56. PDF 47–48 là phần cuối Unit 5 bản gốc.',
    '- **Sách 4:** Unit 5 giữ PDF 40–45; Unit 6 giữ PDF 46–55. PDF 46–47 là phần cuối Unit 5 bản gốc.',
    '- Sách 1–2 giữ Review hai trang đúng yêu cầu, bao gồm trang Let’s Learn About. Sách 3–6 tách Review và Read riêng.',
    '- Challenge chỉ lấy nội dung trong phạm vi Unit đã tách. Không thêm Challenge riêng cho Review/Read.',
    '- Giữ cấu trúc 5 Challenge của mẫu, điều chỉnh từ vựng, câu và bài đọc theo từng Unit. Chỉ dẫn hình dùng PDF nguồn; chưa tạo ảnh/audio mới. Bài nghe gốc không có đáp án suy đoán.','',
    '## Kiểm tra và nguồn biên soạn','',
    '- [Báo cáo kiểm tra 432 trang và toàn bộ liên kết](audit/series/validation.json).',
    '- Dữ liệu nội dung theo trang: `series-content/book1.json` đến `book6.json`.',
    '- Tạo lại tài liệu: `python series_build.py`; kiểm tra: `python series_validate.py`; cập nhật danh mục: `python series_index.py`.',
    '- PDF nguồn và tài liệu mẫu Let_s Go Begin được giữ nguyên.','']
    (ROOT/'LET_GO_SERIES_INDEX.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':build_index()
