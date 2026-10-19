# Tranh và mẫu câu cùng hoạt động

Trang xem hiện dùng ảnh ghép cho các track thuộc cùng một hoạt động. Audio vẫn riêng; nút nghe cả cụm phát theo thứ tự mã track, bỏ qua MP3 nguồn còn thiếu. Ảnh ghép rộng 768 px, chiều cao theo nội dung. Bản WebP đơn và PNG nguồn được giữ để đối chiếu.

## Bản regenerate WebP

Trang `index.html` dùng ảnh trong `regenerated/`, kích thước 512×512. Mỗi batch được regenerate cả lưới, sau đó mới cắt ảnh. Xem `index-original.html` để đối chiếu ảnh PNG gốc.

# Review 7-8 — Trang và ảnh theo audio

- 2 ảnh trang đầy đủ trong `pages/`.
- 4 ảnh cắt trong `tracks/`; 4 MP3 nguồn trong `audio/`. Mỗi ảnh gắn một mã track.
- [Mở preview ảnh và audio](index.html) · [Mapping JSON](manifest.json).
- Audio thiếu nguồn: không có.

| Track | Trang PDF gốc | Trang in | Mục | Ảnh | Audio |
|---|---:|---:|---|---|---|
| CD2_96 | 73 | 72 | A. Listen and circle: Units 7–8 | [PNG](tracks/CD2_96.png) | [MP3](audio/CD2_96.mp3) |
| CD2_97 | 73 | 72 | B. Listen and number: animals | [PNG](tracks/CD2_97.png) | [MP3](audio/CD2_97.mp3) |
| CD2_98 | 74 | 73 | A. Feelings: Are you happy? | [PNG](tracks/CD2_98.png) | [MP3](audio/CD2_98.mp3) |
| CD2_99 | 74 | 73 | B. Hungry, thirsty, hot, cold | [PNG](tracks/CD2_99.png) | [MP3](audio/CD2_99.mp3) |
