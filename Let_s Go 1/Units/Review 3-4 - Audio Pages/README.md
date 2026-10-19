# Tranh và mẫu câu cùng hoạt động

Trang xem hiện dùng ảnh ghép cho các track thuộc cùng một hoạt động. Audio vẫn riêng; nút nghe cả cụm phát theo thứ tự mã track, bỏ qua MP3 nguồn còn thiếu. Ảnh ghép rộng 768 px, chiều cao theo nội dung. Bản WebP đơn và PNG nguồn được giữ để đối chiếu.

## Bản regenerate WebP

Trang `index.html` dùng ảnh trong `regenerated/`, kích thước 512×512. Mỗi batch được regenerate cả lưới, sau đó mới cắt ảnh. Xem `index-original.html` để đối chiếu ảnh PNG gốc.

# Review 3-4 — Trang và ảnh theo audio

- 2 ảnh trang đầy đủ trong `pages/`.
- 5 ảnh cắt trong `tracks/`; 5 MP3 nguồn trong `audio/`. Mỗi ảnh gắn một mã track.
- [Mở preview ảnh và audio](index.html) · [Mapping JSON](manifest.json).
- Audio thiếu nguồn: không có.

| Track | Trang PDF gốc | Trang in | Mục | Ảnh | Audio |
|---|---:|---:|---|---|---|
| CD1_95 | 37 | 36 | A. Listen and circle: Units 3–4 | [PNG](tracks/CD1_95.png) | [MP3](audio/CD1_95.mp3) |
| CD1_96 | 37 | 36 | B. Listen and number: family | [PNG](tracks/CD1_96.png) | [MP3](audio/CD1_96.mp3) |
| CD1_97 | 38 | 37 | A. Parts of the body | [PNG](tracks/CD1_97.png) | [MP3](audio/CD1_97.mp3) |
| CD1_98 | 38 | 37 | Touch your nose | [PNG](tracks/CD1_98.png) | [MP3](audio/CD1_98.mp3) |
| CD1_99 | 38 | 37 | B. Finger / fingers, toe / toes, foot / feet | [PNG](tracks/CD1_99.png) | [MP3](audio/CD1_99.mp3) |
