from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent/'Let_s Go Begin/Units/Unit 5 - Animals - Lesson Pages'
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
ranges={2:(.15,.64),3:(.64,.94),4:(.04,.54),5:(.54,.82),6:(.54,.82),7:(.02,.89),8:(.02,.89),9:(.02,.71),10:(.71,.95),11:(.02,.89),12:(.02,.89),13:(.03,.59),14:(.03,.59),15:(.69,.95),16:(.07,.30),17:(.29,.94),18:(.09,.47),19:(.46,.94)}
for p in m['items']:
 n=int(p['track'].split('_')[1]);a,b=ranges[n]
 with Image.open(root/'source-pages'/f"page-{p['unit_pdf_page']:02}.png") as im:im.crop((int(im.width*.02),int(im.height*a),im.width,int(im.height*b))).save(root/p['source_reference'])
specs={
2:"A. Let's talk. Pet shop cashier man mustache green shirt navy apron hands change to Jenny black bob yellow shirt, girl holding dogfood bag. Man says 'Here you are.' Girl 'Thank you.' Correct speech tails, parrots/rabbits/fish in source background.",
3:"B. Say and act. Two numbered exchanges1 adult woman red shirt hands ice cream to Andy navy-striped shirt says 'Here you are.' boy blank answer. 2 Scott green stripes seated bench hands soccer ball to Kate blonde glasses red dress, Scott blank speech line, Kate says 'Thank you.' Preserve blanks.",
4:"C. Let's sing. Title 'Here You Are. Thank You.' Jenny holds birdhouse on pole, Scott hands her small tray of birdfood outdoors, source tools nearby. Full exact lyrics: Here you are. / Thank you, thank you! / Here you are. / Thank you! / Here you are. / Thank you, thank you! / Here you are. / Thank you! Keep eight lines and repeats readable.",
5:"D. Let's move. Andy navy-striped shirt JUMP with both feet off ground and upward motion lines; Kate blonde glasses red dress SKIP with alternating raised knee, clear different actions. Labels '1. Jump.' '2. Skip.' Outdoors.",
6:"E. Listen and do. Same jump/skip actions as5, labels '1. Jump.' '2. Skip.' correct title only.",
7:"A. Words. Six numbered singular/plural animal groups in 2 columns3rows: 1. dog (ONE dog),2. dogs (THREE dogs),3. cat (ONE cat),4. cats (TWO cats),5. bird (ONE bird),6. birds (FIVE birds on wire). These labels are group IDs not counts. Preserve exact source quantities. Header example dialogue 'Let's count the cats.' / '1 cat, 2 cats.' with two small cats separately if included.",
8:"B. Listen and point. Same six groups exact quantities/labels1dog,2dogs(3animals),3cat,4cats(2animals),5bird,6birds(5animals). Correct title only.",
9:"C. Sentences. Pet shop mother green shirt tells daughter yellow shirt red trousers 'Let's count the cats.' girl replies '1 cat, 2 cats.' Source groups small blue ID1 by EXACTLY TWO cats in stacked cages; ID2 by THREE dogs in pen; ID3 by FIVE birds in cage. Keep countable animals distinct. Source sale boxes may simplify.",
10:"D. Listen, point, and sing. Three groups from left to right EXACTLY TWO birds, THREE dogs, TWO cats, labels 'birds', 'dogs', 'cats' under groups. No invented lyrics. Rightmost must cats.",
11:"A. Words. Farm six groups IDs/labels: 1. cow (ONE black-white cow near barn);2. cows (THREE cows together);3. rabbit (ONE rabbit on stump);4. rabbits (SIX rabbits);5. duck (ONE duck on grass);6. ducks (FOUR ducks at pond). IDs not quantities. Header model 'How many ducks?' / '3 ducks.' with three small ducks clearly separate from main pond if included.",
12:"B. Listen and point. Same farm six IDs/labels and quantities as11:1cow,2cows(3),3rabbit,4rabbits(6),5duck,6ducks(4). Correct title only.",
13:"C. Question and answer. Farm bicycle-riding girl pink shirt/purple helmet asks boy blue shirt/red helmet 'How many cows?' boy '8 cows.' Source GROUPS: ID1 eight cows in field together, ID2 one duck on grass near pond, ID3 six ducks IN pond, ID4 one additional separate cow by fence, ID5 three running rabbits, ID6 one sitting rabbit. Do not confuse eight-cow group with separate single cow. Exact quantities, IDs placed beside matching groups.",
14:"D. Listen and point. Same farm and source group counts/IDs as13; preserve 'How many cows?' / '8 cows.' Use correct title only.",
15:"E. Listen, point, and sing. Five animal groups in source reading order: EXACTLY TWO ducks, THREE cows, FIVE rabbits, SEVEN dogs, TEN birds. Large clear separate animals, each group labeled plural 'ducks','cows','rabbits','dogs','birds'. No extra decorative animals or invented lyrics. May arrange groups in rows but birds must last/rightmost.",
16:"A. Sing and say. Full26 uppercase/lowercase pairs A a through Z z, correct sequential reading order. Emphasize M m N n O o P p in contrasting color as source. All pairs clear and accurate.",
17:"B. Letters and words. Four pictures/labels1. M m — moon,2. N n — nest,3. O o — octopus (eight arms),4. P p — peach. Below C. Find the letters. Source underwater friendly purple octopus, moon overhead, peach in nest; embed all eight glyphs M m N n O o P p as source. Clear typography, no missing words.",
18:"A. Count. Toyshop two children looking at trains. Speech 'Let's count.' / '1 train, 2 trains, 3 trains.' EXACTLY THREE locomotives each with carriages along one track, not count carriages as trains. GroupIDs1trains3,2ball1,3teddy bears6 on two shelves3+3,4yo-yos9 in3x3display. All objects distinct, no added counted toys.",
19:"B. Question and answer. Girl pinkshirt/turquoise apron asks boy purple white-striped shirt 'How many cars?' boy '8 cars.' EXACTLY EIGHT toy cars clearly separated on floor. Other groupIDs source:1cars8,2blue rectangular paper cards10 on desk(5+5),3jump ropes4 on wall,4rabbit toys2 on counter,5balls5 on shelves,6one red bicycle foreground. Accurate counts, groupIDs not quantities."
}
m['lesson_specs']={f'CD2_{n:02}':s for n,s in specs.items()}
m['batches']=[{'id':f'unit5-batch{i+1}','tracks':[p['track'] for p in m['items'][i*4:i*4+4]],'status':'pending'} for i in range(5)]
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Configured Unit5 with singular/plural and counted animal groups.')
