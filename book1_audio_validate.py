from pathlib import Path
import json,hashlib,re,subprocess
from urllib.parse import unquote
from PIL import Image,ImageDraw
import pymupdf as fitz
from book1_audio_pages import UNITS,INDEX,SOURCE,SECTIONS,ROOT
from book1_audio_specs import SPECS

def validate():
    manifest=json.loads((INDEX/'manifest.json').read_text(encoding='utf-8'))
    manifest['asset_base']='..'
    manifest['asset_paths_relative_to']='Let_s Go 1/Units'
    manifest['source_paths_relative_to']='workspace root'
    manifest['user_scope_note']='User confirmed on 2026-10-19 that missing MP3 files should not block image extraction; images must correspond to printed audio track IDs.'
    (INDEX/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    errors=[];image_count=0;page_count=0;audio_count=0
    doc=fitz.open(SOURCE);byid={r['id']:r for r in manifest['tracks']}
    assert len(byid)==196
    assert set(byid)=={f'CD{d}_{t:02}' for d in [1,2] for t in range(2,100)}
    # Distinct printed activities cannot share any unmasked source pixels.
    from PIL import ImageChops
    for a in SPECS:
        for b in SPECS:
            if a['source_pdf_page']!=b['source_pdf_page'] or a['track']>=b['track'] or a['region_id']==b['region_id']:continue
            masks=[]
            for row in [a,b]:
                mask=Image.new('1',(2000,2000));draw=ImageDraw.Draw(mask)
                x0,y0,x1,y1=row['crop_normalized']
                draw.rectangle([round(x0*2000),round(y0*2000),round(x1*2000)-1,round(y1*2000)-1],fill=1)
                for ex in row.get('exclude_normalized',[]):
                    draw.rectangle([round(ex[0]*2000),round(ex[1]*2000),round(ex[2]*2000),round(ex[3]*2000)],fill=0)
                masks.append(mask)
            if ImageChops.logical_and(*masks).getbbox():errors.append(f"Overlapping activities: CD{a['disc']}_{a['track']} / {b['track']}")
    assert len(SPECS)==196
    for sec in SECTIONS:
        folder=UNITS/(sec['name']+' - Audio Pages')
        local=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        expected=[s for s in SPECS if sec['start']<=s['source_pdf_page']<=sec['end']]
        if len(list((folder/'tracks').glob('*.png')))!=len(expected):errors.append(sec['name']+': extra/missing PNG')
        if len(local['tracks'])!=len(expected):errors.append(sec['name']+': local manifest count')
        for i in range(sec['start'],sec['end']+1):
            with Image.open(folder/'pages'/f'PDF-{i:03}.png') as im:
                pix=doc[i-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
                if im.size!=(pix.width,pix.height) or im.convert('RGB').tobytes()!=pix.samples:errors.append(f'Full page PDF {i}: differs from source')
            page_count+=1
        for r in local['tracks']:
            globalrow=byid[r['id']]
            if r['source_pdf_page']!=globalrow['source_pdf_page']:errors.append(r['id']+': inconsistent source page')
            with Image.open(folder/r['page_image']) as page:
                w,h=page.size;expected_crop=page.crop(r['crop_pixels'])
                for ex in r.get('exclude_normalized',[]):
                    b=r['crop_pixels'];eb=[round(ex[0]*w)-b[0],round(ex[1]*h)-b[1],round(ex[2]*w)-b[0],round(ex[3]*h)-b[1]]
                    ImageDraw.Draw(expected_crop).rectangle(eb,fill='white')
                with Image.open(folder/r['image']) as actual:
                    if actual.size!=tuple(r['image_size']) or actual.tobytes()!=expected_crop.tobytes():errors.append(r['id']+': crop mismatch')
            image_count+=1
            if r['audio']:
                target=folder/r['audio'];src=ROOT/r['source_audio']
                if hashlib.sha256(target.read_bytes()).hexdigest()!=r['audio_sha256'] or target.read_bytes()!=src.read_bytes():errors.append(r['id']+': MP3 changed')
                if r['duration_seconds']<=0:errors.append(r['id']+': invalid duration')
                audio_count+=1
            else:
                if not (r['disc']==1 and 31<=r['track']<=40 and r['audio_status']=='missing_source'):errors.append(r['id']+': unexpected missing audio')
            for field in ['image','page_image']:
                if not (UNITS/globalrow[field]).exists():errors.append(r['id']+': global link '+field)
        # Check preview script syntax without executing page content in the shell.
        text=(folder/'index.html').read_text(encoding='utf-8')
        script=re.search(r'<script>([\s\S]*?)</script>',text).group(1)
        result=subprocess.run(['node','--check','--input-type=commonjs'],input=script,text=True,encoding='utf-8',capture_output=True)
        if result.returncode:errors.append(sec['name']+': JS syntax '+result.stderr)
        if text.count('<option')>0:errors.append(sec['name']+': unexpected duplicate selector data')
        for file in ['README.md','index.html']:
            content=(folder/file).read_text(encoding='utf-8')
            targets=re.findall(r'\]\(([^)]+)\)',content) if file.endswith('.md') else re.findall(r'href="([^"#]+)"',content)
            for target in targets:
                if target.startswith(('http:','https:')) or '__' in target:continue
                if not (folder/unquote(target.split('#')[0])).exists():errors.append(sec['name']+': broken link '+target)
    assert page_count==72
    assert image_count==196
    assert audio_count==186
    report=dict(status='passed' if not errors else 'failed',scope='All 8 Units and 4 Reviews in Let_s Go 1/Units; original PDF pages 3–74',page_images=page_count,track_images=image_count,mapped_audio_track_ids=196,discs={'CD1':'02–99','CD2':'02–99'},source_mp3_copies=audio_count,missing_source_mp3=manifest['missing_audio'],missing_mp3_blocks_image_completion=False,excluded_intro_track_ids=['CD1_01','CD2_01'],checks=['Distinct printed activities have no overlapping unmasked crop pixels','72 full-page PNGs pixel-identical to original PDF renders','196 unique track IDs cover CD1/CD2 02–99 exactly once','196 PNG crops match recorded source regions and neighbouring-region clipping','all section manifests and asset paths resolve','186 copied MP3s byte-identical to source; source-missing MP3s explicitly flagged','all 12 preview scripts pass JavaScript syntax checks'],visual_review={'source_pages_mapped':72,'method':'Printed CD icons checked on all source page contact sheets; per-activity rectangles reviewed on boundary overlays; final crop samples reviewed including dialogue, song, action, alphabet, practice and review layouts.','original_scan_limitations':'Some source pages already have clipped text at the outer page edge. Extracts preserve source content; missing original scan content is not invented.'},errors=errors)
    (INDEX/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':validate()
