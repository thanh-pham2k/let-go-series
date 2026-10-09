from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
specs=[
"Birthday conversation: striped boy asks How old are you?; blonde crown/red glasses girl replies I'm 6.; yellow-shirt girl right. Six candles, HAPPY BIRTHDAY banner, cake/pizza/chicken/ice cream.",
"Two numbered roleplays: grandmother asks How old are you?; girl reply blank. Playground boy question blank; red-cap boy says I'm 10. Do not fill blanks.",
"How Old Are You? song: How old are you? / I'm 6. / How old are you? / I'm 7. / 1, 2, 3, 4, 5, 6, 7! / How old are you? / I'm 5. / How old are you? / I'm 10. / 1, 2, 3, 4, 5, 6, 7, 8, 9, 10! Six candles.",
"1. Make a line. 2. Make a circle. Four children in both actions, matching clothes.",
"Listen and do: supporting two Let's move actions from same page, four children, line and circle; gray cat pointing. No additional spoken text inferred.",
"Words: 1. ice cream (white/pink/brown scoops); 2. pizza; 3. cake (yellow/pink, blue flowers); 4. chicken. Header cats: gray says I like ice cream.",
"Listen and point: same page's four Words illustrations and labels, orange cat pointing, header I like ice cream.",
"Sentences party: pink-shirt girl says I like cake.; green boy ice cream; orange girl chicken; blue boy pizza. Food badges 1 cake, 2 ice cream, 3 chicken, 4 pizza.",
"Listen, point, and sing: cake, ice cream sundae, pizza slice, chicken drumstick, left to right. No lyrics printed, do not invent lyrics.",
"Words: 1 milk white glass; 2 fish pink fillet; 3 bread orange loaf; 4 rice white in blue/yellow bowl. Gray cat asks Do you like milk? Orange cat replies Yes, I do.",
"Chant: use same-page four Words and numbered labels plus cat pointing; preserve header milk question/Yes answer; no chant lyrics printed.",
"Question and answer: center orange-haired girl asks Do you like fish? Left red boy Yes, I do.; right dark orange-shirt boy No, I don't. Six exercises: happy milk/bread/rice 1/2/3; unhappy milk/bread/rice 4/5/6. D. Ask and answer: fish1 ice cream2 pizza3 milk4 and cat Do you like milk?.",
"Sing and say: all uppercase A-Z and lowercase a-z once, Q R S T and q r s t pink, other glyphs purple. Source CD1 32 normalized CD2_32.",
"Letters and words: 1 Qq queen; 2 Rr rabbit; 3 Ss sun; 4 Tt tiger. C. Find the letters garden scene: queen purple robe, white rabbit red cushion on white bench, yellow sun, orange tiger; preserve hidden Q/q R/r S/s T/t from source without giving answers.",
"Play a game: left red boy Do you like birds? center black-bob pink girl Yes, I do.; right blonde green girl No, I don't. Winding board START then cake,pizza,empty red,ice cream,two rabbits,empty pink,two bicycles,three cats,empty green,two birds,empty orange,three bears,empty green,two trains,empty pink,FINISH. Source CD1 34 normalized CD2_34."
]
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for p,s in zip(m['items'],specs):
    p['lesson_specs']={'source_content':s,'review_basis':'All eight source-page PNGs visually read; source PDF references retained. Audio speech not independently audited.'}
(ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
