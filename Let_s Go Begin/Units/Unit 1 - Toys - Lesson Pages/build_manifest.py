"""Build portable per-track layout metadata from the Unit 1 source mapping."""
from pathlib import Path
import json, re, shutil

ROOT=Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/'source.metadata.json').read_text(encoding='utf-8'))
QUESTION_FILE=ROOT.parent/'Unit 1 - Toys - Cau hoi theo trang.md'
QUESTIONS=QUESTION_FILE.read_text(encoding='utf-8')
TOYS=['ball','jump-rope','yo-yo','bicycle','train','car','doll','teddy-bear']
TOY_WORDS={'ball':'a ball','jump-rope':'a jump rope','yo-yo':'a yo-yo','bicycle':'a bicycle','train':'a train','car':'a car','doll':'a doll','teddy-bear':'a teddy bear'}

def rect(box,fill='#F2F7FD',stroke=None,radius=18):
    return {'type':'rect','box':box,'fill':fill,'stroke':stroke,'radius':radius}

def text(value,box,size=34,center=False,bold=False,color='#25334A'):
    return {'type':'text','text':value,'box':box,'font_size':size,'align':'center' if center else 'left','bold':bold,'color':color}

def image(asset,box,semantic=None):
    value={'type':'image','asset':asset,'box':box,'fit':'contain'}
    if semantic:value['semantic']=semantic
    return value

def badge(value,x,y):
    return [rect([x,y,48,48],'#315AA6',radius=24),text(str(value),[x,y+7,48,34],27,True,True,'#FFFFFF')]

def panel_caption(value,box,size=30):
    x,y,w,h=box
    return [rect(box,'#FFFFFF','#B8CDDE'),text(value,[x+12,y+12,w-24,h-24],size,True)]

def header(item):
    return [rect([0,0,1200,105],'#EAF3FB',radius=0),text(item['exercise'],[40,30,920,55],40,bold=True),rect([1000,25,165,55],'#FFFFFF',radius=20),text(item['track'].replace('_',' '),[1007,38,150,40],27,True,True)]

def grid(items):
    layers=[]
    for i,toy in enumerate(items):
        x=40+(i%2)*590;y=140+(i//2)*580
        layers += [rect([x,y,530,550],'#FFFFFF','#DFE8F0'),image('assets/toys/'+toy+'.png',[x+25,y+20,480,450],{'object':toy,'number':i+1}),text(f'{i+1}. {TOY_WORDS[toy]}',[x+15,y+490,500,45],33,True)]
    return layers

def toy_row(items):
    layers=[];width=1120//len(items)
    for i,toy in enumerate(items):
        layers.append(image('assets/toys/'+toy+'.png',[40+i*width,130,width-10,260],{'object':toy,'order':i+1}))
    return layers

def marker_on_scene(n,rx,ry,box,asset):
    from PIL import Image
    with Image.open(ROOT/asset) as im:
        scale=min(box[2]/im.width,box[3]/im.height);w=int(im.width*scale);h=int(im.height*scale)
    x=box[0]+(box[2]-w)//2+int(rx*w);y=box[1]+(box[3]-h)//2+int(ry*h)
    return badge(n,x,y)

def question(track):
    match=re.search(rf'^## {track} .*?\n(.*?)(?=^## |\Z)',QUESTIONS,re.M|re.S)
    assert match,track
    block=match[1];prompt=re.search(r'^\*\*Câu hỏi:\*\* (.+)$',block,re.M)[1]
    choices=[{'id':letter,'text':value} for letter,value in re.findall(r'^- ([ABC])\. (.+)$',block,re.M)]
    row=next(line for line in QUESTIONS.splitlines() if line.startswith('| U1-'+track+' |'))
    answer=row.split('|')[-2].strip().split('.')[0]
    assert answer in [c['id'] for c in choices]
    return {'id':'U1-'+track,'prompt':prompt,'choices':choices,'correct_choice_id':answer,'show_after_audio':True,'render_in_lesson_image':False}

def main():
    (ROOT/'assets/toys').mkdir(parents=True,exist_ok=True);(ROOT/'audio').mkdir(exist_ok=True)
    for toy in TOYS:
        shutil.copy2(ROOT.parent/'Unit 1 - Toys - Visuals'/'originals'/(toy+'.png'),ROOT/'assets/toys'/(toy+'.png'))
    pages=[]
    for item in SOURCE['items']:
        track=item['track'];num=int(track[-2:]);layers=header(item);height=1050;reuse=[];notes=[];targets=[]
        if num==2:
            height=1080
            layers+=panel_caption("Hi, what's your name?",[45,125,640,75],36)
            layers+=panel_caption("I'm Kate.",[815,125,330,75],36)
            layers.append(image('assets/scenes/talk.png',[40,220,1120,820],{'characters':['Scott','Kate']}))
        elif num==3:
            height=660
            qs=["What's your name?","________________?","What's your name?"]
            answers=['________________.',"I'm Ginger.",'________________.']
            for i in range(3):
                x=40+i*390
                layers+=badge(i+1,x,125)
                layers+=panel_caption(qs[i],[x,190,350,65],26)
                layers.append(image('assets/scenes/pets.png',[x,275,350,180],{'panel':i+1,'characters':['Ginger','gray cat']}))
                layers+=panel_caption(answers[i],[x,495,350,65],28)
            notes.append('Third response blank is supplied to complete the practice panel whose source crop cuts off the response area. Blanks remain blank.')
        elif num==4:
            height=1060
            layers.append(image('assets/scenes/song.png',[20,115,1160,820],{'characters':['Kate','Jenny','Scott','Andy']}))
            layers.append(text("Hi, What's Your Name?",[330,220,550,50],34,True,True,'#B1426E'))
            lyrics="Hi, what's your name?\nI'm Kate.\nHi, what's your name?\nI'm Jenny.\nHi, what's your name?\nI'm Scott.\nHi, what's your name?\nI'm Andy.\n\nKate, Jenny, Scott, Andy—\nKate, Jenny, Scott, Andy—\nJenny, Andy, Jenny, Andy—\nKate, Jenny, Scott!"
            layers += [rect([335,280,530,555],'#EEF9FB',radius=18),text(lyrics,[350,295,500,525],27,True)]
            for name,box in [('Kate',[45,155,245,45]),('Jenny',[45,890,245,45]),('Scott',[920,155,245,45]),('Andy',[920,890,245,45])]: layers+=panel_caption(name,[box[0],box[1],box[2],65],28)
        elif num in [5,6]:
            height=740
            layers.append(image('assets/scenes/move.png',[40,155,1120,465],{'left_action':'stand up','right_action':'sit down'}))
            layers+=panel_caption('1. Stand up.',[45,635,530,65],36)
            layers+=panel_caption('2. Sit down.',[625,635,530,65],36)
            if num==6:
                reuse=['CD1_05'];notes.append('Source E crop has only the instruction/icon; standing/sitting visuals from D on the same page are included for audio practice.')
        elif num in [7,8,11,12]:
            height=1320;toys=TOYS[:4] if num in [7,8] else TOYS[4:];layers+=grid(toys)
            targets=[{'number':i+1,'object':toy} for i,toy in enumerate(toys)]
            if num in [8,12]:reuse=[f'CD1_{num-1:02d}']
        elif num==9:
            height=1320;box=[40,225,1120,1050];asset='assets/scenes/playground.png'
            layers+=panel_caption("It's a yo-yo.",[410,125,380,75],36);layers.append(image(asset,box))
            positions=[(1,'yo-yo',.53,.48),(2,'ball',.38,.74),(3,'jump-rope',.12,.67),(4,'bicycle',.80,.63)]
            for n,obj,x,y in positions:
                layers+=marker_on_scene(n,x,y,box,asset);targets.append({'number':n,'object':obj,'marker_source_fraction':[x,y]})
        elif num in [10,14]:
            height=440;toys=['yo-yo','ball','jump-rope','bicycle'] if num==10 else ['ball','teddy-bear','doll','train','bicycle'];layers+=toy_row(toys)
            targets=[{'order':i+1,'object':toy} for i,toy in enumerate(toys)]
        elif num==13:
            height=1320;box=[40,225,1120,1050];asset='assets/scenes/shop.png'
            layers+=panel_caption('What is it?',[45,125,370,75],36)
            layers+=panel_caption("It's a teddy bear.",[645,125,510,75],36);layers.append(image(asset,box))
            positions=[(1,'teddy-bear',.50,.20),(2,'train',.29,.71),(3,'doll',.90,.61),(4,'car',.67,.76)]
            for n,obj,x,y in positions:
                layers+=marker_on_scene(n,x,y,box,asset);targets.append({'number':n,'object':obj,'marker_source_fraction':[x,y]})
            notes.append('Decorative shop details are simplified; target teddy bear, train, doll and car retain original numbered associations.')
        elif num in [15,16]:
            height=1310;palette=['#88B82A','#E99735','#279CD0','#CF5642','#956CAC','#E8B844','#D7699A','#CD585D']
            for i in range(26):
                x=40+(i%4)*290;y=155+(i//4)*155
                layers += [rect([x,y,250,135],'#F7FAFD'),text(chr(65+i)+' '+chr(97+i),[x+5,y+24,240,105],74,True,True,palette[i%len(palette)])]
            targets=[{'upper':chr(65+i),'lower':chr(97+i)} for i in range(26)]
            if num==15: notes.append('Full A–Z shared alphabet is retained; letters are rendered using fonts, not generated lettering.')
            else:reuse=['CD1_15']
        elif num==17:
            height=1020
            layers+=panel_caption("Hi, what's your name?",[280,125,640,75],36)
            layers.append(image('assets/scenes/names.png',[40,230,1120,650],{'left_to_right':['Pete','Beth','Ann','Matt']}))
            for i,name in enumerate(['Pete','Beth','Ann','Matt']):
                layers+=panel_caption(f"{i+1}. I'm {name}.",[40+i*290,910,250,70],30)
                targets.append({'number':i+1,'character':name})
        elif num==18:
            height=1100
            layers+=panel_caption('What is it?',[390,125,420,65],36)
            layers.append(image('assets/scenes/answer.png',[40,205,1120,740],{'left_to_right':['Pete','Beth','Ann','Matt'],'held_objects':['ball','teddy-bear','doll','bicycle']}))
            for i,(name,toy) in enumerate(zip(['Pete','Beth','Ann','Matt'],['ball','teddy-bear','doll','bicycle'])):
                x=40+i*290
                layers.append(text(f'{i+1}. {name}',[x,960,250,45],30,True,True))
                layers.append(text("It's a ball." if i==0 else '______________.',[x,1020,250,45],28,True))
                targets.append({'number':i+1,'character':name,'object':toy})
            notes.append('Only the ball response is filled, as in the source. Remaining response lines stay blank.')
        else:raise ValueError(num)
        audio=f'audio/Track{num:02d}.mp3';shutil.copy2(ROOT.parent.parent/'Oxford - Let_s Go Begin Student_s Book 3rd Edition CD1'/f'Track{num:02d}.mp3',ROOT/audio)
        q=question(track)
        pages.append({'track':track,'audio_key':track.replace('_','-'),'exercise':item['exercise'],'unit_pdf_page':item['page'],'book_page':item['page']+1,'source_image_in_zip':item['image'],'source_reference':'references/'+Path(item['image']).name,'audio_file':audio,'output':{'png':f'pages/png/{track}.png','webp':f'pages/webp/{track}.webp'},'canvas':{'size':[1200,height],'background':'#FFFFFF'},'shared_visual_tracks':reuse,'learning_targets':targets,'adaptation_notes':notes,'question':q,'layers':layers})
    manifest={'schema_version':'1.0','unit':1,'source_archive':'Unit_1_Toys_audio_mapping.zip','source_item_count':17,'image_count':17,'coordinate_system':'pixel boxes [x,y,width,height], top-left origin','image_fit':'contain; preserve aspect ratio; center in box','text_font':'Arial (DejaVu Sans fallback)','question_policy':'Questions and answer keys are separate from lesson image. Do not show correct_choice_id to learners before submission.','items':pages}
    assert len(pages)==17 and len({p['track'] for p in pages})==17
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
