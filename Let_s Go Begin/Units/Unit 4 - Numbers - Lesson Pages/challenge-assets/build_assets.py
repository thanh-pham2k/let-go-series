from PIL import Image, ImageDraw
from pathlib import Path
import shutil, math

ROOT = Path(r"E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\challenge-assets")
SRC = Path(r"E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\pages\png")
ROOT.mkdir(parents=True, exist_ok=True)
for d in ("webp", "batches", "references"):
    (ROOT/d).mkdir(exist_ok=True)

def card():
    return Image.new("RGBA", (512, 512), (255,255,255,255))

def save_webp(im, asset_id):
    if im.mode != "RGBA": im = im.convert("RGBA")
    bg = Image.new("RGBA", (512,512), (255,255,255,255))
    bbox = im.getbbox()
    if bbox:
        crop = im.crop(bbox)
        crop.thumbnail((430,430), Image.Resampling.LANCZOS)
        bg.alpha_composite(crop, ((512-crop.width)//2,(512-crop.height)//2))
    out = ROOT/"webp"/f"{asset_id}.webp"
    bg.convert("RGB").save(out, "WEBP", quality=80, method=6)
    return out

def draw_group(kind, n, color):
    im = card(); d=ImageDraw.Draw(im)
    cols = 5 if n >= 8 else (4 if n >= 6 else n)
    rows = (n+cols-1)//cols
    size = 54 if n>=9 else 64
    gapx = 512//(cols+1); gapy = 512//(rows+1)
    for i in range(n):
        r,c=divmod(i,cols); x=(c+1)*gapx; y=(r+1)*gapy
        if kind == "dot": d.ellipse((x-size//2,y-size//2,x+size//2,y+size//2), fill=(25,25,25,255))
        elif kind == "ring":
            d.ellipse((x-size//2,y-size//2,x+size//2,y+size//2), outline=color, width=7)
            inner=size//3
            d.ellipse((x-inner,y-inner,x+inner,y+inner), outline=color, width=5)
        elif kind == "triangle": d.polygon([(x,y-size//2),(x-size//2,y+size//2),(x+size//2,y+size//2)], outline=color, width=7)
        elif kind == "star":
            pts=[]
            for j in range(10):
                a=-math.pi/2+j*math.pi/5; rad=size//2 if j%2==0 else size//4
                pts.append((x+rad*math.cos(a),y+rad*math.sin(a)))
            d.line(pts+[pts[0]], fill=color, width=7, joint="curve")
        elif kind == "circle": d.ellipse((x-size//2,y-size//2,x+size//2,y+size//2), outline=color, width=7)
        elif kind == "heart":
            pts=[(x,y+size//2),(x-size//2,y),(x-size//2,y-size//4),(x-size//4,y-size//2),(x,y-size//4),(x+size//4,y-size//2),(x+size//2,y-size//4),(x+size//2,y),(x,y+size//2)]
            d.line(pts, fill=color, width=7, joint="curve")
        elif kind == "square": d.rectangle((x-size//2,y-size//2,x+size//2,y+size//2), outline=color, width=7)
    return im

native = [
    ("u04_dots_01","dot",1,(25,25,25)), ("u04_dots_02","dot",2,(25,25,25)),
    ("u04_dots_03","dot",3,(25,25,25)), ("u04_dots_04","dot",4,(25,25,25)),
    ("u04_dots_05","dot",5,(25,25,25)), ("u04_rings_05","ring",5,(110,46,170)),
    ("u04_triangles_06","triangle",6,(35,125,70)), ("u04_stars_07","star",7,(242,92,25)),
    ("u04_circles_08","circle",8,(220,36,45)), ("u04_hearts_09","heart",9,(100,42,165)),
    ("u04_squares_10","square",10,(30,160,220)),
]
masters=[]
for aid,k,n,c in native:
    im=draw_group(k,n,c); masters.append((aid,im)); save_webp(im,aid)

def source_crop(name, box):
    return Image.open(SRC/name).convert("RGBA").crop(box)

cars3 = source_crop("CD1_60.png", (65,535,720,718))
teddies4 = source_crop("CD1_60.png", (45,795,710,1025))
save_webp(cars3,"u04_cars_03")
save_webp(teddies4,"u04_teddy_bears_04")

page=Image.open(SRC/"CD1_60.png").convert("RGBA")
generated_car=Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-6e5f-7d90-82fa-23481e4f77ee\exec-f0ccbe1b-77d2-4a0d-a33e-dfbc5bb5271b.png")
# Explicit silhouettes prevent neighboring cars and the worksheet background from
# leaking into the seven-car composition. Coordinates are source-page pixels.
silhouettes=[
    [(72,650),(82,618),(98,604),(101,580),(128,550),(220,547),(246,560),(270,585),(279,615),(296,632),(304,670),(288,696),(250,711),(205,708),(170,711),(124,710),(94,700),(76,680)],
    [(312,650),(316,608),(333,589),(340,560),(382,546),(447,546),(470,560),(490,590),(500,630),(508,645),(508,680),(500,700),(460,711),(410,708),(369,710),(330,699),(313,680)],
    [(525,646),(525,604),(540,582),(550,552),(612,546),(678,550),(699,575),(708,610),(714,636),(720,650),(720,690),(700,706),(660,711),(610,710),(570,706),(530,700),(525,680)],
]
parts=[]
for poly in silhouettes:
    mask=Image.new("L",page.size,0); ImageDraw.Draw(mask).polygon(poly,fill=255)
    b=mask.getbbox(); q=page.crop(b); q.putalpha(mask.crop(b)); px=q.load()
    for yy in range(q.height):
        for xx in range(q.width):
            r,g,bl,a=px[xx,yy]
            if a and ((r>185 and g>190 and bl>190) or (bl>205 and g>190 and r<205)):
                px[xx,yy]=(r,g,bl,0)
    parts.append(q)
seven=card(); positions=[(22,32),(187,32),(352,32),(22,190),(187,190),(352,190),(187,348)]
if generated_car.exists():
    shutil.copy2(generated_car, ROOT/"references"/"car-generated.png")
    base=Image.open(generated_car).convert("RGBA").crop(Image.open(generated_car).convert("RGBA").getbbox())
    base.thumbnail((138,110),Image.Resampling.LANCZOS)
    for pos in positions: seven.alpha_composite(base,pos)
else:
    for i,pos in enumerate(positions):
        q=parts[i%3].copy(); q.thumbnail((138,110),Image.Resampling.LANCZOS); seven.alpha_composite(q,pos)
save_webp(seven,"u04_cars_07")

igloo=source_crop("CD1_69.png",(55,210,350,545))
generated_kangaroo=Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-6e5f-7d90-82fa-23481e4f77ee\exec-19bc11ee-0995-4521-bbb9-1ed16ece2a66.png")
if generated_kangaroo.exists():
    shutil.copy2(generated_kangaroo, ROOT/"references"/"kangaroo-generated.png")
    kangaroo=Image.open(generated_kangaroo).convert("RGBA")
else:
    kangaroo=source_crop("CD1_69.png",(585,195,855,545))
# Keep the full ears and tail while removing the pale sky/white page artefacts.
kp=kangaroo.load()
for yy in range(kangaroo.height):
    for xx in range(kangaroo.width):
        r,g,bl,a=kp[xx,yy]
        if a and ((r>235 and g>235 and bl>235) or (bl>190 and g>160 and bl-r>25)):
            kp[xx,yy]=(r,g,bl,0)
lion=source_crop("CD1_69.png",(875,225,1150,545))
save_webp(igloo,"u04_igloo"); save_webp(kangaroo,"u04_kangaroo"); save_webp(lion,"u04_lion")

generated=Path(r"C:\Users\Admin\.codex\generated_images\01a1241b-6e5f-7d90-82fa-23481e4f77ee\exec-3c38cbde-eacf-4a4b-aa7c-ffaba02ce992.png")
if generated.exists():
    shutil.copy2(generated, ROOT/"references"/"jump-rope-generated.png")
    save_webp(Image.open(generated).convert("RGBA"),"u04_jump_rope")

def sheet(items, name, cols=4):
    thumb=170; rows=(len(items)+cols-1)//cols
    out=Image.new("RGB",(cols*thumb,rows*thumb),(255,255,255)); d=ImageDraw.Draw(out)
    for i,(aid,im) in enumerate(items):
        x=(i%cols)*thumb; y=(i//cols)*thumb; q=im.convert("RGBA"); q.thumbnail((145,145),Image.Resampling.LANCZOS)
        out.paste(q.convert("RGB"),(x+(thumb-q.width)//2,y+8)); d.text((x+4,y+150),aid,fill=(20,20,20))
    out.save(ROOT/"batches"/name,quality=90)
    out.save(ROOT/"batches"/(Path(name).stem+".png"))
sheet(masters,"native_graphics.jpg")
sheet([("u04_cars_03",cars3),("u04_teddy_bears_04",teddies4),("u04_cars_07",seven)],"composed_crops.jpg",3)
sheet([("u04_igloo",igloo),("u04_jump_rope",Image.open(generated) if generated.exists() else card()),("u04_kangaroo",kangaroo),("u04_lion",lion)],"phonics_objects.jpg",4)
print("built", len(list((ROOT/"webp").glob("*.webp"))))
