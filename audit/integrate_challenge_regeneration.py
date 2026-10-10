"""Integrate the visually reviewed 18 regenerated masters; retain restorable prior cards."""
import json,hashlib,shutil,math,os
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/'audit/challenge-regeneration-staging'
BACKUP=ROOT/'audit/challenge-regeneration-backup'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
index=read(ROOT/'parallel-prompts/challenge-images/regenerate-12/batch-index.json')
assert not (BACKUP/'integration.json').exists(),'Already integrated: do not run again blindly.'
qa_notes={
1:'Eight complete toys, correct source designs/colors; rope handles and yo-yo string intact; four correct paint swatches.',
2:'Six correct swatches including white outline; red train, blue ball, brown teddy, green yo-yo/car, red apple. Yo-yo loop and car bumper crop rechecked separately.',
3:'Bird/cat/dog full silhouettes; eight precise shapes plus blue square; square sides equal, rectangle elongated, diamond a rhombus.',
4:'Five colored shapes, egg, live fish, complete gorilla; dot groups exactly 1,2,3,4.',
5:'Counts individually checked: 5 dots,5 rings,6 triangles,7 stars,8 circles,9 hearts,10 squares,3 cars,4 teddies,7 cars; igloo and rope complete.',
6:'Kangaroo/lion complete; single/pair dog,cat,bird,cow,rabbit counts and species designs match; actual whitespace crop protects all ears/tails/feet.',
7:'Duck counts1/2/3, bird count3, cow count8, car count8; octopus eight arms; moon/nest/peach/icecream/pizza correct. Adjacent pizza fragment excluded from icecream.',
8:'Correct food set including fish fillet rather than live fish; queen, rabbit, sun, tiger, two birds, girl visibly liking milk.',
9:'Same body character; target highlights correctly identify head, both shoulders/knees/toes/eyes/ears, mouth/nose; touch head/nose/both eyes correct; five toes on each close-up foot.',
10:'Watch is wristwatch; bicycle pedaling, singing, flying kite, bouncing ball, swimming/dancing distinct; smile both eyes open, wink exactly one eye shut.',
11:'Negative kite same child and orange kite grounded with slack string; playing ball/tag/jumping rope distinct; fox/yarn/zebra full; closed four-child circle and straight line; review toys match reference.',
12:'Review ball/colors and school supplies correct; paint/glue contain no vocabulary label; same child/chair standing versus seated clearly distinct.',
13:'Girl approaches teacher versus turning; circle/square/star/heart/triangle/diamond/oval correct; walking versus running; green pedestrian signal correct.',
14:'Red STOP hand corrected by full-batch retry; pencil out/up versus away/down, open versus shut book; triangle counts2,3,4,5,6,7 and four diamonds checked.',
15:'Diamond counts5/6/7, five circles, seven ovals; cat counts1/3/4; rabbit counts1/2/5; icecream correct.',
16:'Cake/bread/rice correct; skip alternating legs versus jump paired legs; line versus closed circle; sunny/cloudy/windy/rainy/snowy cues distinct.',
17:'Wink/touch knees correct; same girl toes contact versus large gap; ride/fly/swim/dance/stamp/clap/point board/stand distinct and complete.',
18:'Calendar cues exact digits1 through7 in source colors, no weekday answer names; five empty slots not exported.'}
cards={};old_hashes={};total_bytes=0
# Protect all source Markdown, original lesson images/audio and other files outside challenge-assets.
units=ROOT/'Let_s Go Begin/Units'
baseline={str(p.relative_to(ROOT)):sha(p) for p in units.rglob('*') if p.is_file() and 'challenge-assets' not in p.parts}
write(BACKUP/'protected-source-hashes.json',baseline)
for name in ['challenge-visual-review.json','challenge-images-completion.json','challenge-images-completion.md','challenge-generation-provenance-index.json']:
    p=ROOT/'audit'/name
    if p.exists():shutil.copy2(p,BACKUP/name)
for b in index['batches']:
    out=STAGE/f"batch-{b['batch']:02}";exp=read(out/'export.json')
    assert len(exp['assets'])==len(b['cards']) and (out/'master.png').exists() and (out/'prompt.txt').exists()
    log=dict(batch=b['batch'],tool='built-in image_gen',calls=2 if b['batch']==14 else 1,accepted_master='master.png',master_dimensions=exp['master_size'],rows=3,columns=4,occupied_cells=len(b['cards']),blank_cells=12-len(b['cards']),prompt_file='prompt.txt',source_reference_paths=sorted({r for a in b['cards'] for r in a['references']}),actual_crop_boxes=[a['crop_box'] for a in exp['assets']],visual_review=dict(status='pass',method='Root inspected every decoded compressed card at 512px in lossless full-size QA grids; targeted crop repairs viewed separately',notes=qa_notes[b['batch']]),retry_reason='First full batch rejected: STOP displayed red walking person instead of red hand' if b['batch']==14 else None)
    write(out/'generation-log.json',log)
    for a in exp['assets']:
        f=out/'webp'/f"{a['id']}.webp"
        with Image.open(f) as im:assert im.format=='WEBP' and im.size==(512,512);im.load()
        assert f.stat().st_size<=61440
        a.update(sha256=sha(f),visual_review=dict(status='pass',notes=qa_notes[b['batch']]))
        cards[a['id']]=(b,out,a);total_bytes+=f.stat().st_size
    exp['status']='visual_review_pass';write(out/'export.json',exp)
assert len(cards)==211 and len({a['sha256'] for _,_,a in cards.values()})==211
review={'reviewer':'root','method':'Every final WebP decoded and inspected at 512px in original-resolution grids; repairs separately rechecked','cards':{}}
for ip in sorted((ROOT/'parallel-prompts/challenge-images').glob('*.inventory.json')):
    inv=read(ip);folder=Path(inv['lesson_folder'])/'challenge-assets';setname=ip.stem.replace('.inventory','');backup=BACKUP/setname
    for name in ['manifest.json','question-image-map.json','validation.json','README.md','contact-sheet.jpg']:
        shutil.copy2(folder/name,backup/name) if backup.exists() else (backup.mkdir(parents=True),shutil.copy2(folder/name,backup/name))
    manifest=read(folder/'manifest.json');new=[]
    for old in manifest['assets']:
        aid=old['id'];b,stage,a=cards[aid];dest=folder/'webp'/f'{aid}.webp'
        old_hashes[aid]=sha(dest);assert old_hashes[aid]!=a['sha256'],aid
        (backup/'webp').mkdir(exist_ok=True);shutil.copy2(dest,backup/'webp'/dest.name)
        shutil.copy2(stage/'webp'/dest.name,dest)
        qa=dict(sha256=a['sha256'],status='pass',notes=qa_notes[b['batch']],evidence=str((stage/'qa-512.png').relative_to(ROOT)))
        review['cards'][aid]=qa
        keep={k:v for k,v in old.items() if k in ['id','brief','semantic','uses','references','required','kind','shape','count','adaptation_notes','fixed_cue_uses']}
        master_rel=os.path.relpath(stage/'master.png',folder).replace('\\','/')
        keep.update(file=f'webp/{aid}.webp',webp=f'webp/{aid}.webp',files=[f'webp/{aid}.webp'],creation_method='built_in_image_gen',method='built_in_image_gen',format='WEBP',dimensions=[512,512],quality=a['quality'],webp_method=6,file_bytes=a['bytes'],sha256=a['sha256'],batch=master_rel,generated_master=master_rel,crop_box=a['crop_box'],source_crop_size=a['original_cell_size'],visual_review=qa,root_visual_review=qa,contains_text=aid.startswith('r78_day_'),provenance=dict(tool='built-in image_gen',batch=b['batch'],generation_log=os.path.relpath(stage/'generation-log.json',folder).replace('\\','/'),source_references=b['cards'][next(i for i,c in enumerate(b['cards']) if c['id']==aid)]['references'],resized_from=a['original_cell_size'],upscaled=max(a['original_cell_size'])<512))
        new.append(keep)
    manifest['assets']=new
    manifest['format']=dict(width=512,height=512,format='webp',quality=80,method=6,target_bytes=61440)
    manifest['root_final_audit']=dict(all_cards_reviewed_at_512=True,file_hashes_bound_to_reviews=True,regenerated=True,webp_quality=80,webp_method=6,source_lessons_unchanged=True)
    manifest['regeneration']=dict(batch_capacity=12,total_batches=18,last_batch_occupied=7,old_cards_backup=str(backup/'webp'),masters_location=str(STAGE),active_format='WebP only; older masters/optional PNGs are historical references')
    write(folder/'manifest.json',manifest)
    sheet=Image.new('RGB',(1200,math.ceil(len(new)/6)*240),'white');draw=ImageDraw.Draw(sheet)
    for i,a in enumerate(new):
        x=i%6*200;y=i//6*240;sheet.paste(Image.open(folder/a['file']).resize((200,200)),(x,y));draw.text((x+3,y+204),a['id'],fill='black')
    sheet.save(folder/'contact-sheet.jpg',quality=90)
    validation=read(folder/'validation.json')
    # Retain source coverage/context facts, replace all generation/export facts.
    for k in ['provenance','root_final_doll_repair','compression','visual_review','root_final_audit']:
        validation.pop(k,None)
    validation.update(complete=True,missing=[],asset_count=len(new),webp_count=len(new),dimensions=dict(expected=[512,512],all_pass=True),compression=dict(quality=80,method=6,target_bytes=61440,over_target=[],bytes={a['id']:a['file_bytes'] for a in new}),provenance=dict(built_in_image_gen=len(new)),visual_review=dict(reviewed_at_512=True,content_pass=True,method=review['method']),root_final_audit=dict(card_count=len(new),all_visual_reviews_pass=True,all_dimensions=[512,512],all_links_exist=True,max_bytes=max(a['file_bytes'] for a in new),over_60kb=[],unique_hashes=len(new),contact_sheet_regenerated_from_final_webps=True))
    write(folder/'validation.json',validation)
    (folder/'README.md').write_text(f"# Challenge — {setname}\n\nBộ đang dùng: {len(new)} ảnh WebP 512×512, regenerate từ master 12 ô/lần bằng built-in image_gen. Mọi ảnh ≤60 KiB, đã kiểm nội dung và vùng cắt sau nén ở 512px. Preview và question-image-map giữ nguyên câu hỏi/đáp án; ảnh không có nhãn đáp án. Thẻ ngày chỉ giữ số cue1–7 theo nguồn.\n\nManifest ghi batch/master, crop box, kích thước ô gốc, bytes/hash và QA. Master1448×1086 có ô khoảng350px nên có upscale khi xuất512; không coi upscale là tăng chi tiết. Ảnh vẫn rõ ở512 và kích thước thẻ thực tế.\n\nMaster và prompt: `{STAGE}`. Bản cũ để khôi phục: `{backup}`. Ảnh PNG/master cũ trong references/batches là lịch sử, không phải ảnh đang dùng; preview chỉ dùng WebP mới. Audio Challenge do chủ dự án bổ sung.\n",encoding='utf-8')
write(ROOT/'audit/challenge-visual-review.json',review)
assert all(sha(ROOT/p)==h for p,h in baseline.items()),'Protected source changed'
write(BACKUP/'integration.json',dict(status='complete',old_hashes=old_hashes,new_hashes={aid:a['sha256'] for aid,(_,_,a) in cards.items()}))
report=dict(status='integrated',assets=211,sets=12,batches=18,generation_calls=19,retried_batches=[14],full_batches=17,last_batch_assets=7,last_batch_blank_cells=5,all_dimensions=[512,512],format='WEBP',total_bytes=total_bytes,max_bytes=max(a['bytes'] for _,_,a in cards.values()),duplicate_ids=[],duplicate_hashes=[],missing=[],all_replaced=True,protected_source_files=len(baseline),protected_source_hashes_unchanged=True,source_resolution_note='Masters1448x1086; card crops roughly350px, upscaled with contain to512',visual_review='pass at512px',backup=str(BACKUP),masters=str(STAGE))
write(ROOT/'audit/challenge-regeneration-completion.json',report)
print(json.dumps(report,ensure_ascii=False))
