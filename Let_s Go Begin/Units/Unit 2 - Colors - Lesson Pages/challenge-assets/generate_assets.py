from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
PNG = ROOT / "png"
WEBP = ROOT / "webp"
BATCHES = ROOT / "batches"
REFERENCES = ROOT / "references"
for d in (PNG, WEBP, BATCHES, REFERENCES):
    d.mkdir(parents=True, exist_ok=True)

SRC = Path(r"E:\let-go-series\Let_s Go Begin\Units\Unit 2 - Colors - Lesson Pages\pages\png")
GEN = Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-3f2a-7470-8b16-d2b463a7c7bc\exec-d18a29d5-d035-4d68-a586-6290c1c46e57.png")
GEN_TRAIN = Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-3f2a-7470-8b16-d2b463a7c7bc\exec-a46d8506-2bcb-4e79-844c-f7fa27d7171b.png")
GEN_TEDDY = Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-3f2a-7470-8b16-d2b463a7c7bc\exec-e2a5e494-743f-4796-885b-89c17a5104af.png")
GEN_BIRD = Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-3f2a-7470-8b16-d2b463a7c7bc\exec-e6207008-a3f4-47be-a702-34bfce03636b.png")
GEN_CAT = Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-3f2a-7470-8b16-d2b463a7c7bc\exec-24dd7904-b269-414f-96c1-f21ff769ab16.png")
GEN_DOG = Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-3f2a-7470-8b16-d2b463a7c7bc\exec-e351f589-9326-4c39-b4f0-8747bc993171.png")

def card_from_image(im, out_png, size=512):
    im = im.convert("RGBA")
    # white card, contain the source crop without stretching
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    scale = min((size * 0.82) / im.width, (size * 0.82) / im.height)
    nw, nh = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    canvas.alpha_composite(im, ((size - nw) // 2, (size - nh) // 2))
    canvas.convert("RGB").save(out_png, "PNG", optimize=True)

def export_webp(stem):
    p = PNG / f"{stem}.png"
    w = WEBP / f"{stem}.webp"
    Image.open(p).convert("RGB").save(w, "WEBP", quality=80, method=6, optimize=True)

# Native swatches: identical rounded-square geometry, with a faint grey edge for white.
colors = {
    "red": (239, 55, 55), "blue": (58, 112, 218), "yellow": (251, 205, 45),
    "green": (71, 188, 78), "brown": (157, 93, 48), "purple": (145, 78, 174),
    "orange": (246, 139, 43), "black": (34, 34, 40), "white": (255, 255, 255),
    "pink": (243, 104, 177),
}
for name, rgb in colors.items():
    im = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    # restrained shadow below the swatch, matching the lesson's soft shading
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((112, 118, 400, 406), radius=28, fill=(0, 0, 0, 32))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(shadow)
    d = ImageDraw.Draw(im)
    outline = (170, 170, 170, 255) if name == "white" else (35, 35, 45, 255)
    d.rounded_rectangle((104, 104, 392, 392), radius=28, fill=(*rgb, 255), outline=outline, width=5)
    im.convert("RGB").save(PNG / f"u02_color_{name}.png", "PNG", optimize=True)
    export_webp(f"u02_color_{name}")

# Clean crops from the lesson page; boxes stop before the printed labels.
src34 = Image.open(SRC / "CD1_34.png")
src35 = Image.open(SRC / "CD1_35.png")
src33 = Image.open(SRC / "CD1_33.png")
crops = {
    "u02_red_train": (525, 135, 830, 415),
    "u02_blue_ball": (825, 120, 1155, 410),
    "u02_brown_teddy_bear": (565, 510, 825, 895),
    "u02_green_yo_yo": (835, 525, 1155, 905),
}
for stem, box in crops.items():
    crop = src34.crop(box)
    crop.save(REFERENCES / f"{stem}_source.png")
    card_from_image(crop, PNG / f"{stem}.png")
    export_webp(stem)

# The source page places a second partial train and a neighboring figure beside these two
# cards; use the reviewed single-subject generations so no distractor fragments remain.
for stem, generated in (
    ("u02_red_train", GEN_TRAIN),
    ("u02_brown_teddy_bear", GEN_TEDDY),
):
    if generated.exists():
        card_from_image(Image.open(generated), PNG / f"{stem}.png")
        export_webp(stem)
        Image.open(generated).save(BATCHES / f"{stem}-imagegen.png")

# Phonics cards: crop only the illustration panel and stop before the printed word.
phonics = {
    "u02_apple": (65, 175, 310, 475),
    "u02_bird": (345, 185, 595, 475),
    "u02_cat": (635, 185, 850, 475),
    "u02_dog": (925, 190, 1125, 475),
}
for stem, box in phonics.items():
    crop = src33.crop(box)
    crop.save(REFERENCES / f"{stem}_source.png")
    card_from_image(crop, PNG / f"{stem}.png")
    export_webp(stem)

# Replace the three phonics crops whose source panels clipped the silhouette; keep the
# original crops in references/ for provenance, but use complete reviewed cards.
for stem, generated in (("u02_bird", GEN_BIRD), ("u02_cat", GEN_CAT), ("u02_dog", GEN_DOG)):
    if generated.exists():
        card_from_image(Image.open(generated), PNG / f"{stem}.png")
        export_webp(stem)
        Image.open(generated).save(BATCHES / f"{stem}-imagegen.png")

# Green car was too small in CD1_35 for a faithful crop; use the reviewed generated card.
if GEN.exists():
    card_from_image(Image.open(GEN), PNG / "u02_green_car.png")
    export_webp("u02_green_car")
    Image.open(GEN).save(BATCHES / "green-car-imagegen.png")

# Preserve exact source pages used for review, without modifying lesson pages.
for name in ("CD1_24", "CD1_28", "CD1_33", "CD1_34", "CD1_35"):
    p = SRC / f"{name}.png"
    target = REFERENCES / f"{name}.png"
    if not target.exists():
        Image.open(p).save(target)

print(f"exported {len(list(WEBP.glob('*.webp')))} WebP cards")
