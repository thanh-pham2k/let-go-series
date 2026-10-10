# Unit 3 — Shapes Challenge assets

Status: **complete — 17/17 required IDs**.

This folder contains only the independent image cards for Challenge 1–5 of Unit 3. The source lesson Markdown and lesson-page renders remain unchanged.

## Output

- `webp/`: 17 canonical cards, all 512×512 WebP, quality 80, method 6.
- `batches/`: two native shape masters and one phonics crop master retained for reproducibility.
- `references/CD1_52.png`: provenance copy used to verify phonics crops.
- `manifest.json`: semantic metadata, provenance, bytes, hashes and uses.
- `question-image-map.json`: every inventory visual occurrence plus every text-only section.
- `preview.html`: visual QA grid.
- `contact-sheet.jpg`: contact sheet used during review.
- `validation.json`: final validation evidence.

## Production notes

The 14 geometric cards are deterministic native raster graphics matching the bright textbook style in CD1_43, CD1_47, CD1_53 and CD1_54: white background, bold clean outlines, simple soft shading, and no words or answer hints. The three phonics cards are clean crops from CD1_52 with the printed letters and labels excluded: egg, fish and gorilla. No AI generation was needed because the source contains suitable phonics illustrations and the prompt explicitly permits native geometry.

All 17 WebPs were opened individually at 512px and checked again in the contact sheet. Every file is under 60 KB, has dimensions 512×512, and contains no embedded label, answer, ID or watermark. The shapes are single subjects; the diamond is a geometric rhombus, not a gemstone.

## Mapping and adaptation

`question-image-map.json` covers all Challenge 1–5 sections. Sections without prescribed static art are explicitly marked `image_required=false` with a reason (text/audio, learner action, or conversation task). Every visual occurrence in the shared inventory is mapped to its canonical ID, and all repeated uses share that ID.

C3§6 has six repeated color blanks in the source and no visual cue. Following the unit prompt, the output mapping documents the sequence from C5§3: blue square, purple heart, orange triangle, yellow circle, green square, pink heart. This is an output adaptation only; the source Markdown was not modified.

The challenge can be integrated after the app consumes `question-image-map.json`; no audio was generated here.



Root completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.
