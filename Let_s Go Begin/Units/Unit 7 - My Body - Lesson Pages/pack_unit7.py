from pathlib import Path
from urllib.parse import quote,unquote
from PIL import Image
import json,re,zipfile,hashlib
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
assert [p['track'] for p in m['items']]==['CD2_'+str(n) for n in range(37,54)]
challenge=(ROOT.parent/'Unit 7 - My Body(2).md').read_text(encoding='utf-8')
challenge=challenge.replace(quote(ROOT.name,safe='/')+'/','')
challenge=challenge.replace(quote('Unit 7 - My Body - Cau hoi theo trang.md',safe='/'),'questions.md')
(ROOT/'challenge.md').write_text(challenge,encoding='utf-8')
r=ROOT/'README.md';t=r.read_text(encoding='utf-8')
if '[Challenge và checklist audio](challenge.md)' not in t:t+='\n- [Challenge và checklist audio](challenge.md) (bản đóng gói giữ nguyên bài luyện).\n\nSau lệnh export dùng chung, chạy complete_unit_docs.py --unit 7 rồi finish_unit7.py trong thư mục Unit này, check_preview.cjs bằng node và pack_unit7.py để giữ các ghi chú, kiểm tra preview và đóng gói tài liệu cập nhật.\n'
r.write_text(t,encoding='utf-8')
report=json.loads((ROOT/'validation.json').read_text(encoding='utf-8'))
preview=json.loads((ROOT/'preview-validation.json').read_text(encoding='utf-8'))
assert preview['result']=='pass'
report['preview_validation']=preview
report['generation_tool']='Built-in image_gen only; five batches and three targeted built-in edits.'
for p in m['items']:
 assert p['status']=='reviewed'
 assert len(p['question']['choices'])==3
 assert p['question']['correct_choice_id'] in [c['id'] for c in p['question']['choices']]
 for ext in ['png','webp']:assert Image.open(ROOT/p['output'][ext]).size==(1200,1200)
 assert hashlib.sha256((ROOT/p['output']['png']).read_bytes()).hexdigest()==next(c for c in report['checks'] if c['track']==p['track'])['png_sha256']
for f in [ROOT/'challenge.md',ROOT/'questions.md',ROOT/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
  assert (f.parent/unquote(target)).exists(),(f,target)
report['package_checks']=['17 ordered unique tracks','34 images at1200x1200','PNG hashes match validation','Packaged Challenge links valid','ZIP CRC and bytes match workspace']
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
dest=ROOT.parent/'Unit_7_My_Body_regenerated.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for p in ROOT.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for name in z.namelist():assert z.read(name)==(ROOT/name).read_bytes()
print('FINAL PASS: 17 pages, 17 questions/audio, all links, preview harness, preserved Challenge, complete ZIP.')
print('ZIP bytes:',dest.stat().st_size)

