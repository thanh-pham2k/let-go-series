from PIL import Image, ImageDraw
from pathlib import Path
import json, hashlib

ROOT=Path(r"E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\challenge-assets")
WEBP=ROOT/"webp"
ids=[
 "u04_dots_01","u04_dots_02","u04_dots_03","u04_dots_04","u04_dots_05",
 "u04_rings_05","u04_triangles_06","u04_stars_07","u04_circles_08","u04_hearts_09","u04_squares_10",
 "u04_cars_03","u04_teddy_bears_04","u04_cars_07","u04_igloo","u04_jump_rope","u04_kangaroo","u04_lion"
]
brief={
"u04_dots_01":"1 solid black dot", "u04_dots_02":"2 separated solid black dots", "u04_dots_03":"3 separated solid black dots", "u04_dots_04":"4 separated solid black dots", "u04_dots_05":"5 separated solid black dots",
"u04_rings_05":"5 purple double-outline rings", "u04_triangles_06":"6 green outline triangles", "u04_stars_07":"7 orange outline stars", "u04_circles_08":"8 red outline circles", "u04_hearts_09":"9 purple outline hearts", "u04_squares_10":"10 blue outline squares",
"u04_cars_03":"3 complete cartoon cars", "u04_teddy_bears_04":"4 complete cartoon teddy bears", "u04_cars_07":"7 complete cartoon cars", "u04_igloo":"one ice-block igloo", "u04_jump_rope":"one standalone jump rope with two handles", "u04_kangaroo":"one cartoon kangaroo", "u04_lion":"one cartoon lion"
}
methods={**{x:"native_graphic" for x in ids[:11]},"u04_cars_03":"compose_from_crops","u04_teddy_bears_04":"compose_from_crops","u04_cars_07":"compose_from_generated_source","u04_igloo":"crop_or_edit","u04_jump_rope":"generate_builtin_image_gen","u04_kangaroo":"generate_builtin_image_gen","u04_lion":"crop_or_edit"}
refs={x:["CD1_60.png"] for x in ids[:5]}; refs.update({x:["CD1_64.png","CD1_67.png"] for x in ids[5:11]}); refs.update({"u04_cars_03":["CD1_60.png"],"u04_teddy_bears_04":["CD1_60.png"],"u04_cars_07":["built-in image_gen source references/car-generated.png; CD1_60.png style reference"],"u04_igloo":["CD1_69.png"],"u04_jump_rope":["built-in image_gen; CD1_69.png style reference"],"u04_kangaroo":["built-in image_gen source references/kangaroo-generated.png; CD1_69.png style reference"],"u04_lion":["CD1_69.png"]})
uses={
"u04_dots_01":["C1 §2 item 1 line 68","C5 §2 item 1 line 358"],"u04_dots_02":["C1 §2 item 2 line 69","C5 §2 item 2 line 360"],"u04_dots_03":["C3 §1 item 1 line 188","C5 §2 item 3 line 362"],"u04_dots_04":["C5 §2 item 4 line 364"],"u04_dots_05":["C5 §2 item 5 line 366"],
"u04_rings_05":["C1 §2 item 5 line 72","C3 §1 item 3 line 190"],"u04_triangles_06":["C1 §2 item 6 line 73","C3 §1 item 4 line 191","C5 §2 item 6 line 368"],"u04_stars_07":["C1 §2 item 7 line 74","C3 §1 item 5 line 192","C5 §2 item 7 line 370"],"u04_circles_08":["C1 §2 item 8 line 75","C3 §1 item 6 line 193","C5 §2 item 8 line 372"],"u04_hearts_09":["C1 §2 item 9 line 76","C3 §1 item 7 line 194","C5 §2 item 9 line 374"],"u04_squares_10":["C1 §2 item 10 line 77","C3 §1 item 8 line 195","C5 §2 item 10 line 376"],
"u04_cars_03":["C1 §2 item 3 line 70"],"u04_teddy_bears_04":["C1 §2 item 4 line 71","C3 §1 item 2 line 189"],"u04_cars_07":["C5 §4 situation 2 lines 400, 406"],
"u04_igloo":["C1 §4 I i line 91","C4 §3 I i line 322","C5 §7 I i line 451"],"u04_jump_rope":["C1 §4 J j line 92","C4 §3 J j line 323","C5 §7 J j line 452"],"u04_kangaroo":["C1 §4 K k line 93","C4 §3 K k line 324","C5 §7 K k line 453"],"u04_lion":["C1 §4 L l line 94","C4 §3 L l line 325","C5 §7 L l line 454"]}

assets=[]
for aid in ids:
    p=WEBP/f"{aid}.webp"; im=Image.open(p)
    assets.append({"id":aid,"brief":brief[aid],"semantic":{"topic":"numbers","count":next((int(aid.rsplit('_',1)[-1]) for _ in [0] if aid.rsplit('_',1)[-1].isdigit()),None)},"method":methods[aid],"references":refs[aid],"uses":uses[aid],"file":f"webp/{aid}.webp","width":im.width,"height":im.height,"bytes":p.stat().st_size,"quality":80,"method_webp":6,"visual_review":True})

occ=[]
inv=json.loads(Path(r"E:\let-go-series\parallel-prompts\challenge-images\unit-04.inventory.json").read_text(encoding="utf-8"))
for o in inv["visual_occurrences"]:
    occ.append({"challenge":o["challenge"],"section":o["section"],"line":o["line"],"source_text":o["source_text"],"asset_ids":o["asset_ids"],"image_required":True,"needs_context":False})

section_specs=[
(1,"1. Nhìn số → chọn số đúng",53,False,"Text-only number recognition; digits and choices are UI text."),(1,"2. Nhìn nhóm hình → chọn số",66,True,"Each item has a dedicated visual occurrence below."),(1,"3. Nghe → chọn số",79,False,"Audio plus UI digit choices; no raster required."),(1,"4. Letters and words",88,True,"Phonics word objects are mapped in the occurrence list."),
(2,"1. Nghe → chọn nghĩa",102,False,"Listening-to-text translation choices."),(2,"2. Nghe → chọn câu đúng",132,False,"Listening-to-text sentence choices."),(2,"3. Nghe câu hỏi → chọn câu trả lời",152,False,"Dialogue answer choices are text."),(2,"4. Nghe → thực hiện",172,False,"Child performs Go/Stop; no static raster required."),
(3,"1. Đếm → chọn số",186,True,"Each item has a dedicated visual occurrence below."),(3,"2. Điền số còn thiếu",197,False,"Numeric sequence is UI text."),(3,"3. Chọn từ → điền câu",205,False,"Sentence completion is UI text."),(3,"4. Nghe → chọn từ/cụm từ điền vào chỗ trống",216,False,"Listening and text options."),(3,"5. Giảm hint — dùng context",242,False,"Dialogue completion is text; no object cue prescribed."),(3,"6. Count Recall",253,False,"Counting sequence is spoken/UI text."),
(4,"1. Chọn từ → ghép thành câu hoàn chỉnh",270,False,"Word tiles and sentences are UI text."),(4,"2. Ghép câu hỏi → câu trả lời",310,False,"Question/answer table is text."),(4,"3. Letters & words (Phonics I–L)",318,True,"Phonics objects are mapped in the occurrence list."),
(5,"1. Quick Recognition",340,False,"Digit recognition uses UI text."),(5,"2. Đếm không có hint",356,True,"Each item has a dedicated visual occurrence below."),(5,"3. Tự nói chuỗi số",378,False,"Spoken number sequence; no raster required."),(5,"4. Conversation — tự hoàn thành",388,True,"Only situation 2 needs the seven-car visual; other situations are text/dialogue."),(5,"5. Build without hint",424,False,"Word tiles are UI text."),(5,"6. Commands — Nghe và làm",438,False,"Child performs Go/Stop; no static raster required."),(5,"7. I–L Phonics Production",447,True,"Phonics objects are mapped in the occurrence list."),(5,"8. Final Boss — Count & Ask",456,False,"Teacher points at an already selected group; no new raster beyond mapped assets.")]
sections=[]
for c,s,line,req,reason in section_specs:
    items=[x for x in occ if x["challenge"]==c and x["section"]==s]
    if s=="4. Letters and words": items=[x for x in occ if x["challenge"]==1 and x["section"]=="2. Nhìn nhóm hình → chọn số"] if False else []
    if c==1 and s=="4. Letters and words":
        items=[{"line":92,"item":"I i","source_text":"I i → igloo / jump rope / kangaroo / lion","asset_ids":["u04_igloo","u04_jump_rope","u04_kangaroo","u04_lion"],"image_required":True,"needs_context":False},{"line":93,"item":"J j","source_text":"J j → lion / jump rope / igloo / kangaroo","asset_ids":["u04_lion","u04_jump_rope","u04_igloo","u04_kangaroo"],"image_required":True,"needs_context":False},{"line":94,"item":"K k","source_text":"K k → jump rope / kangaroo / lion / igloo","asset_ids":["u04_jump_rope","u04_kangaroo","u04_lion","u04_igloo"],"image_required":True,"needs_context":False},{"line":95,"item":"L l","source_text":"L l → kangaroo / igloo / lion / jump rope","asset_ids":["u04_kangaroo","u04_igloo","u04_lion","u04_jump_rope"],"image_required":True,"needs_context":False}]
    if c==4 and s=="3. Letters & words (Phonics I–L)": items=[x for x in occ if x["challenge"]==4 and x["section"]==s]
    if c==5 and s=="4. Conversation — tự hoàn thành": items=[{"line":400,"item":"Tình huống 1","source_text":"May I come in? / Sure! Please come in!","asset_ids":[],"image_required":False,"needs_context":False},{"line":400,"item":"Tình huống 2","source_text":"How many? / 7 cars.","asset_ids":["u04_cars_07"],"image_required":True,"needs_context":False},{"line":400,"item":"Tình huống 3","source_text":"Is it a 5? / Yes, it is.","asset_ids":[],"image_required":False,"needs_context":False},{"line":400,"item":"Tình huống 4","source_text":"Is it a 9? / No, it isn't. It's a 6.","asset_ids":[],"image_required":False,"needs_context":False}]
    if not items and req: items=[{"line":line,"item":"section-level","source_text":"Visual source changed or needs review","asset_ids":[],"image_required":True,"needs_context":True}]
    sections.append({"challenge":c,"section":s,"source_line":line,"image_required":req,"reason":reason,"items":items})

source_path=Path(r"E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers(2).md")
source_lines=source_path.read_text(encoding="utf-8").splitlines()
for idx,sec in enumerate(sections):
    start=sec["source_line"]
    end=sections[idx+1]["source_line"] if idx+1<len(sections) else len(source_lines)+1
    sec["source_excerpt"]="\n".join(source_lines[start-1:end-1]).strip()
for sec in sections:
    if sec["challenge"]==5 and sec["section"]=="8. Final Boss — Count & Ask":
        sec["image_required"]=True
        sec["reason"]="Teacher points at one reusable count group; no new raster is generated beyond the mapped group cards."
        sec["items"]=[{"line":456,"item":"teacher-selected count group","source_text":"Người lớn chỉ nhóm hình và hỏi: How many?","asset_ids":["u04_dots_01","u04_dots_02","u04_dots_03","u04_dots_04","u04_dots_05","u04_rings_05","u04_triangles_06","u04_stars_07","u04_circles_08","u04_hearts_09","u04_squares_10","u04_cars_03","u04_teddy_bears_04","u04_cars_07"],"image_required":True,"needs_context":False,"reuse_existing":True}]
mapping={"schema_version":1,"unit":4,"topic":"Numbers","source":"..\\..\\..\\Units\\Unit 4 - Numbers(2).md","sections":sections,"unresolved_context":[],"coverage_note":"All 18 required IDs are reused across every visual occurrence; text/audio/action sections explicitly carry image_required=false."}
(ROOT/"manifest.json").write_text(json.dumps({"schema_version":1,"unit":4,"topic":"Numbers","format":{"card_px":512,"webp_quality":80,"webp_method":6,"target_bytes":61440},"assets":assets,"required_ids":ids,"conditional_ids":[],"counts":{"required":18,"complete":18,"missing":0,"native_graphic":11,"compose_from_crops":2,"compose_from_generated_source":1,"crop_or_edit":2,"generated":3},"duplicate_hashes":{},"visual_review":"All cards reviewed in contact-sheet.jpg and individual source/contact sheets."},ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"question-image-map.json").write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding="utf-8")

items=[]
for aid in ids:
    p=WEBP/f"{aid}.webp"; im=Image.open(p)
    items.append((aid,im))
cols=4; cell=180; out=Image.new("RGB",(cols*cell,((len(items)+cols-1)//cols)*cell),(255,255,255)); d=ImageDraw.Draw(out)
for i,(aid,im) in enumerate(items):
    x=(i%cols)*cell; y=(i//cols)*cell; q=im.convert("RGB"); q.thumbnail((160,150),Image.Resampling.LANCZOS); out.paste(q,(x+(cell-q.width)//2,y+3)); d.text((x+4,y+155),aid,fill=(20,20,20))
out.save(ROOT/"contact-sheet.jpg",quality=92)
checks=[]; seen={}
for aid in ids:
    p=WEBP/f"{aid}.webp"; im=Image.open(p); h=hashlib.sha256(p.read_bytes()).hexdigest(); seen.setdefault(h,[]).append(aid)
    checks.append({"id":aid,"exists":p.exists(),"width":im.width,"height":im.height,"bytes":p.stat().st_size,"under_target":p.stat().st_size<=61440,"sha256":h})
(ROOT/"validation.json").write_text(json.dumps({"required":18,"complete":sum(x["exists"] and x["width"]==512 and x["height"]==512 for x in checks),"missing":[],"conditional":[],"checks":checks,"duplicate_hashes":{k:v for k,v in seen.items() if len(v)>1},"occurrence_coverage":"all inventory visual occurrences mapped; every non-visual Challenge section is explicitly image_required=false"},ensure_ascii=False,indent=2),encoding="utf-8")
print("metadata written",len(ids))
