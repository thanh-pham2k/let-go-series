# Kiểm tra bộ ảnh – 2026-10-10

**Kết quả: đủ bộ ảnh học chính cho Unit1–8 và4 Review,142/142 mục.**

| Bộ | Số mục đã có / nguồn yêu cầu | PNG | WebP | Kích thước |
|---|---:|---:|---:|---|
| Unit 1 - Toys | 17/17 | 17 | 17 |1200×1200 |
| Unit 2 - Colors | 17/17 | 17 | 17 |1200×1200 |
| Unit 3 - Shapes | 17/17 | 17 | 17 |1200×1200 |
| Unit 4 - Numbers | 16/16 | 16 | 16 |1200×1200 |
| Unit 5 - Animals | 18/18 | 18 | 18 |1200×1200 |
| Unit 6 - Food | 15/15 | 15 | 15 |1200×1200 |
| Unit 7 - My Body | 17/17 | 17 | 17 |1200×1200 |
| Unit 8 - Abilities | 16/16 | 16 | 16 |1200×1200 |
| Review 1-2 | 2/2 | 2 | 2 |1200×1200 |
| Review 3-4 | 2/2 | 2 | 2 |1200×1200 |
| Review 5-6 | 2/2 | 2 | 2 |1200×1200 |
| Review 7-8 | 3/3 | 3 | 3 |1200×1200 |

## Bằng chứng kiểm tra

- Đối chiếu142 track với mapping tổng: không thiếu hoặc trùng track.
- Đọc/giải mã toàn bộ284 filePNG/WebP; đều1200×1200 và khớp kích thước trong metadata.
- Dựng lại trong bộ nhớ cả142 trang từ manifest: tất cảPNG khớp từng pixel, không có file xuất cũ hoặc thiếu lớp dựng.
- Không có hai trangPNG giống hệt nhau. WebP khớp nội dungPNG trong sai số nén (sai số màu trung bình lớn nhất2.63/255).
- Mỗi mục cóMP3 khớp từng byte với CD nguồn và một câu trắc nghiệm hợp lệ. Preview nhúng đúng dữ liệu bài học; không có liên kết Markdown hỏng.
- Kiểm tra12 ZIP: mở/CRC hợp lệ, ảnh/audio/manifest/metadata/preview trong ZIP khớp file hiện tại.
- Xem lại toàn bộ12 contact sheet. Đối chiếu lớn với reference các trang CD1_66 (7táo/8chó/9mèo/6tim/5sao), CD2_15 (2vịt/3bò/5thỏ/7chó/10chim) và CD2_61 (can/cannot, đúng người nói và4 nhóm khả năng). Không phát hiện thiếu nội dung ở các trang đã đối chiếu này.

## Giới hạn kết luận

- Đủ bộ ảnh theo track; không có nghĩa đã có ảnh riêng cho từng câu của5 Challenge. Một số bài luyện vẫn dùng mô tả/chỉ hình.
- Audio clip riêng cho Challenge còn cần chủ dự án bổ sung. MP3 bài học chính chưa được nghe/transcribe đối chiếu độc lập.
- Lần này kiểm toàn bộ tính đầy đủ và tính nhất quán file; xem tổng thể mọi trang và đối chiếu sâu các trang nêu trên, không khẳng định đã đối chiếu từng chữ của142 ảnh với PDF trong lần kiểm tra này.

[Kiểm tra độ đầy đủ](completeness.json) · [Kiểm tra pixel/render](render-integrity.json)
