"""Build source-preserving splits and exercises from reviewed page content."""
from pathlib import Path
import json, re, random, hashlib
import pymupdf as fitz
from series_extract import ROOT, BOOKS, RANGES

TITLES={1:['Things for School','Colors and Shapes','At the Store','People at Home','Birthday and Toys','Outdoors','Food','Animals'],2:['At School','My Things','My House','Things to Eat','Occupations','Locations','Doing Things','After School'],3:['At School','Places','My Home','Clothing','Transportation','Activities','Occupations','Sports'],4:['Birthdays','The Great Outdoors','Hopes and Dreams','School','Indoors and Outdoors','People','Future Plans','Work and Play'],5:['Food','At the Zoo','The Weekend','Activities','The Future','Seasons','The Five Senses','New Experiences'],6:['School Days','Weekend Fun','Going Shopping','Around Town','Explore the World','Doing Things','About Me','In the Future']}

def split_all():
    index=[]
    for n,ranges in RANGES.items():
        src=BOOKS[n]; d=fitz.open(src); outdir=src.parent/'Units';outdir.mkdir(exist_ok=True)
        chunks=[]
        for u,(a,b) in enumerate(ranges,1):
            chunks.append((f'Unit {u} - {TITLES[n][u-1]}',a,b,'Unit',u))
            if u%2==0:
                if n<3: chunks.append((f'Review {u-1}-{u}',b+1,b+2,'Review',u))
                else:
                    chunks.append((f'Review {u-1}-{u}',b+1,b+1,'Review',u))
                    chunks.append((f'Read {u-1}-{u}',b+2,b+2,'Read',u))
        manifest={'book':n,'source':src.name,'numbering':'PDF, one-based; preserve requested ranges even if unit boundaries differ in source','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sections':[]}
        for name,a,b,kind,u in chunks:
            target=outdir/(name+'.pdf')
            if not target.exists():
                sub=fitz.open();sub.insert_pdf(d,from_page=a-1,to_page=b-1);sub.save(target,garbage=4,deflate=True);sub.close()
            assert len(fitz.open(target))==b-a+1
            offset={1:1,2:3,3:3,4:2,5:2,6:2}[n]
            manifest['sections'].append(dict(name=name,start=a,end=b,printed_start=a-offset,printed_end=b-offset,kind=kind,unit=u,pdf=target.name))
        (outdir/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        index.append(manifest)
    return index

def link(name):
    from urllib.parse import quote
    return quote(name)

def parse_pairs(s):
    return [tuple(t.strip() for t in x.split('=',1)) for x in s.split('|') if '=' in x]

def mcq(q,correct,pool,seed):
    wrong=list(dict.fromkeys(x for x in pool if x!=correct))
    if not wrong:
        return q.replace('chọn','nói').replace('Chọn','Nói')+' (Trả lời mở.)',correct
    random.Random(seed).shuffle(wrong)
    opts=[correct]+wrong[:3];random.Random(seed+71).shuffle(opts)
    return q+'\n\n'+'\n'.join(f'- {chr(65+i)}. {v}' for i,v in enumerate(opts)),chr(65+opts.index(correct))+'. '+correct

def make_questions(page,n):
    vs=page.get('v',[]);ss=page.get('s',[]); result=[]
    for i,(en,vi) in enumerate(vs):
        if len(vs)>1:
            result.append(mcq(f'Từ/cụm từ nào có nghĩa “{vi}”?',en,[e for e,v in vs],n*100+i))
        ix=next((k for k,c in enumerate(en) if c.isalpha() and k>0),0)
        blank=en[:ix]+'_'+en[ix+1:]
        result.append((f'Điền chữ cái còn thiếu: **{blank}** ({vi}).',en[ix]+' → '+en))
        result.append((f'Tìm hình hoặc nhãn tương ứng với **{en}** trên trang nguồn, chỉ vào đó rồi đọc từ.',f'Chỉ đúng hình/nhãn {en}; đọc đúng từ.'))
    for i,(en,vi) in enumerate(ss):
        if len(ss)>1: result.append(mcq(f'Chọn câu diễn đạt: “{vi}”.',en,[e for e,v in ss],n*100+40+i))
        words=en.split()
        if len(words)>1:
            k=max(0,len(words)-1);answer=words[k]; masked=words[:];masked[k]='_____'
            result.append((f'Hoàn thành câu theo nghĩa “{vi}”: **'+ ' '.join(masked)+'**',answer+' → '+en))
            shuffled=words[:];random.Random(n*100+i).shuffle(shuffled)
            if shuffled==words:shuffled=words[1:]+words[:1]
            result.append(('Sắp xếp các thẻ từ để diễn đạt “'+vi+'”: **'+' / '.join(shuffled)+'**',en))
        result.append((f'Không nhìn mẫu tiếng Anh, nói câu: “{vi}”.',en))
    for i,(q,a) in enumerate(page.get('qa',[])):
        result.append((f'Đáp lại câu hỏi **“{q}”** theo nội dung/hình trên trang.',a))
        result.append((f'Bạn nghe câu trả lời **“{a}”**. Hãy nói câu hỏi tương ứng.',q))
    return result

def build_book(n):
    path=ROOT/f'series-content/book{n}.json'
    if not path.exists():return
    data=json.loads(path.read_text(encoding='utf-8'));pages={int(k):v for k,v in data['pages'].items()}
    # Infer only adjacent question/answer models; explicit reading answers take priority.
    for p in pages.values():
        existing={q for q,a in p.get('qa',[])}
        for (q,_),(ans,_) in zip(p.get('s',[]),p.get('s',[])[1:]):
            if q.endswith('?') and not ans.endswith('?') and q not in existing:
                p.setdefault('qa',[]).append([q,ans]);existing.add(q)
    outdir=BOOKS[n].parent/'Units';manifest=json.loads((outdir/'source-manifest.json').read_text(encoding='utf-8'))
    report=[]
    for section in manifest['sections']:
        a,b=section['start'],section['end'];name=section['name']
        if any(i not in pages for i in range(a,b+1)):continue
        lines=[f'# {name} - Câu hỏi theo từng trang','',f'> Nguồn: [{name}.pdf]({link(name+".pdf")}). Phạm vi: **trang PDF {a}–{b}**; số trang in trên sách có thể khác.','',
        '## Cách dùng','',
        '- Mở đúng trang nguồn trước khi làm bài. Mỗi mục dưới đây ứng với một trang PDF gốc.',
        '- Câu hỏi mở rộng cách luyện từ/câu đã có trên trang. Phần nói chấp nhận câu tương đương trong phạm vi bài.',
        '- Mẫu câu gồm câu trong sách và câu luyện ghép từ cùng khung của trang; không phải bản chép nguyên văn. Đáp án cho câu cá nhân là mẫu tham khảo, không ép người học nhận thông tin mẫu là của mình.',
        '- Đáp án và gợi ý chấm đặt ở cuối file để người học có thể làm trước.',
        '- Bài nghe gốc cần audio gốc để chấm; không suy đoán đáp án nghe từ hình. Các câu dưới đây là bài luyện bổ sung từ nội dung nhìn thấy.', '']
        answers=[];total=0
        for i in range(a,b+1):
            p=pages[i];qs=make_questions(p,i)
            offset={1:1,2:3,3:3,4:2,5:2,6:2}[n]
            lines.extend([f'## Trang PDF {i} - {p["topic"]}','',f'- **Trang in trong sách:** {i-offset}. **Trang trong file tách:** {i-a+1}. [Mở trang nguồn]({link(name+".pdf")}#page={i-a+1}).'])
            if p.get('note'):lines.extend(['- **Lưu ý phạm vi:** '+p['note']])
            lines.extend(['','### Nội dung cần nắm',''])
            if p.get('v'):lines.append('**Từ/cụm từ:** '+'; '.join(f'{e} ({v})' for e,v in p['v'])+'.')
            if p.get('s'):lines.extend(['','**Mẫu câu:**']+[f'- {e} — {v}' for e,v in p['s']])
            lines.extend(['','### Câu hỏi',''])
            for j,(q,ans) in enumerate(qs,1):
                ident=f'B{n}-P{i:02}-Q{j:02}';lines.extend([f'#### {ident}',q,'']);answers.append((ident,ans));total+=1
            report.append(dict(section=name,page=i,questions=len(qs)))
        lines.extend(['---','','# Đáp án và gợi ý chấm',''])
        lines.extend(f'- **{ident}:** {ans}' for ident,ans in answers)
        (outdir/(name+' - Cau hoi theo trang.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
        if section['kind']=='Unit':build_challenge(n,section,pages,outdir)
    (outdir/'content-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

def build_challenge(n,section,pages,outdir):
    name=section['name'];a,b=section['start'],section['end']
    vocab={};sentences={};qa={}
    for i in range(a,b+1):
        for en,vi in pages[i].get('v',[]):vocab.setdefault(en,(vi,i))
        for en,vi in pages[i].get('s',[]):sentences.setdefault(en,(vi,i))
        for q,ans in pages[i].get('qa',[]):qa.setdefault(q,(ans,i))
    lines=[f'# {name}','',f'> Chỉ dùng nội dung trong phạm vi trang PDF **{a}–{b}** đã tách theo yêu cầu.','',
    f'- [PDF nguồn]({link(name+".pdf")}) · [Câu hỏi theo từng trang]({link(name+" - Cau hoi theo trang.md")}).',
    '- Người lớn đọc câu nghe theo kịch bản cuối file. Các chỉ dẫn hình dùng hình trong PDF nguồn; không phải ảnh hoặc audio mới đã được tạo.',
    '- Lộ trình: Recognition → Recall → Comprehension → Production. Đáp án nằm cuối file.','', '## Nội dung cần nắm','','### Vocabulary']
    lines.extend(f'- {en} — {vi}; trang PDF {p}.' for en,(vi,p) in vocab.items())
    lines.extend(['','### Sentences / classroom language'])
    lines.extend(f'- {en} — {vi}; trang PDF {p}.' for en,(vi,p) in sentences.items())
    keys=[];audio=[]
    def add(ident,q,ans):
        lines.extend([f'### {ident}',q,'']);keys.append((ident,ans))
    lines.extend(['','---','','# Challenge 1 - Vocabulary Master','**Level: Recognition**','','## 1. Nhìn hình → chọn từ',''])
    for k,(en,(vi,p)) in enumerate(vocab.items(),1):
        q,ans=mcq(f'🖼️ Người lớn chỉ hình/nhãn **{vi}** ở trang PDF {p}. Chọn từ tương ứng.',en,list(vocab),k)
        add(f'C1.1.{k:02}',q,ans)
    if not vocab:
        for k,(en,(vi,p)) in enumerate(sentences.items(),1):
            add(f'C1.1.{k:02}',f'Quan sát ngữ cảnh trang PDF {p}. Tìm câu diễn đạt “{vi}”.',en)
    lines.extend(['## 2. Nghe → chọn từ/cụm từ',''])
    for k,(en,(vi,p)) in enumerate(vocab.items(),1):
        ident=f'C1.2.{k:02}';audio.append((ident,en));q,ans=mcq('Nghe người lớn đọc. Chọn từ/cụm từ vừa nghe.',en,list(vocab),k+30);add(ident,q,ans)
    lines.extend(['# Challenge 2 - Listen & Understand','**Level: Recognition**','','## 1. Nghe → chọn nghĩa',''])
    for k,(en,(vi,p)) in enumerate(sentences.items(),1):
        ident=f'C2.1.{k:02}';audio.append((ident,en));q,ans=mcq('Nghe câu rồi chọn ý nghĩa phù hợp.',vi,[x[0] for x in sentences.values()],k+60);add(ident,q,ans)
    lines.extend(['## 2. Nghe → chọn câu trả lời phù hợp',''])
    for k,(q,(ans,p)) in enumerate(qa.items(),1):
        ident=f'C2.2.{k:02}';audio.append((ident,q));add(ident,f'Nghe câu hỏi. Dựa vào tình huống ở trang PDF {p}, nói câu trả lời.',ans)
    lines.extend(['# Challenge 3 - Fill & Recall','**Level: Recall**','','## 1. Điền chữ cái còn thiếu vào từ',''])
    for k,(en,(vi,p)) in enumerate(vocab.items(),1):
        ix=next((j for j,c in enumerate(en) if c.isalpha() and j>0),0)
        add(f'C3.1.{k:02}',f'Điền chữ cái: **{en[:ix]}_{en[ix+1:]}** ({vi}).',en)
    lines.extend(['## 2. Hoàn thành mẫu câu; giảm gợi ý',''])
    for k,(en,(vi,p)) in enumerate(sentences.items(),1):
        words=en.split();add(f'C3.2.{k:02}',f'Hoàn thành theo nghĩa “{vi}”: **'+ ' '.join(words[:-1]+['_____'])+'**',en)
    lines.extend(['# Challenge 4 - Build & Match','**Level: Comprehension**','','## 1. Ghép từ thành câu hoàn chỉnh',''])
    for k,(en,(vi,p)) in enumerate(sentences.items(),1):
        words=en.split();random.Random(k+13).shuffle(words);add(f'C4.1.{k:02}','Sắp xếp theo nghĩa “'+vi+'”: **'+' / '.join(words)+'**',en)
    lines.extend(['## 2. Ghép câu hỏi với câu trả lời phù hợp',''])
    qas=list(qa.items()); shuffled=list(dict.fromkeys(v[0] for _,v in qas));random.Random(71).shuffle(shuffled)
    for k,(q,(ans,p)) in enumerate(qas,1):
        add(f'C4.2.{k:02}',q+'\n\n'+'\n'.join(f'- {j+1}. {v}' for j,v in enumerate(shuffled)),ans)
    lines.extend(['## 3. Xây dựng hội thoại',''])
    for k,(q,(ans,p)) in enumerate(qas,1):add(f'C4.3.{k:02}',f'Đóng vai hai người trong tình huống trang PDF {p}. Người A hỏi, người B đáp; sau đó đổi vai.',q+' → '+ans)
    lines.extend(['# Challenge 5 - Final Boss','**Level: Production**','','## 1. Quick Recognition',''])
    for k,(en,(vi,p)) in enumerate(vocab.items(),1):add(f'C5.1.{k:02}',f'Không nhìn chữ: chỉ và gọi tên hình **{vi}** trong trang PDF {p}.',en)
    lines.extend(['## 2. Recall / Context & Nói theo mẫu',''])
    for k,(en,(vi,p)) in enumerate(sentences.items(),1):add(f'C5.2.{k:02}',f'Che câu mẫu ở trang PDF {p}. Nói câu diễn đạt “{vi}”.',en)
    lines.extend(['## 3. Speak - không hint / Mini Conversation',''])
    for k,(q,(ans,p)) in enumerate(qas,1):add(f'C5.3.{k:02}',f'Không nhìn mẫu, thực hiện lượt hỏi–đáp theo ngữ cảnh trang PDF {p}; đổi vai rồi lặp lại.',q+' → '+ans)
    lines.extend(['## 4. Action Challenge','',
    'Người lớn chọn một câu chỉ dẫn/hành động đã xuất hiện trong phạm vi Unit, đọc câu đó và yêu cầu người học thực hiện hoặc đóng vai. Nếu Unit không có câu chỉ dẫn vận động, dùng các lượt hội thoại ở trên. Chấm đúng ý, đúng từ và đúng mẫu câu của bài.','',
    '# Coverage Check','', '| Nội dung | Trang PDF | Bài luyện |','|---|---:|---|'])
    lines.extend(f'| {en} | {p} | C1, C3.1, C5.1 |' for en,(vi,p) in vocab.items())
    lines.extend(f'| {en} | {p} | C2.1, C3.2, C4.1, C5.2 |' for en,(vi,p) in sentences.items())
    lines.extend(['','# Đáp án và gợi ý chấm',''])
    lines.extend(f'- **{ident}:** {ans}' for ident,ans in keys)
    lines.extend(['','# Danh sách Audio cần bổ sung','', 'Kịch bản để người lớn đọc hoặc thu âm. Đây là danh sách yêu cầu, chưa có file audio riêng. Không thay thế đáp án của bài nghe gốc.',''])
    lines.extend(f'- **{ident}:** {script}' for ident,script in audio)
    (outdir/(name+' - Challenge.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__':
    manifests=split_all()
    for n in range(1,7):build_book(n)
    print('PDF sections:',sum(len(m['sections']) for m in manifests))
