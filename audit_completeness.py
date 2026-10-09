from pathlib import Path
from urllib.parse import unquote
from collections import Counter
import json,re,hashlib,zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parent
UNITS=ROOT/'Let_s Go Begin/Units'
source=json.loads((UNITS.parent/'lets_go_audio_mapping.metadata').read_text(encoding='utf-8'))
expected=source['audio_mappings']
results=[];all_tracks=[];broken=[]
for folder in sorted(UNITS.glob('* - Lesson Pages')):
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    meta_path=next(folder.glob('*.regenerated.metadata'))
    metadata=json.loads(meta_path.read_text(encoding='utf-8'))
    items=manifest['items'];metas={p['track']:p for p in metadata['items']}
    prefix=folder.name.split(' - Lesson Pages')[0]
    src_pdf=prefix+'.pdf'
    expected_tracks=[f"{p['audio']['disc']}_{p['audio']['track']:02}" for p in expected if p['source_pdf']==src_pdf]
    issues=[];sizes=set();audio_ok=0;questions=0;stale=[];assets=0
    tracks=[p['track'] for p in items];all_tracks+=tracks
    if set(tracks)!=set(expected_tracks):issues.append('Track set differs from master mapping')
    if len(tracks)!=len(set(tracks)):issues.append('Duplicate track in manifest')
    if set(metas)!=set(tracks):issues.append('Metadata track set differs from manifest')
    validation=json.loads((folder/'validation.json').read_text(encoding='utf-8')) if (folder/'validation.json').exists() else {}
    checks={p['track']:p for p in validation.get('checks',[])}
    for p in items:
        track=p['track'];q=p.get('question',{});meta=metas.get(track,{})
        if meta.get('image')!=p['output']['webp'] or meta.get('audio_file')!=p['audio_file']:issues.append(track+': metadata path mismatch')
        if q!=meta.get('question'):issues.append(track+': metadata question mismatch')
        choices=q.get('choices',[])
        if not q.get('prompt') or len(choices)<2 or q.get('correct_choice_id') not in [c['id'] for c in choices]:issues.append(track+': invalid question')
        else:questions+=1
        if not q.get('show_after_audio') or q.get('render_in_lesson_image'):issues.append(track+': wrong quiz display policy')
        for fmt in ['png','webp']:
            path=folder/p['output'][fmt]
            if not path.exists():issues.append(track+': missing '+fmt);continue
            with Image.open(path) as im:
                im.load();sizes.add(im.size)
                if list(im.size)!=p['canvas']['size']:issues.append(track+': canvas size mismatch')
                if 'size' in meta and list(im.size)!=meta['size']:issues.append(track+': metadata size mismatch')
            hash_field=fmt+'_sha256'
            if checks.get(track,{}).get(hash_field) and checks[track][hash_field]!=hashlib.sha256(path.read_bytes()).hexdigest():stale.append(track+' '+fmt)
        audio=folder/p['audio_file']
        cd=track.split('_')[0]
        original=UNITS.parent/f'Oxford - Let_s Go Begin Student_s Book 3rd Edition {cd}'/audio.name
        if audio.exists() and original.exists() and audio.read_bytes()==original.read_bytes():audio_ok+=1
        else:issues.append(track+': audio missing or differs from source')
        for layer in p.get('layers',[]):
            if layer.get('type')=='image':
                if not (folder/layer['asset']).exists():issues.append(track+': missing render asset '+layer['asset'])
                else:assets+=1
        if not (folder/p['source_reference']).exists():issues.append(track+': missing reference')
    png_count=len(list((folder/'pages/png').glob('*.png')))
    webp_count=len(list((folder/'pages/webp').glob('*.webp')))
    if png_count!=len(items) or webp_count!=len(items):issues.append('Unexpected PNG/WebP file count')
    for name in ['preview.html','preview.jpg','README.md','questions.md']:
        if not (folder/name).exists():issues.append('Missing '+name)
    preview=(folder/'preview.html').read_text(encoding='utf-8')
    match=re.search(r'const\s+manifest\s*=\s*',preview)
    preview_check='not parsed'
    if match:
        try:
            embedded,_=json.JSONDecoder().raw_decode(preview[match.end():])
            fields=['track','exercise','output','audio_file','book_page','question','canvas']
            embedded_items=embedded.get('items',[])
            if len(embedded_items)!=len(items) or any(any(p.get(k)!=a.get(k) for k in fields) for p,a in zip(items,embedded_items)):
                issues.append('Preview lesson data differs from current manifest')
            else:preview_check='current lesson data matches; audit-note-only differences ignored'
        except Exception as e:issues.append('Preview embedded data parse error: '+str(e))
    if prefix.startswith('Unit '):
        unit=manifest['unit'];zip_path=UNITS/f"Unit_{unit}_{prefix.split(' - ',1)[1].replace(' ','_')}_regenerated.zip"
        docs=list(UNITS.glob(f'Unit {unit} - *(*).md'));question_doc=UNITS/(prefix+' - Cau hoi theo trang.md')
    else:
        pair=manifest['review'];zip_path=UNITS/f'Review_{pair}_regenerated.zip'
        docs=list(UNITS.glob(f'Review {pair}(*).md'));question_doc=UNITS/(prefix+' - Cau hoi theo trang.md')
    if not question_doc.exists():issues.append('Missing external question document')
    if len(docs)!=1:issues.append('External exercise document count differs from1')
    chapter_titles=[];audio_note=False
    if docs:
        doc_text=docs[0].read_text(encoding='utf-8-sig')
        chapter_titles=re.findall(r'^# Challenge [1-5]\s*[—-]\s*(.+)$',doc_text,re.M)
        audio_note=bool(re.search(r'(?i)audio.*(?:bổ sung|cần)',doc_text))
        if len(chapter_titles)!=5:issues.append('Exercise document does not have exactly5 Challenges')
        if not audio_note:issues.append('No additional audio notes in exercise document')
    zip_ok=False;zip_stale=[]
    if zip_path.exists():
        with zipfile.ZipFile(zip_path) as z:
            zip_ok=z.testzip() is None
            for p in items:
                for rel in [p['output']['png'],p['output']['webp'],p['audio_file']]:
                    if rel not in z.namelist():zip_stale.append(rel+' missing')
                    elif z.read(rel)!=(folder/rel).read_bytes():zip_stale.append(rel+' differs')
            for rel in [meta_path.name,'preview.html','questions.md','manifest.json']:
                if rel not in z.namelist() or z.read(rel)!=(folder/rel).read_bytes():zip_stale.append(rel+' differs or missing')
    else:issues.append('Missing ZIP '+zip_path.name)
    if not zip_ok:issues.append('ZIP missing or invalid')
    if zip_stale:issues.append('ZIP stale: '+', '.join(zip_stale))
    if stale:issues.append('Validation hashes stale: '+', '.join(stale))
    results.append({'package':prefix,'expected_tracks':len(expected_tracks),'tracks':len(items),'png':png_count,'webp':webp_count,'audio_verified':audio_ok,'questions':questions,'sizes':[list(s) for s in sorted(sizes)],'status_reviewed':sum(p.get('status')=='reviewed' for p in items),'visual_review_notes':sum(bool(p.get('visual_review')) for p in items),'validation_result':validation.get('result'),'five_challenges':len(chapter_titles)==5,'challenge_titles':chapter_titles,'audio_notes':audio_note,'preview':preview_check,'zip_ok':zip_ok,'issues':issues})

for file in [*UNITS.glob('*.md'),*UNITS.glob('* - Lesson Pages/README.md'),*UNITS.glob('* - Lesson Pages/questions.md'),*UNITS.glob('* - Lesson Pages/challenge-guide.md')]:
    for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8-sig')):
        target=unquote(target)
        if target.startswith(('http:','https:','#','mailto:')):continue
        target=target.split('#',1)[0]
        if target and not (file.parent/target).exists():broken.append({'document':str(file.relative_to(ROOT)),'target':target})
expected_all=[f"{p['audio']['disc']}_{p['audio']['track']:02}" for p in expected]
report={'packages':results,'total_tracks':len(all_tracks),'expected_total':len(expected_all),'missing_tracks':sorted(set(expected_all)-set(all_tracks)),'duplicate_tracks':[t for t,c in Counter(all_tracks).items() if c>1],'broken_links':broken,'limits':['Speech in MP3 not independently transcribed','Existing visual-review notes and hash checks do not replace a fresh full source-by-source visual audit']}
out=ROOT/'audit';out.mkdir(exist_ok=True)
(out/'completeness.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
