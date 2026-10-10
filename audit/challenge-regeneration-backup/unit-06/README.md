# Unit 6 Food — Challenge assets

**Cue đã chốt theo yêu cầu người dùng: các ô mơ hồ của bộ này hiện có hình cụ thể và một đáp án cố định. Không còn needs_context ở các mục đã xử lý.**

This folder contains the dedicated picture cards for Challenge 1–5 in `Unit 6 - Food(2).md`. It does not modify the lesson pages, source Markdown, or audio.

## Result

- 15/15 required IDs have a final WebP card.
- Every card is 512×512, WebP quality 80, method 6, and under 60 KB.
- The food cards and the plural birds card are clean crops/compositions from the existing lesson artwork; ice cream and cake use full-object imagegen edits from that same source artwork to preserve complete contours and stands.
- The Q–T phonics cards, the two fixed preference scenes, and the complete ice cream/cake object edits were generated with the built-in image generation tool after checking that the source crops left letters, numbers, or answer cues at the edges.
- Every final WebP was opened and reviewed individually after export. The contact sheet is only a navigation aid: `batches/unit6-challenge-assets-contact-sheet.jpg`.

## Card rules

Cards contain no vocabulary labels, answer text, speech bubbles, numbers, IDs, check marks, or X marks. `u06_fish`, `u06_dislikes_fish`, and the fish scene in the latter card show food on a plate; the live fish phonics/animal artwork from another unit is not used.

`u06_birds` is a five-bird group adapted from the existing plural example. It is a plural cue, not a fixed counting question. `u06_likes_milk` and `u06_dislikes_fish` are reserved for the fixed model situations in Challenge 5 §9. Challenge 5 §4 uses the neutral food cards and keeps the learner's Yes/No preference open.

## Mapping and review

`question-image-map.json` covers every Challenge 1–5 section. Items that are text/audio/action only are explicitly marked `image_required: false`; personal age and preference responses are marked `personal_response: true`. Only the repeated food/preference blanks in Challenge 3 §2 remain `needs_context: true`, because the source provides no target cue for those fixed blanks.

`manifest.json` records semantic meaning, provenance/crop boxes, export settings, byte sizes, and the required ID set. `validation.json` records the final link, dimension, size, duplicate-hash, occurrence-coverage, and visual-review checks.

## Provenance

Source crops: `CD2_25.png` (ice cream, pizza, cake, chicken), `CD2_29.png` (milk, food fish, bread, rice), and Unit 5 `CD2_07.png` (birds). The original pages remain untouched. Generated source masters for all eight generated or edited cards are kept in `references/`.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.


Cập nhật cue theo quyết định được người dùng giao: dòng 273 → cake, dòng 274 → milk, dòng 275 → fish, dòng 276 → ice cream. Đã gắn ảnh cụ thể và đáp án duy nhất; thay thế các ghi chú needs_context cũ ở các mục này. Không tạo thêm ảnh.
