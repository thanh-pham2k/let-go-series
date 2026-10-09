# Unit 1 – 17 trang bài học, V2

Đã regenerate theo nhóm CD1_02–05, 06–09, 10–13, 14–17; CD1_18 tạo riêng. Mỗi track có một ảnh, một audio và một câu trắc nghiệm.

- [preview.html](preview.html): xem hình/chữ, nghe audio, trả lời câu hỏi khi audio kết thúc hoặc bấm ôn tập.
- [preview.jpg](preview.jpg): xem cả bộ 17 trang.
- [unit1_toys.regenerated.metadata](unit1_toys.regenerated.metadata): mapping track → image → audio_file → question.
- [questions.md](questions.md): một câu cho mỗi track.
- [generation-v2.md](generation-v2.md): bộ yêu cầu prompt và nguồn ảnh.
- [validation.json](validation.json): kết quả kiểm tra V2.

Giữ câu thoại, từ vựng, toàn bộ lời hát trang 04, tên nhân vật, số chỉ đồ chơi và dòng trả lời trống của nguồn. Trang 03 giữ ba tình huống khác nhau. Trang 05/06 có mũi tên đứng/ngồi. Trang 13 đặt số sát đồ chơi. Beth mặc quần short tím ở cả 17 và 18; tên nằm trên áo như nguồn.

Trang 10/14 gốc không in lời hát; V2 bổ sung nhãn từ vựng dưới đồ chơi, không thêm lời hát chưa xác minh. Trang 06 gốc chỉ có tiêu đề nên bổ sung minh họa đứng/ngồi. Trang 08/12 dùng nội dung Words tương ứng. Trang 15/16 dựng đủ 26 cặp chữ bằng Arial để bảo đảm chính xác.

Chữ bài học nằm trong ảnh; câu hỏi trắc nghiệm nằm riêng trong metadata. PNG ở pages/png, WebP dùng cho ứng dụng ở pages/webp. Giữ tỷ lệ với object-fit: contain, nên hỗ trợ phóng to để đọc lời hát trên điện thoại.

Dựng lại bằng Python và Pillow:

```sh
python render.py
python export.py
```

Bộ chuẩn: pages/webp/CD1_02.webp đến CD1_18.webp (17 ảnh). pages/png là bản PNG tương ứng. assets/batches-v2 chỉ giữ 17 lớp ảnh cần để dựng lại; references là ảnh sách gốc để đối chiếu. Ảnh ghép trung gian và bộ Visuals cũ đã bỏ. Manifest hiện tại chứa lớp ảnh và lớp font bảng chữ cái. Export kiểm tra 17 mapping, 17 câu hỏi, audio, kích thước, chữ bảng chữ cái, PNG khớp manifest; xuất preview, metadata và Unit_1_Toys_regenerated.zip ở thư mục cha.

Đã đối chiếu 17 reference và xem ảnh sau khi cắt. ZIP nguồn không có trong checkout này; reference được kiểm tra từng byte với Git HEAD. Audio khớp CD1 nguồn; chưa nghe/transcribe độc lập. Repo chưa có ứng dụng sản phẩm; đây là tài nguyên và preview cục bộ.

## Kích thước đồng nhất

Toàn bộ17 PNG/WebP được xuất1200×1200, giống Unit2–8 và4 Review. Giữ tỷ lệ bằng contain, căn giữa trên nền trắng, không cắt chữ/đồ vật. native_layout_size trong manifest giữ kích thước bố cục và các lớp font gốc để dựng lại chính xác. [normalization-validation.json](normalization-validation.json) ghi box nội dung từng trang và kiểm tra toàn bộ nội dung gốc được giữ sau khi scale.
