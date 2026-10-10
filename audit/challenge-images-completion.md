# Bộ ảnh Challenge đã regenerate

Đã thay toàn bộ **211 ảnh** của **Unit 1–8 và 4 Review** bằng WebP **512×512** mới. Đủ ID, không thiếu/trùng/ảnh thừa. Toàn bộ cue và đáp án được giữ nguyên, không còn ô thiếu cue.

18 master lưới4×3: 17 batch đủ12 ảnh; batch18 có7 ảnh +5 ô trắng không xuất. Mỗi lượt tạo một master bằng built-in image_gen. Batch14 cần chạy lại toàn bộ một lần để sửa biểu tượng STOP: **19 lần gọi tổng cộng**, không sinh từng thẻ riêng.

## Dung lượng và kiểm tra

- Tổng WebP: **3,437,244 bytes**, khoảng **3.28 MiB**.
- Ảnh lớn nhất: **39,850 bytes**, khoảng **38.9 KiB**; mọi ảnh dưới60 KiB.
- Quality80, method6; tất cả file đã decode và kiểm định dạng/kích thước.
- Root đã xem từng thẻ sau nén ở512px trong bảng lossless đủ kích thước, đếm vật và kiểm màu/động tác/anatomy. Các vùng cắt lỗi đã sửa và xem riêng lại. SHA256 gắn với QA của211 file hiện tại.
- Cả12 preview đã được kiểm bằng browser: không ảnh hỏng, mọi ảnh512×512, đáp án giáo viên đóng; đã thử chọn radio và điền chữ.
- 1467 file nguồn/lesson/audio ngoài Challenge giữ nguyên hash trong lượt regenerate này.

Master thực tế1448×1086; ô gốc khoảng350px, có upscale giữ tỷ lệ khi xuất512. Upscale không tạo thêm chi tiết; ảnh sau nén đã được xem ở512px và ở kích thước thẻ nhỏ. Phong cách chung là minh họa textbook2D màu sáng, viền sạch, nền trắng; đặc điểm nội dung theo từng trang nguồn. Thẻ ngày giữ số cue1–7, không tên ngày để lộ đáp án.

## Các bộ

| Bộ | Số ảnh | Kích thước | Max KiB |
|---|---:|---|---:|
| review-1-2 | 17 | 512×512 | 38.9 |
| review-3-4 | 27 | 512×512 | 25.9 |
| review-5-6 | 19 | 512×512 | 33.3 |
| review-7-8 | 19 | 512×512 | 27.1 |
| unit-01 | 8 | 512×512 | 21.6 |
| unit-02 | 19 | 512×512 | 31.6 |
| unit-03 | 17 | 512×512 | 17.6 |
| unit-04 | 18 | 512×512 | 24.9 |
| unit-05 | 20 | 512×512 | 30.4 |
| unit-06 | 15 | 512×512 | 26.8 |
| unit-07 | 15 | 512×512 | 20.5 |
| unit-08 | 17 | 512×512 | 31.3 |

Preview tổng: [challenge-preview.html](challenge-preview.html).

Ảnh đang dùng nằm trong `Let_s Go Begin/Units/<bộ> - Lesson Pages/challenge-assets/webp`. Manifest, contact sheet và preview đã cập nhật. Prompt/master/log/QA của18 batch nằm trong `audit/challenge-regeneration-staging`; bộ prompt: `parallel-prompts/challenge-images/regenerate-12`.

Bản ảnh cũ và metadata để khôi phục nằm trong `audit/challenge-regeneration-backup`. Các PNG/master cũ trong thư mục references/batches là lịch sử; preview chỉ dùng WebP mới. Audio Challenge do chủ dự án tự bổ sung. Chưa commit/push.
