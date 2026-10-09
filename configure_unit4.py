from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent/'Let_s Go Begin/Units/Unit 4 - Numbers - Lesson Pages'
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
ranges={55:(.15,.64),56:(.64,.94),57:(.03,.54),58:(.53,.82),59:(.53,.82),60:(.02,.88),61:(.02,.88),62:(.02,.71),63:(.70,.95),64:(.02,.89),65:(.02,.89),66:(.03,.72),67:(.72,.95),68:(.07,.31),69:(.30,.94),70:(.09,.94)}
for p in m['items']:
 n=int(p['track'].split('_')[1]);a,b=ranges[n]
 with Image.open(root/'source-pages'/f"page-{p['unit_pdf_page']:02}.png") as im:im.crop((int(im.width*.03),int(im.height*a),im.width,int(im.height*b))).save(root/p['source_reference'])
specs={
55:"A. Let's talk. Andy curly hair navy-striped shirt at doorway asks 'May I come in?' Jenny black bob yellow shirt blue floral shorts in kitchen replies 'Sure! Please come in!' Refrigerator displays numerals 1,2,3,4,5 as source. Correct speech tails.",
56:"B. Say and act. Two numbered exchanges: 1 Kate blonde glasses red dress at classroom doorway asks Miss Jones teacher 'May I come in?' Teacher has blank answer line ending period. 2 Scott red hair green-striped shirt at room doorway has blank question ending ?; Kate/Jenny seated with number cards, reply 'Sure! Please come in!' Keep blank question/answer.",
57:"C. Let's sing. Title 'May I Come In?' Kate blonde glasses red dress at doorway; Scott green-striped shirt seated reading at desk, toy truck and turtle poster. Full lyrics exactly: May I come in? / Sure! Please come in! / Please come in! / May I come in? / May I come in? / Sure! Please come in! Retain repeats and punctuation.",
58:"D. Let's move. Two clear scenes: Jenny shows green GO paddle to Scott and Andy running; then Jenny shows red STOP paddle and boys halt. Labels '1. Go.' '2. Stop.' Preserve source girl/children identities.",
59:"E. Listen and do. Same go/stop scenes from58, labels '1. Go.' '2. Stop.', correct title only.",
60:"A. Numbers. Five distinct counting groups: EXACTLY 1 ball labeled 1; EXACTLY 2 dolls labeled 2; EXACTLY 3 toy cars labeled 3; EXACTLY 4 teddy bears (including panda) labeled 4; EXACTLY 5 yo-yos labeled 5. Clear separated countable objects, no duplicates/background extra toys. Source example 'Let's count. 1, 2, 3.'",
61:"B. Listen and point. Same exact groups 1 ball, 2 dolls, 3 toy cars, 4 teddy bears including panda, 5 yo-yos, numeral labels1–5. Quantity accuracy essential. Correct title only.",
62:"C. Sentences. Source two children seated among toys counting. Speech 'Let's count. 1, 2, 3, 4…' and response '5!' EXACT quantities: five red spotted balls in total (one held by left child, three between children, one held behind right child), two dolls, four yo-yos, three bicycles, one train with attached carriages. Blue exercise GROUP markers 1 by ball group, 2 dolls, 3 yo-yos, 4 bicycles, 5 train are group IDs, NOT quantities. Keep source learning quantities correct and separate from group markers.",
63:"D. Listen, point, and sing. Five large colorful numerals in reading order 1 2 3 4 5. Add corresponding words one two three four five below numerals. No invented lyrics.",
64:"A. Numbers. Five counting groups exact source quantities: SIX green outline triangles (2x3), SEVEN orange outline stars (3+3+1), EIGHT red outline circles (3+3+2), NINE purple outline hearts (3x3), TEN blue outline squares (2+3+3+2). Labels 6,7,8,9,10 adjacent matching group. Source header model 'How many?' / '6.' Quantity MUST match labels; no extra shapes.",
65:"B. Listen and point. Same exact groups 6 green triangles, 7 orange stars, 8 red circles, 9 purple hearts, 10 blue squares. Each isolated group clearly labeled numeral. Quantity accuracy essential.",
66:"C. Question and answer. Boy blue shirt asks curly-haired girl yellow star shirt 'How many?' girl shows two fingers on one hand and five on other, answers '7.' Background exact counting groups: SEVEN red apples, EIGHT dog toys, NINE cat toys, SIX pink hearts on wall string, FIVE white stars on chalkboard. Blue exercise GROUP IDs 1 apples,2 dogs,3 cats,4 hearts,5 stars NOT quantity labels. Arrange repeated cats3x3 and dogs2x4 if needed for count clarity, preserve source scene and colors. All counts exact.",
67:"D. Listen, point, and sing. Three counting groups EXACTLY FIVE red hearts, SEVEN yellow stars, TEN purple diamonds. Clear separated countable shapes, add words/numerals '5 / five', '7 / seven', '10 / ten'. No invented lyrics.",
68:"A. Sing and say. All26 upper/lowercase alphabet pairs A a to Z z in correct sequential reading order. Emphasize I i J j K k L l in different color as source. Large legible glyphs, complete alphabet.",
69:"B. Letters and words. Four source labeled pictures 1. I i — igloo, 2. J j — jump rope (child using rope), 3. K k — kangaroo, 4. L l — lion. Below C. Find the letters. snowy source scene with child holding jump rope by igloo/kangaroo/lion and embedded I i J j K k L l. Keep all eight glyphs readable.",
70:"A. Ask and answer. Classroom numeral balloons learning scene as source. Two model exchanges 'Is it a 5?' / 'Yes, it is.' and 'Is it a 9?' / 'No, it isn't. It's a 6.' Child holds clearly upright numeral6, never9. Balloons exercise IDs map 1→5,2→3,3→2,4→7,5→1,6→6,7→4,8→8,9→10,10→9. Preserve distinct small group IDs and big numeral shapes. Below supporting B. Find the numbers. classroom shelf/desks with 1 in fishbowl,2 pencil holder,3 backpack,4 wall picture,5 book. No omissions."
}
m['lesson_specs']={f'CD1_{n:02}':s for n,s in specs.items()}
m['batches']=[{'id':f'unit4-batch{i+1}','tracks':[p['track'] for p in m['items'][i*4:i*4+4]],'status':'pending'} for i in range(4)]
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Configured Unit 4; exact quantities required in specs.')
