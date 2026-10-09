from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
regions={37:(.04,.16,.98,.63),38:(.04,.64,.98,.92),39:(.02,.05,.97,.55),40:(.02,.54,.97,.83),41:(.02,.54,.97,.93),42:(.04,.01,.98,.78),43:(.04,.01,.98,.93),44:(.02,.06,.97,.7),45:(.02,.7,.97,.94),46:(.04,.02,.98,.78),47:(.04,.02,.98,.94),48:(.02,.06,.97,.66),49:(.02,.68,.97,.92),50:(.04,.05,.97,.29),51:(.04,.29,.97,.92),52:(.02,.05,.97,.4),53:(.02,.4,.97,.93)}
out=ROOT/'references'/'lesson-crops'
out.mkdir(exist_ok=True)
for p in m['items']:
 n=int(p['track'].split('_')[1])
 im=Image.open(ROOT/'source-pages'/('page-%02d.png'%p['unit_pdf_page']))
 box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(regions[n]))
 rel='references/lesson-crops/'+p['track']+'.png'
 im.crop(box).save(ROOT/rel)
 p['lesson_source_crop']={'path':rel,'box':box,'source':'source-pages/page-%02d.png'%p['unit_pdf_page']}
(ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved 17 source lesson-region references; these are not generated lesson assets.')

