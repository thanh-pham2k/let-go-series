"""Prepare single-call eight-cell sheets; install generated sheets as WebP tiles."""
from pathlib import Path
from PIL import Image, ImageOps
import json, shutil, argparse, hashlib, zipfile

ROOT=Path(__file__).resolve().parent
UNITS=ROOT/'Let_s Go 1/Units'
OUT=ROOT/'output/imagegen/book1-all-batches'
PLAN=OUT/'plan.json'

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((UNITS/'Audio Pages/manifest.json').read_text(encoding='utf-8'))
    jobs=[]
    for sec in manifest['sections']:
        rows=[r for r in manifest['tracks'] if r['section']==sec['name'] and r['id'] not in [f'CD1_{t:02}' for t in range(2,10)]]
        for start in range(0,len(rows),8):
            batch=rows[start:start+8];jobid=f'batch-{len(jobs)+1:02}'
            folder=OUT/jobid;folder.mkdir(exist_ok=True)
            sheet=Image.new('RGB',(2048,1024),'white')
            for i,row in enumerate(batch):
                with Image.open(UNITS/row['image']) as im:
                    tile=ImageOps.contain(im.convert('RGB'),(488,488),Image.Resampling.LANCZOS)
                sheet.paste(tile,(i%4*512+(512-tile.width)//2,i//4*512+(512-tile.height)//2))
            source=folder/'input.png';sheet.save(source)
            order='; '.join(f'cell {i+1}: {r["id"]}, {r["activity"]}' for i,r in enumerate(batch))
            prompt=f'''Edit target: attached sheet of {len(batch)} textbook activity images. Regenerate the ENTIRE sheet in ONE image. Exact 4-column by 2-row grid of equal square cells; 2:1 canvas, preferably 2048x1024. Final tiles will be cropped at quarter-width and half-height, so preserve all cell positions precisely. Reading order: {order}. Cells {len(batch)+1} through 8, if any, must remain pure blank white. Restore clean readable textbook artwork and legible original English text; remove only scan noise and bleed-through. Preserve all original instructional content, exact words, punctuation, numbers, audio/CD/track badges, headings, labels, object counts, character identities, poses and spatial relations. Do not invent, translate, summarize, omit or rewrite text. Preserve duplicate images if present. Pay special attention to every numbered action/vocabulary label and every digit in track badges. Keep original textbook style and composition; do not invent scenes for narrow sentence strips. White background, small inset in each cell, all content fully inside its own cell. No visible grid lines, new captions, page titles, or crop marks. This is faithful restoration, not a new lesson. The source is authoritative for every word and picture.'''
            (folder/'prompt.txt').write_text(prompt,encoding='utf-8')
            jobs.append(dict(id=jobid,section=sec['name'],input=str(source),prompt=prompt,rows=batch))
    PLAN.write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps([dict(id=j['id'],section=j['section'],tracks=[r['id'] for r in j['rows']],input=j['input']) for j in jobs],ensure_ascii=False))

def install(jobid,source):
    job=next(j for j in json.loads(PLAN.read_text(encoding='utf-8')) if j['id']==jobid)
    folder=OUT/jobid;target=folder/'generated.png'
    if Path(source).resolve()!=target.resolve():shutil.copy2(source,target)
    im=Image.open(target).convert('RGB');w,h=im.size
    if abs(w/h-2)>.08:raise ValueError(f'Unexpected grid aspect ratio: {im.size}')
    layout_path=folder/'layout.json'
    layout=json.loads(layout_path.read_text(encoding='utf-8')) if layout_path.exists() else {}
    xcuts=layout.get('x_cuts',[0,.25,.5,.75,1]);ycuts=layout.get('y_cuts',[0,.5,1])
    results=[]
    for i,row in enumerate(job['rows']):
        x,y=i%4,i//4
        box=layout.get('rects',{}).get(str(i+1),[xcuts[x],ycuts[y],xcuts[x+1],ycuts[y+1]])
        crop=im.crop(tuple(round(v*(w if k%2==0 else h)) for k,v in enumerate(box)))
        content=ImageOps.contain(crop,(512,512),Image.Resampling.LANCZOS)
        tile=Image.new('RGB',(512,512),'white');tile.paste(content,((512-content.width)//2,(512-content.height)//2))
        dest=UNITS/(row['section']+' - Audio Pages')/'regenerated'/f'{row["id"]}.webp'
        dest.parent.mkdir(exist_ok=True);tile.save(dest,'WEBP',quality=85,method=6)
        with Image.open(dest) as check:assert check.size==(512,512) and check.format=='WEBP'
        results.append(dict(id=row['id'],image=str(dest.relative_to(UNITS)).replace('\\','/'),bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
    (folder/'result.json').write_text(json.dumps(dict(job=jobid,generated=str(target),tracks=results),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{jobid}: installed {len(results)} tiles, {sum(r["bytes"] for r in results)} bytes')

def sample():
    folder=UNITS/'Unit 1 - Things for School - Audio Pages/regenerated'
    folder.mkdir(exist_ok=True)
    for t in range(2,10):
        shutil.copy2(ROOT/f'output/imagegen/book1-batch8-sample/CD1_{t:02}-sample.webp',folder/f'CD1_{t:02}.webp')
    print('Applied eight accepted sample WebPs')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','install','sample']);parser.add_argument('--job');parser.add_argument('--source');args=parser.parse_args()
    if args.command=='prepare':prepare()
    elif args.command=='sample':sample()
    else:install(args.job,args.source)
