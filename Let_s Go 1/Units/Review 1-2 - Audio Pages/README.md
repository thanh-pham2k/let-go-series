# Tranh và mẫu câu cùng hoạt động

Trang xem hiện dùng ảnh ghép cho các track thuộc cùng một hoạt động. Audio vẫn riêng; nút nghe cả cụm phát theo thứ tự mã track, bỏ qua MP3 nguồn còn thiếu. Ảnh ghép rộng 768 px, chiều cao theo nội dung. Bản WebP đơn và PNG nguồn được giữ để đối chiếu.

## Bản regenerate WebP

Trang `index.html` dùng ảnh trong `regenerated/`, kích thước 512×512. Mỗi batch được regenerate cả lưới, sau đó mới cắt ảnh. Xem `index-original.html` để đối chiếu ảnh PNG gốc.

# Review 1-2 — Trang và ảnh theo audio

- 2 ảnh trang đầy đủ trong `pages/`.
- 3 ảnh cắt trong `tracks/`; 3 MP3 nguồn trong `audio/`. Mỗi ảnh gắn một mã track.
- [Mở preview ảnh và audio](index.html) · [Mapping JSON](manifest.json).
- Audio thiếu nguồn: không có.

| Track | Trang PDF gốc | Trang in | Mục | Ảnh | Audio |
|---|---:|---:|---|---|---|
| CD1_47 | 19 | 18 | A. Listen and circle: Units 1–2 | [PNG](tracks/CD1_47.png) | [MP3](audio/CD1_47.mp3) |
| CD1_48 | 20 | 19 | A. Count to ten | [PNG](tracks/CD1_48.png) | [MP3](audio/CD1_48.mp3) |
| CD1_49 | 20 | 19 | B. Count to twenty | [PNG](tracks/CD1_49.png) | [MP3](audio/CD1_49.mp3) |
