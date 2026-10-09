# Review 1–2 – Bộ bài học chuẩn

Hai trang CD1_36–37, PNG/WebP **1200 × 1200**, contain giữ tỷ lệ. Minh họa mới bằng built-in image_gen; không dùng ảnh nguồn làm ảnh học.

- [Preview](preview.html) · [Contact sheet](preview.jpg)
- [Metadata](review.regenerated.metadata) · [Câu hỏi](questions.md)
- [Validation](validation.json) · [Generation](generation.json)

Ảnh chuẩn: pages/webp; PNG tương ứng: pages/png. references/source-pages chỉ dùng đối chiếu PDF. assets giữ minh họa và batch gốc để dựng lại.

CD1_36 giữ sáu cặp theo thứ tự: car/train, bicycle/ball, green/red, purple/yellow, stand up/sit down, come here/turn around; mỗi cặp giữ a bên trái, b bên phải, không khoanh đáp án. CD1_37 giữ năm đồ dùng 1 paper, 2 scissors, 3 glue, 4 paint, 5 tape và câu cô giáo “I have paper.” ở cùng trang. Cảnh câu mẫu không có track riêng; giữ cùng trang, không khẳng định audio đọc câu này.

Điều chỉnh: bố cục nguồn được chuyển thành canvas vuông; style cartoon sáng/soft shading theo Unit3; sửa “go/đi” trong bài luyện thành “come here/lại đây” theo hình6 và nội dung Unit2. Tape dùng mô tả hộp băng keo thay emoji giấy vệ sinh dễ gây hiểu sai. Câu bổ sung kiểm nhận biết hình/câu mẫu, không phải đáp án bài nghe gốc.

Audio copy đúng từng byte từ CD1 nguồn. Chưa nghe/transcribe độc lập; không suy đoán đáp án Listen and circle. Audio Challenge riêng chưa có, chủ dự án tự cung cấp theo checklist. Preview hiện câu hỏi sau audio ended hoặc bấm ôn tập, chỉ phản hồi đáp án sau khi chọn.

Dựng lại: python build_review.py --build --split-x SPLIT (đọc split_x trong batch1.json). Lệnh này đặt lại trạng thái chờ duyệt; chỉ --export sau khi xem lại ảnh và ghi reviewed cùng bằng chứng vào manifest.

<!-- five-challenge-guide -->
## Bài luyện theo5 Challenge

[Hướng dẫn/bài luyện/đáp án/audio notes](challenge-guide.md) · [Nội dung câu luyện có mã](challenge-content.json).

Chuẩn hóa Recognition → Listen & Understand → Recall → Build & Match → Final Boss. Dịch nghĩa là phụ lục hỗ trợ. Kho câu luyện bổ sung riêng với câu trắc nghiệm theo track; preview hiện tại vẫn phục vụ trang học chính, chưa có giao diện chạy toàn bộ Challenge.
