from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,argparse
ROOT=Path(__file__).resolve().parent
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),n)
def save(name,d):(ROOT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def render(p):
 im=Image.new('RGB',tuple(p['canvas']['size']),p['canvas']['background'])
 draw=ImageDraw.Draw(im)
 for layer in p['layers']:
  x,y,w,h=layer['box']
  assert x>=0 and y>=0 and x+w<=1200 and y+h<=1200
  if layer['type']=='image':
   pic=ImageOps.contain(Image.open(ROOT/layer['asset']).convert('RGB'),(w,h),Image.Resampling.LANCZOS)
   im.paste(pic,(x+(w-pic.width)//2,y+(h-pic.height)//2))
  elif layer['type']=='rect':draw.rectangle([x,y,x+w-1,y+h-1],fill=layer['fill'])
  elif layer['type']=='text':
   f=font(layer['font_size'],layer.get('bold',False));value=layer['text'];bounds=draw.multiline_textbbox((0,0),value,font=f,spacing=layer.get('spacing',6))
   tw=bounds[2]-bounds[0];th=bounds[3]-bounds[1]
   assert tw<=w and th<=h,(p['track'],value,bounds,layer['box'])
   tx=x+(w-tw)//2 if layer.get('align')=='center' else x
   draw.multiline_text((tx,y-bounds[1]),value,font=f,fill=layer.get('color','#25334A'),spacing=layer.get('spacing',6),align=layer.get('align','left'))
  else:raise ValueError(layer['type'])
 return im
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--split-x',type=int);ap.add_argument('--split-y',type=int);ap.add_argument('--sheet',default='assets/batches/batch1.png');ap.add_argument('--approve',action='store_true')
 args=ap.parse_args();m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
 if args.split_x is not None:
  assert args.split_y is not None
  sheet=Image.open(ROOT/args.sheet).convert('RGB');w,h=sheet.size;x,y=args.split_x,args.split_y
  assert 0<x<w and 0<y<h
  boxes=[(1,1,x-1,y-1),(x+1,1,w-1,y-1),(1,y+1,x-1,h-1)]
  for p,box in zip(m['items'],boxes):
   rel='assets/'+p['track']+'-lesson.png';sheet.crop(box).save(ROOT/rel)
   p['layers']=[{'type':'image','asset':rel,'box':[0,0,1200,1200]}]
   p['generation_batch']='batch1';p['source_crop_box']=list(box);p['status']='generated_needs_review'
  m['batch_split']={'sheet':args.sheet,'size':[w,h],'split':[x,y],'boxes':[list(b) for b in boxes]}
 if args.approve:
  reviews=json.loads((ROOT/'visual-review.json').read_text(encoding='utf-8'))
  assert reviews['result']=='pass' and reviews['source_pages_viewed']==2
  for p in m['items']:
   r=reviews['pages'][p['track']];assert r['result']=='pass' and r['final_png_viewed'] is True
   p['visual_review']=r['notes'];p['status']='reviewed'
 save('manifest.json',m)
 thumb=Image.new('RGB',(1200,420),'#EDF2F7');draw=ImageDraw.Draw(thumb)
 for i,p in enumerate(m['items']):
  assert p['layers']
  im=render(p);im.save(ROOT/p['output']['png']);im.save(ROOT/p['output']['webp'],quality=92,method=6)
  t=ImageOps.contain(im,(390,390),Image.Resampling.LANCZOS);thumb.paste(t,(i*400+5,28));draw.text((i*400+12,5),p['track'],font=font(19,True),fill='#25334A')
 thumb.save(ROOT/'preview.jpg',quality=94)
 print('Rendered3 separate PNG/WebP canvases1200x1200; status:',[p['status'] for p in m['items']])
if __name__=='__main__':main()

