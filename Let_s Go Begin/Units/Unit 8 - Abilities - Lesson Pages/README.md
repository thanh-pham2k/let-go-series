# Unit 8 – Abilities: Bộ bài học chuẩn

Đủ 16 ảnh + audio + câu trắc nghiệm. Ảnh PNG/WebP đều **1200 × 1200**, giữ tỷ lệ minh họa và chữ. Regenerate bằng **image_gen tích hợp**, theo nhóm nhiều trang rồi cắt riêng; không dùng fallback.

- [Preview học và làm bài](preview.html)
- [Xem cả bộ](preview.jpg)
- [Metadata tích hợp](unit.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Báo cáo kiểm tra](validation.json)

Ảnh chuẩn dùng cho app: pages/webp. Bản PNG tương ứng: pages/png. assets giữ lớp ảnh phục vụ dựng lại; references và source-pages giữ nguồn PDF đối chiếu. assets/batches lưu prompt, ảnh ghép và đánh giá từng batch; không dùng ảnh ghép làm trang học.

Giữ chữ bài học, số chỉ hình, câu thoại và chỗ trống; câu trắc nghiệm nằm riêng. Các mục chỉ có tiêu đề được bổ sung bằng nội dung của mục cùng trang. Nên hỗ trợ phóng to để đọc lời bài hát trên điện thoại.

Audio khớp file CD nguồn, chưa nghe/transcribe độc lập. Tài liệu Challenge luyện thêm có checklist audio riêng do chủ dự án tự bổ sung.

Dựng lại từ thư mục gốc repo: python build_lesson_unit.py --unit 8 --render --export

## Đối chiếu và điều chỉnh cụ thể

- CD2_54: sắp lại thành các khung hội thoại để chỉ rõ người nói; giữ bốn câu gốc.
- CD2_55: bỏ chữ viết tay trên bản scan; giữ hai chỗ trống chưa điền và dấu chấm gốc.
- CD2_58 dùng hai lệnh ở D cùng trang65; CD2_60 dùng bốn hình/từ ở A cùng trang66.
- CD2_62 dùng hai câu và bốn cặp hình suy nghĩ cùng trang67; CD2_64 dùng bốn hình/từ cùng trang68; CD2_66 dùng hội thoại và tám hình cùng trang69. Đây là các mục nguồn chỉ có tiêu đề; không thêm lời chant chưa in.
- CD2_67 sắp52 glyph thành nhiều hàng để đọc rõ, vẫn đúng thứ tự và màu X/Y/Z.
- CD2_68 giữ hoạt động Find the letters, cả X/x Y/y Z/z, không khoanh đáp án.
- CD2_69 giữ14 ô liên tục, **Move ahead 2 spaces** và **Move back 3 spaces** đúng PDF. Hình Make a circle có 5 trẻ; Make a line có 4 trẻ.
- Bố cục minh họa được vẽ lại, không phải bản sao pixel của scan. Những lần sinh có sai nội dung được ghi trong job; chỉ selected_regions được đưa vào trang cuối.

Đã xem riêng cả16 PNG sau cắt và contact sheet. lesson_specs.json lưu chữ bắt buộc; manifest ghi box cắt thực tế. Các cặp sửa được sinh trái/phải, trang sửa đơn dùng toàn ảnh; mọi trang contain trên canvas1200×1200, không kéo méo.

Để dựng lại từ batch đã chọn: chạy assemble_unit8.py trong thư mục này, rồi lệnh render/export ở root. Không chỉnh script chung.
