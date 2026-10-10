# Prompt độc lập — Unit 3: Shapes — ảnh Challenge

Hãy hoàn thiện bộ ảnh riêng cho **Challenge 1–5 của Unit 3 — Shapes** trong repo `E:\let-go-series`. Làm đến khi có ảnh thật và mapping kiểm tra được, không chỉ đưa kế hoạch. Chỉ làm Unit này; các chat Unit khác chạy song song.

## Nguồn phải đọc

- Bài luyện chuẩn: `E:\let-go-series\Let_s Go Begin\Units\Unit 3 - Shapes(2).md`. Đọc đầy đủ Challenge 1–5; các số dòng bên dưới chỉ giúp tìm, có thể đổi sau khi source được sửa.
- Inventory chỉ đọc: `E:\let-go-series\parallel-prompts\challenge-images\unit-03.inventory.json`. Dùng `assets` và `visual_occurrences` để nối ID→mọi chỗ dùng. Kiểm tra lại nội dung nguồn nếu đã có thay đổi, cập nhật manifest trong thư mục output của mình, không sửa inventory chung.
- Ảnh/phong cách chuẩn: `E:\let-go-series\Let_s Go Begin\Units\Unit 3 - Shapes - Lesson Pages\pages\png`, manifest và PDF Unit cùng thư mục Units. Các đường dẫn tuyệt đối của ảnh tham khảo có sẵn trong inventory.
- Mẫu phong cách chung chỉ đọc: `E:\let-go-series\Let_s Go Begin\Units\Unit 1 - Toys - Lesson Pages\pages\png\CD1_07.png` và `E:\let-go-series\Let_s Go Begin\Units\Unit 2 - Colors - Lesson Pages\pages\png\CD1_34.png`.

## Phạm vi ghi riêng và chạy song song

Chỉ tạo/sửa trong `E:\let-go-series\Let_s Go Begin\Units\Unit 3 - Shapes - Lesson Pages\challenge-assets`. Tạo `png/`, `webp/`, `batches/`, `references/` nếu cần, `manifest.json`, `question-image-map.json`, `preview.html`, `contact-sheet.jpg`, `validation.json`, `README.md`. Không sửa Markdown Unit gốc, trang lesson, audio, ZIP lesson, root helpers, file prompt/inventory chung, Unit khác. Không commit/push. Không cần chờ chat khác; tất cả nguồn tham khảo hiện đã có. Nếu phát hiện bài nguồn thiếu cue, ghi trong README và mapping chứ không tự ghi đè source.

Trước khi làm, đọc manifest/output đã có để tiếp tục đúng trạng thái; không tạo lại asset đã đạt yêu cầu. Mỗi ID một WebP nhẹ, PNG thẻ riêng là tùy chọn; giữ ảnh batch gốc để xuất lại. Mọi câu trùng dùng cùng ID. Không sinh một bản mới cho mỗi Challenge. Không xóa ảnh nguồn. Chỉ dọn bản output bỏ trong phạm vi mình sau khi xác nhận không còn được tham chiếu.

## Format và chữ

Giữ textbook cartoon như ảnh mẫu: màu sáng, nét viền đậm gọn, soft shading, nhân vật trẻ em cùng thiết kế, thân thiện; không đổi sang ảnh thật, 3D hoặc icon emoji. Nền trắng/sáng, chủ thể rõ, không trang trí gây nhầm, khoảng trống an toàn. Xuất thẻ **WebP 512×512** mặc định, contain giữ tỷ lệ, không kéo méo/cắt vật. Nếu nhóm đếm/động tác mất chi tiết, được dùng 640×640 và ghi lý do riêng trong manifest. Đây là thẻ hình đơn nhỏ cho câu luyện, không phải trang lesson 1200×1200. Không phóng crop nguồn nhỏ để giả chi tiết.

WebP lightweight: bắt đầu quality=80, method=6, bỏ metadata không cần thiết; mục tiêu thường 15–60 KB/thẻ. Nếu quá 60 KB, thử quality 75 rồi 70, xem lại ở kích thước hiển thị thật; không giảm chất lượng đến mức khó nhận vật/màu/ngón tay/số lượng. Nếu vẫn lớn, giữ bản rõ và ghi ngoại lệ cùng bytes thực tế, không tuyên bố đã đạt ngân sách. PNG thẻ không bắt buộc; giữ batch/crop master trong batches/references để có thể xuất lại. Preview/mapping chỉ dùng WebP.

Giữ chữ bài học ở bộ lesson. Trong ảnh Challenge để đoán từ/đếm/nói không hint: **không nhãn từ vựng, không câu trả lời, không tên file/ID, không lựa chọn, không speech bubble trả lời sẵn**. Câu hỏi/câu thoại cần hiện và lựa chọn giữ nguyên văn, đặt ngoài bitmap trong preview/mapping. Chữ cái, số, chỗ trống render bằng font ở UI để chính xác; không tạo ảnh AI chỉ để viết chữ. Dấu ✓/✗ của bài khả năng có thể thay bằng cảnh làm được/không làm được rõ, không dùng một vật tĩnh cho cả hai trạng thái.

## Danh sách duy nhất cần xử lý

**17 ID bắt buộc**. `native_graphic`: đồ họa xác định hợp lệ cho mảng màu/hình học, không placeholder. `compose_from_crops`: ghép từ một hình thật chuẩn thành nhóm đúng số. `crop_or_edit`: ưu tiên cắt nguồn khi không mất nội dung/không còn nhãn; nếu không đủ thì sửa hoặc sinh bằng built-in image_gen. `edit_or_generate`: chỉ dùng lại crop nếu thật sự có đúng cảnh/động tác; cần sửa/sinh nếu thiếu. `conditional`: đọc ghi chú trước khi làm.

| ID / tên file | Nội dung cần thấy | Cách ưu tiên | Track tham khảo | Dòng nguồn dùng chung |
|---|---|---|---|---|
| `u03_circle` | Một hình circle, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_43 | 76, 235, 243, 247, 289, 302, 464 |
| `u03_square` | Một hình square, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_43 | 83, 243, 290, 303, 466 |
| `u03_triangle` | Một hình triangle, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_43 | 90, 243, 291, 307, 468 |
| `u03_heart` | Một hình heart, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_43 | 97, 235, 247, 292, 308, 427, 470, 553 |
| `u03_star` | Một hình star, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_47 | 104, 235, 239, 258, 293, 304, 346, 416, 456, 472, 502, 565, 570 |
| `u03_rectangle` | Một hình rectangle, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_47 | 111, 239, 247, 294, 305, 474 |
| `u03_diamond` | Một hình diamond, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_47 | 118, 235, 239, 247, 264, 295, 306, 349, 417, 444, 476, 507, 573, 578 |
| `u03_oval` | Một hình oval, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý. | native_graphic | CD1_47 | 125, 239, 243, 296, 309, 450, 478 |
| `u03_blue_square` | Một hình square màu blue thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes. | native_graphic | CD1_53, CD1_54 | 162, 359, 482 |
| `u03_purple_heart` | Một hình heart màu purple thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes. | native_graphic | CD1_53, CD1_54 | 169, 360, 485 |
| `u03_orange_triangle` | Một hình triangle màu orange thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes. | native_graphic | CD1_53, CD1_54 | 176, 361, 488 |
| `u03_yellow_circle` | Một hình circle màu yellow thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes. | native_graphic | CD1_53, CD1_54 | 183, 362, 491 |
| `u03_green_square` | Một hình square màu green thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes. | native_graphic | CD1_53, CD1_54 | 363, 494 |
| `u03_pink_heart` | Một hình heart màu pink thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes. | native_graphic | CD1_53, CD1_54 | 364, 418, 497, 581, 586 |
| `u03_egg` | Một egg giống phonics E–H; fish là cá sống, gorilla rõ dáng khỉ đột; không chữ. | crop_or_edit | CD1_52 | 424, 550 |
| `u03_fish` | Một fish giống phonics E–H; fish là cá sống, gorilla rõ dáng khỉ đột; không chữ. | crop_or_edit | CD1_52 | 425, 551 |
| `u03_gorilla` | Một gorilla giống phonics E–H; fish là cá sống, gorilla rõ dáng khỉ đột; không chữ. | crop_or_edit | CD1_52 | 426, 552 |

## Context và chỗ cần chú ý

- C3§6: hai câu square và hai câu heart trùng dạng; dùng bộ 6 hình của C5§3 theo thứ tự blue square, purple heart, orange triangle, yellow circle, green square, pink heart. Đây là đề xuất nối context dựa trên C5, phải ghi adaptation_notes.

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
