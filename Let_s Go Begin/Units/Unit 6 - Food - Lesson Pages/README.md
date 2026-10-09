# Unit 6 – Food: Bộ bài học chuẩn

Đủ 15 ảnh + audio + câu trắc nghiệm. Ảnh PNG/WebP đều **1200 × 1200**, giữ tỷ lệ minh họa và chữ. Regenerate bằng **image_gen tích hợp**, theo nhóm nhiều trang rồi cắt riêng; không dùng fallback.

- [Preview học và làm bài](preview.html)
- [Xem cả bộ](preview.jpg)
- [Metadata tích hợp](unit.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Báo cáo kiểm tra](validation.json)

Ảnh chuẩn dùng cho app: pages/webp. Bản PNG tương ứng: pages/png. assets giữ lớp ảnh phục vụ dựng lại; references và source-pages giữ nguồn PDF đối chiếu. assets/batches lưu prompt, ảnh ghép và đánh giá từng batch; không dùng ảnh ghép làm trang học.

Giữ chữ bài học, số chỉ hình, câu thoại và chỗ trống; câu trắc nghiệm nằm riêng. Các mục chỉ có tiêu đề được bổ sung bằng nội dung của mục cùng trang. Nên hỗ trợ phóng to để đọc lời bài hát trên điện thoại.

Audio khớp file CD nguồn, chưa nghe/transcribe độc lập. Tài liệu Challenge luyện thêm có checklist audio riêng do chủ dự án tự bổ sung.

Dựng lại từ thư mục gốc repo: python build_lesson_unit.py --unit 6 --render --export

## Nguồn và điều chỉnh đã đối chiếu

- PDF gốc: ../Unit 6 - Food.pdf, 8 trang sách 46–53. Đã xem trực quan đủ 8 trang và mọi trang sau cắt, không chỉ dựa vào câu hỏi.
- Hai nhãn **CD1 32 / CD1 34** in sai trong PDF và mapping ZIP cũ được chuẩn hóa thành **CD2_32 / CD2_34**, theo mapping tổng và MP3 CD2. Không sử dụng CD1/Track32 hoặc CD1/Track34.
- Bốn nhóm 4/4/4/3 trang được vẽ lại bằng built-in image_gen. Prompt, reference, kết quả và log sửa lưu tại assets/batches. Các box cắt thực tế nằm trong manifest; contain giữ tỷ lệ, bỏ gutter/viền ảnh ghép.
- CD2_24, CD2_26, CD2_30 dùng hình hành động/từ vựng cùng trang nguồn vì phần audio chỉ có tiêu đề. CD2_31 giữ cả D. Ask and answer; CD2_33 giữ C. Find the letters; không thêm track hoặc câu trắc nghiệm cho phần không có audio riêng.
- CD2_32 xuống dòng bảng chữ cái để dễ đọc, giữ đủ A–Z/a–z và màu Q–T. CD2_33 giữ cảnh Find the letters với chữ S/s và các nét cuộn trong tán cây, viền áo, ghế; nét trang trí được vẽ lại, không phải bản sao tọa độ của PDF. Không có bảng giải đáp trên ảnh.
- Đã đếm 6 nến ở cả hai cảnh sinh nhật và các nhóm trên game: 2 thỏ, 2 xe đạp, 3 mèo, 2 chim, 3 gấu, 2 tàu. Giữ các ô trống trên bảng và các chỗ trống trong Say and act.
- MP3 chỉ được kiểm tra đồng nhất byte với thư mục nguồn CD2. **Chưa nghe hoặc transcribe kiểm chứng độc lập**; chưa xác nhận nội dung lời nói ở CD2_32/CD2_34 bằng nghe. Audio Challenge chưa tạo; chủ dự án tự bổ sung.
