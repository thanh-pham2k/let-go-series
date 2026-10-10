# Prompt ảnh Challenge — Unit 1–8

Kiểm kê ngày 2026-10-10. **Bộ ảnh Challenge của 8 Unit đã có đầy đủ; các cue được chốt theo yêu cầu người dùng.** Xem trạng thái hiện tại ở audit/challenge-images-completion.md; không sinh lại ảnh đã đạt. Bộ trang học chính đã có: 133 trang Unit + 9 trang Review. Các prompt dưới đây chỉ bổ sung Challenge 1–5, không regenerate bộ trang học hoặc 4 Review.

**Format mới cho cả 12 prompt:** ưu tiên batch **8–12 hình** (8: 4×2, 9: 3×3, 12: 4×3; 10/11 để ô dư trắng). Sau khi xem và cắt từng ô, xuất **WebP 512×512**, quality 80/method 6, mục tiêu thường **15–60 KB/thẻ**. PNG từng thẻ không bắt buộc; giữ ảnh batch gốc để xuất lại. Tranh đếm/động tác cần chi tiết có thể xuất 640×640 hoặc tách batch ít ô hơn, ghi lý do. Không thêm ảnh dư để đủ batch; mapping/preview dùng WebP. Kiểm tra chất lượng sau nén, ghi bytes thực tế và ngoại lệ trên 60 KB.

| Unit | Asset bắt buộc trong kế hoạch | Asset có điều kiện | Prompt độc lập |
|---|---:|---:|---|
| 1 — Toys | 8 | 0 | [Prompt](unit-01.md) |
| 2 — Colors | 19 | 0 | [Prompt](unit-02.md) |
| 3 — Shapes | 17 | 0 | [Prompt](unit-03.md) |
| 4 — Numbers | 18 | 0 | [Prompt](unit-04.md) |
| 5 — Animals | 20 | 0 | [Prompt](unit-05.md) |
| 6 — Food | 15 | 0 | [Prompt](unit-06.md) |
| 7 — My Body | 15 | 0 | [Prompt](unit-07.md) |
| 8 — Abilities | 17 | 0 | [Prompt](unit-08.md) |

Tổng **129 asset bắt buộc + 0 asset có điều kiện**. Đây là số mã hình cần chuẩn bị/tách và nối bài tập, **không phải số hình bắt buộc sinh mới bằng AI**. Phần lớn hình có thể cắt từ tranh chuẩn, ghép nhóm đúng số lượng, hoặc dựng mảng màu/hình học bằng đồ họa xác định. Số lần image_gen thực tế chỉ biết sau khi xem từng crop.

Copy toàn bộ nội dung một file `unit-NN.md` vào một chat riêng. Mỗi chat chỉ ghi `Unit N - TOPIC - Lesson Pages/challenge-assets/`; không sửa các file Unit gốc, script dùng chung hoặc output Unit khác. Các file `unit-NN.inventory.json` là nguồn danh sách/mapping cùng line và câu nguồn; chỉ đọc. Các chat không phụ thuộc vào ảnh mới sinh của chat khác.

Chữ bài học vẫn giữ ở bộ trang học. Với Challenge nhìn hình đoán từ/đếm/nói không hint, chữ câu hỏi và lựa chọn đặt ngoài bitmap; ảnh không chứa nhãn đáp án. Các đoạn thoại, tên, chữ cái và số dùng để học được render riêng bằng font. Không biến bài text/audio/hành động thực tế thành một loạt tranh không cần thiết.

Đã kiểm tra: đủ 8 Unit; mỗi asset có dẫn chứng nguồn; toàn bộ dòng có ký hiệu hình trong Challenge được nối ít nhất một asset; không ID trùng, không tham chiếu asset mồ côi, tất cả ảnh tham khảo tồn tại. Dòng tiêu đề/câu mẫu cũng được ghi để truy vết, nên số `visual_occurrences` không phải số câu hỏi. Các câu chưa đủ context được liệt kê riêng trong từng prompt: chưa thể khẳng định mỗi câu có đáp án duy nhất.

Chống trùng: một ID dùng lại trong mọi Challenge của cùng Unit, H–heart của Unit 3 dùng luôn hình heart, nhóm đếm phân biệt bằng loại vật + số lượng, Unit 8 tách vật dây nhảy khỏi hành động nhảy dây. Cùng từ ở Unit khác không tự động là cùng tranh: cá Food khác cá sống phonics; xe đạp Toys khác hành động ride. Phonics và đối tượng chung ưu tiên lấy lại nguồn lesson hiện hữu thay vì sinh thêm bản mới. Không yêu cầu global shared assets mới để tránh phụ thuộc giữa các chat song song.

Unit8 make_circle/make_line đã được chốt dùng cho câu5 circle/câu6 line và trở thành bắt buộc; không cần tạo lại ảnh hiện có. Audio Challenge vẫn do chủ dự án bổ sung; công việc này không tạo audio. Báo cáo validation.json chỉ kiểm kê Unit; Review có báo cáo riêng bên dưới.

## Challenge của 4 Review — thêm 4 prompt độc lập

Cả 4 Review có 5 Challenge riêng và đã có đủ bộ challenge-assets; các prompt dưới đây dùng để kiểm tra/tiếp tục khi nguồn thay đổi. Copy một prompt vào một chat riêng; có thể chạy song song với 8 Unit vì mỗi chat chỉ ghi thư mục Review của mình. Không dùng các prompt Review cũ ở thư mục cha để làm việc này: chúng là prompt trang lesson.

| Review | Asset cần chuẩn bị | Prompt |
|---|---:|---|
| 1–2: Toys, Colors, School Supplies, Commands | 17 | [Review 1–2](review-1-2.md) |
| 3–4: Shapes, Counts, Classroom Commands | 27 | [Review 3–4](review-3-4.md) |
| 5–6: Animals, Food, Weather, Commands | 19 | [Review 5–6](review-5-6.md) |
| 7–8: Body Actions, Abilities, Days of the Week | 19 | [Review 7–8](review-7-8.md) |

Tổng Review: **82 asset**, nhiều hình có thể crop/ghép/native thay vì sinh mới. Inventory Review có bản ghi cho mọi question_id trong Challenge 1–5, cả câu không cần raster. Nhóm đếm dùng một ảnh cho mọi câu lặp; cặp ghép kiến thức dùng nhiều ID riêng thay vì sinh một tranh mới cho mỗi cặp. Thẻ ngày dùng graphic/font và chế độ giấu tên khi kiểm tra; phân biệt thứ tự thẻ Sunday1–Saturday7 với lịch tháng. Xem [reviews-validation.json](reviews-validation.json). Dựng lại bằng `python audit/build_review_challenge_prompts.py`.

Để dựng lại danh sách từ các bản Markdown hiện tại: `python audit/build_challenge_prompt_inventory.py`. Xem [validation.json](validation.json) để biết kết quả kiểm tra danh sách; đây không phải chứng nhận chất lượng ảnh chưa tạo.
