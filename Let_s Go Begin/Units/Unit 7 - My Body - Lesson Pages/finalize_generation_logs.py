from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
B=ROOT/'assets/batches'
fixes={'batch2-fix1':('batch2-original.png','CD2_43 title and model sentence no longer overlap.'),'batch4-fix1':('batch4-original.png','Analog watch has each digit1-12 once.'),'batch4-fix2':('batch4-fix1.png','Lowercasev smaller than uppercaseV; all six search glyphs preserved.')}
for name,(ref,note) in fixes.items():
 p=B/(name+'.json');d=json.loads(p.read_text(encoding='utf-8'))
 d['refs']=['assets/batches/'+ref];d['status']='reviewed';d['visual_review']=note
 if name=='batch2-fix1':d['selected_asset']='assets/batches/batch2.png'
 elif name=='batch4-fix1':d['selected_asset']='assets/batches/batch4-fix1.png'
 else:d['selected_asset']='assets/batches/batch4.png'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for b in range(1,6):
 p=B/('batch%d.json'%b);d=json.loads(p.read_text(encoding='utf-8'))
 d['selected_asset']='assets/batches/batch%d.png'%b
 d['fix_logs']=[name+'.json' for name in fixes if name.startswith('batch'+str(b)+'-')]
 d['final_sha256']=hashlib.sha256((B/('batch%d.png'%b)).read_bytes()).hexdigest()
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('All generation and repair logs finalized; workspace provenance retained.')

