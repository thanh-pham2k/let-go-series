from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
B=ROOT/'assets/batches'
histories={1:['batch1-fix1'],2:['batch2-fix1','batch2-fix2'],3:['batch3-fix1','batch3-fix2','batch3-fix3','batch3-fix4','batch3-fix5'],4:['batch4-fix1','batch4-fix2']}
for n,history in histories.items():
    for i,name in enumerate(history):
        p=B/(name+'.json');j=json.loads(p.read_text(encoding='utf-8'))
        j['refs']=[str(B/(f'batch{n}-original.png' if i==0 else history[i-1]+'.png'))]+([str(ROOT/'assets/find-letters-source-detail.png')] if name=='batch4-fix2' else [])
        j['local_result']=f'assets/batches/{name}.png' if i<len(history)-1 else f'assets/batches/batch{n}.png'
        if i==len(history)-1:j['status']='reviewed_selected'
        elif name not in ['batch3-fix1','batch3-fix4']:j['status']='superseded'
        p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
    p=B/f'batch{n}.json';j=json.loads(p.read_text(encoding='utf-8'))
    j['original_local_result']=f'assets/batches/batch{n}-original.png'
    j['selected_local_result']=f'assets/batches/batch{n}.png'
    j['selected_result']=json.loads((B/(history[-1]+'.json')).read_text(encoding='utf-8'))['result']
    j['repair_logs']=history
    j['sha256']=hashlib.sha256((B/f'batch{n}.png').read_bytes()).hexdigest()
    p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for p in m['items']:
    if p['track']=='CD2_33':p['lesson_specs']['source_content']='1 Qq queen; 2 Rr rabbit; 3 Ss sun; 4 Tt tiger. C. Find the letters: queen purple robe with S/s-shaped trim, white rabbit/red cushion/ornate cream bench, sun, tiger, tree foliage subtle S/s curls. Preserve activity without answer key; ornamental positions redrawn.'
(ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
report=json.loads((ROOT/'validation.json').read_text(encoding='utf-8'))
report['preview_checks']='Node VM with DOM/event stubs: all 15 track/image/audio/question mappings, hidden until synthetic ended, feedback, navigation/reset. Not a real listening audit.'
report['generation_audit']={'tool':'built-in image_gen only','batches':4,'tracks_per_batch':[4,4,4,3],'repair_logs_retained':True,'prompt_files':'assets/batches/batch*.json'}
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for p in B.glob('*.json'):
    j=json.loads(p.read_text(encoding='utf-8'))
    assert isinstance(j['tracks'],list) and j['prompt'] and j['refs'] and j['tool']=='built-in image_gen'
    assert all(Path(ref).exists() for ref in j['refs']),(p,j['refs'])
    if 'local_result' in j:assert (ROOT/j['local_result']).exists()
print('All generation/repair jobs contain tracks/prompt/refs/tool; local inputs/results verified.')
