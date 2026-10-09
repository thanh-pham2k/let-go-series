from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
B=ROOT/'assets/batches'
p=B/'batch1.json';d=json.loads(p.read_text(encoding='utf-8'))
d.update({'status':'reviewed','selected_asset':'assets/batches/batch1.png','initial_asset':'assets/batches/batch1-original.png','repair_logs':['assets/batches/batch1-fix1.json','assets/batches/batch1-fix2.json'],'final_sha256':hashlib.sha256((B/'batch1.png').read_bytes()).hexdigest(),'sheet_size':[1086,1448],'observed_split':[552,881],'visual_review':'All3 final pages compared with bothPDF sourcepages and contact sheet; see visual-review.json. Unequal row sizes detected, split uses real boundary not midpoint.'})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=B/'batch1-fix1.json';d=json.loads(p.read_text(encoding='utf-8'));d['status']='rejected_superseded';d['visual_review']='8 visible but misplaced in first data row; not accepted. Input for second repair retained.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=B/'batch1-fix2.json';d=json.loads(p.read_text(encoding='utf-8'));d['status']='reviewed';d['visual_review']='All1-14 visible exactlyonce in correct2 rows;8 below row separator, child reduced; top two cells remain faithful to source.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=ROOT/'generation.json';d=json.loads(p.read_text(encoding='utf-8'));d.update({'status':'visually_reviewed','batches':['assets/batches/batch1.json'],'repairs':['assets/batches/batch1-fix1.json','assets/batches/batch1-fix2.json'],'selected_sheet':'assets/batches/batch1.png','sheet_size':[1086,1448],'split':[552,881],'font_overlays_used':False,'fallback_used':False});p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Generation provenance finalized:1 built-in batch,2 built-in repairs, correct final crop boundaries.')

