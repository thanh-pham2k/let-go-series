# Prompt độc lập — Unit 6: Food — ảnh Challenge

Hãy hoàn thiện bộ ảnh riêng cho **Challenge 1–5 của Unit 6 — Food** trong repo `E:\let-go-series`. Làm đến khi có ảnh thật và mapping kiểm tra được, không chỉ đưa kế hoạch. Chỉ làm Unit này; các chat Unit khác chạy song song.

## Nguồn phải đọc

- Bài luyện chuẩn: `E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food(2).md`. Đọc đầy đủ Challenge 1–5; các số dòng bên dưới chỉ giúp tìm, có thể đổi sau khi source được sửa.
- Inventory chỉ đọc: `E:\let-go-series\parallel-prompts\challenge-images\unit-06.inventory.json`. Dùng `assets` và `visual_occurrences` để nối ID→mọi chỗ dùng. Kiểm tra lại nội dung nguồn nếu đã có thay đổi, cập nhật manifest trong thư mục output của mình, không sửa inventory chung.
- Ảnh/phong cách chuẩn: `E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Lesson Pages\pages\png`, manifest và PDF Unit cùng thư mục Units. Các đường dẫn tuyệt đối của ảnh tham khảo có sẵn trong inventory.
- Mẫu phong cách chung chỉ đọc: `E:\let-go-series\Let_s Go Begin\Units\Unit 1 - Toys - Lesson Pages\pages\png\CD1_07.png` và `E:\let-go-series\Let_s Go Begin\Units\Unit 2 - Colors - Lesson Pages\pages\png\CD1_34.png`.

## Phạm vi ghi riêng và chạy song song

Chỉ tạo/sửa trong `E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Lesson Pages\challenge-assets`. Tạo `png/`, `webp/`, `batches/`, `references/` nếu cần, `manifest.json`, `question-image-map.json`, `preview.html`, `contact-sheet.jpg`, `validation.json`, `README.md`. Không sửa Markdown Unit gốc, trang lesson, audio, ZIP lesson, root helpers, file prompt/inventory chung, Unit khác. Không commit/push. Không cần chờ chat khác; tất cả nguồn tham khảo hiện đã có. Nếu phát hiện bài nguồn thiếu cue, ghi trong README và mapping chứ không tự ghi đè source.

Trước khi làm, đọc manifest/output đã có để tiếp tục đúng trạng thái; không tạo lại asset đã đạt yêu cầu. Mỗi ID một WebP nhẹ, PNG thẻ riêng là tùy chọn; giữ ảnh batch gốc để xuất lại. Mọi câu trùng dùng cùng ID. Không sinh một bản mới cho mỗi Challenge. Không xóa ảnh nguồn. Chỉ dọn bản output bỏ trong phạm vi mình sau khi xác nhận không còn được tham chiếu.

## Format và chữ

Giữ textbook cartoon như ảnh mẫu: màu sáng, nét viền đậm gọn, soft shading, nhân vật trẻ em cùng thiết kế, thân thiện; không đổi sang ảnh thật, 3D hoặc icon emoji. Nền trắng/sáng, chủ thể rõ, không trang trí gây nhầm, khoảng trống an toàn. Xuất thẻ **WebP 512×512** mặc định, contain giữ tỷ lệ, không kéo méo/cắt vật. Nếu nhóm đếm/động tác mất chi tiết, được dùng 640×640 và ghi lý do riêng trong manifest. Đây là thẻ hình đơn nhỏ cho câu luyện, không phải trang lesson 1200×1200. Không phóng crop nguồn nhỏ để giả chi tiết.

WebP lightweight: bắt đầu quality=80, method=6, bỏ metadata không cần thiết; mục tiêu thường 15–60 KB/thẻ. Nếu quá 60 KB, thử quality 75 rồi 70, xem lại ở kích thước hiển thị thật; không giảm chất lượng đến mức khó nhận vật/màu/ngón tay/số lượng. Nếu vẫn lớn, giữ bản rõ và ghi ngoại lệ cùng bytes thực tế, không tuyên bố đã đạt ngân sách. PNG thẻ không bắt buộc; giữ batch/crop master trong batches/references để có thể xuất lại. Preview/mapping chỉ dùng WebP.

Giữ chữ bài học ở bộ lesson. Trong ảnh Challenge để đoán từ/đếm/nói không hint: **không nhãn từ vựng, không câu trả lời, không tên file/ID, không lựa chọn, không speech bubble trả lời sẵn**. Câu hỏi/câu thoại cần hiện và lựa chọn giữ nguyên văn, đặt ngoài bitmap trong preview/mapping. Chữ cái, số, chỗ trống render bằng font ở UI để chính xác; không tạo ảnh AI chỉ để viết chữ. Dấu ✓/✗ của bài khả năng có thể thay bằng cảnh làm được/không làm được rõ, không dùng một vật tĩnh cho cả hai trạng thái.

## Danh sách duy nhất cần xử lý

**15 ID bắt buộc**. `native_graphic`: đồ họa xác định hợp lệ cho mảng màu/hình học, không placeholder. `compose_from_crops`: ghép từ một hình thật chuẩn thành nhóm đúng số. `crop_or_edit`: ưu tiên cắt nguồn khi không mất nội dung/không còn nhãn; nếu không đủ thì sửa hoặc sinh bằng built-in image_gen. `edit_or_generate`: chỉ dùng lại crop nếu thật sự có đúng cảnh/động tác; cần sửa/sinh nếu thiếu. `conditional`: đọc ghi chú trước khi làm.

| ID / tên file | Nội dung cần thấy | Cách ưu tiên | Track tham khảo | Dòng nguồn dùng chung |
|---|---|---|---|---|
| `u06_ice_cream` | Một món ice_cream theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 68, 136, 214, 258, 276, 420, 440, 481 |
| `u06_pizza` | Một món pizza theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 75, 210, 218, 259, 442 |
| `u06_cake` | Một món cake theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 82, 141, 210, 260, 273, 444, 483 |
| `u06_chicken` | Một món chicken theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 89, 210, 218, 261, 426, 446 |
| `u06_milk` | Một món milk theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 96, 206, 214, 262, 274, 448, 469 |
| `u06_fish` | Một món fish theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 103, 206, 210, 263, 275, 450, 474 |
| `u06_bread` | Một món bread theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 110, 206, 214, 218, 264, 452 |
| `u06_rice` | Một món rice theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3). | crop_or_edit | CD2_25, CD2_29 | 117, 206, 214, 218, 265, 432, 454 |
| `u06_queen` | Một queen theo phonics Q–T, không chữ. | crop_or_edit | CD2_33 | 400, 520 |
| `u06_rabbit` | Một rabbit theo phonics Q–T, không chữ. | crop_or_edit | CD2_33 | 401, 521 |
| `u06_sun` | Một sun theo phonics Q–T, không chữ. | crop_or_edit | CD2_33 | 402, 522 |
| `u06_tiger` | Một tiger theo phonics Q–T, không chữ. | crop_or_edit | CD2_33 | 403, 523 |
| `u06_birds` | Nhóm chim để thể hiện birds, không số lượng cố định trong câu. Có thể dùng 2 con tách rõ, ghi là adaptation cho số nhiều, không biến câu thành bài đếm. | compose_from_crops | CD2_07 | 551, 556 |
| `u06_likes_milk` | Bé với ly sữa, biểu cảm và cử chỉ thích rõ; dùng cho tình huống mẫu Yes, I do. Không in câu trả lời hoặc dấu tick. | edit_or_generate | CD2_31 | 535, 540 |
| `u06_dislikes_fish` | Bé với món cá, cử chỉ nhẹ nhàng từ chối rõ; dùng cho tình huống mẫu No, I don’t. Không in câu trả lời hoặc dấu X. | edit_or_generate | CD2_31 | 543, 548 |

## Context và chỗ cần chú ý

- C3§3 bốn câu I’m ____ chỉ khác thứ tự lựa chọn: không xác định được tuổi bằng khuôn mặt. Giữ là luyện nói tuổi tự chọn hoặc bổ sung cue tuổi/audio trước khi gán đáp án; chữ số 5/6/7/10 render bằng font, không cần 4 tranh sinh nhật.
- likes_milk/dislikes_fish chỉ dùng tình huống mẫu cố định C5§9. C5§4 và tình huống birds cho phép trả lời sở thích thật: không ép Yes/No theo ảnh.
- Đã chốt 8 cue theo quyết định được người dùng giao; đọc audit/challenge-cue-decisions.json. Các câu đã gắn hình có expected_answer duy nhất trong mapping, không coi là context mở.

Các bài nghe→chọn chữ, ghép từ/câu, điền ngữ pháp, hỏi tuổi/tên/sở thích/khả năng của chính bé và nghe→bé thực hiện động tác không mặc định cần thêm raster. Ghi `image_required=false` với lý do cho các mục đó. Không tạo thêm cảnh chỉ vì một từ xuất hiện trong đáp án nhiễu. Các câu thiếu cue mà chưa xác định được phải có `needs_context=true`, không báo mapping toàn bộ câu đã hoàn chỉnh.

## Cách tạo, gom 8–12 hình nhỏ/lần

1. Đọc và xem trực quan ảnh tham khảo đúng track trong inventory. Chọn crop sạch nếu giữ nguyên chủ thể; ghi file nguồn và box pixel. Không dùng cả trang có nhãn làm hình đoán đáp án. Không coi tham khảo đã đúng chỉ vì file tồn tại.
2. Khi cần sinh/sửa minh họa, đọc skill imagegen và dùng **built-in image_gen**. Không chuyển sang CLI/API ngoài hoặc tự vẽ thay minh họa nhân vật/đồ vật. Đồ họa mảng màu/hình học và ghép crop nhóm đếm có thể dùng Pillow/SVG rồi raster theo yêu cầu trên. Nếu built-in không dùng được, báo đúng ID còn thiếu.
3. Ưu tiên batch 8–12 ID: 8 hình = 4 cột × 2 hàng; 9 = 3×3; 12 = 4×3. Với 10/11 dùng lưới 4×3, các ô dư để trắng; không sinh hình dư. Đánh số hàng/cột trong prompt/log theo thứ tự đọc, không in số/ID lên ảnh. Mỗi ô vuông, gutter trắng thẳng, cùng style, không lẫn nội dung. Dùng kích thước batch lớn nhất phù hợp tool, ưu tiên 2048×2048 nếu được hỗ trợ; kiểm độ phân giải thực của từng ô sau cắt. Lưới 4×3 ô vuông không kéo giãn để lấp canvas vuông: giữ khoảng trắng ngoài lưới. Không ép batch đủ 8 nếu chỉ còn ít ID hoặc nhiều ID đã crop sạch. Nếu nhóm đếm/anatomy quá nhỏ hoặc lẫn ô, tách riêng nhóm lỗi thành batch ít ô hơn. Không giả định mỗi ô gốc đủ 512px; xuất nhỏ không bổ sung chi tiết bị mất.
4. Khung prompt: “Create [N] independent square educational illustration cards, arranged in [columns] columns and [rows] rows with straight white gutters and safe outer margins, matching the supplied Let’s Go Begin references: bright textbook cartoon, clean bold outlines, soft shading. Keep all cells square, use blank margins rather than stretching, and leave unused cells empty. Each panel contains only its specified subject/action/count, no labels, words, numbers, answer hints, watermarks or panel IDs. Row 1, column 1: [full brief]. Row 1, column 2: [full brief]. Continue with one explicit row/column brief for EVERY requested ID. Keep subjects fully visible; no cross-panel objects.” Trước khi gọi tool, thay hết placeholder và liệt kê đủ 8–12 ô đúng vị trí. Nhóm đếm nhắc lại số lượng, không thêm vật cùng loại ở nền.
5. Log batch gồm IDs, prompt chính xác, tool, refs, rows/columns, occupied_cells, kết quả, crop_boxes thực tế và trạng thái xem. Giữ ảnh batch gốc. Xem từng ô, sửa lỗi bằng built-in, cắt theo gutter thực tế (không chia pixel mù), bỏ ô trắng, contain về 512×512 rồi xuất `webp/ID.webp` theo thông số nén trên. PNG thẻ tùy chọn, không phải cổng hoàn tất.
6. Manifest mỗi asset ghi semantic (loại, màu, lượng, hành động, trạng thái), WebP, cách tạo, refs/crop box, provenance/batch, kích thước, quality, method, file_bytes và visual_review thật. Mapping theo Challenge/section/item và câu nguồn; số dòng chỉ là locator phụ. Một câu có thể nhiều ID (lựa chọn hình), giữ đủ lựa chọn, không chỉ hình đáp án đúng.
7. Preview phải cho xem tất cả ảnh ở kích thước thẻ và thử các câu tiêu biểu: câu hỏi/blank và text choices nằm ngoài ảnh; answer key giáo viên tách riêng, không hiển thị sẵn. Cùng ID có thể dùng nhiều câu. Ghi các câu thiếu cue như trong phần Context; không âm thầm đoán hoặc đổi bài.

## Kiểm tra trước khi báo xong

- Đủ toàn bộ ID bắt buộc, không ID trùng/ngoài danh sách; conditional báo riêng. Mọi occurrence trong inventory được nối hoặc có lý do rõ nếu nguồn đã đổi. Mọi section Challenge 1–5 có mapping ảnh hoặc `image_required=false` / `needs_context=true` trung thực.
- Xem **mọi WebP sau cắt và nén**, không chỉ batch/contact sheet. Đối chiếu vật/màu/động tác/lượng ở 512px và kích thước thẻ UI; đếm thực tế từng vật, anatomy đúng, smile khác wink, bounce khác cầm bóng, tag khác chạy, can khác can’t. Nếu nén mất chi tiết phải xuất lại.
- Không còn chữ/đáp án gợi ý, không mất vật; WebP 512×512 mặc định (640×640 có lý do), quality/bytes được ghi, mọi link mapping/preview tồn tại. Báo số thẻ vượt 60 KB và lý do; không buộc PNG riêng cho từng thẻ.
- Kiểm tra duplicate hash: cùng nội dung trong Unit phải dùng cùng ID; nếu hai ID khác semantic nhưng pixel giống nhau là lỗi cần sửa. Không dùng ảnh tĩnh của đồ vật thay động tác.
- validation ghi required/complete/missing/conditional, occurrence coverage, unresolved context, dimensions, links và visual review. Check kỹ thuật không thay thế kiểm tra nội dung. Không khẳng định Challenge sẵn sàng tích hợp nếu còn `needs_context` chưa xử lý.

Cuối cùng báo số ID xong/thiếu, số sinh mới/crop/ghép/native, preview và mapping, cùng các context còn mở. Không tạo audio: chủ dự án sẽ tự bổ sung.
