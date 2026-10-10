from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).parent
files = sorted((root / "webp").glob("*.webp"))
thumbs = []
for f in files:
    im = Image.open(f).convert("RGB")
    canvas = Image.new("RGB", (200, 220), "white")
    canvas.paste(ImageOps.contain(im, (180, 180)), (10, 5))
    ImageDraw.Draw(canvas).text((8, 190), f.stem, fill="black")
    thumbs.append(canvas)
out = Image.new("RGB", (1000, ((len(thumbs) + 4) // 5) * 220), (235, 235, 235))
for i, thumb in enumerate(thumbs):
    out.paste(thumb, ((i % 5) * 200, (i // 5) * 220))
out.save(root / "contact-sheet.jpg", quality=90)
print(len(files), [(f.name, Image.open(f).size, f.stat().st_size) for f in files])
