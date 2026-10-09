from pathlib import Path
from urllib.parse import unquote
from PIL import Image,ImageChops,ImageStat
import json,re,zipfile,hashlib,math
from render_review import render
ROOT=Path(__file__).resolve().parent
UNITS=ROOT.parent
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def save(name,d):(ROOT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
m=load('manifest.json');meta=load('review.regenerated.metadata');mapping=load('references/audio-mapping.json')['items']
assert [p['track'] for p in m['items']]==['CD2_70','CD2_71','CD2_72']
assert len(meta['items'])==len(mapping)==3
assert m['source_pdf_page_count']==2
assert (ROOT/'references/source.pdf').read_bytes()==(UNITS/'Review 7-8.pdf').read_bytes()
reviews=load('visual-review.json');assert reviews['result']=='pass' and reviews['source_pages_viewed']==2 and reviews['contact_sheet_viewed']
preview=load('preview-validation.json');assert preview['result']=='pass'
resources=load('resource-validation.json');assert resources['result']=='pass' and len(resources['checks'])==8
generation=load('generation.json');assert not generation['fallback_used']
batch=load('assets/batches/batch1.json')
sheet=Image.open(ROOT/batch['selected_asset']).convert('RGB')
assert hashlib.sha256((ROOT/batch['selected_asset']).read_bytes()).hexdigest()==batch['final_sha256']
ids=set();qids=set();checks=[]
for p,it,r in zip(m['items'],meta['items'],mapping):
 track=p['track'];assert p['status']=='reviewed' and reviews['pages'][track]['final_png_viewed']
 assert r['source_pdf']=='Review 7-8.pdf' and r['audio']['disc']=='CD2'
 assert track=='CD2_'+str(r['audio']['track'])
 assert p['pdf_page']==r['pdf_page'] and p['book_page']==r['book_page']
 assert track not in ids;ids.add(track)
 q=p['question'];assert q['id'] not in qids;qids.add(q['id'])
 assert len(q['choices'])==3 and len({c['id'] for c in q['choices']})==3
 assert q['correct_choice_id'] in {c['id'] for c in q['choices']}
 assert q['show_after_audio'] is True and q['render_in_lesson_image'] is False
 assert it['track']==track and it['image']==p['output']['webp'] and it['audio_file']==p['audio_file'] and it['question']==q and it['size']==[1200,1200]
 assert (ROOT/p['audio_file']).read_bytes()==Path(p['audio_source']).read_bytes()
 for rel in [p['source_reference'],p['source_region']['path'],p['output']['png'],p['output']['webp'],p['audio_file']]:assert (ROOT/rel).is_file()
 asset=Image.open(ROOT/p['layers'][0]['asset']).convert('RGB')
 assert asset.tobytes()==sheet.crop(tuple(p['source_crop_box'])).tobytes()
 expected=render(p)
 png=Image.open(ROOT/p['output']['png']).convert('RGB');webp=Image.open(ROOT/p['output']['webp']).convert('RGB')
 assert png.size==webp.size==(1200,1200)
 assert png.tobytes()==expected.tobytes()
 diff=ImageStat.Stat(ImageChops.difference(png,webp)).rms
 rms=math.sqrt(sum(v*v for v in diff)/3)
 assert rms<10,(track,rms)
 checks.append({'track':track,'png_matches_manifest':True,'webp_png_rms':round(rms,4),'audio_byte_identical':True,'question_valid':True,'source_mapping_matches':True})
html=(ROOT/'preview.html').read_text(encoding='utf-8')
embedded=json.loads(re.search(r'const manifest=(.*?);\nconst pages=',html,re.S).group(1))
assert embedded==m
original=(ROOT/'references/challenge-original.md').read_text(encoding='utf-8-sig')
current=(UNITS/'Review 7-8(2).md').read_text(encoding='utf-8')
def body(t):return t[t.index('# Challenge 1'):t.index('# Coverage Check')]
assert body(original)==body(current)
assert 'Coverage:' not in current and '☐' in current
assert 'Bắt buộc' in current and 'Tùy chọn' in current
for f in list(ROOT.rglob('*.md'))+[UNITS/'Review 7-8(2).md',UNITS/'Review 7-8 - Cau hoi theo trang.md']:
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8-sig')):
  assert (f.parent/unquote(link)).exists(),(str(f),link)
# Add precise boundaries of verification; real browser never claimed.
r=load('validation.json')
r.update({'result':'pass','package_checks':checks,'preview_validation':preview,'http_resource_validation':resources,'browser_validation':load('browser-validation.json'),'source_and_link_validation':'Source PDF copy,3 filtered mapping records, all metadata joins, all Markdown links checked.','challenge_exercises_preserved':True,'limitations':['MP3 speech and original listening answers not independently audited.','Additional Challenge short clips not created; checklist marks all pending.','Real browser rendering/playback not run; Node DOM behavior and direct HTTP serving tested.']})
save('validation.json',r)
readme=ROOT/'README.md';text=readme.read_text(encoding='utf-8')
if '## Giới hạn kiểm tra preview' not in text:
 text+='\n## Giới hạn kiểm tra preview\n\nĐã chạy [Node DOM checks](preview-validation.json) cho cả3 mục, gồm chọn mục, reset, nút ôn tập, sự kiện ended mô phỏng, phản hồi đúng/sai và chuyển trước/sau. Đã kiểm [HTTP resources](resource-validation.json): preview/metadata/3WebP/3MP3 trả200 và trùng byte với file.\n\nKiểm tra trình duyệt thật chưa chạy: công cụ IAB lỗi khởi tạo kernel; lệnh Edge headless qua Start-Process bị automatic approval review từ chối với lý do blocked by policy. [Chi tiết](browser-validation.json). Không coi sự kiện ended mô phỏng là đã nghe audio.\n'
 readme.write_text(text,encoding='utf-8')
dest=UNITS/'Review_7-8_regenerated.zip'
files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'edge-profile' not in p.parts]
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(ROOT))
required={'manifest.json','review.regenerated.metadata','preview.html','preview.jpg','questions.md','README.md','generation.json','validation.json','challenge.md'}
required|={p['output'][ext] for p in m['items'] for ext in ['png','webp']}
required|={p['audio_file'] for p in m['items']}
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 assert required.issubset(z.namelist())
 for name in z.namelist():assert z.read(name)==(ROOT/name).read_bytes()
print('FINAL PASS:3tracks,2sourcepages,6images1200x1200,3audio byte comparisons,3questions, manifest/metadata/links/preview logic/HTTP/Challenge preservation/ZIP.')
print('ZIP:',dest,'bytes:',dest.stat().st_size)
print('WebP/PNG RMS:',[c['webp_png_rms'] for c in checks])

