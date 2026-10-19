# Tranh và mẫu câu cùng hoạt động

Trang xem hiện dùng ảnh ghép cho các track thuộc cùng một hoạt động. Audio vẫn riêng; nút nghe cả cụm phát theo thứ tự mã track, bỏ qua MP3 nguồn còn thiếu. Ảnh ghép rộng 768 px, chiều cao theo nội dung. Bản WebP đơn và PNG nguồn được giữ để đối chiếu.

## Bản regenerate WebP

Đã áp dụng 196 ảnh WebP 512×512 cho 8 Unit và 4 Review. Dùng lại 8 ảnh mẫu được duyệt; 188 ảnh còn lại qua 27 batch, mỗi lần regenerate một lưới tối đa 8 ảnh. Prompt thực tế và ảnh ghép nằm trong `output/imagegen/book1-all-batches/` tại workspace.

- [Tải toàn bộ WebP](Let-Go-1-regenerated-512-webp.zip)
- [Mapping mới](mapping-regenerated.csv)
- [Kiểm tra WebP](regenerated-validation.json)

Ảnh AI có thể thay đổi chữ nhỏ hoặc chi tiết; ảnh PNG gốc được giữ để đối chiếu trong từng Unit/Review.

# Let’s Go 1 — Trang và ảnh theo audio

**72 ảnh trang đầy đủ; 196 ảnh cắt theo mã track; 186 MP3 gốc có sẵn.**

- [Mở preview toàn bộ sách](index.html).
- [Mapping CSV](mapping.csv) · [Manifest JSON](manifest.json) · [Kiểm tra](validation.json).

## Quy ước

- `pages/PDF-003.png` là trang PDF gốc 3 (trang in 2); số trang được ghi rõ trong metadata.
- `tracks/CD1_02.png` ghép đúng `audio/CD1_02.mp3`. Không ghép theo thứ tự đọc tên file trên Windows.
- **Nguồn thiếu CD1_31–CD1_40 (10 MP3).** Vẫn cắt đủ ảnh theo ký hiệu trong sách; manifest và preview đánh dấu thiếu nguồn. Không thay bằng track khác.
- Tách riêng từng hoạt động theo ký hiệu track; chỉ track đọc và chant trên cùng khung được dùng chung khung.
- Track 01 của mỗi CD là phần giới thiệu; không có vùng bài học tương ứng trong phạm vi được tách.
- Hoạt động không có ký hiệu audio được giữ ở ảnh trang đầy đủ. Không tự tạo track.
- Ảnh được cắt trực tiếp từ trang scan, giữ nguyên chữ và hình. Chất lượng và phần mất mép nếu có của bản scan gốc được giữ nguyên.

## Các phần

| Phần | Trang | Ảnh–audio | Preview |
|---|---:|---:|---|
| Unit 1 - Things for School | 8 | 22 | [Mở](../Unit%201%20-%20Things%20for%20School%20-%20Audio%20Pages/index.html) |
| Unit 2 - Colors and Shapes | 8 | 23 | [Mở](../Unit%202%20-%20Colors%20and%20Shapes%20-%20Audio%20Pages/index.html) |
| Review 1-2 | 2 | 3 | [Mở](../Review%201-2%20-%20Audio%20Pages/index.html) |
| Unit 3 - At the Store | 8 | 23 | [Mở](../Unit%203%20-%20At%20the%20Store%20-%20Audio%20Pages/index.html) |
| Unit 4 - People at Home | 8 | 22 | [Mở](../Unit%204%20-%20People%20at%20Home%20-%20Audio%20Pages/index.html) |
| Review 3-4 | 2 | 5 | [Mở](../Review%203-4%20-%20Audio%20Pages/index.html) |
| Unit 5 - Birthday and Toys | 8 | 23 | [Mở](../Unit%205%20-%20Birthday%20and%20Toys%20-%20Audio%20Pages/index.html) |
| Unit 6 - Outdoors | 8 | 23 | [Mở](../Unit%206%20-%20Outdoors%20-%20Audio%20Pages/index.html) |
| Review 5-6 | 2 | 3 | [Mở](../Review%205-6%20-%20Audio%20Pages/index.html) |
| Unit 7 - Food | 8 | 23 | [Mở](../Unit%207%20-%20Food%20-%20Audio%20Pages/index.html) |
| Unit 8 - Animals | 8 | 22 | [Mở](../Unit%208%20-%20Animals%20-%20Audio%20Pages/index.html) |
| Review 7-8 | 2 | 4 | [Mở](../Review%207-8%20-%20Audio%20Pages/index.html) |
