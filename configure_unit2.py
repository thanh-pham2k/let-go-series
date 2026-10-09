from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent/'Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages'
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
# Relative vertical crop ranges reviewed against original PDF pages.
ranges={19:(.15,.65),20:(.64,.94),21:(.03,.52),22:(.52,.82),23:(.52,.82),24:(.05,.88),25:(.05,.88),26:(.02,.86),27:(.02,.86),28:(.02,.89),29:(.02,.89),30:(.03,.70),31:(.69,.95),32:(.07,.31),33:(.30,.94),34:(.09,.54),35:(.54,.95)}
for item in manifest['items']:
    n=int(item['track'].split('_')[1]);a,b=ranges[n]
    with Image.open(root/'source-pages'/f"page-{item['unit_pdf_page']:02}.png") as im:
        im.crop((int(im.width*.03),int(im.height*a),im.width,int(im.height*b))).save(root/item['source_reference'])
specs={
19:"A. Let's talk. Two scenes: teacher Miss Jones greets seated students 'Hi, boys and girls.' children reply 'Hello, Miss Jones.' Then students leaving classroom teacher says 'Good-bye.' children reply 'See you later.' Preserve speaker roles with speech bubble tails.",
20:"B. Say and act. Two numbered exchanges as source. 1 teacher says 'Hi, boys and girls.' children have blank answer bubble ending period. 2 girl says 'Good-bye.' friend has blank answer bubble ending period. Keep blanks, do not fill answers.",
21:"C. Let's sing. Title 'Hi, Hello, Good-bye'. Miss Jones waves, yellow school bus children waving. Full lyrics, in readable unobstructed area: Hi, boys and girls. / Hello, Miss Jones. / Hi, boys and girls. / Hello, Miss Jones. / Hi, Andy. / Hello, Jenny. / Good-bye, Kate. / See you later. / Bye-bye, see you later. / Bye-bye, see you later. / Bye, Andy, / Good-bye, Jenny. / Good-bye, Kate. / Bye-bye! Do not omit repeated lines.",
22:"D. Let's move. Two numbered action scenes teacher green shirt blue skirt with children. 1 teacher beckons children toward her, arrow toward teacher, label '1. Come here.' 2 children turning around, curved arrow, label '2. Turn around.'",
23:"E. Listen and do. Use same two action scenes as 22 with labels '1. Come here.' '2. Turn around.' Supplement source title-only exercise using action content from same page.",
24:"A. Words. Five teddy bears, exact numbered color labels: 1. red; 2. blue; 3. yellow; 4. green; 5. brown. Preserve source numbered order, each bear entirely correct color, large clear labels. Add source example speech 'It's red.' beside red bear.",
25:"B. Listen and point. Same five numbered bears and labels: 1. red; 2. blue; 3. yellow; 4. green; 5. brown. Correct title only.",
26:"C. Sentences. Children hold circular five-panel play parachute, numbered colored panels as source: 1 blue upper left, 2 green upper right, 3 brown right, 4 yellow bottom, 5 red left. Speech 'It's blue.' Number markers adjacent relevant panel. Never substitute colors.",
27:"D. Listen and point. Same five-color numbered parachute scene as 26 and example 'It's blue.' Distinct correct title.",
28:"A. Words. Five toy cars numbered labeled exact colors 1. purple; 2. orange; 3. black; 4. white; 5. pink. Source example dialogue 'What color is it?' / 'It's purple.'",
29:"B. Listen and point. Same five cars labels 1. purple; 2. orange; 3. black; 4. white; 5. pink. Correct title only.",
30:"C. Question and answer. Girl pink top asks 'What color is it?' boy blue top answers 'It's purple.' Numbered toy train cars: 1 purple near boy, 2 pink lower left, 3 blue upper left, 4 yellow center, 5 orange right. Red engine on oval track is unnumbered. Preserve source relationships and colored cars.",
31:"D. Listen, point, and chant. Three large toys in order blue ball, red teddy bear, purple train; add labels 'blue', 'red', 'purple' beneath corresponding objects. No invented chant lyrics.",
32:"A. Sing and say. Full uppercase/lowercase alphabet A a through Z z, complete correct reading order. Generous colorful clear typography, 4 columns, all 26 pairs; reference narrow strip may be reformatted without losing letters.",
33:"B. Letters and words. Four pairs with source pictures and words 1. A a — apple (red apple), 2. B b — bird (blue bird), 3. C c — cat (yellow cat), 4. D d — dog (brown dog). Below include supporting C. Find the letters. scene from source with colored a,b,c,d letters among toys. Accurate labels, clearly separate activity.",
34:"A. Sentences. Four numbered objects: 1. a red train; 2. a blue ball; 3. a brown teddy bear; 4. a green yo-yo. Boy holding toy train says 'It's a red train.' Preserve correct colors and labels.",
35:"B. Question and answer. Two children in room, girl asks 'What is it?' boy holds green toy car and replies 'It's a green car.' Surrounding numbered objects preserve source mapping: 1 green car, 2 white dog, 3 black bicycle, 4 green snake, 5 orange jump rope, 6 brown train, 7 yellow cat, 8 blue ball. Preserve placement and colors; do not label an unrelated object."
}
manifest['lesson_specs']={f'CD1_{n:02}':s for n,s in specs.items()}
manifest['batches']=[{'id':f'unit2-batch{i+1}','tracks':[p['track'] for p in manifest['items'][i*4:i*4+4]],'status':'pending'} for i in range(5)]
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Configured 17 references and content specs for Unit 2.')
