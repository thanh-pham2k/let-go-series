"""Render all lesson pages from manifest.json. Requires Pillow: python render.py."""
from pathlib import Path
import json
import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent

def save_image(image, path, **options):
    """Write atomically; tolerate brief Windows preview/indexer file locks."""
    temporary=path.with_name(path.stem+'.writing'+path.suffix)
    for attempt in range(10):
        try:
            image.save(temporary,**options)
            os.replace(temporary,path)
            return
        except OSError:
            if attempt==9:raise
            time.sleep(.2)

def font(size, bold=False):
    candidates = [
        Path(os.environ.get('WINDIR', 'C:/Windows'))/'Fonts'/('arialbd.ttf' if bold else 'arial.ttf'),
        Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)

def _render_native_page(page):
    canvas=Image.new('RGB',tuple(page['canvas']['size']),page['canvas']['background'])
    draw=ImageDraw.Draw(canvas)
    for layer in page['layers']:
        kind=layer['type']; box=layer['box'];x,y,w,h=box
        assert x>=0 and y>=0 and x+w<=canvas.width and y+h<=canvas.height,(page['track'],box)
        if kind=='image':
            with Image.open(ROOT/layer['asset']) as source:
                image=ImageOps.contain(source.convert('RGB'),(w,h),Image.Resampling.LANCZOS)
                canvas.paste(image,(x+(w-image.width)//2,y+(h-image.height)//2))
        elif kind=='rect':
            draw.rounded_rectangle((x,y,x+w-1,y+h-1),radius=layer.get('radius',0),fill=layer['fill'],outline=layer.get('stroke'),width=layer.get('stroke_width',1))
        elif kind=='text':
            f=font(layer['font_size'],layer.get('bold',False));value=layer['text'];spacing=layer.get('spacing',8)
            bounds=draw.multiline_textbbox((0,0),value,font=f,spacing=spacing)
            tw=bounds[2]-bounds[0];th=bounds[3]-bounds[1]
            assert tw<=w and th<=h,(page['track'],value,(tw,th),(w,h))
            tx=x+(w-tw)//2 if layer.get('align')=='center' else x
            draw.multiline_text((tx,y-bounds[1]),value,font=f,fill=layer.get('color','#25334A'),spacing=spacing,align=layer.get('align','left'))
        else:
            raise ValueError(kind)
    return canvas

def render_page(page):
    """Render editable native layers, then contain the entire page on its canvas."""
    native_size=page.get('native_layout_size',page['canvas']['size'])
    native_page={**page,'canvas':{**page['canvas'],'size':native_size}}
    native=_render_native_page(native_page)
    target_size=tuple(page['canvas']['size'])
    if native.size==target_size:return native
    fitted=ImageOps.contain(native,target_size,Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',target_size,page['canvas']['background'])
    canvas.paste(fitted,((canvas.width-fitted.width)//2,(canvas.height-fitted.height)//2))
    return canvas

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    for folder in ['pages/png','pages/webp']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
    for page in manifest['items']:
        im=render_page(page)
        save_image(im,ROOT/page['output']['png'])
        save_image(im,ROOT/page['output']['webp'],quality=88,method=6)
        print(page['track'],im.size)
    thumbs=Image.new('RGB',(1200,((len(manifest['items'])+3)//4)*360),'#EDF2F7')
    draw=ImageDraw.Draw(thumbs)
    for i,page in enumerate(manifest['items']):
        im=ImageOps.contain(Image.open(ROOT/page['output']['webp']),(280,300),Image.Resampling.LANCZOS)
        x=(i%4)*300+(300-im.width)//2;y=(i//4)*360+30
        thumbs.paste(im,(x,y));draw.text(((i%4)*300+12,(i//4)*360+8),page['track'],font=font(18,True),fill='#25334A')
    save_image(thumbs,ROOT/'preview.jpg',quality=92)

if __name__=='__main__':main()
