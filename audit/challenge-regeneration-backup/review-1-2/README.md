# Review 1–2 Challenge assets

Completed dedicated visual set for Challenge 1–5. The 17 required IDs are present once and reused by the 51 image-required questions; the other 32 questions are mapped as text/audio/live-roleplay with `image_required=false`.

Production summary: 8 clean crops, 9 built-in image edits (including the repaired car, train, bicycle, swatches, paper and action cards), 0 native graphics, 0 composites, and no open context items.

## Sources and provenance

- Lesson references: `pages/png/CD1_36.png` and `pages/png/CD1_37.png`.
- Most cards are clean crops with question numbers, a/b markers, and printed answer labels removed.
- `r12_paint` was edited with the built-in image generation tool to remove the printed word “Red” while preserving the paint jar and brush.
- `come here` keeps the teacher and direction cue from source image 6a.

## Outputs

- `webp/`: 17 cards, all 512×512, quality 80, method 6.
- `png/`: crop/edit masters.
- `batches/`: two source crop boards, retained for re-export.
- `manifest.json`: asset provenance, crop boxes, bytes and hashes.
- `batches/imagegen-log.json`: the nine actual built-in imagegen edit calls, with exact prompts, input references and result paths. `creation_method` is separate from WebP codec `method=6`.
- `question-image-map.json`: all 83 source question IDs; original `source_prompt` is provenance only, while `learner_prompt` is neutral.
- `preview.html`: all cards and representative questions without answer keys or teacher audio scripts.
- `contact-sheet.jpg`: visual QA board.
- `validation.json`: source parity, coverage, dimensions, duplicate and size checks.

No audio, source Markdown, lesson metadata, or other Review/Unit folders were changed.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
