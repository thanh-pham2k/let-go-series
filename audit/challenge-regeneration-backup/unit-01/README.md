# Unit 1 — Toys Challenge assets

This folder contains the dedicated image cards for Challenge 1–5 in `Unit 1 - Toys(5).md`. The eight required cards are reused across every relevant question so the same toy never receives duplicate artwork.

The cards were cropped from the approved lesson vocabulary pages `CD1_07.png` and `CD1_11.png`, then contained on a white 512×512 canvas and exported as WebP quality 80, method 6. The source pages remain untouched. Each final card was checked individually at 512px after compression; all are below the 60 KB target and contain no printed vocabulary labels or answer choices.

Use `question-image-map.json` for section-level integration. It includes every Challenge section: visual sections list their reusable asset IDs, while audio/text/order/physical-response sections are explicitly marked `image_required: false`. Challenge 2 section 2 uses all eight toy cards as its shared picture choices even though the source has no `🖼️` marker on every answer line.

`manifest.json` records the source crop box, batch master, file size, hash, semantic content, and visual review. `batches/u01_toys_8_cards.png` is the 4×2 crop master; `png/` keeps optional lossless cards for re-export, and `webp/` is the integration set. `preview.html` shows the final cards and links the mapping.

No audio was created. Audio for Challenge activities is tracked in the source Unit markdown and remains the project owner's follow-up work.


Root final QA correction: 7 source crops + 1 built-in image_gen edit for doll, restoring complete rounded shoes/bow. Final master/provenance in batches/doll-final-imagegen.*; contact sheet/batch updated. Original yo-yo vignette has open string at its top boundary, retained faithfully.


Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
