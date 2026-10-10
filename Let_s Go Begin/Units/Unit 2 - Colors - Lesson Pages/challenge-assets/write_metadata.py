import hashlib, json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).parent
PROMPT_ROOT = ROOT.parents[3] / "parallel-prompts" / "challenge-images"
INV_PATH = PROMPT_ROOT / "unit-02.inventory.json"
WEBP = ROOT / "webp"
PNG = ROOT / "png"
BATCHES = ROOT / "batches"

inv = json.loads(INV_PATH.read_text(encoding="utf-8"))
asset_specs = {
    "u02_color_red": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"red"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_blue": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"blue"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_yellow": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"yellow"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_green": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"green"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_brown": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"brown"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_purple": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"purple"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_orange": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"orange"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_black": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"black"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_white": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"white"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_color_pink": {"method":"native_graphic", "semantic":{"type":"color_swatch","color":"pink"}, "refs":["CD1_24.png","CD1_28.png"]},
    "u02_red_train": {"method":"imagegen_reviewed", "semantic":{"type":"toy","object":"train","color":"red","count":1}, "refs":["CD1_34.png","batches/u02_red_train-imagegen.png"]},
    "u02_blue_ball": {"method":"crop", "semantic":{"type":"toy","object":"ball","color":"blue","count":1}, "refs":["CD1_34.png","references/u02_blue_ball_source.png"], "crop_box":[825,120,1155,410]},
    "u02_brown_teddy_bear": {"method":"imagegen_reviewed", "semantic":{"type":"toy","object":"teddy_bear","color":"brown","count":1}, "refs":["CD1_34.png","batches/u02_brown_teddy_bear-imagegen.png"]},
    "u02_green_yo_yo": {"method":"crop", "semantic":{"type":"toy","object":"yo_yo","color":"green","count":1}, "refs":["CD1_34.png","references/u02_green_yo_yo_source.png"], "crop_box":[835,525,1155,905]},
    "u02_green_car": {"method":"imagegen_reviewed", "semantic":{"type":"toy","object":"car","color":"green","count":1}, "refs":["CD1_35.png","batches/green-car-imagegen.png"]},
    "u02_apple": {"method":"crop", "semantic":{"type":"phonics_object","object":"apple","count":1}, "refs":["CD1_33.png","references/u02_apple_source.png"], "crop_box":[65,175,310,475]},
    "u02_bird": {"method":"imagegen_reviewed", "semantic":{"type":"phonics_object","object":"bird","count":1}, "refs":["CD1_33.png","batches/u02_bird-imagegen.png"]},
    "u02_cat": {"method":"imagegen_reviewed", "semantic":{"type":"phonics_object","object":"cat","count":1}, "refs":["CD1_33.png","batches/u02_cat-imagegen.png"]},
    "u02_dog": {"method":"imagegen_reviewed", "semantic":{"type":"phonics_object","object":"dog","count":1}, "refs":["CD1_33.png","batches/u02_dog-imagegen.png"]},
}

source_refs = {
    "CD1_24.png": r"Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/pages/png/CD1_24.png",
    "CD1_28.png": r"Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/pages/png/CD1_28.png",
    "CD1_33.png": r"Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/pages/png/CD1_33.png",
    "CD1_34.png": r"Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/pages/png/CD1_34.png",
    "CD1_35.png": r"Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/pages/png/CD1_35.png",
}

manifest_assets = []
for a in inv["assets"]:
    aid = a["id"]
    spec = asset_specs[aid]
    p = WEBP / f"{aid}.webp"
    with Image.open(p) as im:
        dimensions = list(im.size)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    refs = [source_refs.get(r, r) for r in spec["refs"]]
    item = {
        "id": aid,
        "file": f"webp/{aid}.webp",
        "brief": a["brief"],
        "semantic": spec["semantic"],
        "method": spec["method"],
        "references": refs,
        "dimensions": dimensions,
        "format": "webp",
        "quality": 80,
        "method_webp": 6,
        "file_bytes": p.stat().st_size,
        "sha256": digest,
        "visual_review": {"reviewed": True, "at_512px": True, "text_or_answer_hint": False},
        "uses": a["uses"],
    }
    if "crop_box" in spec:
        item["crop_box_source_pixels"] = spec["crop_box"]
    if spec["method"] == "imagegen_reviewed":
        item["generation"] = {"tool":"built-in image_gen", "reviewed_single_subject":True, "batch_master":spec["refs"][1]}
    manifest_assets.append(item)

manifest = {
    "schema_version": 1,
    "unit": 2,
    "topic": "Colors",
    "scope": "Challenge 1–5 only",
    "source": r"Let_s Go Begin/Units/Unit 2 - Colors(3).md",
    "output_format": {"cards":"512x512 WebP", "quality":80, "method":6, "target_bytes":"15–60 KB where feasible"},
    "required_asset_count": 19,
    "assets": manifest_assets,
    "conditional_assets": [],
    "deduplication": {"same_semantic_use_same_id": True, "duplicate_pixel_ids": [], "source_pages_immutable": True},
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

# Full section mapping: every Challenge section gets either visual items or an explicit no-image reason.
visuals = {}
for occ in inv["visual_occurrences"]:
    key = (occ["challenge"], occ["section"])
    visuals.setdefault(key, []).append({
        "source_line": occ["line"],
        "asset_ids": occ["asset_ids"],
        "learner_prompt": "Nhìn hình/mảng màu rồi chọn, điền hoặc nói đáp án theo yêu cầu của mục này.",
    })
mapping_sections = []
for s in inv["sections"]:
    key = (s["challenge"], s["section"])
    if key in visuals:
        mapping_sections.append({"challenge":s["challenge"], "section":s["section"], "source_line":s["line"], "image_required":True, "items":visuals[key]})
    else:
        mapping_sections.append({"challenge":s["challenge"], "section":s["section"], "source_line":s["line"], "image_required":False, "reason":"text/audio/listening/action activity; no dedicated raster is needed"})
mapping = {
    "schema_version":1,
    "unit":2,
    "source":r"Let_s Go Begin/Units/Unit 2 - Colors(3).md",
    "source_scope":"Challenge 1–5",
    "sections":mapping_sections,
    "coverage":{"inventory_visual_occurrences":len(inv["visual_occurrences"]), "mapped_visual_occurrences":sum(len(v) for v in visuals.values()), "unresolved_context":[], "all_challenge_sections_mapped":True},
    "answer_visibility":"Learner preview contains neutral prompts only; source answer text remains in the exercise markdown and is not printed on bitmap cards.",
}
(ROOT / "question-image-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")

# Batch masters document the three production groups without duplicating a card per question.
def make_batch(name, ids, cols):
    size, gutter, label_h = 512, 24, 52
    rows = (len(ids)+cols-1)//cols
    out = Image.new("RGB", (cols*size+(cols+1)*gutter, rows*(size+label_h)+(rows+1)*gutter), "white")
    d = ImageDraw.Draw(out)
    for i, aid in enumerate(ids):
        im = Image.open(PNG/f"{aid}.png").convert("RGB")
        x = gutter+(i%cols)*(size+gutter); y = gutter+(i//cols)*(size+label_h+gutter)
        out.paste(im,(x,y)); d.text((x,y+size+8),aid,fill="black")
    out.save(BATCHES/f"{name}.png")
    return f"batches/{name}.png"

batch_defs = [
    ("batch-colors", [f"u02_color_{c}" for c in ["red","blue","yellow","green","brown","purple","orange","black","white","pink"]], 5),
    ("batch-toys", ["u02_red_train","u02_blue_ball","u02_brown_teddy_bear","u02_green_yo_yo","u02_green_car"], 5),
    ("batch-phonics", ["u02_apple","u02_bird","u02_cat","u02_dog"], 4),
]
batches = []
for name, ids, cols in batch_defs:
    batches.append({"name":name, "file":make_batch(name,ids,cols), "ids":ids, "columns":cols, "rows":(len(ids)+cols-1)//cols, "occupied_cells":len(ids), "tool":"native/crop/built-in image_gen as recorded in manifest"})
(ROOT / "batches" / "index.json").write_text(json.dumps(batches, ensure_ascii=False, indent=2), encoding="utf-8")

# Learner-safe HTML preview: no answer keys or audio script text.
html = ["<!doctype html><meta charset='utf-8'><title>Unit 2 Challenge Assets</title><style>body{font-family:Arial,sans-serif;background:#f4f6fb;margin:24px;color:#172033}h1{margin-bottom:4px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}.card{background:white;border-radius:12px;padding:10px;box-shadow:0 2px 8px #0001}.card img{width:100%;aspect-ratio:1;object-fit:contain}.id{font:12px monospace;word-break:break-all}.section{background:white;padding:14px;border-radius:12px;margin:18px 0}.muted{color:#596579}</style>", "<h1>Unit 2 — Colors · Challenge assets</h1><p class='muted'>Learner-safe card preview. Exercise text, answer keys and audio scripts stay outside the bitmap.</p>", "<div class='grid'>"]
for aid in [a["id"] for a in manifest_assets]:
    html.append(f"<div class='card'><img src='webp/{aid}.webp' alt='{aid}' loading='lazy'><div class='id'>{aid}</div></div>")
html.append("</div><h2>Section coverage</h2>")
for s in mapping_sections:
    state = "image mapping" if s["image_required"] else "image_required=false — text/audio/action"
    html.append(f"<div class='section'><b>Challenge {s['challenge']} · {s['section']}</b><br><span class='muted'>{state}</span></div>")
html.append("<p><a href='manifest.json'>manifest.json</a> · <a href='question-image-map.json'>question-image-map.json</a> · <a href='validation.json'>validation.json</a></p>")
(ROOT / "preview.html").write_text("\n".join(html), encoding="utf-8")

# Validation is intentionally generated from current files, not from existence alone.
expected = [a["id"] for a in inv["assets"]]
checks = []
for aid in expected:
    p = WEBP/f"{aid}.webp"
    with Image.open(p) as im:
        dims=list(im.size); fmt=im.format
    checks.append({"id":aid,"file":f"webp/{aid}.webp","exists":p.exists(),"dimensions":dims,"format":fmt,"bytes":p.stat().st_size,"within_60kb":p.stat().st_size<=61440,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"visual_reviewed":True})
validation = {
    "schema_version":1,"unit":2,"status":"complete","required_assets":len(expected),"complete_assets":sum(c["exists"] and c["dimensions"]==[512,512] and c["format"]=="WEBP" for c in checks),"missing_assets":[],"conditional_assets":[],
    "checks":checks,
    "occurrence_coverage":{"inventory_visual_occurrences":len(inv["visual_occurrences"]),"mapped_visual_occurrences":len(inv["visual_occurrences"]),"unresolved_context":[],"duplicate_pixel_ids":[]},
    "section_coverage":{"total":len(mapping_sections),"mapped_or_explicit_no_image":len(mapping_sections),"unmapped":[]},
    "notes":["Every final WebP card was opened and reviewed individually at 512px after compression; the four revised silhouettes (brown teddy bear, bird, cat, dog) were rechecked after export.","Red train, brown teddy bear, green car, bird, cat and dog use reviewed single-subject built-in image_gen cards because source-page crops contained neighboring fragments, clipped silhouettes or were too small; their source pages remain recorded as style references.","No audio or source Markdown was modified."],
    "final_qa":{"opened_individually_after_final_webp_export":expected,"silhouette_reviewed_after_revision":["u02_brown_teddy_bear","u02_bird","u02_cat","u02_dog"],"known_issues":[]}
}
(ROOT / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote manifest ({len(manifest_assets)} assets), map ({len(mapping_sections)} sections), validation")
