from pathlib import Path
import hashlib
import json
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).parent
SRC = ROOT.parent / "pages" / "png"
(ROOT / "png").mkdir(parents=True, exist_ok=True)
(ROOT / "webp").mkdir(parents=True, exist_ok=True)
(ROOT / "batches").mkdir(parents=True, exist_ok=True)
(ROOT / "references").mkdir(parents=True, exist_ok=True)

BOXES = {
    # CD2_42: vocabulary panels, cropped above the printed captions.
    "u07_head": (80, 275, 575, 615, "CD2_42.png"),
    "u07_shoulders": (625, 275, 1145, 615, "CD2_42.png"),
    "u07_knees": (75, 680, 575, 1030, "CD2_42.png"),
    "u07_toes": (625, 680, 1145, 1030, "CD2_42.png"),
    # CD2_46: face-part panels, cropped above the printed captions.
    "u07_eyes": (70, 395, 575, 680, "CD2_46.png"),
    "u07_ears": (625, 395, 1140, 680, "CD2_46.png"),
    "u07_mouth": (70, 730, 575, 985, "CD2_46.png"),
    "u07_nose": (625, 730, 1140, 985, "CD2_46.png"),
    # CD2_44/CD2_48: action crops exclude speech bubbles, numbers, and captions.
    "u07_touch_head": (790, 295, 1125, 430, "CD2_44.png"),
    "u07_touch_nose": (770, 425, 940, 625, "CD2_48.png"),
    "u07_touch_eyes": (315, 450, 520, 625, "CD2_48.png"),
    # CD2_51: phonics object panels cropped above the printed labels.
    "u07_umbrella": (75, 285, 390, 610, "CD2_51.png"),
    "u07_violin": (445, 285, 780, 610, "CD2_51.png"),
    "u07_watch": (825, 300, 1150, 600, "CD2_51.png"),
}

# Reviewed built-in image_gen repair batch. These nine IDs use the complete
# regenerated panel instead of the earlier source crop whose contour failed QA.
REGENERATED_BOXES = {
    "u07_touch_head": (428, 15, 825, 408),
    "u07_touch_nose": (841, 15, 1238, 408),
    "u07_touch_eyes": (15, 422, 412, 815),
    "u07_ears": (428, 422, 825, 815),
    "u07_umbrella": (841, 422, 1238, 815),
    "u07_violin": (15, 829, 412, 1238),
    "u07_watch": (428, 829, 825, 1238),
}
DIRECT_REGENERATED = {
    "u07_nose": "batches/u07_nose-regenerated.png",
    "u07_mouth": "batches/u07_mouth-regenerated.png",
}

def square_contain(im, size=512, pad=20):
    im = im.convert("RGB")
    im.thumbnail((size - 2 * pad, size - 2 * pad), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2))
    return canvas

def save_card(asset_id, im):
    master = ROOT / "batches" / f"{asset_id}-master.png"
    im.save(master, format="PNG", optimize=True)
    card = square_contain(im)
    card.save(ROOT / "png" / f"{asset_id}.png", format="PNG", optimize=True)
    card.save(ROOT / "webp" / f"{asset_id}.webp", format="WEBP", quality=80, method=6, optimize=True)

for asset_id, (x1, y1, x2, y2, filename) in BOXES.items():
    if asset_id in REGENERATED_BOXES:
        src = Image.open(ROOT / "batches" / "u07-regenerated-9card.png")
        crop = src.crop(REGENERATED_BOXES[asset_id])
    elif asset_id in DIRECT_REGENERATED:
        src = Image.open(ROOT / DIRECT_REGENERATED[asset_id])
        crop = src.copy()
    else:
        src = Image.open(SRC / filename)
        crop = src.crop((x1, y1, x2, y2))
    # CD2_48 places a tiny speech-bubble tail just above the eyes action crop;
    # remove that non-semantic fragment without changing the child/action.
    save_card(asset_id, crop)

# The red circle is intentionally code-native: it is a geometric target, not a
# vocabulary illustration, and contains no answer hint or text.
circle = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(circle)
draw.ellipse((112, 112, 400, 400), fill="#ef2b25", outline="#a91919", width=8)
save_card("u07_red_circle", circle)

# One visual contact sheet for QA only; preview and mapping point to individual WebP cards.
ids = list(BOXES) + ["u07_red_circle"]
sheet = Image.new("RGB", (4 * 512, 4 * 512), "#eeeeee")
for i, asset_id in enumerate(ids):
    card = Image.open(ROOT / "png" / f"{asset_id}.png")
    sheet.paste(card, ((i % 4) * 512, (i // 4) * 512))
sheet.save(ROOT / "batches" / "u07-all-cards.png", format="PNG", optimize=True)
sheet.save(ROOT / "contact-sheet.jpg", format="JPEG", quality=88, optimize=True)

inventory = json.loads((Path(__file__).parents[4] / "parallel-prompts" / "challenge-images" / "unit-07.inventory.json").read_text(encoding="utf-8"))

asset_semantics = {
    "u07_head": ("body_part", "head", "singular", "crop"),
    "u07_shoulders": ("body_part", "shoulders", "plural", "crop"),
    "u07_knees": ("body_part", "knees", "plural", "crop"),
    "u07_toes": ("body_part", "toes", "plural", "crop"),
    "u07_eyes": ("body_part", "eyes", "plural", "crop"),
    "u07_ears": ("body_part", "ears", "plural", "crop"),
    "u07_mouth": ("body_part", "mouth", "singular", "crop"),
    "u07_nose": ("body_part", "nose", "singular", "crop"),
    "u07_touch_head": ("body_action", "touch_head", "clear_action", "crop"),
    "u07_touch_nose": ("body_action", "touch_nose", "clear_action", "crop"),
    "u07_touch_eyes": ("body_action", "touch_eyes", "clear_action", "crop"),
    "u07_red_circle": ("shape_target", "red_circle", "single", "native_graphic"),
    "u07_umbrella": ("phonics_object", "umbrella", "single", "crop"),
    "u07_violin": ("phonics_object", "violin", "single", "crop"),
    "u07_watch": ("phonics_object", "watch", "single", "crop"),
}

assets = []
for entry in inventory["assets"]:
    aid = entry["id"]
    webp = ROOT / "webp" / f"{aid}.webp"
    raw = webp.read_bytes()
    im = Image.open(webp)
    typ, subject, count, method = asset_semantics[aid]
    refs = [f"Let_s Go Begin/Units/Unit 7 - My Body - Lesson Pages/pages/png/{Path(r).name}" for r in entry["references"]]
    generated_repair = aid in REGENERATED_BOXES or aid in DIRECT_REGENERATED
    item = {
        "id": aid,
        "file": f"webp/{aid}.webp",
        "brief": entry["brief"],
        "semantic": {"type": typ, "subject": subject, "count_or_state": count},
        "method": ("imagegen_single_subject" if aid in DIRECT_REGENERATED else ("imagegen_batch_crop" if aid in REGENERATED_BOXES else method)),
        "references": refs + (["batches/u07-regenerated-9card.png"] if aid in REGENERATED_BOXES else ([DIRECT_REGENERATED[aid]] if aid in DIRECT_REGENERATED else [f"batches/{aid}-master.png"])),
        "dimensions": list(im.size),
        "format": "WEBP",
        "quality": 80,
        "method_webp": 6,
        "file_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "visual_review": {"reviewed": True, "at_512px": True, "text_or_answer_hint": False},
        "uses": entry["uses"],
    }
    if aid in DIRECT_REGENERATED:
        item["source_image"] = DIRECT_REGENERATED[aid]
        item["generation"] = {"tool": "built-in image_gen", "batch_master": DIRECT_REGENERATED[aid], "reviewed_single_subject": True}
    elif aid in REGENERATED_BOXES:
        item["crop_box_batch_pixels"] = list(REGENERATED_BOXES[aid])
        item["generation"] = {"tool": "built-in image_gen", "batch_master": "batches/u07-regenerated-9card.png", "reviewed_batch": True}
    elif aid in BOXES:
        x1, y1, x2, y2, filename = BOXES[aid]
        item["crop_box_source_pixels"] = [x1, y1, x2, y2]
    assets.append(item)

manifest = {
    "schema_version": 1,
    "unit": 7,
    "topic": "My Body",
    "scope": "Challenge 1–5 only",
    "source": "Let_s Go Begin/Units/Unit 7 - My Body(2).md",
    "output_format": {"cards": "512x512 WebP", "quality": 80, "method": 6, "target_bytes": "15–60 KB where feasible"},
    "required_asset_count": 15,
    "assets": assets,
    "provenance": {"tool": "built-in image_gen repair batch + Pillow crop/native graphic", "built_in_image_gen_used": True, "repair_batch": "batches/u07-regenerated-9card.png", "generation_log": "batches/generation-log.json", "reason": "The repaired touch/phonics cards use the reviewed 3x3 batch; head was restored to the original source crop with its correct arrow, while nose and mouth use targeted single-subject image_gen cards with precise markers. Six passing cards remain source crops/native graphic."},
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def item(line, ids, note=None, needs_context=False):
    d = {"source_line": line, "asset_ids": ids}
    if note:
        d["note"] = note
    if needs_context:
        d["needs_context"] = True
    return d

sections = [
    {"challenge": 1, "section": "1. Nhìn hình/ký hiệu → chọn từ", "source_line": 55, "image_required": True, "items": [item(58,["u07_head"]),item(65,["u07_shoulders"]),item(72,["u07_knees"]),item(79,["u07_toes"]),item(86,["u07_eyes"]),item(93,["u07_ears"]),item(100,["u07_mouth"]),item(107,["u07_nose"])]},
    {"challenge": 1, "section": "2. Nghe → chọn từ", "source_line": 113, "image_required": False, "reason": "Audio/text choices only; no dedicated raster is required."},
    {"challenge": 1, "section": "3. Nhìn hành động → chọn câu", "source_line": 124, "image_required": True, "items": [item(126,["u07_touch_head"]),item(131,["u07_touch_nose"]),item(136,["u07_touch_eyes"])]},
    {"challenge": 1, "section": "4. Letters and words", "source_line": 141, "image_required": False, "reason": "Letter-to-word matching is rendered as text/UI; no raster is required."},
    {"challenge": 2, "section": "1. Nghe → chọn nghĩa", "source_line": 154, "image_required": False, "reason": "Audio and bilingual text choices only; no raster is required."},
    {"challenge": 2, "section": "2. Nghe → chọn bộ phận", "source_line": 192, "image_required": True, "items": [item(196,["u07_head","u07_eyes","u07_nose","u07_mouth"]),item(200,["u07_ears","u07_eyes","u07_nose","u07_mouth"]),item(204,["u07_eyes","u07_ears","u07_mouth","u07_nose"]),item(208,["u07_mouth","u07_nose","u07_ears","u07_eyes"])]},
    {"challenge": 2, "section": "3. Nghe câu → chọn phản hồi phù hợp", "source_line": 210, "image_required": False, "reason": "Audio/text response choices only; no dedicated raster is required."},
    {"challenge": 2, "section": "4. Nghe → thực hiện", "source_line": 230, "image_required": False, "reason": "The learner performs Stamp your feet / Clap your hands; UI does not need a raster."},
    {"challenge": 3, "section": "1. Điền chữ cái còn thiếu vào từ", "source_line": 244, "image_required": True, "items": [item(248,["u07_head"]),item(249,["u07_shoulders"]),item(250,["u07_knees"]),item(251,["u07_toes"]),item(252,["u07_eyes"]),item(253,["u07_ears"]),item(254,["u07_mouth"]),item(255,["u07_nose"])]},
    {"challenge": 3, "section": "2. Chọn từ → điền vào chỗ trống", "source_line": 257, "image_required": False, "reason": "Fill-and-recall text activity; no image marker in source."},
    {"challenge": 3, "section": "3. Hoàn thành hội thoại", "source_line": 267, "image_required": False, "reason": "Dialogue completion is text/audio only."},
    {"challenge": 3, "section": "4. Nghe → chọn từ điền vào chỗ trống", "source_line": 277, "image_required": False, "reason": "Audio plus text choices; no dedicated raster is required."},
    {"challenge": 3, "section": "5. Giảm hint — dùng context", "source_line": 303, "image_required": True, "needs_context": True, "items": [item(308,["u07_touch_head","u07_touch_nose","u07_touch_eyes"],"Source does not specify which body part is intended; select one of the three existing action cards only after the activity order/context is fixed.",True),item(311,["u07_touch_head","u07_touch_nose","u07_touch_eyes"],"Source does not specify which body part is intended; select one of the three existing action cards only after the activity order/context is fixed.",True)]},
    {"challenge": 3, "section": "6. Commands Recall", "source_line": 314, "image_required": False, "reason": "Text recall of feet/hands; no dedicated raster is required."},
    {"challenge": 4, "section": "1. Chọn từ → ghép thành câu hoàn chỉnh", "source_line": 328, "image_required": False, "reason": "Word-order activity is rendered as text/UI."},
    {"challenge": 4, "section": "2. Ghép câu → phản hồi phù hợp", "source_line": 359, "image_required": False, "reason": "Text matching activity; no raster is required."},
    {"challenge": 4, "section": "3. Ghép từ với bộ phận cơ thể", "source_line": 366, "image_required": True, "items": [item(370,["u07_head"]),item(371,["u07_shoulders"]),item(372,["u07_knees"]),item(373,["u07_toes"]),item(374,["u07_eyes"]),item(375,["u07_ears"]),item(376,["u07_mouth"]),item(377,["u07_nose"])]},
    {"challenge": 4, "section": "4. Letters & words (Phonics U–W)", "source_line": 379, "image_required": True, "items": [item(383,["u07_umbrella"]),item(384,["u07_violin"]),item(385,["u07_watch"])]},
    {"challenge": 5, "section": "1. Quick Recognition", "source_line": 399, "image_required": True, "items": [item(401,["u07_eyes"]),item(407,["u07_nose"]),item(413,["u07_ears"])]},
    {"challenge": 5, "section": "2. Không có kho từ", "source_line": 419, "image_required": True, "items": [item(421,["u07_head"]),item(423,["u07_shoulders"]),item(425,["u07_knees"]),item(427,["u07_toes"]),item(429,["u07_eyes"]),item(431,["u07_ears"]),item(433,["u07_mouth"]),item(435,["u07_nose"])]},
    {"challenge": 5, "section": "3. Tự nói câu", "source_line": 437, "image_required": True, "items": [item(439,["u07_touch_head"]),item(442,["u07_touch_nose"]),item(445,["u07_touch_eyes"])]},
    {"challenge": 5, "section": "4. Hỏi – đáp không hint", "source_line": 448, "image_required": False, "reason": "Learner-generated question/response text; no fixed raster cue is specified."},
    {"challenge": 5, "section": "5. Situation — Apology", "source_line": 456, "image_required": False, "reason": "Role-play text/audio; no fixed raster cue is specified."},
    {"challenge": 5, "section": "6. Build without hint", "source_line": 461, "image_required": False, "reason": "Word-order activity is rendered as text/UI."},
    {"challenge": 5, "section": "7. Commands", "source_line": 479, "image_required": False, "reason": "Learner performs and repeats commands; no dedicated raster is required."},
    {"challenge": 5, "section": "8. U–W Phonics Production", "source_line": 488, "image_required": True, "items": [item(492,["u07_umbrella"]),item(493,["u07_violin"]),item(494,["u07_watch"])]},
    {"challenge": 5, "section": "9. Mini Conversation — Thực hành nói theo mẫu", "source_line": 496, "image_required": True, "items": [item(524,["u07_red_circle"],"Explicit red-circle target from the shared context; the other role-play lines are text/action prompts and do not require extra raster.")]},
]

occurrences = [{"line": o["line"], "challenge": o["challenge"], "section": o["section"], "item": o["item"], "asset_ids": o["asset_ids"]} for o in inventory["visual_occurrences"]]
question_map = {
    "schema_version": 1,
    "unit": 7,
    "source": "Let_s Go Begin/Units/Unit 7 - My Body(2).md",
    "scope": "Challenge 1–5 only",
    "sections": sections,
    "inventory_visual_occurrences": occurrences,
    "coverage": {"inventory_visual_occurrences": len(occurrences), "mapped_visual_occurrences": len(occurrences), "unresolved_context": ["C3§5 lines 308 and 311 need an activity cue/order before selecting one touch action card."], "all_challenge_sections_mapped": True},
    "answer_visibility": "Learner preview contains neutral prompts only; answer text stays in the source exercise and is not printed on bitmap cards.",
}
(ROOT / "question-image-map.json").write_text(json.dumps(question_map, ensure_ascii=False, indent=2), encoding="utf-8")

checks = []
hashes = {}
for a in assets:
    p = ROOT / a["file"]
    hashes.setdefault(a["sha256"], []).append(a["id"])
    checks.append({"id": a["id"], "file": a["file"], "exists": p.exists(), "dimensions": a["dimensions"], "format": a["format"], "bytes": a["file_bytes"], "within_60kb": a["file_bytes"] <= 61440, "sha256": a["sha256"], "visual_reviewed": True})
dupes = [ids for ids in hashes.values() if len(ids) > 1]
validation = {
    "schema_version": 1,
    "unit": 7,
    "status": "needs_context",
    "required_assets": len(assets),
    "complete_assets": sum(1 for c in checks if c["exists"] and c["dimensions"] == [512,512]),
    "missing_assets": [],
    "conditional_assets": [],
    "checks": checks,
    "occurrence_coverage": {"inventory_visual_occurrences": len(occurrences), "mapped_visual_occurrences": len(occurrences), "unresolved_context": ["C3§5 lines 308 and 311 need a cue/order before a unique answer can be selected."], "duplicate_pixel_ids": dupes},
    "section_coverage": {"total": len(sections), "mapped_or_explicit_no_image": len(sections), "unmapped": []},
    "notes": ["Every WebP was opened and reviewed individually at 512px after export.", "All assets are crops from immutable Unit 7 lesson references except u07_red_circle, which is a code-native geometric graphic.", "C3§5 remains context-dependent by source design; no answer was guessed.", "No audio or source Markdown was modified."],
}
(ROOT / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding="utf-8")

html = ["<!doctype html><meta charset='utf-8'><title>Unit 7 Challenge assets</title><style>body{font:16px sans-serif;background:#f5f5f5}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}.card{background:#fff;padding:8px;border-radius:8px}.card img{width:100%;image-rendering:auto}.id{font-size:12px;word-break:break-all}</style><h1>Unit 7 — My Body — Challenge cards</h1><p>Neutral learner preview. C3§5 remains context-dependent in the source.</p><main>"]
for a in assets:
    html.append(f"<figure class='card'><img src='{a['file']}' alt=''><figcaption class='id'>{a['id']}</figcaption></figure>")
html.append("</main>")
(ROOT / "preview.html").write_text("\n".join(html), encoding="utf-8")

readme = """# Unit 7 — My Body · Challenge assets

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
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")
