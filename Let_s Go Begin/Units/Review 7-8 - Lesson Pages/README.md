# Review 7–8 – Bộ bài học chuẩn

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

## Giới hạn kiểm tra preview

Đã chạy [Node DOM checks](preview-validation.json) cho cả3 mục, gồm chọn mục, reset, nút ôn tập, sự kiện ended mô phỏng, phản hồi đúng/sai và chuyển trước/sau. Đã kiểm [HTTP resources](resource-validation.json): preview/metadata/3WebP/3MP3 trả200 và trùng byte với file.

Kiểm tra trình duyệt thật chưa chạy: công cụ IAB lỗi khởi tạo kernel; lệnh Edge headless qua Start-Process bị automatic approval review từ chối với lý do blocked by policy. [Chi tiết](browser-validation.json). Không coi sự kiện ended mô phỏng là đã nghe audio.

<!-- five-challenge-guide -->
## Bài luyện theo5 Challenge

[Hướng dẫn/bài luyện/đáp án/audio notes](challenge-guide.md) · [Nội dung câu luyện có mã](challenge-content.json).

Chuẩn hóa Recognition → Listen & Understand → Recall → Build & Match → Final Boss. Dịch nghĩa là phụ lục hỗ trợ. Kho câu luyện bổ sung riêng với câu trắc nghiệm theo track; preview hiện tại vẫn phục vụ trang học chính, chưa có giao diện chạy toàn bộ Challenge.
