# Unit 8 Challenge assets — Abilities

**Cue đã chốt theo yêu cầu người dùng: các ô mơ hồ của bộ này hiện có hình cụ thể và một đáp án cố định. Không còn needs_context ở các mục đã xử lý.**

Status: **15/15 mandatory assets complete**. Two additional cue assets are prepared as conditional: `u08_make_circle`, `u08_make_line`.

All files in this folder are scoped to Challenge 1–5 for Unit 8. The source Markdown, lesson pages, audio and other Units were not edited.

## Output

- `webp/`: 17 lightweight cards, each 512×512, WebP quality 80 / method 6.
- `png/`: 17 crop masters for repeatable export.
- `batches/`: three original image_gen sheets and their exact crop logs.
- `batches/generation-log.json`: exact five-job image_gen/edit history, arguments, absolute reference inputs, actual result paths and workspace crop/export operations.
- `manifest.json`: semantic metadata, provenance, dimensions, bytes and hashes.
- `question-image-map.json`: all inventory visual occurrences plus every Challenge section status.
- `preview.html`: neutral visual preview; card labels are hidden so answer words are not shown in the bitmap preview.
- `contact-sheet.jpg`: neutral contact sheet for quick review.
- `validation.json`: completion and QA checks.

## Provenance

The action sheet was generated with the built-in image_gen tool using CD2_59, CD2_63, CD2_54 and CD2_61 as style references. It was cropped row-major into 12 cards. The phonics sheet was generated with CD2_68 as a style reference and cropped into full-body fox, yarn and zebra cards without letters or words. The conditional sheet used CD2_69 as a style reference. Root QA then triggered two targeted repairs: the negative kite card was regenerated with the exact same child, clothing and kite identity as the positive fly-kite card, and the tag card was recomposed so both children have complete heads, hair and feet with safe margins. The repair prompts and outputs are logged in `batches/repair-cannot-fly-kite.json` and `batches/repair-play-tag.json`.

Every WebP was opened and checked at 512×512. The visual distinctions called out in the prompt were verified: riding versus standing, singing versus silence, flying versus failed kite, bouncing versus holding a ball, swim action, both eyes open for smile, one eye closed for wink, dancing versus running, shared ball play, tag chase, and active jump rope.

## Mapping and open context

All 58 visual occurrences in the inventory map to a dedicated ID. Repeated uses reuse the same ID; no duplicate hash groups exist inside this Unit. Sections that are text/audio/action only are explicitly marked image_required=false.

The blank-only items 5–8 in Challenge 3 §2 are documented with the applied vocabulary-order cues swim, smile, wink and dance. The fixed stems in Challenge 3 §3 are documented with positive/negative fly-kite and swim/dance cues; these remain optional UI cues and do not alter the source. The two identical `Make a ________` blanks in Challenge 3 §7 do not establish circle/line order. The two conditional cards are therefore prepared but should be wired only when the app chooses a fixed closed-practice order. Open-ended Can/Can't and personal-answer prompts remain learner production and are not treated as unresolved context.

No audio was created; audio remains the project owner's separate task.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.


Cập nhật cue theo quyết định được người dùng giao: dòng 390 → circle, dòng 391 → line. Đã gắn ảnh cụ thể và đáp án duy nhất; thay thế các ghi chú needs_context cũ ở các mục này. Không tạo thêm ảnh.
