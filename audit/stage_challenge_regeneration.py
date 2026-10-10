import argparse,json,shutil
from pathlib import Path
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('batch',type=int);p.add_argument('master');p.add_argument('--boxes',required=True);args=p.parse_args()
b=json.loads((ROOT/'parallel-prompts/challenge-images/regenerate-12/batch-index.json').read_text(encoding='utf-8'))['batches'][args.batch-1]
out=ROOT/'audit/challenge-regeneration-staging'/f'batch-{args.batch:02}'
out.mkdir(parents=True,exist_ok=True);(out/'webp').mkdir(exist_ok=True)
shutil.copy2(args.master,out/'master.png')
im=Image.open(out/'master.png').convert('RGB');boxes=json.loads(args.boxes)
assert len(boxes)==len(b['cards'])
items=[]
for a,box in zip(b['cards'],boxes):
    crop=im.crop(box);card=Image.new('RGB',(512,512),'white');fit=ImageOps.contain(crop,(512,512),Image.Resampling.LANCZOS);card.paste(fit,((512-fit.width)//2,(512-fit.height)//2))
    target=out/'webp'/f"{a['id']}.webp"
    for q in [80,75,70]:
        card.save(target,'WEBP',quality=q,method=6)
        if target.stat().st_size<=61440:break
    items.append(dict(id=a['id'],crop_box=box,original_cell_size=crop.size,export_size=[512,512],quality=q,method=6,bytes=target.stat().st_size,visual_review='pending',output=a['output']))
(out/'export.json').write_text(json.dumps(dict(batch=args.batch,master_size=im.size,assets=items,status='staged_pending_visual_review'),ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1024,768),'white')
for i,a in enumerate(items):
    sheet.paste(Image.open(out/'webp'/f"{a['id']}.webp").resize((256,256)),(i%4*256,i//4*256))
sheet.save(out/'export-contact-sheet.jpg',quality=92)
print(json.dumps(dict(batch=args.batch,staged=len(items),master_size=im.size,max_bytes=max(a['bytes'] for a in items))))
