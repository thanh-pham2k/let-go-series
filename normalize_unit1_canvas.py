from pathlib import Path
import json,importlib.util,hashlib
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parent
folder=ROOT/'Let_s Go Begin/Units/Unit 1 - Toys - Lesson Pages'
p=folder/'manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('unit1_render',folder/'render.py')
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
checks=[]
for page in m['items']:
    if 'native_layout_size' not in page:
        with Image.open(folder/page['output']['png']) as old:
            native=renderer._render_native_page(page)
            assert old.convert('RGB').tobytes()==native.tobytes(),page['track']
    page.setdefault('native_layout_size',list(page['canvas']['size']))
    page['canvas']['size']=[1200,1200]
    rendered=renderer.render_page(page)
    native=renderer._render_native_page({**page,'canvas':{**page['canvas'],'size':page['native_layout_size']}})
    fitted=ImageOps.contain(native,(1200,1200),Image.Resampling.LANCZOS)
    x=(1200-fitted.width)//2;y=(1200-fitted.height)//2
    assert rendered.crop((x,y,x+fitted.width,y+fitted.height)).tobytes()==fitted.tobytes()
    checks.append({'track':page['track'],'native_layout_size':page['native_layout_size'],'canvas_size':[1200,1200],'content_box':[x,y,fitted.width,fitted.height],'full_native_content_preserved':True})
m['uniform_size']=[1200,1200]
m['canvas_policy']='Render native_layout_size with original image/font layer geometry, then scale uniformly with contain and center the complete page on1200x1200 white canvas.'
p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
(folder/'normalization-validation.json').write_text(json.dumps({'result':'pass','item_count':17,'checks':checks},indent=2),encoding='utf-8')
readme=folder/'README.md';s=readme.read_text(encoding='utf-8')
if '## Kích thước đồng nhất' not in s:
    s+='\n## Kích thước đồng nhất\n\nToàn bộ17 PNG/WebP được xuất1200×1200, giống Unit2–8 và4 Review. Giữ tỷ lệ bằng contain, căn giữa trên nền trắng, không cắt chữ/đồ vật. native_layout_size trong manifest giữ kích thước bố cục và các lớp font gốc để dựng lại chính xác. [normalization-validation.json](normalization-validation.json) ghi box nội dung từng trang và kiểm tra toàn bộ nội dung gốc được giữ sau khi scale.\n'
readme.write_text(s,encoding='utf-8')
exercise=folder.parent/'Unit 1 - Toys(5).md';s=exercise.read_text(encoding='utf-8')
needle='Phần học chính **xem hình có chữ → nghe audio → làm một câu trắc nghiệm mỗi trang** đã có đủ 17 mục CD1_02–CD1_18.'
if needle in s and 'PNG/WebP của17 trang đều1200×1200' not in s:s=s.replace(needle,needle+' PNG/WebP của17 trang đều1200×1200, giữ tỷ lệ nội dung.')
exercise.write_text(s,encoding='utf-8')
print('PASS:17 native pages preserved, standardized canvas1200x1200 configured.')
