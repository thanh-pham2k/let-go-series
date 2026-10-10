# Prompt độc lập — Review 1-2 — ảnh Challenge 1–5

Hoàn thiện RIÊNG bộ ảnh Challenge của Review 1-2 trong repo `E:\let-go-series`. Các Review/Unit khác chạy song song. Làm ảnh thật, mapping và preview đến khi kiểm tra được; không chỉ lập kế hoạch, không regenerate bộ trang học chính đã có.

Nguồn bài luyện: `E:\let-go-series\Let_s Go Begin\Units\Review 1-2(3).md`. Đọc cả 5 Challenge và đáp án dành cho người lớn để hiểu ngữ cảnh; không đưa đáp án vào tranh. Inventory chỉ đọc: `E:\let-go-series\parallel-prompts\challenge-images\review-1-2.inventory.json`, gồm mọi question_id, câu nguồn, dòng và asset cần dùng. Tham khảo trực quan PDF `E:\let-go-series\Let_s Go Begin\Units\Review 1-2.pdf`, manifest và các PNG sau:

- `E:\let-go-series\Let_s Go Begin\Units\Review 1-2 - Lesson Pages\pages\png\CD1_36.png`
- `E:\let-go-series\Let_s Go Begin\Units\Review 1-2 - Lesson Pages\pages\png\CD1_37.png`

Phạm vi ghi duy nhất: `E:\let-go-series\Let_s Go Begin\Units\Review 1-2 - Lesson Pages\challenge-assets`. Tạo `png/`, `webp/`, `batches/`, `manifest.json`, `question-image-map.json`, `preview.html`, `contact-sheet.jpg`, `validation.json`, `README.md`. Không sửa Markdown nguồn, lesson pages/metadata, audio, ZIP, script chung, prompt/inventory chung hoặc thư mục Review/Unit khác. Không commit/push. Không cần output mới của chat khác; dùng nguồn lesson hiện đã tồn tại. Đọc output hiện tại trước khi làm để tiếp tục, không tạo lại ảnh đã đạt.

## Danh sách duy nhất — 17 asset

| ID/tên file | Nội dung phải thấy | Cách ưu tiên | Câu dùng chung |
|---|---|---|---|
| `r12_car` | Ô tô đồ chơi ở 1a | crop_or_edit | R12-C1-01, R12-C4-06, R12-C4-10, R12-C5-01, R12-C5-04 |
| `r12_train` | Đoàn tàu đồ chơi ở 1b | crop_or_edit | R12-C1-02, R12-C5-05 |
| `r12_bicycle` | Xe đạp ở 2a | crop_or_edit | R12-C1-03, R12-C5-06 |
| `r12_ball` | Bóng ở 2b | crop_or_edit | R12-C1-04, R12-C4-11, R12-C5-02, R12-C5-07 |
| `r12_green` | Mảng xanh lá 3a | native_graphic | R12-C1-05, R12-C4-07, R12-C4-10, R12-C5-01, R12-C5-08 |
| `r12_red` | Mảng đỏ 3b | native_graphic | R12-C1-06, R12-C5-09 |
| `r12_purple` | Mảng tím 4a | native_graphic | R12-C1-07, R12-C5-10 |
| `r12_yellow` | Mảng vàng 4b | native_graphic | R12-C1-08, R12-C4-11, R12-C5-02, R12-C5-11 |
| `r12_paper` | Một tờ giấy, hình 1 School Supplies | crop_or_edit | R12-C1-09, R12-C3-14, R12-C4-08, R12-C5-12, R12-C5-21 |
| `r12_scissors` | Kéo học sinh, hình 2 | crop_or_edit | R12-C1-10, R12-C5-13 |
| `r12_glue` | Lọ keo có đầu nhọn, hình 3, không chai mỹ phẩm | crop_or_edit | R12-C1-11, R12-C4-12, R12-C5-03, R12-C5-14 |
| `r12_paint` | Lọ màu vẽ và cọ, hình 4 | crop_or_edit | R12-C1-12, R12-C5-15 |
| `r12_tape` | Hộp/cuộn băng keo đúng hình 5, không giấy vệ sinh | crop_or_edit | R12-C1-13, R12-C4-13, R12-C5-16 |
| `r12_stand_up` | Bé đứng dậy, 5a | crop_or_edit | R12-C1-14, R12-C3-15, R12-C4-09, R12-C5-17 |
| `r12_sit_down` | Bé ngồi xuống ghế, 5b | crop_or_edit | R12-C1-15, R12-C3-16, R12-C4-12, R12-C5-03, R12-C5-18 |
| `r12_come_here` | Bé đi về phía cô giáo/người đang gọi, 6a; có người gọi để thấy hướng | crop_or_edit | R12-C1-16, R12-C3-17, R12-C5-19 |
| `r12_turn_around` | Bé quay người, 6b; vệt xoay nhẹ rõ | crop_or_edit | R12-C1-17, R12-C3-18, R12-C4-13, R12-C5-20 |

Một ID một WebP nhẹ; PNG thẻ riêng tùy chọn, giữ batch/crop master để xuất lại. Mọi câu lặp dùng cùng ảnh. Nhóm đếm khác loại/số là ID khác; hình 1 tam giác dùng `triangle`, không thêm triangles_01. Câu nhiều ID giữ đủ hình so sánh/ghép, không chỉ ảnh đáp án. Với nhóm mèo/thỏ ghi “hoặc”: chọn một biến thể đúng câu, không cộng dồn hai nhóm. Câu text/audio/live roleplay không cần raster giữ `image_required=false`; không tạo cảnh từ đáp án nhiễu.

## Nội dung riêng của Review

Giữ come here ở hình 6a, không đổi thành go. Lọ keo/hộp băng keo dùng hình nguồn, không dùng emoji chai mỹ phẩm/giấy vệ sinh. Cặp đồ chơi–màu là ghép hai hình riêng; không khẳng định ô tô nguồn có màu xanh lá. Câu nguồn chỉ có I have paper.; không ghi I have scissors/glue/paint/tape là câu đã in trong PDF.

Cặp từ ở bài ghép hai nhóm là hai hình riêng, không tự biến thành một đối tượng có cả hai đặc điểm (ví dụ car/green không có nghĩa phải tô ô tô xanh). Các biến thể luyện đếm/số ít được ghi là adaptation, không tuyên bố đã có trong PDF. Giữ lệnh/câu mẫu đúng nội dung nguồn. Audio Challenge do chủ dự án bổ sung: không tạo audio, không đoán đáp án MP3 Listen and circle từ tranh.

## Format, phong cách và chữ

Giữ style theo ảnh Review chuẩn và Unit hiện có: textbook cartoon màu sáng, nét viền rõ, soft shading, nhân vật trẻ em cùng thiết kế; nền trắng/sáng, chủ thể đủ lớn, không trang trí gây nhầm. Xuất **WebP 512×512** mặc định, contain không méo/cắt mất vật; được dùng 640×640 nếu nhóm đếm/động tác cần chi tiết và ghi lý do. Mỗi file là thẻ nhỏ đúng ID, không trang lesson 1200×1200 hoặc emoji. Không upscale để giả chi tiết.

WebP lightweight: bắt đầu quality=80, method=6, bỏ metadata thừa; mục tiêu thường 15–60 KB/thẻ. Nếu quá 60 KB thử quality 75 rồi 70 và xem lại sau nén ở kích thước dùng thật. Ưu tiên nhận diện/đếm/anatomy đúng; nếu vẫn lớn giữ bản rõ và ghi ngoại lệ cùng bytes thực tế. PNG thẻ tùy chọn; giữ batch gốc/crop master, preview và mapping dùng WebP.

Ảnh cho đoán từ/đếm/không hint không có nhãn đáp án, speech bubble trả lời, chữ ID, watermark, số lượng in sẵn hay lựa chọn. Câu hỏi, chữ cái lựa chọn, từ/thẻ câu/chỗ trống render bằng font ngoài bitmap. Giữ đủ chữ nguồn trong lesson; không xóa chữ khỏi bộ trang học. Những nội dung học bằng chữ như ngày trong tuần dùng font/UI với chế độ giấu tên khi kiểm tra, không nhờ image_gen viết chữ.

## Quy trình, gom 8–12 hình nhỏ/lần

1. Xem trực quan các PNG nguồn và đối chiếu PDF/mô tả. Ưu tiên crop sạch đúng hình, bỏ nhãn a/b, số câu và text mà không cắt mất chủ thể. Ghi source file và box pixel. Với nhóm đếm giữ đúng lượng; bản đơn có thể cắt một con từ nhóm và ghi adaptation. Không lấy nguyên trang làm ảnh câu hỏi.
2. Nếu crop không đủ, đọc skill imagegen và dùng **built-in image_gen** để sửa/sinh minh họa. Không CLI/API ngoài. Mảng màu/hình học/thẻ ngày được dựng xác định bằng graphic/font; nhóm có thể ghép crop thật theo đúng số lượng. Không thay cảnh người/đồ vật bằng placeholder/SVG để báo đã regenerate.
3. Ưu tiên batch 8–12 ID: 8 = 4 cột × 2 hàng; 9 = 3×3; 12 = 4×3; 10/11 dùng 4×3 và để ô dư trắng. Mỗi ô vuông, gutter trắng thẳng, cùng style, không chữ/ID và không lẫn vật. Batch dùng độ phân giải lớn nhất phù hợp tool, ưu tiên 2048×2048 nếu hỗ trợ; lưới 4×3 trên canvas vuông giữ khoảng trắng ngoài, không kéo méo ô. Kiểm kích thước crop thực tế, không giả định đủ 512px/ô. Chỉ gom ID cần sinh/sửa, không sinh lại crop sạch để đủ nhóm, nhóm cuối được ít hơn 8. Nếu đếm/anatomy mất chi tiết, tách riêng nhóm lỗi thành batch ít ô hơn.
4. Khung prompt: “Create [N] independent square educational cards in [columns] columns and [rows] rows, separated by straight white gutters with safe outer margins, matching the supplied Let’s Go Begin Review references: bright textbook cartoon, bold clean outlines, soft shading, consistent children and objects. Keep cells square and leave unused cells empty. Each panel shows exactly its specified subject/action/count, fully visible. No labels, answer text, numbers, IDs, speech bubbles or watermarks. Row 1, column 1: [full brief]. Row 1, column 2: [full brief]. Continue with one explicit row/column brief for EVERY requested ID. No objects cross panels; no extra countable objects.” Thay hết placeholder và liệt kê đủ các ô trước khi gọi tool. Nhóm đếm nhắc số chính xác; động tác thấy rõ chuyển động/hướng.
5. Log batch gồm IDs, prompt, refs, tool, rows/columns, occupied_cells, crop_boxes thực tế, kết quả/review; giữ ảnh batch gốc. Xem từng ô, sửa bằng built-in, cắt theo gutter thực tế (không chia mù), bỏ ô trắng, contain về 512×512 và xuất `webp/ID.webp` theo thông số nén trên; PNG thẻ tùy chọn.
6. Manifest ghi semantic loại/màu/lượng/hành động/trạng thái, WebP, nguồn/crop hoặc provenance/batch, kích thước, quality, method, file_bytes, visual_review thật. Mapping theo question_id/câu nguồn; cho phép nhiều ID/alternate variants. Mọi câu trong 5 Challenge có bản ghi, kể cả câu không cần ảnh; số dòng chỉ là locator.
7. Preview có toàn bộ thẻ và các câu tiêu biểu, text/câu hỏi đặt ngoài ảnh; answer key/script audio giáo viên giấu trước khi trả lời. Tình huống người lớn diễn/đưa giấy và bài nghe→bé thực hiện dùng lại asset đã có nếu cần minh họa; không tự sinh thêm cảnh không bắt buộc. Nếu nguồn có thêm/mất câu so với inventory, ghi rõ và cập nhật mapping output, không ghi đè nguồn.

## Cổng kiểm tra

- Đủ 17 ID bắt buộc, không ID trùng/thừa; tất cả question_id source có mapping hoặc lý do không cần ảnh. Kiểm source hiện tại, không chỉ số đếm trong inventory.
- Xem mọi WebP sau cắt và nén ở 512px và kích thước thẻ UI; đối chiếu type/color/count/action, đếm từng vật thật, anatomy tự nhiên. Phân biệt take out/put away, open/close, go/stop, skip/jump, line/circle, weather, touch knees/toes và chạm được/chưa chạm được khi có trong Review này.
- Không nhãn đáp án/đánh dấu đúng sai, không mất vật; WebP 512×512 mặc định (640×640 có lý do), quality/file_bytes ghi đủ, mọi link tồn tại. Báo số thẻ vượt 60 KB và lý do, PNG thẻ không bắt buộc. Duplicate hash giữa hai ID khác semantic phải kiểm tra/sửa; cùng nội dung nhiều câu dùng một ID.
- validation ghi số ID có/thiếu, số câu mapped/không cần ảnh/context chưa rõ, dimensions, links và review trực quan. Không báo hoàn chỉnh nếu còn missing/context chưa giải quyết; check kỹ thuật không chứng minh tranh đúng.

Cuối cùng báo asset xong/thiếu, số crop/ghép/native/sinh mới, đường dẫn preview/mapping và hạn chế còn lại. Chỉ làm ảnh Challenge Review 1-2; không tạo audio hoặc thêm lời hát.
