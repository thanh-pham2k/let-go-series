"""Consistent learner-safe gallery and source-backed sample questions for all 12 sets."""
from pathlib import Path
import json,re,html,shutil

ROOT=Path(__file__).resolve().parents[1]
MARKERS=set('⬛⬜🍎🐦🐱🐶🖼🚗🟥🟦🟧🟨🟩🟪🟫🩷▭◆❤⬭⭐⭕🐟💜🔺🟡🥚🦍□△○◎●☆♡🛖🦁🦘🧸🪢🌙🍑🐄🐇🐙🦆🪺☀🍕🍗🍚🍞🍦🎂🐅👸🥛⌚☂🎻👀👂👃👄👤🙌🦵🦶🧍⚽🎤🎵🏀🏃🏊💃😉😊🚲🦊🦓🧶🪁✓✗')
def clean(s):
    s=re.sub(r'\*?\([^)]*\)\*?','',s)
    s=''.join(c for c in s if c not in MARKERS and c!='\ufe0f')
    return re.sub(r'^[\s|]*\d+[.)]\s*','',s).strip(' *|')

def nearest(lines,line):
    c=0;section='';item=''
    for s in lines[:line]:
        m=re.match(r'# Challenge (\d)',s)
        if m:c=int(m[1]);section='';item=''
        if re.match(r'#{2,3} \d+\. ',s):section=s.lstrip('# ');item=''
        if re.match(r'### \d+\.\d+',s):item=s[4:]
    return c,section,item

def extract(lines,ln,raw,challenge):
    i=ln-1;start=i
    while start>0 and not lines[start].startswith('### '):
        if lines[start-1].startswith(('## ','# ')):break
        start-=1
    end=i+1
    while end<len(lines) and not lines[end].startswith(('### ','## ','# ')):
        if re.match(r'^\d+[.] ',lines[end]) and end>i+1:break
        if any(m in lines[end] for m in MARKERS) and not re.match(r'^\s*- \[ \]',lines[end]) and not lines[end].startswith(('Nghe','**Nghe')) and end>i+1:break
        if re.search(r'Nghe|Người lớn đọc',lines[end]) and end>i+1:break
        end+=1
    block='\n'.join(lines[start:end]);opts=re.findall(r'^\s*- \[ \] (.+)$',block,re.M)
    if not opts:
        hits=re.findall(r'`([^`]+/[^`]+)`',raw)
        if hits:opts=[v.strip() for v in hits[-1].split('/')]
    teacher=''
    if challenge==2:
        heard=[s.strip() for s in lines[max(0,i-10):i+1] if re.search(r'Nghe(?: từ| câu|:)|Người lớn đọc',s)]
        heard.extend(s.strip() for s in block.splitlines() if re.search(r'Nghe:|Người lớn đọc',s))
        teacher=heard[-1] if heard else 'Người lớn chọn một nội dung hợp lệ trong bài nguồn để đọc; audio Challenge sẽ bổ sung sau.'
    prompt=''
    if 'Điền:' in raw:prompt='Nhìn hình. Điền: '+clean(raw.split('Điền:',1)[1])
    elif raw.strip().startswith('|'):
        cols=raw.strip('| ').split('|');prompt=clean(cols[0].split('🖼',1)[0])
        # Response table: show the full answer pool, not only the same row's answer.
        sec_start=i
        while sec_start>0 and not lines[sec_start].startswith('## '):sec_start-=1
        sec_end=i+1
        while sec_end<len(lines) and not lines[sec_end].startswith(('## ','# ')):sec_end+=1
        pool=[]
        for s in lines[sec_start:sec_end]:
            cs=s.strip('| ').split('|')
            if s.startswith('|') and len(cs)>1 and re.match(r'\s*\d+[.]',cs[0]):pool.append(cs[1].strip())
        if pool:opts=pool
    elif '🖼' in raw:
        prefix=raw.split('🖼',1)[0]
        if '_' in prefix or '?' in prefix:prompt=clean(prefix)
    elif '_' in raw and not raw.startswith(('Người lớn','Che nhãn')):prompt=clean(raw)
    if not prompt:
        if challenge==2:prompt='Nghe audio hoặc người lớn đọc, rồi chọn hình/câu trả lời phù hợp.'
        elif challenge==3:prompt='Nhìn hình. Điền hoặc nói câu trả lời của em.'
        elif challenge==4:prompt='Nhìn hình. Ghép với từ hoặc câu phù hợp.'
        elif challenge==5:prompt='Nhìn hình. Tự nói từ hoặc một câu phù hợp.'
        else:prompt='Nhìn hình và chọn từ/cụm từ đúng.'
    if challenge==2 and 'Nghe:' in prompt:prompt='Nghe audio hoặc người lớn đọc, rồi chọn đáp án phù hợp.'
    if prompt.startswith('→'):prompt='Nhìn hình. Nói hoặc điền câu trả lời: '+prompt
    if challenge==4 and not opts:
        sec_start=i
        while sec_start>0 and not lines[sec_start].startswith('## '):sec_start-=1
        shared=[s.split('**Các thẻ từ:**',1)[1].strip() for s in lines[sec_start:i+1] if '**Các thẻ từ:**' in s]
        if shared:opts=[v.strip() for v in shared[-1].split('·')]
    return prompt,opts,teacher

def main():
    report=[]
    for ip in sorted((ROOT/'parallel-prompts/challenge-images').glob('*.inventory.json')):
        inv=json.loads(ip.read_text(encoding='utf-8'));folder=Path(inv['lesson_folder'])/'challenge-assets';manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));mapping=json.loads((folder/'question-image-map.json').read_text(encoding='utf-8'));lines=Path(inv['source']).read_text(encoding='utf-8-sig').splitlines()
        title=('Unit '+str(inv['unit'])+' — '+inv['topic']) if 'unit' in inv else 'Review '+inv['review']
        candidates=[]
        if 'questions' in inv:
            # Read actual output mapping: it includes corrections missing from initial inventory.
            for q in mapping.get('questions',[]):
                if q.get('image_required') and q.get('asset_ids'):
                    iq=next(v for v in inv['questions'] if v['question_id']==q['question_id'])
                    ln=q.get('line',iq['line'])+1
                    candidates.append({'id':q['question_id'],'challenge':q['challenge'],'line':ln,'raw':q.get('source_prompt',''),'ids':q['asset_ids'],'needs_context':q.get('needs_context',False),'existing_prompt':q.get('learner_prompt',q.get('learner_text')),'choices':q.get('choices')})
        else:
            for q in inv['visual_occurrences']:
                if q['source_text'].startswith('#'):continue
                c,sec,item=nearest(lines,q['line']);c=q.get('challenge') or c
                if c not in range(1,6):continue
                candidates.append({'id':f'C{c} · dòng {q["line"]}','challenge':c,'line':q['line'],'raw':q['source_text'],'ids':q['asset_ids'],'needs_context':False})
        samples=[]
        for c in range(1,6):
            pool=[q for q in candidates if q['challenge']==c]
            selected=[]
            if pool:selected.append(pool[0])
            if c==5:
                for q in pool:
                    if q['id']!=selected[0]['id'] and (('→' in q['raw'] and '_' in q['raw']) or 'chỉ/diễn' in q['raw']):selected.append(q);break
            for q in selected:
                if c==2 and 'unit' in inv and len(q['ids'])==1:
                    # Picture-option lists use multiple marker lines for the same listening item.
                    start=q['line']
                    while start>1 and not lines[start-1].startswith(('## ','### ')) and not re.search(r'Nghe|Người lớn đọc',lines[start-1]):start-=1
                    end=q['line']+1
                    while end<=len(lines) and not lines[end-1].startswith('#') and not re.search(r'Nghe|Người lớn đọc',lines[end-1]):end+=1
                    related=[v for v in pool if start<=v['line']<end]
                    q['ids']=list(dict.fromkeys(aid for v in related for aid in v['ids'])) or q['ids']
                prompt,opts,teacher=extract(lines,q['line'],q['raw'],c)
                if q.get('existing_prompt') and not ('Điền:' in q['raw'] or '_' in q['raw']):prompt=q['existing_prompt']
                if q.get('choices'):opts=q['choices']
                if c==2 and len(q['ids'])>1 and (not opts or all(not clean(str(opt)) for opt in opts)):
                    opts=['Hình '+chr(65+j) for j in range(len(q['ids']))]
                q.update(prompt=prompt,options=opts,teacher_audio=teacher);samples.append(q)
        # Some source sections require no static image; use an actual text task as sample.
        for c in range(1,6):
            if any(q['challenge']==c for q in samples):continue
            if c==2:
                if 'questions' in inv:
                    q=next(q for q in mapping['questions'] if q['challenge']==2)
                    iq=next(v for v in inv['questions'] if v['question_id']==q['question_id'])
                    ln=q.get('line',iq['line'])+1;raw=q.get('source_prompt','');prompt,opts,teacher=extract(lines,ln,raw,2)
                    if q.get('choices'):opts=q['choices']
                    samples.append({'id':q['question_id'],'challenge':2,'line':ln,'raw':raw,'ids':[],'prompt':'Nghe audio hoặc người lớn đọc, rồi chọn đáp án phù hợp.','options':opts,'teacher_audio':teacher,'needs_context':False})
                else:
                    for i,s in enumerate(lines,1):
                        nc,sec,item=nearest(lines,i)
                        if nc==2 and (re.match(r'### \d+\.\d+',s) or re.match(r'^\d+\. \*\*',s)):
                            prompt,opts,teacher=extract(lines,i,s,2)
                            if opts:
                                samples.append({'id':f'C2 · dòng {i}','challenge':2,'line':i,'raw':s,'ids':[],'prompt':'Nghe audio hoặc người lớn đọc, rồi chọn đáp án phù hợp.','options':opts,'teacher_audio':s+' '+teacher,'needs_context':False});break
                continue
            if 'unit' in inv:
                for i,s in enumerate(lines,1):
                    nc,sec,item=nearest(lines,i)
                    if nc==c and ('Các từ:' in s or 'Các thẻ:' in s or s.startswith('Sắp xếp:')):
                        actual=s if not s.startswith('Sắp xếp:') else '\n'.join(lines[i:i+3]).strip()
                        samples.append({'id':f'C{c} · dòng {i}','challenge':c,'line':i,'raw':s,'ids':[],'prompt':clean(actual),'options':[],'teacher_audio':'','needs_context':False});break
        for r in mapping.get('resolved_visual_cues',[]):
            samples.append({'id':f'C3 · cue dòng {r["question_line"]}','challenge':3,'line':r['cue_line'],'raw':r['learner_prompt'],'ids':r['asset_ids'],'prompt':r['learner_prompt'],'options':[],'teacher_audio':'Đáp án: '+r['expected_answer'],'needs_context':False})
        samples.sort(key=lambda q:q['challenge'])
        assert {q['challenge'] for q in samples}==set(range(1,6)),ip
        assets=manifest['assets'];gallery=''
        for i,a in enumerate(assets,1):
            aid=a['id'];gallery+=f'<figure><img src="webp/{aid}.webp" width="240" height="240" alt="Thẻ {i}"><figcaption>Thẻ {i:02d}</figcaption><small class="debug">{html.escape(aid)}</small></figure>'
        examples=''
        for i,q in enumerate(samples):
            pictures=''.join(f'<figure><img src="webp/{aid}.webp" width="220" height="220" alt="Hình lựa chọn {j+1}">'+('<figcaption>Hình '+chr(65+j)+'</figcaption>' if q['challenge']==2 and len(q['ids'])>1 else '')+'</figure>' for j,aid in enumerate(q['ids']))
            choices=''.join(f'<label><input type="radio" name="q{i}" value="{j}"> {html.escape(str(opt))}</label>' for j,opt in enumerate(q['options']))
            if not choices:choices='<label>Câu trả lời của em: <input type="text" aria-label="Câu trả lời"></label>'
            teacher='<details><summary>Người lớn: nguồn/ghi chú</summary><pre>'+html.escape(q['raw'])+'</pre><p>'+html.escape(q['teacher_audio'])+'</p><p>Đáp án giáo viên xem trong bài nguồn, không hiển thị trước cho bé.</p></details>'
            examples+=f'<article data-challenge="{q["challenge"]}"><h3>Challenge {q["challenge"]}</h3><p>{html.escape(q["prompt"])}</p><div class="pictures">{pictures}</div><div class="choices">{choices}</div>{teacher}</article>'
        css='body{font:16px Arial;margin:24px;color:#182332;background:#f7f8fb}h1{font-size:28px}.gallery,.pictures{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;background:white;border:1px solid #e0e5ec;border-radius:10px;padding:8px;text-align:center}img{object-fit:contain;max-width:100%;height:auto}article{background:white;padding:20px;border:1px solid #dce3ed;border-radius:12px;margin:18px 0}.choices{display:flex;flex-direction:column;gap:8px;padding:12px 0}details{margin:12px 0;color:#576274}pre{white-space:pre-wrap}.debug{display:none}body.debug-on .debug{display:block}input[type=text]{padding:8px;max-width:90%}'
        page='<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+' — Challenge preview</title><style>'+css+'</style><h1>'+html.escape(title)+' — Challenge</h1><p>Ảnh WebP nhẹ, không có nhãn đáp án trong bitmap. Câu hỏi và lựa chọn nằm riêng. Audio Challenge do chủ dự án bổ sung; hiện có thể nhờ người lớn đọc từ bài nguồn.</p><label><input type="checkbox" onchange="document.body.classList.toggle(\'debug-on\',this.checked)">Người lớn: hiện mã ảnh để kiểm tra</label><h2>Bộ thẻ</h2><div class="gallery">'+gallery+'</div><h2>Thử các câu tiêu biểu</h2>'+examples+'<p>Các câu chưa có cue cố định được ghi trong <a href="question-image-map.json">mapping</a>. Câu trả lời cá nhân không bị ép Yes/No. Toàn bộ bài luyện gốc được giữ nguyên.</p></html>'
        backup=folder/'references/preview-before-unified.html';backup.parent.mkdir(exist_ok=True)
        if not backup.exists():shutil.copy2(folder/'preview.html',backup)
        (folder/'preview.html').write_text(page,encoding='utf-8')
        (folder/'preview-samples.json').write_text(json.dumps({'source':inv['source'],'samples':samples,'gallery_count':len(assets),'debug_labels_hidden_by_default':True},ensure_ascii=False,indent=2),encoding='utf-8')
        report.append({'set':ip.stem.replace('.inventory',''),'sample_challenges':sorted({q['challenge'] for q in samples}),'sample_count':len(samples),'gallery_count':len(assets)})
    (ROOT/'audit/challenge-preview-content.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
