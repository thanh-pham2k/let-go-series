# Unit 4 — Numbers · Challenge assets

This folder contains the dedicated image cards for Challenge 1–5 of Unit 4. The lesson page PNGs, source Markdown, audio, and ZIP exports remain unchanged.

## Status

- 18/18 required asset IDs complete.
- 11 native count graphics, 2 exact-count compositions from lesson crops, 1 exact-count composition from a clean built-in `image_gen` car source, 2 clean lesson crops, and 3 built-in `image_gen` assets in total (car source, jump rope, kangaroo).
- Every card is WebP 512×512, quality 80, method 6. Native cards are intentionally very small because they are simple line/fill graphics; all remain crisp at the intended card size.
- `contact-sheet.jpg` was reviewed together with the source batch sheets and individual crop cards. `validation.json` records dimensions, bytes, hashes, and link coverage.

## Files

- `manifest.json` — asset provenance, semantic brief, use sites, dimensions, bytes, and review status.
- `question-image-map.json` — all Challenge sections and visual occurrences. Text/audio/action sections explicitly use `image_required: false` with a reason.
- `validation.json` — existence, dimensions, size, duplicate hash, and occurrence coverage checks.
- `preview.html` — learner-style neutral visual preview; prompt text and answer choices stay in the exercise UI.
- `contact-sheet.jpg` — all 18 final WebP cards at once.
- `batches/` — native, crop-composition, and phonics source previews used for QA.
- `batches/generation-log.json` — exact built-in image generation prompts, tool arguments, result paths, source references, and final crop/compose provenance for the three generated assets.
- `references/jump-rope-generated.png` — built-in image generation source for the standalone jump-rope card.

## Source and mapping notes

The five dot cards are native black filled dots, matching the worksheet symbol `●`; they are not toy balls. The five-to-ten outline groups follow the worksheet distinction between double-outline rings (`◎`) and single-outline circles (`○`). The 3-car and 4-teddy groups are clean crops of `CD1_60.png`; the 7-car card uses seven exact-count copies of one complete built-in generated car source and has no answer numeral. The igloo and lion remain crops from the unlabeled upper picture row of `CD1_69.png`; the jump rope and kangaroo are standalone built-in generated objects so neither contains an action scene or clipped edge.

The source's C5 Challenge 4 situation 2 says `7 cars` while the source heading only shows one car emoji. That context issue is resolved by `u04_cars_07`, and is recorded in the mapping as the only raster needed for that conversation section. May-I-come-in, number recognition, word building, and Go/Stop actions stay text/audio/action based. C5 Final Boss reuses the count-group cards above when the adult points to a group; it does not create another duplicate asset.

The final QA pass checked the individual 3-car, 4-teddy, 7-car, igloo, jump-rope, kangaroo, and lion cards after crop repair. The 7-car card now uses seven non-overlapping copies of one complete built-in generated car, with no edge fragments; the teddy crop includes complete feet; the kangaroo card is a complete standalone generated subject with both ears, nose, tail, and feet visible. The native group sheet was checked for the exact counts 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, and 10.

No audio was created. The project owner can add audio independently.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
