"""Inspect on-disk Challenge deliverables; never substitute technical checks for visual QA."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,re
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
INVROOT=ROOT/'parallel-prompts/challenge-images'
ARTIFACTS=['manifest.json','question-image-map.json','preview.html','contact-sheet.jpg','validation.json','README.md']

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))

def walk(node):
    if isinstance(node,dict):
        yield node
        for value in node.values():yield from walk(value)
    elif isinstance(node,list):
        for value in node:yield from walk(value)

def main():
    rows=[];all_hashes=defaultdict(list)
    qa_path=ROOT/'audit/challenge-visual-review.json';rootqa=read(qa_path).get('cards',{}) if qa_path.exists() else {}
    for ip in sorted(INVROOT.glob('*.inventory.json')):
        inv=read(ip);folder=Path(inv['lesson_folder'])/'challenge-assets'
        mandatory={a['id'] for a in inv['assets'] if a.get('method')!='conditional'}
        conditional={a['id'] for a in inv['assets'] if a.get('method')=='conditional'}
        row={'set':ip.stem.replace('.inventory',''),'required':len(mandatory),'conditional':sorted(conditional),
             'missing_artifacts':[f for f in ARTIFACTS if not (folder/f).is_file()],
             'missing_ids':[],'extra_ids':[],'bad_dimensions':[],'bad_links':[],'unreviewed':[],
             'over_60kb':[],'methods':{},'unresolved_context':[],'context_items':[],'root_visual_failed':[],'root_visual_pending':[],'orphan_webps':[],'preview':str(folder/'preview.html')}
        entries=[]
        if (folder/'manifest.json').is_file():
            m=read(folder/'manifest.json');entries=m.get('assets',m.get('items',[]))
        idcounts=Counter(a.get('id') for a in entries);actual=set(idcounts)
        row['duplicate_ids']=[aid for aid,n in idcounts.items() if n>1]
        row['missing_ids']=sorted(mandatory-actual);row['extra_ids']=sorted(actual-mandatory-conditional)
        sizes=[];hashes=defaultdict(list);success=[]
        for a in entries:
            aid=a.get('id');rel=a.get('file',a.get('webp',a.get('output',{}).get('webp')))
            if not rel:rel=f'webp/{aid}.webp'
            p=folder/rel
            if not p.is_file():row['bad_links'].append(rel);continue
            try:
                with Image.open(p) as im:
                    if im.format!='WEBP' or im.size!=(512,512):row['bad_dimensions'].append({'id':aid,'format':im.format,'size':im.size})
                    im.load()
            except Exception as e:row['bad_dimensions'].append({'id':aid,'error':str(e)})
            size=p.stat().st_size;sizes.append(size)
            if size>61440:row['over_60kb'].append({'id':aid,'bytes':size})
            h=hashlib.sha256(p.read_bytes()).hexdigest();hashes[h].append(aid);all_hashes[h].append(aid)
            qa=rootqa.get(aid,{})
            if qa.get('sha256')!=h or qa.get('status')=='pending' or not qa:row['root_visual_pending'].append(aid)
            elif qa.get('status')!='pass':row['root_visual_failed'].append({'id':aid,'notes':qa.get('notes')})
            if not a.get('visual_review'):row['unreviewed'].append(aid)
            success.append(aid)
        row['complete_files']=len(mandatory&set(success));row['within_set_duplicate_hashes']=[v for v in hashes.values() if len(v)>1]
        row['orphan_webps']=sorted(p.name for p in (folder/'webp').glob('*.webp') if p.stem not in actual)
        def category(a):
            method=str(a.get('creation_method',a.get('creation',a.get('method','unspecified')))).lower()
            if 'native' in method:return 'native'
            if 'compose' in method:
                if a.get('semantic',{}).get('count')==1 and not a.get('clean_master_reference','').endswith('_generated_master.png'):return 'crop'
                return 'compose'
            if 'gen' in method:return 'AI generate/edit'
            if 'crop' in method:return 'crop'
            return method
        row['methods']=dict(Counter(category(a) for a in entries))
        row['total_bytes']=sum(sizes);row['max_bytes']=max(sizes,default=0)
        if (folder/'question-image-map.json').is_file():
            mapping=read(folder/'question-image-map.json');nodes=list(walk(mapping))
            for node in nodes:
                for key in ['asset_ids','image_ids']:
                    if key in node and isinstance(node[key],list):
                        row['bad_links'].extend('unknown ID '+aid for aid in node[key] if aid not in actual)
                if node.get('needs_context') and not isinstance(node.get('items'),list):
                    source_lines=Path(inv['source']).read_text(encoding='utf-8-sig').splitlines()
                    if node.get('line') or node.get('source_line'):
                        ln=node.get('line',node.get('source_line'))
                        if not source_lines[ln-1].startswith('#'):
                            row['context_items'].append({'id':node.get('question_id',node.get('item',node.get('id',f'line-{ln}'))),'line':ln,'source':source_lines[ln-1],'reason':node.get('reason',node.get('note','Source target cue is not specified.'))})
                    elif node.get('source_lines'):
                        for ln in node['source_lines']:
                            if inv.get('unit')==8 and 'Make a' not in source_lines[ln-1]:continue
                            row['context_items'].append({'id':node.get('id','conditional-command')+f'-{ln}','line':ln,'source':source_lines[ln-1],'reason':node.get('decision','Source does not establish a fixed order.')})
            row['context_items']=list({(c['line'],c['source']):c for c in row['context_items']}.values())
            row['unresolved_context']=[c['id'] for c in row['context_items']]
            row['source_sha256']=hashlib.sha256(Path(inv['source']).read_bytes()).hexdigest()
            if 'questions' in inv:
                sourceids={q['question_id'] for q in inv['questions']}
                mappedids={n.get('question_id',n.get('id')) for n in nodes}
                row['missing_question_ids']=sorted(sourceids-mappedids)
            else:row['missing_question_ids']=[]
        else:row['missing_question_ids']=[]
        if (folder/'preview.html').is_file():
            html=(folder/'preview.html').read_text(encoding='utf-8')
            for link in re.findall(r'(?:src|href)=["\']([^"\']+)["\']',html):
                if link.startswith(('http:','https:','data:','#')):continue
                if not (folder/link.split('#')[0]).is_file():row['bad_links'].append('preview '+link)
        blocking=['missing_artifacts','missing_ids','extra_ids','duplicate_ids','bad_dimensions','bad_links','unreviewed','missing_question_ids','within_set_duplicate_hashes','root_visual_failed','root_visual_pending','orphan_webps']
        row['technical_candidate_complete']=not any(row[k] for k in blocking)
        row['fixed_answer_exercises_ready']=row['technical_candidate_complete'] and not row['context_items']
        rows.append(row)
    result={'scope':'8 Units and 4 Reviews; Challenge 1–5','required_total':sum(r['required'] for r in rows),
      'complete_files':sum(r['complete_files'] for r in rows),'conditional_total':sum(len(r['conditional']) for r in rows),
      'sets':rows,'cross_set_identical_files':[v for v in all_hashes.values() if len(v)>1],
      'context_items_total':sum(len(r['context_items']) for r in rows),
      'image_bundle_complete':all(r['technical_candidate_complete'] for r in rows),
      'note':'Goal requirement 8 explicitly permits source-unknown targets to be delivered as needs_context=true with a report instead of guessed answers. Image-bundle completion does not claim those fixed-answer exercises are ready.'}
    (ROOT/'audit/challenge-images-completion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Challenge image completion audit','',f"Scope: 8 Units + 4 Reviews. Files verified: {result['complete_files']}/{result['required_total']} mandatory IDs; {result['conditional_total']} conditional IDs also prepared.",'',
      '| Set | WebP / required | Creation methods | Max KB | Technical candidate | Preview |','|---|---:|---|---:|---|---|']
    for r in rows:
        methods=', '.join(f'{k}: {v}' for k,v in r['methods'].items()) or 'pending'
        lines.append(f"| {r['set']} | {r['complete_files']}/{r['required']} | {methods} | {r['max_bytes']/1024:.1f} | {'images passed; context exceptions below' if r['technical_candidate_complete'] and r['context_items'] else 'passed' if r['technical_candidate_complete'] else 'in progress'} | [preview](<{r['preview']}>) |")
    lines+=['','## Remaining evidence and issues','']
    for r in rows:
        issues={k:r[k] for k in ['missing_artifacts','missing_ids','extra_ids','duplicate_ids','bad_dimensions','bad_links','unreviewed','missing_question_ids','within_set_duplicate_hashes','root_visual_failed','root_visual_pending','over_60kb','orphan_webps'] if r[k]}
        if issues:lines.append(f'- {r["set"]}: '+json.dumps(issues,ensure_ascii=False))
    lines+=['','## Source context exceptions required by goal item 8','', 'No missing pictures are concealed here. Unknown fixed targets remain needs_context=true instead of invented answer keys; personal ages/preferences/abilities remain valid open responses.']
    for r in rows:
        for c in r['context_items']:lines.append(f'- {r["set"]}, {c["id"]}, source line {c["line"]}: `{c["source"]}` — {c["reason"]}')
    lines+=['','No lesson/source/audio modification is authorized; no commit/push. Individual visual review, source fidelity, preview behavior and context checks remain separate from file/dimension checks.','',
      'Original batch/crop masters and provenance are kept within each challenge-assets folder. See each manifest/validation for adaptation notes and actual review evidence.']
    (ROOT/'audit/challenge-images-completion.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'required':result['required_total'],'complete_files':result['complete_files'],'candidate_sets':[r['set'] for r in rows if r['technical_candidate_complete']]},ensure_ascii=False))

if __name__=='__main__':main()
