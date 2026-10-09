# Unit 5 – Animals: Bộ bài học chuẩn

Đủ 18 ảnh + audio + câu trắc nghiệm. Ảnh PNG/WebP đều **1200 × 1200**, giữ tỷ lệ minh họa và chữ. Regenerate bằng **image_gen tích hợp**, theo nhóm nhiều trang rồi cắt riêng; không dùng fallback.

- [Preview học và làm bài](preview.html)
- [Xem cả bộ](preview.jpg)
- [Metadata tích hợp](unit.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Báo cáo kiểm tra](validation.json)

Ảnh chuẩn dùng cho app: pages/webp. Bản PNG tương ứng: pages/png. assets giữ lớp ảnh phục vụ dựng lại; references và source-pages giữ nguồn PDF đối chiếu. assets/batches lưu prompt, ảnh ghép và đánh giá từng batch; không dùng ảnh ghép làm trang học.

Giữ chữ bài học, số chỉ hình, câu thoại và chỗ trống; câu trắc nghiệm nằm riêng. Các mục chỉ có tiêu đề được bổ sung bằng nội dung của mục cùng trang. Nên hỗ trợ phóng to để đọc lời bài hát trên điện thoại.

Audio khớp file CD nguồn, chưa nghe/transcribe độc lập. Tài liệu Challenge luyện thêm có checklist audio riêng do chủ dự án tự bổ sung.

Dựng lại từ thư mục gốc repo: python build_lesson_unit.py --unit 5 --render --export

## Điều chỉnh và đối chiếu nguồn

Nguồn đối chiếu: ../Unit 5 - Animals.pdf; references/CD2_02.png–CD2_19.png và source-pages/page-01.png–page-08.png. Minh họa được vẽ lại bằng built-in image_gen. Một số nhóm được giãn hoặc sắp theo hàng để đếm rõ; giữ số nhóm, số lượng, màu và chữ học. CD2_06/08/12/14 dùng nội dung bài tương ứng cùng trang nguồn thay cho crop chỉ có tiêu đề. CD2_10/15 chỉ giữ nội dung in trong PDF, không thêm lời hát. CD2_15 sửa lựa chọn “Gà” thành “Chim” theo nhóm birds trong nguồn. CD2_16 chia bảng chữ thành hàng để đủ 26 cặp; M–P giữ màu nhấn. Câu hỏi và đáp án nằm trong metadata, không ghép lên ảnh.

Đường chia batch được lưu trong manifest; mỗi crop được contain trên canvas vuông, không kéo méo. Kiểm tra nội dung trực quan được ghi riêng cho từng track; kiểm tra kỹ thuật không thay cho đếm vật hoặc so chữ. Audio chưa được nghe/transcribe độc lập; clip Challenge còn chờ chủ dự án bổ sung.
