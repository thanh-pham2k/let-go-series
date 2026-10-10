# Bộ prompt regenerate toàn bộ Challenge — 12 ô/lần

Bộ mới này thay hướng dẫn tạo ảnh trước đây: regenerate toàn bộ 211 ID của Unit 1–8 và 4 Review, không bỏ qua ảnh hiện có, không ngoại lệ 640px. Mỗi file batch là một prompt độc lập và đúng một lần gọi image_gen tạo master 4×3. Sau đó cắt ra WebP 512×512 lightweight, giữ nguyên ID và ý nghĩa nguồn. Hai mẫu lesson chung áp dụng cho mọi batch để giữ phong cách.

211 không chia hết cho 12: 17 batch đầy đủ 12 ảnh, batch 18 có 7 ảnh + 5 ô trắng. Không tạo 5 ảnh dư. Batch có thể đi qua ranh giới Unit/Review để gom đủ 12; đường dẫn từng ID đã ghi rõ. Có thể chạy các batch song song trong staging riêng; tích hợp manifest/mapping chung tuần tự sau QA để tránh ghi đè nhau.

Đây là bộ prompt, chưa phải bộ ảnh regenerate đã hoàn thành. Một lần generate là một master, không phải tool trả trực tiếp 12 file WebP. Phải cắt và nén sau khi tạo. Nếu batch lỗi, báo cần chạy lại; không coi lần tạo là bảo đảm chất lượng.

- [Batch 01](batch-01.md): 12 ảnh, 0 ô trắng.
- [Batch 02](batch-02.md): 12 ảnh, 0 ô trắng.
- [Batch 03](batch-03.md): 12 ảnh, 0 ô trắng.
- [Batch 04](batch-04.md): 12 ảnh, 0 ô trắng.
- [Batch 05](batch-05.md): 12 ảnh, 0 ô trắng.
- [Batch 06](batch-06.md): 12 ảnh, 0 ô trắng.
- [Batch 07](batch-07.md): 12 ảnh, 0 ô trắng.
- [Batch 08](batch-08.md): 12 ảnh, 0 ô trắng.
- [Batch 09](batch-09.md): 12 ảnh, 0 ô trắng.
- [Batch 10](batch-10.md): 12 ảnh, 0 ô trắng.
- [Batch 11](batch-11.md): 12 ảnh, 0 ô trắng.
- [Batch 12](batch-12.md): 12 ảnh, 0 ô trắng.
- [Batch 13](batch-13.md): 12 ảnh, 0 ô trắng.
- [Batch 14](batch-14.md): 12 ảnh, 0 ô trắng.
- [Batch 15](batch-15.md): 12 ảnh, 0 ô trắng.
- [Batch 16](batch-16.md): 12 ảnh, 0 ô trắng.
- [Batch 17](batch-17.md): 12 ảnh, 0 ô trắng.
- [Batch 18](batch-18.md): 7 ảnh, 5 ô trắng.

Đối chiếu đầy đủ: `batch-index.json`; kiểm tra coverage: `validation.json`. Không cần tạo audio.
