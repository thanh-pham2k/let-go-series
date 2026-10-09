from pathlib import Path
from PIL import Image
import json,shutil,hashlib,re
ROOT=Path(__file__).resolve().parent
UNITS=ROOT.parent
BOOK=UNITS.parent
def save(name,data):(ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for d in ['audio','pages/png','pages/webp','assets','references']:(ROOT/d).mkdir(parents=True,exist_ok=True)
data=json.loads((BOOK/'lets_go_audio_mapping.metadata').read_text(encoding='utf-8-sig'))
rows=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('source_pdf')=='Review 7-8.pdf' and isinstance(v.get('audio'),dict):rows.append(v)
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(data)
rows.sort(key=lambda r:r['audio']['track'])
assert [r['audio']['track'] for r in rows]==[70,71,72]
save('references/audio-mapping.json',{'source_file':'lets_go_audio_mapping.metadata','filter':'source_pdf == Review 7-8.pdf','items':rows})
shutil.copy2(UNITS/'Review 7-8.pdf',ROOT/'references/source.pdf')
doc=UNITS/'Review 7-8(2).md'
if not (ROOT/'references/challenge-original.md').exists():shutil.copy2(doc,ROOT/'references/challenge-original.md')
pairs=[
 {'number':1,'a':'One eye closed, other open: wink; green sweater red-haired boy points beside eye.','b':'Boy bends knees, both hands on knees; green sweater and blue trousers.'},
 {'number':2,'a':'Ponytailed girl bends with straight legs; fingertips contact shoe toes.','b':'Same girl bends; hands above shoes with visible gap: cannot reach toes.'},
 {'number':3,'a':'Child rides green bicycle with two wheels.','b':'Child flies red diamond kite on grass.'},
 {'number':4,'a':'Boy swims horizontally in blue pool with ladder.','b':'Boy dances beside pool, crossed arms and torso movement, red patterned shorts.'},
 {'number':5,'a':'Curly-haired child stamps feet, pink shirt and blue trousers.','b':'Same child claps hands at chest; pink shirt and blue trousers.'},
 {'number':6,'a':'Seated pupil points to green classroom board.','b':'Pupil stands upright before green classroom board, arms down.'}]
days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
specs={
 'CD2_70':{'source_title':'Units 7-8 Listen and Review','exercise':'A. Listen and circle.','pairs':pairs,'text':['1.','2.','3.','4.','5.','6.','a','b'],'original_audio_answers':'Unknown; no marked answers without an independent listening audit.'},
 'CD2_71':{'source_title':'Days of the Week','exercise':'A. Say these.','day_cards':[{'day':d,'number':i+1,'number_color':c} for i,(d,c) in enumerate(zip(days,['blue','green','yellow','orange-red','lavender','pink','teal-green']))],'model_sentence':"It's Monday.",'monthly_calendar_headers':['SUN.','MON.','TUES.','WEDS.','THUR.','FRI.','SAT.'],'monthly_rows':[[None,1,2,3,4,5,6],list(range(7,14)),list(range(14,21)),list(range(21,28)),[28,29,30,None,None,None,None]],'speaker':'red-haired child points to Monday column'},
 'CD2_72':{'source_title':'Days of the Week','exercise':"B. Let's sing.",'headers':[d.upper() for d in days],'calendar_rows':[list(range(1,8)),list(range(8,15))],'visual':'Green-shirt child holding yellow pointer to Wednesday header, purple backdrop, red headers.','printed_lyrics':None}}
questions=[
 {'prompt':'Ở cặp hình số 3, hình a minh họa hành động nào?','texts':['ride a bicycle','fly a kite','swim'],'answer':'A'},
 {'prompt':'Trong các thẻ ngày của mục Say these, Wednesday được ghi số nào?','texts':['3','4','5'],'answer':'B'},
 {'prompt':"Trong lịch của mục Let's sing, ô số 14 nằm dưới tên ngày nào?",'texts':['Thursday','Friday','Saturday'],'answer':'C'}]
notes=[
 'Recompose the twelve source options into six numbered a/b pairs with identical order. No source answer circles added; pair2 retains can/cannot reach toes. Additional quiz asks visible picture recognition, not unverified MP3 order.',
 'Retain seven day cards Sunday1 throughSaturday7, the printed model sentence, and the monthly calendar. The calendar dates and card numbers are separate source numbering systems; character may overlap dates as in source.',
 'Retain the source two-row calendar Sunday1 throughSaturday7 and Sunday8 throughSaturday14, plus child and pointer. No lyrics are printed in the PDF; none added or transcribed. Same source page as71, separate image and audio.']
items=[]
for r,q,note in zip(rows,questions,notes):
 num=r['audio']['track'];track='CD2_'+str(num);name='Track'+str(num)+'.mp3'
 audio_source=BOOK/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD2'/name
 assert audio_source.is_file()
 shutil.copy2(audio_source,ROOT/'audio'/name)
 assert (ROOT/'audio'/name).read_bytes()==audio_source.read_bytes()
 ref='references/'+track+'.png'
 im=Image.open(ROOT/'source-pages'/('page-'+str(r['pdf_page'])+'.png'))
 if num==70:box=(round(im.width*.04),round(im.height*.04),round(im.width*.97),round(im.height*.93))
 elif num==71:box=(round(im.width*.02),round(im.height*.04),round(im.width*.97),round(im.height*.62))
 else:box=(round(im.width*.02),round(im.height*.62),round(im.width*.97),round(im.height*.92))
 im.crop(box).save(ROOT/ref)
 items.append({'track':track,'audio_key':r['audio']['audio_key'],'exercise':r['exercise']+'. '+r['exercise_title'],'pdf_page':r['pdf_page'],'book_page':r['book_page'],'section':r['lesson_section'],'source_pdf':'Review 7-8.pdf','source_reference':ref,'source_region':{'path':'source-pages/page-'+str(r['pdf_page'])+'.png','box':list(box)},'audio_file':'audio/'+name,'audio_source':str(audio_source),'output':{'png':'pages/png/'+track+'.png','webp':'pages/webp/'+track+'.webp'},'canvas':{'size':[1200,1200],'background':'#FFFFFF'},'layers':[],'question':{'id':'R7-8-'+track,'prompt':q['prompt'],'choices':[{'id':chr(65+i),'text':t} for i,t in enumerate(q['texts'])],'correct_choice_id':q['answer'],'show_after_audio':True,'render_in_lesson_image':False},'adaptation_notes':note,'status':'pending_generation'})
m={'schema_version':'2.0','review':'7-8','topic':'Listen and Review / Days of the Week','source_pdf':'Review 7-8.pdf','source_pdf_reference':'references/source.pdf','source_pdf_sha256':hashlib.sha256((ROOT/'references/source.pdf').read_bytes()).hexdigest(),'source_pdf_page_count':2,'source_item_count':3,'image_count':3,'image_fit':'contain','coordinate_system':'pixel boxes [x,y,width,height], top-left origin','items':items,'lesson_specs':specs,'generation_policy':'Built-in image_gen only; three independent cells in2x2 batch with last blank; split along observed gutters then contain1200x1200.'}
save('manifest.json',m)
save('lesson_specs.json',specs)
save('generation.json',{'tool':'image_gen__imagegen','status':'generation_running','batches':['assets/batches/batch1.json'],'source_pages':['source-pages/page-1.png','source-pages/page-2.png'],'independent_audio_audit':False})
template=(UNITS/'Unit 2 - Colors - Lesson Pages/preview.html').read_text(encoding='utf-8')
template=re.sub(r'const manifest=.*?;\nconst pages=',r'const manifest=/*MANIFEST_JSON*/;\nconst pages=',template,count=1,flags=re.S)
assert '/*MANIFEST_JSON*/' in template
template=template.replace('Unit 2 · Colors','Review 7–8').replace('17 bài nghe','3 bài nghe')
(ROOT/'preview.template.html').write_text(template,encoding='utf-8')
print('Prepared exact3 mapping records, byte-identical audio copies, references, pending manifest and private template.')

