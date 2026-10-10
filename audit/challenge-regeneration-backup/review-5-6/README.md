# Review 5–6 Challenge assets

This folder contains the dedicated picture-card set for Challenge 1–5 in `Review 5-6(2).md`.

- 19 required semantic IDs, each with one `webp/<id>.webp` card at 512×512.
- 88 source questions are represented in `question-image-map.json`; 56 require a static picture and 32 are text/audio/live-roleplay activities with `image_required=false`.
- Repeated questions reuse the same semantic ID. No extra duplicate card was added.
- `preview.html` is a neutral learner-facing preview. It contains no answer labels, printed counts, Vietnamese prompts, or teacher audio hints in the images.
- `contact-sheet.jpg` is an adult QA sheet. `batches/` contains two 4×3 batch masters (10 and 9 occupied cells) kept for regeneration/audit.
- `manifest.json` records semantic meaning, source/provenance, file size, compression, uses, and visual review. `validation.json` records the source-locator, duplicate, dimension, link, and mapping checks.

## Provenance

Five cards remain clean crops/edits from the Review lesson pages. Fourteen cards use the built-in `image_gen` tool with the Review page or a viewed source crop as reference: the isolated variants `r56_cat_01`, `r56_rabbit_01`, `r56_rabbit_05`, plus a second-pass edit of eleven cards whose original crop cut anatomy or object edges. The five-rabbit card replaces a source crop whose lowest rabbit was clipped. No lesson page, source Markdown, audio, or shared script was changed.

The source groups remain semantically distinct: 3/4 cats, 2/5 rabbits, `skip` versus `jump`, `make a line` versus `make a circle`, and `sunny`, `cloudy`, `windy`, `rainy`, `snowy`. Windy visibly includes moving leaves/scarf cues; it is not represented by a cloud-only scene.

## Output checks

All 19 WebPs were opened and reviewed individually at the target size after the second export. They are 512×512, quality 80, method 6, and currently below the 60 KB target. The exact SHA-256 duplicate check is empty. Use the JSON files as the authoritative machine-readable records.

## Exact generation provenance

`provenance.json` preserves the exact built-in `image_gen.imagegen` prompts, referenced paths, arguments, completed result paths, session-log call IDs, and the master/crop operations used to produce the cards. The manifest and both batch JSON files link each final generated card to its provenance event.

`r56_make_circle` is an action adaptation: the final card shows four children making a closed circle while the original lesson crop showed three. The scene is used for the action cue only; no source count is claimed.



Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
