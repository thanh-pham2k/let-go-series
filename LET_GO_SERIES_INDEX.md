# Let’s Go Series 1–6 — Nội dung theo trang và Challenge

Đã tách **88 PDF**, biên soạn câu hỏi cho **432 trang** trong **88 file Markdown**, và **48 file Challenge** gồm **240 nhóm Challenge**.

Tổng cộng **14,213 câu hỏi theo trang** (ít nhất 12 câu/trang) và **13,248 mục luyện Challenge**. Các dạng luyện gồm nhận biết, nghe người lớn đọc, điền từ, sắp xếp câu, hỏi–đáp và nói theo tình huống của bài.

| Sách | Danh mục tài liệu | PDF | Câu hỏi theo trang | Challenge |
|---|---|---:|---:|---:|
| let-go-series-1 | [Mở danh mục sách 1](Let_s%20Go%201/Units/README.md) | 12 | 2,265 | 8 × 5 |
| let-go-series-2 | [Mở danh mục sách 2](Let_s%20Go%202-/Units/README.md) | 12 | 2,350 | 8 × 5 |
| let-go-series-3 | [Mở danh mục sách 3](Let_s%20Go%203/Units/README.md) | 16 | 2,417 | 8 × 5 |
| let-go-series-4 | [Mở danh mục sách 4](Let_s%20Go%204/Units/README.md) | 16 | 2,476 | 8 × 5 |
| let-go-series-5 | [Mở danh mục sách 5](Let_s%20Go%205/Units/README.md) | 16 | 2,366 | 8 × 5 |
| let-go-series-6 | [Mở danh mục sách 6](Let_s%20Go%206/Units/README.md) | 16 | 2,339 | 8 × 5 |

## Cách sử dụng

1. Mở danh mục sách và chọn Unit/Review/Read.
2. Mở PDF và file câu hỏi theo trang cạnh nhau. Mỗi trang ghi cả số trang PDF gốc, số in trong sách và số trong file tách.
3. Sau khi học Unit, dùng file Challenge theo 5 nhóm như mẫu Toys. Đáp án và kịch bản câu nghe ở cuối file.
4. Với câu hỏi cá nhân và phần nói, đáp án là gợi ý; chấp nhận cách diễn đạt đúng trong phạm vi bài.

## Quy ước phạm vi

- Các khoảng trang dùng **số trang PDF, tính từ 1**. Không dịch chuyển ranh giới theo số in trên sách.
- **Sách 2:** Unit 5 giữ PDF 41–46; Unit 6 giữ PDF 47–56. PDF 47–48 là phần cuối Unit 5 bản gốc.
- **Sách 4:** Unit 5 giữ PDF 40–45; Unit 6 giữ PDF 46–55. PDF 46–47 là phần cuối Unit 5 bản gốc.
- Sách 1–2 giữ Review hai trang đúng yêu cầu, bao gồm trang Let’s Learn About. Sách 3–6 tách Review và Read riêng.
- Challenge chỉ lấy nội dung trong phạm vi Unit đã tách. Không thêm Challenge riêng cho Review/Read.
- Giữ cấu trúc 5 Challenge của mẫu, điều chỉnh từ vựng, câu và bài đọc theo từng Unit. Chỉ dẫn hình dùng PDF nguồn; chưa tạo ảnh/audio mới. Bài nghe gốc không có đáp án suy đoán.

## Kiểm tra và nguồn biên soạn

- [Báo cáo kiểm tra 432 trang và toàn bộ liên kết](audit/series/validation.json).
- Dữ liệu nội dung theo trang: `series-content/book1.json` đến `book6.json`.
- Tạo lại tài liệu: `python series_build.py`; kiểm tra: `python series_validate.py`; cập nhật danh mục: `python series_index.py`.
- PDF nguồn và tài liệu mẫu Let_s Go Begin được giữ nguyên.
