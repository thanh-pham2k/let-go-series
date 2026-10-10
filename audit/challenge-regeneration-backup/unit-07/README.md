# Unit 7 — My Body · Challenge assets

**Cue đã chốt theo yêu cầu người dùng: các ô mơ hồ của bộ này hiện có hình cụ thể và một đáp án cố định. Không còn needs_context ở các mục đã xử lý.**

Bộ này dành riêng cho Challenge 1–5 của `Unit 7 - My Body(2).md`. Có đủ 15 ID bắt buộc trong inventory, mỗi thẻ là WebP 512×512, quality 80, method 6. PNG thẻ và master crop được giữ để có thể xuất lại.

## Phạm vi và provenance

- 8 thẻ body-part: head, shoulders, knees, toes, eyes, ears, mouth, nose.
- 3 thẻ hành động: touch_head, touch_nose, touch_eyes.
- 1 red circle native graphic.
- 3 phonics cards: umbrella, violin, watch.

Các thẻ đạt QA ban đầu được crop từ CD2_42, CD2_46 và các nguồn lesson tương ứng. Batch 3×3 tại `batches/u07-regenerated-9card.png` được dùng cho các thẻ action/phonics đã sửa; head được khôi phục về crop nguồn có mũi tên đúng. Nose và mouth dùng hai single-subject cards được regenerate có marker chính xác, giữ trong `batches/u07_nose-regenerated.png` và `batches/u07_mouth-regenerated.png`. Prompt, tool, refs, kết quả và crop boxes thực tế được lưu trong `batches/generation-log.json`. Crop tránh toàn bộ caption, tên từ, lựa chọn đáp án và speech bubble; box pixel nằm trong `manifest.json`. Red circle được raster hóa từ hình học native, không có chữ.

## Mapping và context

`question-image-map.json` nối đủ 52 visual occurrences từ inventory và bao phủ cả 27 section Challenge. Các section text/audio/perform được ghi rõ `image_required=false`. C3§5, dòng 308 và 311, có `needs_context=true` vì bài nguồn không chỉ rõ bộ phận nào; chỉ chọn một trong ba thẻ touch khi app/hoạt động đã cung cấp thứ tự hoặc cue. Không tự đoán đáp án.

C5§3 dùng ba thẻ hành động tương ứng, không dùng ảnh body-part tĩnh. Các câu C5§9 role-play bằng chữ/động tác không tạo cảnh người mới; riêng hình tròn đỏ tại dòng 524 dùng `u07_red_circle`.

## QA

Đã mở từng WebP sau cắt và nén, kiểm tra tại 512px: kích thước, anatomy, động tác, vật thể hoàn chỉnh, màu, không còn chữ/đáp án trên bitmap. Không có file vượt 60 KB và không có duplicate pixel hash. `preview.html` chỉ hiển thị thẻ trung tính; `validation.json` ghi rõ status `needs_context` vì C3§5 còn thiếu cue trong source. Không sửa Markdown, lesson pages hoặc audio.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.


Cập nhật cue theo quyết định được người dùng giao: dòng 308 → head, dòng 311 → eyes. Đã gắn ảnh cụ thể và đáp án duy nhất; thay thế các ghi chú needs_context cũ ở các mục này. Không tạo thêm ảnh.
