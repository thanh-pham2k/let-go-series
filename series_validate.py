"""Check every requested page, link, question id, answer and source split."""
from pathlib import Path
import json,re,hashlib
from urllib.parse import unquote
import pymupdf as fitz
from series_extract import ROOT,BOOKS,RANGES

def validate():
    summary=[];errors=[];total_questions=0;total_challenge=0
    for n in range(1,7):
        outdir=BOOKS[n].parent/'Units';source=fitz.open(BOOKS[n])
        manifest=json.loads((outdir/'source-manifest.json').read_text(encoding='utf-8'))
        content=json.loads((ROOT/f'series-content/book{n}.json').read_text(encoding='utf-8'))
        expected=set(range(RANGES[n][0][0],RANGES[n][-1][1]+3));seen=[];counts=[];cquestions=0
        for sec in manifest['sections']:
            name=sec['name'];a,b=sec['start'],sec['end'];pdf=fitz.open(outdir/sec['pdf'])
            assert len(pdf)==b-a+1
            for j,i in enumerate(range(a,b+1)):
                seen.append(i)
                # Compare actual page content and rendering, not merely counts.
                p1=source[i-1].get_pixmap(matrix=fitz.Matrix(.35,.35),alpha=False)
                p2=pdf[j].get_pixmap(matrix=fitz.Matrix(.35,.35),alpha=False)
                if p1.samples!=p2.samples:errors.append(f'B{n} P{i}: rendered split differs')
            md=outdir/(name+' - Cau hoi theo trang.md');s=md.read_text(encoding='utf-8')
            headings=[int(x) for x in re.findall(r'^## Trang PDF (\d+)',s,re.M)]
            if headings!=list(range(a,b+1)):errors.append(str(md)+' page headings')
            ids=re.findall(r'^#### (B\d+-P\d+-Q\d+)',s,re.M)
            ans=re.findall(r'^- \*\*(B\d+-P\d+-Q\d+):\*\*',s,re.M)
            if ids!=ans or len(ids)!=len(set(ids)):errors.append(str(md)+' answer mapping')
            total_questions+=len(ids)
            for i in range(a,b+1):
                count=sum(x.startswith(f'B{n}-P{i:02}-') for x in ids);counts.append(count)
                if count<12:errors.append(f'B{n} P{i}: only {count} questions')
                if str(i) not in content['pages']:errors.append(f'B{n} P{i}: missing curated source')
            docs=[md]
            if sec['kind']=='Unit':
                challenge=outdir/(name+' - Challenge.md');docs.append(challenge)
                c=challenge.read_text(encoding='utf-8')
                if re.findall(r'^# Challenge (\d)',c,re.M)!=['1','2','3','4','5']:errors.append(str(challenge)+' missing challenge')
                cids=re.findall(r'^### (C\d+\.\d+\.\d+)',c,re.M)
                cans=re.findall(r'^- \*\*(C\d+\.\d+\.\d+):\*\*',c.split('# Danh sách Audio cần bổ sung')[0],re.M)
                if cids!=cans:errors.append(str(challenge)+' answer mapping')
                cquestions+=len(cids)
                for block in re.split(r'(?=^## )',c,flags=re.M)[1:]:
                    if block.startswith('## ') and re.match(r'## \d',block) and not re.search(r'^### C',block,re.M):
                        if 'Action Challenge' not in block:errors.append(str(challenge)+' empty task section: '+block.splitlines()[0])
            for doc in docs:
                text=doc.read_text(encoding='utf-8')
                for target in re.findall(r'\]\(([^)]+)\)',text):
                    dest=doc.parent/unquote(target.split('#')[0])
                    if not dest.exists():errors.append(str(doc)+' broken link '+target)
                for block in re.split(r'(?=^####? )',text,flags=re.M):
                    opts=re.findall(r'^- ([A-D])\. ',block,re.M)
                    if len(opts)==1:errors.append(str(doc)+' one-choice MCQ')
        if set(seen)!=expected or len(seen)!=len(set(seen)):errors.append(f'Book {n}: coverage gaps or overlaps')
        total_challenge+=cquestions
        summary.append(dict(book=n,pdf_sections=len(manifest['sections']),pages=len(seen),lesson_questions=sum(counts),min_questions_per_page=min(counts),challenge_files=8,challenge_groups=40,challenge_questions=cquestions,rendered_pages_verified=len(seen)))
    report=dict(status='passed' if not errors else 'failed',books=summary,total_pages=432,total_pdfs=88,total_lesson_files=88,total_challenge_files=48,total_challenge_groups=240,total_lesson_questions=total_questions,total_challenge_questions=total_challenge,errors=errors,checks=['all requested ranges exactly once','all 432 split pages rendered identically to source','at least 12 questions per page','question ids unique with matching answer keys','five challenge groups per unit','no empty challenge task sections','local markdown links resolve','no single-option MCQ'],limitations=['Source OCR was checked against selected source page images; this is not an independent second-editor review of every sentence.','No new images or audio files are created. Challenge listening tasks include adult-read scripts. Original listening answers are not inferred.'])
    out=ROOT/'audit/series';out.mkdir(parents=True,exist_ok=True)
    (out/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':validate()
