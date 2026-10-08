"""Validate, export simple audio/image metadata, local preview and ZIP package."""
from pathlib import Path
import json, re, zipfile, hashlib
from PIL import Image
from render import render_page

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    original=json.loads((ROOT/'source.metadata.json').read_text(encoding='utf-8'))
    assert len(manifest['items'])==len(original['items'])==17
    assert [p['track'] for p in manifest['items']]==[p['track'] for p in original['items']]
    assert len({p['output']['webp'] for p in manifest['items']})==17
    source_zip=zipfile.ZipFile(ROOT.parent/'Unit_1_Toys_audio_mapping.zip')
    export_items=[];checks=[];total_bytes=0
    for page,source in zip(manifest['items'],original['items']):
        assert page['source_image_in_zip']==source['image']
        assert page['unit_pdf_page']==source['page'] and page['exercise']==source['exercise']
        assert page['book_page']==source['page']+1
        assert (ROOT/page['audio_file']).exists() and (ROOT/page['audio_file']).stat().st_size>0
        source_audio=ROOT.parent.parent/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD1'/Path(page['audio_file']).name
        assert (ROOT/page['audio_file']).read_bytes()==source_audio.read_bytes()
        assert (ROOT/page['source_reference']).read_bytes()==source_zip.read(source['image'])
        for layer in page['layers']:
            if layer['type']=='image':assert (ROOT/layer['asset']).exists()
        for fmt in ['png','webp']:
            p=ROOT/page['output'][fmt]
            with Image.open(p) as im:
                im.load();assert list(im.size)==page['canvas']['size']
            assert p.stat().st_size>0
        # Confirm PNG agrees pixel-for-pixel with current manifest, not stale output.
        expected=render_page(page)
        with Image.open(ROOT/page['output']['png']) as im:assert im.convert('RGB').tobytes()==expected.tobytes()
        q=page['question'];assert len(q['choices'])>=2 and q['correct_choice_id'] in [c['id'] for c in q['choices']]
        assert not q['render_in_lesson_image'] and q['show_after_audio']
        if page['track'] in ['CD1_15','CD1_16']:
            assert [p['upper'] for p in page['learning_targets']]==list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            assert [p['lower'] for p in page['learning_targets']]==list('abcdefghijklmnopqrstuvwxyz')
        if page['track']=='CD1_07':assert [p['object'] for p in page['learning_targets']]==['ball','jump-rope','yo-yo','bicycle']
        if page['track']=='CD1_11':assert [p['object'] for p in page['learning_targets']]==['train','car','doll','teddy-bear']
        if page['track']=='CD1_10':assert [p['object'] for p in page['learning_targets']]==['yo-yo','ball','jump-rope','bicycle']
        if page['track']=='CD1_14':assert [p['object'] for p in page['learning_targets']]==['ball','teddy-bear','doll','train','bicycle']
        if page['track']=='CD1_18':assert [(p['character'],p['object']) for p in page['learning_targets']]==[('Pete','ball'),('Beth','teddy-bear'),('Ann','doll'),('Matt','bicycle')]
        size=(ROOT/page['output']['webp']).stat().st_size;total_bytes+=size
        export_items.append({'track':page['track'],'audio_name_in_book':source['audio_name_in_book'],'exercise':page['exercise'],'page':page['unit_pdf_page'],'book_page':page['book_page'],'image':page['output']['webp'],'audio_file':page['audio_file'],'source_image':page['source_image_in_zip'],'size':page['canvas']['size'],'question':q,'layout_manifest_track':page['track']})
        checks.append({'track':page['track'],'status':'pass','webp_bytes':size,'png_sha256':hashlib.sha256((ROOT/page['output']['png']).read_bytes()).hexdigest()})
    metadata={'format_version':'1.0','unit':'Unit 1 - Toys','source_archive':'Unit_1_Toys_audio_mapping.zip','item_count':17,'image_role':'lesson page, not answer choice icon','layout_file':'manifest.json','items':export_items}
    (ROOT/'unit1_toys.regenerated.metadata').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    template=(ROOT/'preview.template.html').read_text(encoding='utf-8')
    payload=json.dumps(manifest,ensure_ascii=False).replace('<','\\u003c')
    (ROOT/'preview.html').write_text(template.replace('/*MANIFEST_JSON*/',payload),encoding='utf-8')
    report={'result':'pass','item_count':17,'webp_total_bytes':total_bytes,'checks':checks,'visual_review':'All 17 exported pages reviewed as contact sheet; lyrics, numbered toy scenes and four-child answer scene reviewed at full size. Car marker corrected after review.','audio_validation':'File identity and existence checked against source CD1 tracks; spoken content not transcribed or independently audited.'}
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    # Export question links against this package, not paths outside the ZIP.
    question_text='# Unit 1 – Câu hỏi theo 17 trang bài học\n\n'
    answers=[]
    for page in manifest['items']:
        q=page['question']
        question_text+=f"## {page['track']} – {page['exercise']}\n\n[Hình bài học]({page['output']['webp']}) · [Audio]({page['audio_file']})\n\n**Câu hỏi:** {q['prompt']}\n\n"
        for choice in q['choices']:question_text+=f"- {choice['id']}. {choice['text']}\n"
        question_text+='\n'
        correct=next(c for c in q['choices'] if c['id']==q['correct_choice_id'])
        answers.append(f"| {page['track']} | {correct['id']}. {correct['text']} |")
    question_text+='## Đáp án\n\n| Track | Đáp án |\n|---|---|\n'+'\n'.join(answers)+'\n'
    (ROOT/'questions.md').write_text(question_text,encoding='utf-8')
    for name in ['README.md','questions.md']:
        for link in re.findall(r'\]\(([^)]+)\)',(ROOT/name).read_text(encoding='utf-8')):
            assert (ROOT/link).exists(),(name,link)
    dest=ROOT.parent/'Unit_1_Toys_regenerated.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(ROOT.rglob('*')):
            if file.is_file() and '__pycache__' not in file.parts:
                archive.write(file,file.relative_to(ROOT))
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None
        for page in manifest['items']:
            assert page['output']['webp'] in archive.namelist() and page['audio_file'] in archive.namelist()
    print('PASS: 17 tracks, 17 pages, 17 questions, all asset/audio paths valid; PNGs match layout metadata.')
    print('WebP total bytes:',total_bytes)
    print('ZIP bytes:',dest.stat().st_size)

if __name__=='__main__':main()
