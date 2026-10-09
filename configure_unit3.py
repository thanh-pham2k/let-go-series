from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent/'Let_s Go Begin/Units/Unit 3 - Shapes - Lesson Pages'
m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
ranges={38:(.15,.64),39:(.64,.94),40:(.03,.52),41:(.52,.82),42:(.52,.82),43:(.04,.87),44:(.04,.87),45:(.02,.72),46:(.72,.95),47:(.02,.89),48:(.02,.89),49:(.03,.70),50:(.70,.95),51:(.07,.31),52:(.30,.94),53:(.09,.45),54:(.44,.94)}
for p in m['items']:
 n=int(p['track'].split('_')[1]);a,b=ranges[n]
 with Image.open(root/'source-pages'/f"page-{p['unit_pdf_page']:02}.png") as im:im.crop((int(im.width*.03),int(im.height*a),im.width,int(im.height*b))).save(root/p['source_reference'])
specs={
38:"A. Let's talk. Children doing paper crafts in classroom. Foreground Kate blonde glasses red dress holds purple paper star and asks 'How are you today?' Scott red hair green-striped shirt cuts pink paper and replies 'I'm fine, thank you.' Andy/Jenny in background. Correct speech tails. Colored cut-paper shapes on tables.",
39:"B. Say and act. Two exchanges 1 Miss Jones green shirt blue skirt asks Jenny black bob yellow shirt 'How are you today?' Jenny has blank answer line. 2 Andy curly hair navy stripes asks Kate blonde glasses red dress holding football, blank question bubble ending period; Kate replies 'I'm fine, thank you.' Preserve blank questions/answers.",
40:"C. Let's sing. Title 'How Are You Today?' Four children around unobstructed song: Scott claps top left, Andy plays triangle top right, Kate holds tambourine bottom left, Jenny claps bottom right. Full exact lyrics: How are you today? / I'm fine, thank you. / How are you? / I'm fine, thank you. / How are you today? / I'm fine, thank you. / How are you? / I'm fine. Retain all repeated lines.",
41:"D. Let's move. Two clear scenes same red-haired Scott in white green-striped shirt brown trousers outdoors: walking then running. Labels '1. Walk.' '2. Run.' Distinct movement poses.",
42:"E. Listen and do. Same walking/running scenes and labels '1. Walk.' '2. Run.' from same source page, correct title only.",
43:"A. Words. Four plain outline geometric shapes numbered and labeled 1. a circle (orange), 2. a square (green), 3. a triangle (purple), 4. a heart (red). Circle perfectly circular, square four equal sides and right angles. Source header example 'Draw a circle.' Keep all shapes large and clear.",
44:"B. Listen and point. Same numbered outline shapes/labels 1. a circle orange, 2. a square green, 3. a triangle purple, 4. a heart red. Correct title only.",
45:"C. Sentences. Boy orange shirt instructs kneeling girl pink shirt drawing shapes with chalk on pavement 'Draw a square.' Numbered chalk shapes 1 white square, 2 yellow heart, 3 yellow circle, 4 blue triangle. Preserve numbers and actual geometry, no trapezoid instead of square.",
46:"D. Listen, point, and chant. Four large dashed outline shapes in reading order triangle red, square orange, circle purple, heart green. Add clear labels 'a triangle', 'a square', 'a circle', 'a heart' under each. No invented chant lyrics.",
47:"A. Words. Four colored flat shapes labeled 1. a star yellow, 2. a rectangle green, 3. a diamond purple, 4. an oval blue. Rectangle clearly unequal adjacent sides; diamond rhombus. Source example dialogue 'Is it a star?' / 'Yes, it is.'",
48:"B. Listen and point. Same four numbered colored shapes/labels as47, correct title only.",
49:"C. Question and answer. Two model exchanges top: boy blue shirt asks girl pink shirt holding yellow star 'Is it a star?' / 'Yes, it is.' Girl asks boy holding blue diamond 'Is it a rectangle?' / 'No, it isn't. It's a diamond.' Below children making paper shapes numbered 1 yellow star, 2 blue diamond, 3 blue oval, 4 yellow rectangle. Show all relevant objects and accurate geometry.",
50:"D. Listen, point, and sing. Shapes in order orange circle, yellow oval, blue square, red heart, green diamond. Add labels 'a circle', 'an oval', 'a square', 'a heart', 'a diamond'. No invented lyrics.",
51:"A. Sing and say. Complete 26 upper/lower alphabet pairs A a through Z z in correct sequential reading order, big clean colorful glyphs. Four columns allowed. Do not omit any pair.",
52:"B. Letters and words. 1. E e — egg; 2. F f — fish; 3. G g — gorilla; 4. H h — heart. Pictures egg/fish/gorilla/redheart with labels. Below C. Find the letters. source scene gorilla near aquarium table and vase of hearts. Preserve embedded uppercase/lowercase E e F f G g H h as source, accurate English glyphs.",
53:"A. Sentences. Child at crafts desk example 'It's a blue square.' Four numbered flat shapes 1. a blue square, 2. a purple heart, 3. an orange triangle, 4. a yellow circle. Distinct actual geometric shapes.",
54:"B. Question and answer. Two model exchanges: boy asks girl holding green square 'Is it a green square?' girl 'Yes, it is.' Then boy asks girl holding pink heart 'Is it a red square?' girl 'No, it isn't. It's a pink heart.' Beneath numbered shape row source order 1 green square, 2 brown triangle, 3 white oval, 4 blue heart, 5 pink heart, 6 yellow rectangle, 7 purple oval, 8 orange star. All shapes present, numbers correct, accurate geometry."
}
m['lesson_specs']={f'CD1_{n:02}':s for n,s in specs.items()}
m['batches']=[{'id':f'unit3-batch{i+1}','tracks':[p['track'] for p in m['items'][i*4:i*4+4]],'status':'pending'} for i in range(5)]
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Configured Unit 3 references and faithful content specifications.')
