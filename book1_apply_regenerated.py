"""Activate the accepted batch-regenerated WebPs, preserving source crops."""
from pathlib import Path
import json,shutil,hashlib,zipfile,csv,subprocess,re
from PIL import Image,ImageDraw,ImageFont
from book1_audio_pages import preview

ROOT=Path(__file__).resolve().parent;UNITS=ROOT/'Let_s Go 1/Units';INDEX=UNITS/'Audio Pages'
OUT=ROOT/'output/imagegen/book1-all-batches'

def apply():
    manifest=json.loads((INDEX/'manifest.json').read_text(encoding='utf-8'))
    jobs=json.loads((OUT/'plan.json').read_text(encoding='utf-8'))
    results={}
    for job in jobs:
        result=json.loads((OUT/job['id']/'result.json').read_text(encoding='utf-8'))
        assert [r['id'] for r in result['tracks']]==[r['id'] for r in job['rows']]
        for row in result['tracks']:results[row['id']]=job['id']
    assert len(results)==188
    all_files=[]
    for row in manifest['tracks']:
        folder=UNITS/(row['section']+' - Audio Pages');path=folder/'regenerated'/f'{row["id"]}.webp'
        with Image.open(path) as im:
            assert im.size==(512,512) and im.format=='WEBP'
            assert im.convert('L').point(lambda p:255 if p<220 else 0).getbbox(),f'Blank tile: {path}'
        if 'source_crop_image' not in row:row['source_crop_image']=row['image']
        row['image']=str(path.relative_to(UNITS)).replace('\\','/');row['image_size']=[512,512]
        row['image_bytes']=path.stat().st_size
        row['image_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        row['generation_batch']=results.get(row['id'],'accepted-sample')
        row['image_method']='AI-regenerated contact sheet, one image generation per 4x2 sheet, then crop and WebP quality 85'
        all_files.append(path)
    manifest['image_variant']='batch-regenerated-webp-512'
    manifest['generation']={'accepted_sample_images':8,'additional_batches':27,'additional_images':188,'tile_size':[512,512],'webp_quality':85,'individual_image_generation':False,'total_image_bytes':sum(p.stat().st_size for p in all_files)}
    manifest['notes']=['AI-regenerated WebP images are active following user acceptance of the sample.','Source PNG crops and full-page renders remain available for comparison.','Regeneration can change small details or text; these images do not have a pixel-identical fidelity guarantee.','Audio IDs and original audio files remain mapped by manifest.']
    for sec in manifest['sections']:
        folder=UNITS/(sec['name']+' - Audio Pages');mp=folder/'manifest.json'
        local=json.loads(mp.read_text(encoding='utf-8'))
        rows=[dict(r) for r in manifest['tracks'] if r['section']==sec['name']]
        for row in rows:
            for field in ['image','source_crop_image','page_image','audio','expected_audio']:
                if row.get(field):row[field]=str((UNITS/row[field]).relative_to(folder)).replace('\\','/')
        if not (folder/'index-original.html').exists():shutil.copy2(folder/'index.html',folder/'index-original.html')
        if not (folder/'manifest-original.json').exists():shutil.copy2(mp,folder/'manifest-original.json')
        local['tracks']=rows;local['image_variant']=manifest['image_variant']
        mp.write_text(json.dumps(local,ensure_ascii=False,indent=2),encoding='utf-8')
        preview(folder,rows,sec['name']+' — WebP 512×512','../Audio%20Pages/index.html')
        hp=folder/'index.html';text=hp.read_text(encoding='utf-8')
        text=text.replace('Mỗi ảnh cắt tương ứng 1 audio track gốc.','Ảnh regenerate theo batch · WebP 512×512 · Mỗi ảnh tương ứng 1 audio track gốc.')
        text=text.replace('<details class="panel">','<p><a href="index-original.html">Xem bản cắt gốc</a></p><details class="panel">',1)
        hp.write_text(text,encoding='utf-8')
        readme=folder/'README.md';old=readme.read_text(encoding='utf-8')
        if '## Bản regenerate WebP' not in old:
            readme.write_text('## Bản regenerate WebP\n\nTrang `index.html` dùng ảnh trong `regenerated/`, kích thước 512×512. Mỗi batch được regenerate cả lưới, sau đó mới cắt ảnh. Xem `index-original.html` để đối chiếu ảnh PNG gốc.\n\n'+old,encoding='utf-8')
        # Review sheets with IDs outside the image; never imprint metadata on learning tiles.
        for start in range(0,len(rows),8):
            sheet=Image.new('RGB',(2048,1104),'#e9edf3');draw=ImageDraw.Draw(sheet)
            for i,row in enumerate(rows[start:start+8]):
                x,y=i%4*512,i//4*552
                with Image.open(folder/row['image']) as tile:sheet.paste(tile,(x,y+40))
                draw.text((x+12,y+8),row['id'],fill='black',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22))
            sheet.save(OUT/f'{sec["name"]}-webp-{start//8+1}.jpg',quality=90)
    if not (INDEX/'manifest-original.json').exists():shutil.copy2(INDEX/'manifest.json',INDEX/'manifest-original.json')
    (INDEX/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    with (INDEX/'mapping-regenerated.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['id','section','image','source_crop_image','audio','generation_batch','image_bytes'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows({k:r.get(k) for k in fields} for r in manifest['tracks'])
    with zipfile.ZipFile(INDEX/'Let-Go-1-regenerated-512-webp.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in all_files:z.write(path,str(path.relative_to(UNITS)))
        z.write(INDEX/'mapping-regenerated.csv','mapping-regenerated.csv')
    hp=INDEX/'index.html';text=hp.read_text(encoding='utf-8')
    text=text.replace('<h1>Let’s Go 1 — Ảnh theo audio track</h1>','<h1>Let’s Go 1 — Ảnh regenerate WebP 512×512</h1>')
    text=text.replace('href="validation.json"','href="regenerated-validation.json"')
    text=text.replace('<section>','<p><a href="Let-Go-1-regenerated-512-webp.zip">Tải toàn bộ 196 ảnh WebP</a> · <a href="mapping-regenerated.csv">Mapping ảnh regenerate</a></p><section>',1)
    hp.write_text(text,encoding='utf-8')
    readme=INDEX/'README.md';old=readme.read_text(encoding='utf-8')
    if '## Bản regenerate WebP' not in old:
        readme.write_text('## Bản regenerate WebP\n\nĐã áp dụng 196 ảnh WebP 512×512 cho 8 Unit và 4 Review. Dùng lại 8 ảnh mẫu được duyệt; 188 ảnh còn lại qua 27 batch, mỗi lần regenerate một lưới tối đa 8 ảnh. Prompt thực tế và ảnh ghép nằm trong `output/imagegen/book1-all-batches/` tại workspace.\n\n- [Tải toàn bộ WebP](Let-Go-1-regenerated-512-webp.zip)\n- [Mapping mới](mapping-regenerated.csv)\n- [Kiểm tra WebP](regenerated-validation.json)\n\nẢnh AI có thể thay đổi chữ nhỏ hoặc chi tiết; ảnh PNG gốc được giữ để đối chiếu trong từng Unit/Review.\n\n'+old,encoding='utf-8')
    errors=[]
    for row in manifest['tracks']:
        for field in ['image','source_crop_image','page_image','audio']:
            if row.get(field) and not (UNITS/row[field]).exists():errors.append(row['id']+': '+field)
    for sec in manifest['sections']:
        html=(UNITS/(sec['name']+' - Audio Pages')/'index.html').read_text(encoding='utf-8')
        script=re.search(r'<script>([\s\S]*?)</script>',html).group(1)
        proc=subprocess.run(['node','--check'],input=script,text=True,encoding='utf-8',capture_output=True)
        if proc.returncode:errors.append(sec['name']+': JS syntax')
    assert len(all_files)==196 and len({r['id'] for r in manifest['tracks']})==196
    report={'status':'passed' if not errors else 'failed','images':196,'sections':12,'new_sheet_generations':27,'accepted_sample_images':8,'size':[512,512],'total_bytes':sum(p.stat().st_size for p in all_files),'errors':errors,'scope':'Checks format, size, coverage, provenance, mapping and preview syntax. Does not certify identical text or object counts after AI regeneration.'}
    (INDEX/'regenerated-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));assert not errors

if __name__=='__main__':apply()
