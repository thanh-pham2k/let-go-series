# Tranh và mẫu câu cùng hoạt động

Trang xem hiện dùng ảnh ghép cho các track thuộc cùng một hoạt động. Audio vẫn riêng; nút nghe cả cụm phát theo thứ tự mã track, bỏ qua MP3 nguồn còn thiếu. Ảnh ghép rộng 768 px, chiều cao theo nội dung. Bản WebP đơn và PNG nguồn được giữ để đối chiếu.

## Bản regenerate WebP

Trang `index.html` dùng ảnh trong `regenerated/`, kích thước 512×512. Mỗi batch được regenerate cả lưới, sau đó mới cắt ảnh. Xem `index-original.html` để đối chiếu ảnh PNG gốc.

# Review 5-6 — Trang và ảnh theo audio

- 2 ảnh trang đầy đủ trong `pages/`.
- 3 ảnh cắt trong `tracks/`; 3 MP3 nguồn trong `audio/`. Mỗi ảnh gắn một mã track.
- [Mở preview ảnh và audio](index.html) · [Mapping JSON](manifest.json).
- Audio thiếu nguồn: không có.

| Track | Trang PDF gốc | Trang in | Mục | Ảnh | Audio |
|---|---:|---:|---|---|---|
| CD2_48 | 55 | 54 | A. Listen and circle: Units 5–6 | [PNG](tracks/CD2_48.png) | [MP3](audio/CD2_48.mp3) |
| CD2_49 | 56 | 55 | A. Days of the week | [PNG](tracks/CD2_49.png) | [MP3](audio/CD2_49.mp3) |
| CD2_50 | 56 | 55 | B. Today is Monday | [PNG](tracks/CD2_50.png) | [MP3](audio/CD2_50.mp3) |
