"""Assemble only reviewed built-in ImageGen regions for Unit 8."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent
B=ROOT/'assets/batches'
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
# Explicit measured gutters; boxes are [left,top,right,bottom].
selected={
54:('repair54tail',(0,0,1254,1254)),
55:('batch1-fix1',(630,1,1253,624)),
56:('batch1-fix1',(1,631,624,1253)),
57:('batch1-fix1',(630,631,1253,1253)),
58:('batch2',(1,1,626,621)),
59:('batch2',(631,1,1253,621)),
60:('batch2',(1,626,626,1253)),
61:('repair6162',(1,1,885,886)),
62:('repair6162',(889,1,1773,886)),
63:('batch3',(630,2,1252,663)),
64:('batch3',(2,668,625,1252)),
65:('repair6566',(1,1,885,886)),
66:('repair6566',(889,1,1773,886)),
67:('batch4',(630,1,1253,625)),
68:('repair68',(0,0,1254,1254)),
69:('repair69',(0,0,1254,1254))}
lyrics=["Let's play.","OK!","Let's play.","OK, OK!","Let's play, let's play.","OK, let's play!","Let's play tag.","OK, let's play, let's play!","Let's jump rope.","OK, OK, let's play!","Let's play ball.","OK, let's play, let's play!","Hey, let's play, let's play!","OK!"]
vocab1=['1. ride a bicycle','2. sing a song','3. fly a kite','4. bounce a ball']
vocab2=['1. swim','2. smile','3. wink','4. dance']
commands=['1. Point to the board.','2. Go to the board.']
abilities=['I can fly a kite.',"I can't fly a kite."]
dialogs=['Can you dance?','Yes, I can.','Can you dance?', "No, I can't."]
game=['GO','Jump','Stand up','Make a circle','Sit down','Walk','Move ahead 2 spaces','Go to the board','Skip','Point to the board','Make a line','Move back 3 spaces','Run','STOP']
texts={54:["Let's play.","OK. Let's play ball.","OK. Let's play tag.","OK. Let's jump rope."],55:["1. Let's play.","________________.","2. ________________.","OK. Let's jump rope."],56:["Let's Play"]+lyrics,57:commands,58:commands,59:['I can ride a bicycle.']+vocab1,60:vocab1,61:abilities,62:abilities,63:['Can you swim?', "No, I can't."]+vocab2,64:vocab2,65:dialogs,66:dialogs,67:[' '.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),' '.join('abcdefghijklmnopqrstuvwxyz')],68:['1. X x','fox','2. Y y','yarn','3. Z z','zebra','C. Find the letters.'],69:['Can you jump?','Yes, I can.']+game}
notes={
54:'Four exact invitations/replies; speaker tails now identify striped boy, yellow-shirt girl, navy-shirt boy, red-dress girl. Rearranged as separate comic panels.',
55:'Two numbered situations; original reply/prompt blanks retained without scanned handwritten answers; periods restored; soccer ball and jump rope, correct speakers.',
56:'All 14 printed lyric lines checked word by word; title retained; curly-haired boy playing tag with blonde glasses girl red dress.',
57:'Pointing girl and walking striped boy distinguished; both numbered board commands retained.',
58:'Source heading only: reused two classroom commands from D on same PDF page; no new commands.',
59:'All four numbered actions correct; pink bicycle helmeted girl, singing boy, orange kite boy, basketball bouncing girl; cat bicycle sentence retained.',
60:'Source heading only: reused four labeled action pictures from A on same PDF page.',
61:'Both can/cannot kite examples; four numbered same-child thought pairs, eight activities checked; tangled kite and fallen bicycle negative; same orange-shirt girl bicycle and unsuccessful singing.',
62:'Source heading only: reused page67 sentences and eight thought scenes; no invented chant words.',
63:'All four numbered actions; swim, smile both eyes open, wink exactly one eye shut, dance; gray/orange cat swim question and negative reply retained.',
64:'Source heading only: reused four labeled pictures from A same page; wink single eye; swim/smile/dance distinct.',
65:'Both dance exchanges correct speaker and positive/negative; all eight numbered thought scenes and four portraits; unable-to-swim child on dry pool edge with ring.',
66:'Source heading only: reused same page69 question/answer scenes and eight numbered activities; no invented chant.',
67:'All 26 uppercase and 26 lowercase glyphs checked in order; X Y Z and x y z red; no invented song lyrics.',
68:'X x fox, Y y blue yarn, Z z zebra; 1-3 labels; Find the letters zoo scene fox/green yarn and zebra/children retained; answers unmarked.',
69:'Both dialogue speakers checked; all14 board spaces and sequence retained, circle5 children, line4 children; ahead2 and back3 match PDF; full continuous board, stopping distinct from running.'}
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for d in ['pages/png','pages/webp']:(ROOT/d).mkdir(parents=True,exist_ok=True)
for item in m['items']:
 n=int(item['track'].split('_')[1]);batch,box=selected[n]
 with Image.open(B/(batch+'.png')) as sheet:
  assert box[2]<=sheet.width and box[3]<=sheet.height
  sheet.convert('RGB').crop(box).save(ROOT/('assets/'+item['track']+'-lesson.png'))
 item.update(layers=[{'type':'image','asset':'assets/'+item['track']+'-lesson.png','box':[0,0,1200,1200]}],status='reviewed',visual_review=notes[n],generation_batch=batch,source_crop_box=list(box),
 lesson_specs={'printed_text':texts[n],'source_page':item['unit_pdf_page'],'adjustment':notes[n] if n in [54,55,58,60,62,64,66] else 'Redrawn illustrations; retained printed content.'})
 item['canvas']['size']=[1200,1200]
 job=json.loads((B/(batch+'.json')).read_text(encoding='utf-8'))
 job.setdefault('selected_regions',{})[item['track']]={'box':list(box),'visual_review':notes[n]}
 job.update(status='reviewed_selected_regions',sheet_size=list(Image.open(B/(batch+'.png')).size),sha256=hashlib.sha256((B/(batch+'.png')).read_bytes()).hexdigest(),result_file=batch+'.png')
 write(B/(batch+'.json'),job)
m['assembly_helper']='assemble_unit8.py'
m['visual_review_scope']='All selected generated regions inspected against source; final rendered pages require final review.'
write(ROOT/'manifest.json',m)
write(ROOT/'lesson_specs.json',{p['track']:p['lesson_specs'] for p in m['items']})
print('Assembled 16 selected generated regions; no source art used as lesson image.')

