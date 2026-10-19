"""Manually mapped from all 72 rendered source pages and their printed CD icons.

Coordinates are normalized source-page rectangles (full width, y0, y1).
Each crop isolates its printed activity. Only tracks printed on the same activity share a region.
"""
SPECS=[]
def P(page,disc,*groups):
    for tracks,y0,y1,label,kind in groups:
        if isinstance(tracks,int):tracks=[tracks]
        for track in tracks:
            SPECS.append(dict(disc=disc,track=track,source_pdf_page=page,crop_normalized=[0,y0,1,y1],activity=label,kind=kind))

P(3,1,(2,.135,.76,"A. Let's talk",'dialogue'),(3,.135,.895,'Practice: What’s your name?','sentence'))
P(4,1,(4,.015,.435,'B. The Hello Song','song'),(5,.435,.765,"C. Let's move",'words'),([6,7],.435,.89,'Let’s stand up','sentence+actions'))
P(5,1,(8,.135,.705,'A. School things','words'),([9,10],.135,.89,'B. It’s a pencil / an eraser','sentence+words'))
P(6,1,(11,.015,.735,'C. What’s this?','question+picture'),([12,13],.015,.89,'What’s this? It’s a pencil','question+model'))
P(7,1,(14,.135,.765,'A. More school things','words'),([15,16],.135,.89,'B. This is a map','sentence+words'))
P(8,1,(17,.015,.55,'C. Is this a poster / map?','question+picture'),([18,19],.015,.755,'Is this a table / crayon?','question+model'))
P(9,1,(20,.135,.555,'A. The Alphabet Song','alphabet+song'),(21,.555,.895,'B. This is my / your pencil','practice'))
P(10,1,(22,.015,.385,'C. Listen and circle','listening'),(23,.385,.905,'D. Is this your eraser / pen?','practice'))

P(11,1,(24,.135,.765,"A. Let's talk: How are you?",'dialogue'),(25,.135,.89,'How are you? I’m fine','sentence'))
P(12,1,(26,.015,.425,'B. Hi! How Are You?','song'),(27,.425,.765,"C. Let's move",'words'),([28,29],.425,.89,'Please take out your book','sentence+actions'))
P(13,1,(30,.135,.715,'A. Colors','words'),([31,32],.135,.89,'B. It’s yellow','sentence+words'))
P(14,1,(33,.015,.435,'C. What color is this?','question+picture'),([34,35],.015,.57,'What color is this? It’s gray','question+model'),(36,.57,.89,'D. What Color Is This?','song'))
P(15,1,(37,.135,.765,'A. Shapes','words'),([38,39],.135,.89,'B. This is a triangle / an oval','sentence+words'))
P(16,1,(40,.015,.435,'C. Is this an oval?','question+picture'),([41,42],.015,.63,'Is this a star / circle?','question+model'))
P(17,1,(43,.135,.405,'A. Alphabet A–C','alphabet'),(44,.405,.89,'B. What’s this? What color is it?','practice'))
P(18,1,(45,.015,.5,'C. This is a blue crayon','practice'),(46,.5,.925,'D. The Black Cat Song','song'))
P(19,1,(47,.085,.89,'A. Listen and circle: Units 1–2','review'))
P(20,1,(48,.085,.48,'A. Count to ten','numbers'),(49,.48,.89,'B. Count to twenty','numbers'))

P(21,1,(50,.135,.765,"A. Let's talk: This is my friend",'dialogue'),(51,.135,.89,'This is my friend, Sarah','sentence'))
P(22,1,(52,.015,.425,'B. This Is My Friend','song'),(53,.425,.765,"C. Let's move",'words'),([54,55],.425,.89,'I can count to ten','sentence+actions'))
P(23,1,(56,.135,.705,'A. Crayons, markers, notebooks, pencil cases','words'),([57,58],.135,.89,'B. One crayon / Three crayons','sentence+words'))
P(24,1,(59,.015,.4,'C. How many crayons / notebooks?','question+picture'),([60,61],.015,.52,'How many? One / Three','question+model'),(62,.52,.925,'D. How Many?','song'))
P(25,1,(63,.135,.75,'A. CDs, video games, cell phones, computers','words'),([64,65],.135,.89,'B. It’s a CD / They’re CDs','sentence+words'))
P(26,1,(66,.015,.545,'C. What’s this / What are these?','question+picture'),([67,68],.015,.705,'It’s a cell phone / They’re video games','question+model'))
P(27,1,(69,.135,.4,'A. Alphabet D–F','alphabet'),(70,.4,.89,'B. Ask and answer: this / these','practice'))
P(28,1,(71,.015,.525,'C. What color are these?','practice'),(72,.525,.925,'D. What’s This?','song'))

P(29,1,(73,.135,.755,"A. Let's talk: Nice to meet you",'dialogue'),(74,.135,.89,'It’s nice to meet you, too','sentence'))
P(30,1,(75,.015,.395,'B. The Family Song','song'),(76,.395,.75,"C. Let's move",'words'),([77,78],.395,.89,'I can / can’t find my book','sentence+actions'))
P(31,1,(79,.135,.715,'A. Family','words'),([80,81],.135,.89,'B. She’s my grandmother / He’s my grandfather','sentence+words'))
P(32,1,(82,.015,.72,'C. Who’s she / he?','question+picture'),([83,84],.015,.89,'Who’s she / he? She’s my sister / He’s my father','question+model'))
P(33,1,(85,.135,.765,'A. Describing people','words'),([86,87],.135,.89,'B. He’s tall / She’s short','sentence+words'))
P(34,1,(88,.015,.435,'C. Is she pretty / Is he old?','question+picture'),([89,90],.015,.57,'Is he short? Yes / No','question+model'),(91,.57,.89,'D. Is He Short? Is He Tall?','song'))
P(35,1,(92,.135,.405,'A. Alphabet G–I','alphabet'),(93,.405,.89,'B. Listen and number: family','listening'))
P(36,1,(94,.455,.89,'D. Talk about your family','practice'))
P(37,1,(95,.085,.515,'A. Listen and circle: Units 3–4','review'),(96,.515,.89,'B. Listen and number: family','review'))
P(38,1,(97,.085,.545,'A. Parts of the body','words'),(98,.085,.675,'Touch your nose','sentence+words'),(99,.675,.89,'B. Finger / fingers, toe / toes, foot / feet','words'))

P(39,2,(2,.135,.755,"A. Let's talk: Happy birthday",'dialogue'),(3,.135,.89,'How old are you? I’m seven years old','sentence'))
P(40,2,(4,.015,.39,'B. The Happy Birthday Song','song'),(5,.39,.75,"C. Let's move",'words'),([6,7],.39,.89,'What can you do? I can ride a bicycle','sentence+actions'))
P(41,2,(8,.135,.715,'A. Toys','words'),([9,10],.135,.89,'B. It’s a yo-yo','sentence+words'))
P(42,2,(11,.015,.49,'C. What is it?','question+picture'),([12,13],.015,.64,'What is it? I don’t know','question+model'))
P(43,2,(14,.135,.765,'A. Describing toys','words'),([15,16],.135,.89,'B. It’s little','sentence+words'))
P(44,2,(17,.015,.435,'C. Is it a long pencil / new doll?','question+picture'),([18,19],.015,.6,'Is it a round yo-yo / new doll?','question+model'),(20,.6,.925,'D. No, It Isn’t. Yes, It Is.','song'))
P(45,2,(21,.135,.395,'A. Alphabet J–M','alphabet'),(22,.395,.89,'B. Guess the shape','practice'))
P(46,2,(23,.015,.55,'C. What are these? Are they pencils?','practice'),(24,.55,.925,'D. Listen and number: toys','listening'))

P(47,2,(25,.135,.755,"A. Let's talk: weather",'dialogue+words'),(26,.135,.89,'How’s the weather? It’s sunny','sentence+words'))
P(48,2,(27,.015,.365,'B. How’s the Weather?','song'),(28,.365,.725,"C. Let's move",'words'),([29,30],.365,.89,'Can you throw a ball?','sentence+actions'))
P(49,2,(31,.135,.44,'A. Flowers, trees, clouds, puddles','words'),([32,33],.135,.65,'B. There’s one flower / There are four trees','sentence+words'))
P(50,2,(34,.015,.69,'D. How many are there?','question+picture'),([35,36],.015,.89,'How many kites / trees are there?','question+model'))
P(51,2,(37,.135,.395,'A. In, on, under, by','words'),(38,.395,.75,'B. The bug is in the bag','sentence+picture'),([39,40],.135,.89,'The bug / bugs are in the bag','sentence+picture'))
P(52,2,(41,.015,.465,'C. Where’s the bat / Where are the books?','question+picture'),([42,43],.015,.63,'Where’s the doll / Where are the balls?','question+model'),(44,.63,.925,'D. Where Are the Bugs?','song'))
P(53,2,(45,.135,.395,'A. Alphabet N–Q','alphabet'),(46,.395,.89,'B. Is there a doll in the bag?','practice'))
P(54,2,(47,.47,.89,'D. Listen and circle: there is / are','listening'))
P(55,2,(48,.085,.89,'A. Listen and circle: Units 5–6','review'))
P(56,2,(49,.085,.715,'A. Days of the week','question+words'),(50,.085,.89,'B. Today is Monday','sentence+calendar'))

P(57,2,(51,.135,.725,"A. Let's talk: Food",'dialogue'),(52,.135,.89,'Here you are. Thank you. You’re welcome','sentence'))
P(58,2,(53,.015,.43,'B. I Want An Apple','song'),(54,.43,.765,"C. Let's move",'words'),([55,56],.43,.89,'I wash my hands every day','sentence+actions'))
P(59,2,(57,.135,.705,'A. Food and drinks','words'),([58,59],.135,.89,'B. I want a banana / an orange','sentence+words'))
P(60,2,(60,.015,.415,'C. What do you want?','question+picture'),([61,62],.015,.545,'What do you want? I want a sandwich','question+model'),(63,.545,.925,'D. What Do You Want?','song'))
P(61,2,(64,.135,.765,'A. More food','words'),([65,66],.135,.89,'B. I want chicken / I don’t want fish','sentence+words'))
P(62,2,(67,.015,.485,'C. Do you want bread?','question+picture'),([68,69],.015,.6,'Do you want cake / rice?','question+model'),(70,.6,.89,'D. Ask your partner: food','practice'))
P(63,2,(71,.135,.395,'A. Alphabet R–U','alphabet'),(72,.395,.89,'B. Listen and circle: I want','listening'))
P(64,2,(73,.455,.89,'D. Do you want a yellow bicycle?','practice'))

P(65,2,(74,.135,.725,"A. Let's talk: favorite color",'dialogue'),(75,.135,.89,'What’s your favorite color?','sentence'))
P(66,2,(76,.015,.415,'B. What’s Your Favorite Color?','song'),(77,.415,.725,"C. Let's move",'words'),([78,79],.415,.89,'I walk / don’t walk the dog every day','sentence+actions'))
P(67,2,(80,.135,.715,'A. Pets','words'),([81,82],.135,.89,'B. I like dogs','sentence+words'))
P(68,2,(83,.015,.465,'C. What do you like?','question+picture'),([84,85],.015,.6,'What do you like? I like frogs','question+model'))
P(69,2,(86,.135,.765,'A. Animals','words'),([87,88],.135,.89,'B. I like monkeys / I don’t like bears','sentence+words'))
P(70,2,(89,.015,.72,'C. Do you like giraffes / lions?','question+picture'),([90,91],.015,.89,'Do you like elephants / tigers?','question+model'))
P(71,2,(92,.135,.395,'A. Alphabet V–Z','alphabet'),(93,.395,.89,'B. Do you like giraffes?','practice'))
P(72,2,(94,.015,.54,'C. What do you like / want?','practice'),(95,.54,.925,'D. I Like Turtles','song'))
P(73,2,(96,.085,.59,'A. Listen and circle: Units 7–8','review'),(97,.59,.89,'B. Listen and number: animals','review'))
P(74,2,(98,.085,.655,'A. Feelings: Are you happy?','question+words'),(99,.655,.89,'B. Hungry, thirsty, hot, cold','words'))

# Refined against boundary overlays of all source pages. Keep complete activity
# headings/icons and stop in the whitespace before the following activity.
def B(d,tracks,start=None,end=None,exclude=None):
    if isinstance(tracks,int):tracks=[tracks]
    for s in SPECS:
        if s['disc']==d and s['track'] in tracks:
            if start is not None:s['crop_normalized'][1]=start
            if end is not None:s['crop_normalized'][3]=end
            if exclude:s['exclude_normalized']=exclude
for s in SPECS:
    if s['crop_normalized'][3]>=.87:s['crop_normalized'][3]=.925
B(1,2,end=.735)
B(1,4,end=.445,exclude=[[0,.415,.6,.445]])
B(1,[5,6,7],start=.415,exclude=[[.6,.415,1,.445]])
B(1,5,end=.75)
B(1,8,end=.68);B(1,14,end=.715);B(1,17,end=.525);B(1,[18,19],end=.73)
B(1,20,end=.525);B(1,21,start=.525);B(1,22,end=.36);B(1,23,start=.36)
B(1,24,end=.735);B(1,26,end=.405);B(1,[27,28,29],start=.405);B(1,27,end=.75)
B(1,30,end=.685);B(1,33,end=.425);B(1,[34,35],end=.55);B(1,36,start=.55)
B(1,37,end=.705);B(1,40,end=.425);B(1,[41,42],end=.615)
B(1,43,end=.375);B(1,44,start=.375);B(1,45,end=.485);B(1,46,start=.485)
B(1,50,end=.735);B(1,52,end=.405);B(1,[53,54,55],start=.405);B(1,53,end=.75)
B(1,56,end=.68);B(1,59,end=.39);B(1,[60,61],end=.51);B(1,62,start=.515)
B(1,63,end=.705);B(1,66,end=.52);B(1,[67,68],end=.625)
B(1,69,end=.375);B(1,70,start=.375);B(1,73,end=.725)
B(1,75,end=.37);B(1,[76,77,78],start=.37);B(1,76,end=.725)
B(1,79,end=.685);B(1,82,end=.69);B(1,85,end=.705)
B(1,88,end=.395);B(1,[89,90],end=.55);B(1,91,start=.545)
B(1,92,end=.38);B(1,93,start=.38);B(1,94,start=.46)
B(1,95,end=.485);B(1,96,start=.485)
B(1,98,end=.65);B(1,99,start=.65)

B(2,2,end=.725);B(2,4,end=.37);B(2,[5,6,7],start=.37);B(2,5,end=.725)
B(2,8,end=.69);B(2,11,end=.475);B(2,[12,13],end=.625)
B(2,14,end=.705);B(2,17,end=.395);B(2,[18,19],end=.565);B(2,20,start=.555)
B(2,21,end=.375);B(2,22,start=.375);B(2,23,end=.53);B(2,24,start=.53)
B(2,25,end=.725);B(2,27,end=.345);B(2,[28,29,30],start=.345);B(2,28,end=.7)
B(2,31,end=.435);B(2,[32,33],end=.675);B(2,34,end=.68)
B(2,37,end=.37);B(2,38,start=.375,end=.73)
B(2,41,end=.42);B(2,[42,43],end=.59);B(2,44,start=.595)
B(2,45,end=.37);B(2,46,start=.37);B(2,47,start=.49)
B(2,49,end=.70)
B(2,51,end=.70);B(2,53,end=.42);B(2,[54,55,56],start=.42);B(2,54,end=.75)
B(2,57,end=.68);B(2,60,end=.40);B(2,[61,62],end=.525);B(2,63,start=.525)
B(2,64,end=.705);B(2,67,end=.465);B(2,[68,69],end=.58);B(2,70,start=.585)
B(2,71,end=.37);B(2,72,start=.37);B(2,73,start=.37)
B(2,74,end=.70);B(2,76,end=.395);B(2,[77,78,79],start=.395);B(2,77,end=.73)
B(2,80,end=.69);B(2,83,end=.45);B(2,[84,85],end=.585)
B(2,86,end=.685);B(2,89,end=.695);B(2,92,end=.37);B(2,93,start=.37)
B(2,98,end=.635);B(2,99,start=.635)

# Alphabet bottom labels sit just above the next activity's raised CD badge.
B(1,20,end=.515)
B(1,43,end=.385);B(1,44,start=.385)
B(1,69,end=.385);B(1,70,start=.385)
B(1,92,end=.389);B(1,93,start=.389)
B(2,21,end=.385);B(2,22,start=.385)
B(2,45,end=.385);B(2,46,start=.385)
B(2,71,end=.384);B(2,72,start=.384)
B(2,92,end=.379);B(2,93,start=.379)

# Isolate sentence/model regions from the preceding dialogue, vocabulary or picture.
# These pairs identify the preceding printed activity and the separate model tracks.
MODEL_PAIRS = {
1: [(2,[3]),(5,[6,7]),(8,[9,10]),(11,[12,13]),(14,[15,16]),(17,[18,19]),
(24,[25]),(27,[28,29]),(30,[31,32]),(33,[34,35]),(37,[38,39]),(40,[41,42]),
(50,[51]),(53,[54,55]),(56,[57,58]),(59,[60,61]),(63,[64,65]),(66,[67,68]),
(73,[74]),(76,[77,78]),(79,[80,81]),(82,[83,84]),(85,[86,87]),(88,[89,90]),(97,[98])],
2: [(2,[3]),(5,[6,7]),(8,[9,10]),(11,[12,13]),(14,[15,16]),(17,[18,19]),
(25,[26]),(28,[29,30]),(31,[32,33]),(34,[35,36]),(38,[39,40]),(41,[42,43]),(49,[50]),
(51,[52]),(54,[55,56]),(57,[58,59]),(60,[61,62]),(64,[65,66]),(67,[68,69]),
(74,[75]),(77,[78,79]),(80,[81,82]),(83,[84,85]),(86,[87,88]),(89,[90,91])]}
for disc,pairs in MODEL_PAIRS.items():
    bytrack={s['track']:s for s in SPECS if s['disc']==disc}
    for preceding,models in pairs:
        boundary=bytrack[preceding]['crop_normalized'][3]
        for track in models:
            model=bytrack[track]
            model['crop_normalized'][1]=boundary
            model.pop('exclude_normalized',None)
B(1,66,end=.425)
B(1,[67,68],start=.425,end=.61)
B(1,[18,19],end=.70)
B(1,[89,90],end=.545)
B(2,[18,19],end=.555)
for spec in SPECS:
    spec['region_id']='PDF-%03d-%.4f-%.4f'%(
        spec['source_pdf_page'],spec['crop_normalized'][1],spec['crop_normalized'][3])

assert len(SPECS)==196,len(SPECS)
assert {(s['disc'],s['track']) for s in SPECS}=={(d,t) for d in [1,2] for t in range(2,100)}
assert {s['source_pdf_page'] for s in SPECS}==set(range(3,75))
