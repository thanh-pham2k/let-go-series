# Unit 1 – 17 ảnh bài học theo audio

Bộ đầu ra thay thế hình hiển thị theo track: **CD1_02–CD1_18**, đúng 17 mục của `Unit_1_Toys_audio_mapping.zip`. Mỗi audio có một ảnh WebP riêng. Đây là hình bài học có lời thoại/nhãn cần thiết; câu hỏi sau nghe được lưu riêng trong metadata, không in đáp án lên ảnh.

## Dùng ngay

- Mở [preview.html](preview.html) trong trình duyệt để chọn từng bài, xem ảnh, nghe audio và làm câu hỏi. Trang chạy từ file cục bộ, không cần server hoặc mạng. Câu hỏi hiện khi audio kết thúc hoặc khi chọn ôn tập.
- Dùng [unit1_toys.regenerated.metadata](unit1_toys.regenerated.metadata) để nối **track → image → audio_file → question**. Các đường dẫn đều tương đối với thư mục này.
- [preview.jpg](preview.jpg) là bản xem cả bộ 17 trang.
- `pages/webp/`: ảnh dùng cho UI; `pages/png/`: bản PNG tương ứng. Hiển thị bằng `object-fit: contain`, giữ nguyên tỷ lệ và cho phép cuộn; không ép ảnh thành hình vuông.

## Dựng lại từ metadata

[manifest.json](manifest.json) chứa từng lớp hình/chữ, vị trí và kích thước. `canvas.size` là kích thước trang. Mỗi `layers[].box` có dạng **[x, y, width, height]**, đơn vị pixel, gốc ở góc trên trái. Vẽ các lớp theo thứ tự mảng; ảnh dùng `contain` và căn giữa trong box. Lớp chữ có nội dung, cỡ chữ, màu, căn lề và độ đậm. Font mặc định Arial; Linux dùng DejaVu Sans nếu có.

```sh
python render.py
python export.py
```

Cần Python và Pillow. `render.py` xuất lại 17 PNG/WebP từ manifest đã chỉnh. `export.py` kiểm tra toàn bộ mapping, kích thước, chữ không tràn và PNG khớp metadata, rồi xuất metadata đơn giản, preview HTML, báo cáo và ZIP. `build_manifest.py` dùng để xây lại manifest ban đầu từ mapping/câu hỏi trong repo; không chạy script đó sau khi tự chỉnh bố cục vì nó sẽ dựng lại manifest mặc định.

Ví dụ ứng dụng dùng `items[...].audio_file` làm nguồn audio và `items[...].image` làm nguồn ảnh. Mục `question` có `prompt`, `choices` và `correct_choice_id`; chỉ hiển thị phản hồi sau khi bé chọn. Metadata chứa đáp án để kiểm tra phía ứng dụng, không dùng như cơ chế bảo mật đáp án.

## Nội dung được giữ và điều chỉnh

- CD1_07/08: bóng, dây nhảy, yo-yo, xe đạp theo lưới 2×2; giữ số 1–4 và từ vựng.
- CD1_11/12: tàu hỏa, ô tô, búp bê, gấu bông theo lưới 2×2; giữ số 1–4.
- CD1_10: hàng yo-yo → bóng → dây nhảy → xe đạp. CD1_14: hàng bóng → gấu bông → búp bê → tàu hỏa → xe đạp.
- CD1_02/03/04/05/09/13/17/18: cảnh mới bám nhân vật, hành động, đồ vật và quan hệ bố cục của crop gốc. Lời thoại, tên, số và lời bài hát được dựng riêng bằng font. Trang 17 giữ Pete/Beth/Ann/Matt theo thứ tự; trang 18 giữ đồ chơi từng bạn và các dòng trả lời còn trống.
- CD1_06: crop gốc chỉ có tiêu đề/biểu tượng, nên bổ sung cảnh đứng/ngồi cùng trang từ CD1_05. CD1_08/12 dùng hình Words cùng trang thay vì chỉ có tiêu đề.
- CD1_15/16: dựng đủ 26 cặp chữ hoa/thường bằng font, dùng chung bảng chữ cái.
- Bố cục được chuẩn hóa để rõ trên UI, không phải bản sao từng pixel. Chi tiết trang trí không phục vụ bài học được giản lược; phần trống trả lời ở tình huống thứ 3 của CD1_03 được bổ sung vì crop gốc cắt mất khu vực này.

## Nguồn và kiểm tra

`references/` giữ đủ 17 crop gốc. `source.metadata.json` giữ nguyên mapping gốc. `assets/toys/` dùng lại 8 asset đã tạo; `assets/scenes/` chứa các cảnh tạo bằng **image_gen tích hợp**. Prompt đầy đủ và nguồn kết quả nằm trong `generation.json` và `answer-generation.json`.

[validation.json](validation.json) ghi kết quả kiểm tra mapping, file, kích thước và sự khớp giữa ảnh PNG với metadata. Đã kiểm tra trực quan cả bộ, kiểm tra chi tiết lời bài hát, các số chỉ đồ chơi và cảnh Answer. Audio được sao chép từ CD1 trong repo, không đổi nội dung; chưa nghe/transcribe để kiểm chứng lời nói từng track.

[browser-validation.json](browser-validation.json) ghi kiểm tra bằng trình duyệt Edge: tải đủ 17 ảnh và metadata audio, 34 lựa chọn đúng/sai, reset khi đổi bài, không có lỗi JavaScript và không tràn ngang ở chiều rộng 390px. Sự kiện kết thúc audio được mô phỏng để kiểm tra chuyển sang câu hỏi; không phải kiểm tra nghe toàn bộ audio.

Bộ này là tài nguyên và bản xem thử; repo chưa có source ứng dụng để tích hợp vào UI sản phẩm. ZIP/crop gốc và bộ câu hỏi Markdown hiện có được giữ nguyên.
