# Unit 2 — Colors · Challenge assets

Bộ này dành riêng cho Challenge 1–5 của `Unit 2 - Colors(3).md`. Có 19 thẻ WebP độc lập ở `webp/`, cùng kích thước 512×512 và nén quality 80/method 6. Không sửa trang lesson, audio hoặc bài Markdown nguồn.

## Phạm vi

- 10 mảng màu: red, blue, yellow, green, brown, purple, orange, black, white, pink.
- 5 đồ chơi có màu: red train, blue ball, brown teddy bear, green yo-yo, green car.
- 4 phonics A–D: apple, bird, cat, dog.

Các câu hỏi trong Challenge dùng lại cùng một ID khi cùng ngữ nghĩa. Các mục nghe chọn câu, ghép câu, điền ngữ pháp, greetings và commands được ghi `image_required=false` trong `question-image-map.json`; không tạo raster thừa cho chúng. Inventory đã được đối chiếu với toàn bộ 26 section Challenge 1–5: 69 visual occurrences đều có mapping, không có context mở.

## Provenance và QA

Mảng màu là native graphics, dùng cùng hình học và viền xám mảnh cho ô trắng. Blue ball, green yo-yo và apple là crop sạch từ trang tham khảo; box pixel được lưu trong `manifest.json` và bản crop master nằm trong `references/`. Red train, brown teddy bear, green car, bird, cat và dog dùng single-subject card đã review bằng built-in `image_gen`: crop trang gốc chứa mảnh vật kế bên, silhouette bị cắt hoặc green car quá nhỏ, nên các batch generated được giữ trong `batches/`.

Đã mở và kiểm tra từng WebP sau export ở 512px. Tất cả có kích thước 512×512, không có chữ/đáp án trên bitmap, không có file vượt 60 KB, và không có duplicate pixel ID. Contact sheet: `contact-sheet.jpg`; learner-safe preview: `preview.html`.

Các file kiểm tra:

- `manifest.json`: semantic, provenance, crop boxes, bytes, hash và uses.
- `question-image-map.json`: mapping theo Challenge/section/item; mục text-only có lý do rõ.
- `validation.json`: kích thước, format, bytes, hash, occurrence coverage và section coverage.
- `batches/index.json`: ba batch master (colors, toys, phonics).

Không tạo audio trong bước này.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
