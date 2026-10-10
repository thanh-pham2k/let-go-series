# Unit 5 — Animals · Challenge assets

Status: 20/20 required WebP cards present and visually reviewed.

The cards are lightweight 512×512 WebP files (quality 80, method 6). Most cards were cropped/assembled from the immutable Unit 5 lesson references. Rabbit, cow, duck, and peach masters were repaired with the built-in image generator; dog footer ink was removed by trimming empty space below the platform. No audio or source Markdown was changed. Debug intermediates are retained under `references/debug`; canonical `pages/png/CD2_*.png` files were untouched. Batch masters are in `batches/`; the learner preview is `preview.html`; mapping and provenance are in `question-image-map.json` and `manifest.json`.

## Coverage

- 20 required IDs: dog 1/2, cat 1/2, bird 1/2/3, cow 1/2/8, rabbit 1/2, duck 1/2/3, car 8, moon, nest, octopus, peach.
- 66/66 visual occurrences from the read-only inventory are mapped. Repeated occurrences reuse the same ID.
- All 26 Challenge sections are accounted for. Text-only, audio-only, sentence-building, personal speaking, and listen-and-act items are explicitly `image_required=false`.
- No card contains answer words, Vietnamese instructions, quantities as labels, audio scripts, or panel IDs. Source excerpts and answer-bearing evidence appear only under teacher/provenance details in the preview and mapping files.

## Applied adaptations

The source has three `How many ____?` blanks in Challenge 3 §3 without an inline picture. The authorized prompt order is applied as `u05_duck_03`, `u05_cow_08`, `u05_car_08`, with `adaptation_applied=true`; the source Markdown is unchanged.

Challenge 3 §5 explicitly asks about ducks, cows, and cars, and Challenge 5 §7 explicitly models the count answers. Those rows reuse the existing 3-duck, 8-cow, 8-car and 2-cat cards. There are no unresolved context flags. The learner preview keeps the question wording and blanks visible, while answer-bearing source excerpts remain in teacher/provenance details.

See `validation.json` for dimensions, byte sizes, hashes, link-level checks, mapping totals, and adaptation status.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
