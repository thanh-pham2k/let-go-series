"""Prepare Unit 2–8 source pages, track/question mapping and batch inventory."""
from pathlib import Path
from urllib.parse import unquote
import json,re,subprocess
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw

ROOT=Path(__file__).resolve().parent
UNITS=ROOT/'Let_s Go Begin/Units'
SOURCE=json.loads((ROOT/'Let_s Go Begin/lets_go_audio_mapping.metadata').read_text(encoding='utf-8'))

def prepare(unit):
    pdf=next(UNITS.glob(f'Unit {unit} - *.pdf'))
    name=pdf.stem
    folder=UNITS/(name+' - Lesson Pages')
    for sub in ['references','source-pages','pages/png','pages/webp','audio','assets/batches']:
        (folder/sub).mkdir(parents=True,exist_ok=True)
    mappings=[m for m in SOURCE['audio_mappings'] if m['unit']==unit and m['source_pdf']==pdf.name]
    questions=next(UNITS.glob(name+' - Cau hoi theo trang.md')).read_text(encoding='utf-8-sig')
    reader=PdfReader(pdf)
    for i,page in enumerate(reader.pages):
        dest=folder/'source-pages'/f'page-{i+1:02}.png'
        if dest.exists():continue
        subprocess.run(['pdftoppm','-f',str(i+1),'-l',str(i+1),'-scale-to','1800','-png','-singlefile',str(pdf),str(dest.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    records=[]
    for m in mappings:
        track=f"{m['audio']['disc']}_{m['audio']['track']:02}"
        legacy_track=('CD1_'+str(m['audio']['track'])) if unit==6 and m['audio']['track'] in (32,34) else track
        block=re.search(r'^## '+re.escape(legacy_track)+r' – (.*?)\n(.*?)(?=^## |\Z)',questions,re.M|re.S)
        assert block,(unit,track)
        title=block[1].strip();body=block[2]
        prompt=re.search(r'\*\*Câu hỏi:\*\* (.*)',body)[1].strip()
        choices=[{'id':cid,'text':value.strip()} for cid,value in re.findall(r'^- ([A-Z])\. (.*)',body,re.M)]
        answer=re.search(r'^\| U'+str(unit)+'-'+re.escape(legacy_track)+r' \|.*?\| ([A-Z])\. (.*?) \|$',questions,re.M)
        assert answer,(unit,track,'answer')
        source=folder/'source-pages'/f"page-{m['pdf_page']:02}.png"
        ref=folder/'references'/f'{track}.png'
        if not ref.exists():
            Image.open(source).save(ref)
        audio_source=ROOT/'Let_s Go Begin'/f"Oxford - Let_s Go Begin Student_s Book 3rd Edition {m['audio']['disc']}"/f"Track{m['audio']['track']:02}.mp3"
        assert audio_source.exists(),audio_source
        audio_dest=folder/'audio'/audio_source.name
        if not audio_dest.exists():audio_dest.write_bytes(audio_source.read_bytes())
        records.append({'track':track,'audio_key':m['audio']['audio_key'],'exercise':title,'unit_pdf_page':m['pdf_page'],'book_page':m['book_page'],
            'source_reference':f'references/{track}.png','audio_file':f'audio/{audio_source.name}',
            'output':{'png':f'pages/png/{track}.png','webp':f'pages/webp/{track}.webp'},
            'question':{'id':f'U{unit}-{track}','prompt':prompt,'choices':choices,'correct_choice_id':answer[1],'show_after_audio':True,'render_in_lesson_image':False},
            'canvas':{'size':[1200,1200],'background':'#FFFFFF'},'layers':[],
            'status':'pending_generation'})
    manifest={'schema_version':'2.0','unit':unit,'topic':name.split(' - ',1)[1],'source_pdf':pdf.name,'source_item_count':len(records),'image_count':len(records),
        'coordinate_system':'pixel boxes [x,y,width,height], top-left origin','image_fit':'contain','text_font':'Arial','items':records,
        'generation_policy':'Built-in image_gen only; group about four pages; split then contain on identical 1200x1200 canvases without distortion.'}
    path=folder/'manifest.json'
    if not path.exists():path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    thumbs=Image.new('RGB',(1200,((len(reader.pages)+3)//4)*440),'#EDF2F7')
    draw=ImageDraw.Draw(thumbs)
    for i in range(len(reader.pages)):
        im=ImageOps.contain(Image.open(folder/'source-pages'/f'page-{i+1:02}.png'),(290,410))
        x=(i%4)*300;y=(i//4)*440+25
        thumbs.paste(im,(x,y));draw.text((x+6,y-18),f'PDF page {i+1}',fill='#25334A')
    thumbs.save(folder/'source-preview.jpg',quality=92)
    return {'unit':unit,'folder':str(folder),'page_count':len(reader.pages),'tracks':[r['track'] for r in records]}

if __name__=='__main__':
    result=[prepare(i) for i in range(2,9)]
    (UNITS/'remaining-units-progress.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in result:print(r['unit'],r['page_count'],len(r['tracks']),r['tracks'][0],r['tracks'][-1])
