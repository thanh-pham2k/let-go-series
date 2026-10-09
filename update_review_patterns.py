"""Author the four review exercise guides from visually audited source content."""
from pathlib import Path
from urllib.parse import quote,unquote
from collections import Counter
import json,re,random,hashlib,zipfile

ROOT=Path(__file__).resolve().parent/'Let_s Go Begin/Units'

def entry(word,picture,group):return {'word':word,'picture':picture,'group':group}
def entries(group,pairs):return [entry(w,p,group) for w,p in pairs]

DATA={
'1-2':dict(file='Review 1-2(3).md',tracks=['CD1_36','CD1_37'],pages='18–19',
 vocab=entries('Đồ chơi',[('car','ô tô ở cặp1a'),('train','đoàn tàu ở cặp1b'),('bicycle','xe đạp ở cặp2a'),('ball','quả bóng ở cặp2b')])+
 entries('Màu sắc',[('green','ô màu xanh lá ở cặp3a'),('red','ô màu đỏ ở cặp3b'),('purple','ô màu tím ở cặp4a'),('yellow','ô màu vàng ở cặp4b')])+
 entries('Đồ dùng học tập',[('paper','tờ giấy, hình1 trang School Supplies'),('scissors','chiếc kéo, hình2'),('glue','lọ keo có đầu nhọn, hình3'),('paint','lọ màu vẽ và cọ, hình4'),('tape','hộp băng keo, hình5')])+
 entries('Hành động',[('stand up','bé đứng dậy ở cặp5a'),('sit down','bé ngồi xuống ở cặp5b'),('come here','bé đi về phía cô giáo ở cặp6a'),('turn around','bé quay người lại ở cặp6b')]),
 phrases=['I have paper.','Stand up.','Sit down.','Come here.','Turn around.'],model='I have paper.',meaning='Tôi có giấy.',
 model_wrong=['Tôi có kéo.','Tôi có băng keo.'],
 cloze=[('I have ________.','paper','🖼️tờ giấy'),('________ up.','Stand','🖼️đứng lên'),('Sit ________.','down','🖼️ngồi xuống'),('Come ________.','here','🖼️đi về phía người gọi'),('Turn ________.','around','🖼️quay người')],
 mixed=[('Nhìn cặp1a và ô màu3a. Chọn cặp từ gọi đúng hai hình.','car / green',['train / green','car / red']),('Nhìn cặp2b và ô màu4b. Chọn cặp từ đúng.','ball / yellow',['bicycle / yellow','ball / purple']),('Nhìn hình3 School Supplies và bé ở cặp5b. Chọn cặp từ đúng.','glue / sit down',['paint / sit down','glue / stand up']),('Nhìn hộp băng keo và hình6b. Chọn cặp đúng.','tape / turn around',['paper / turn around','tape / come here'])],
 audit='Giữ come here ở hình6a, không đổi thành go. Lọ keo/hộp băng keo dùng hình nguồn, không dùng emoji chai mỹ phẩm/giấy vệ sinh. Cặp đồ chơi–màu là ghép hai hình riêng; không khẳng định ô tô nguồn có màu xanh lá. Câu nguồn chỉ có I have paper.; không ghi I have scissors/glue/paint/tape là câu đã in trong PDF.',
 cue='Người lớn đưa tờ giấy cho bé và ra hiệu giới thiệu món mình có.',
 translations={'car':'ô tô','train':'tàu hỏa','bicycle':'xe đạp','ball':'quả bóng','green':'xanh lá','red':'đỏ','purple':'tím','yellow':'vàng','paper':'giấy','scissors':'kéo','glue':'keo dán','paint':'màu vẽ','tape':'băng keo','stand up':'đứng lên','sit down':'ngồi xuống','come here':'lại đây','turn around':'quay người lại'}),
'3-4':dict(file='Review 3-4(2).md',tracks=['CD1_71','CD1_72'],pages='36–37',
 vocab=entries('Hình dạng',[('circle','hình tròn bé đang vẽ ở cặp1a'),('square','hình vuông ở cặp1b'),('star','ngôi sao ở cặp2a'),('heart','trái tim ở cặp2b'),('triangle','tam giác trong nhóm3a'),('diamond','hình thoi trong nhóm4a'),('oval','hình bầu dục trong nhóm4b')])+
 entries('Hành động',[('walk','bé đi bộ ở cặp5a'),('run','bé chạy ở cặp5b'),('go','đèn xanh cho phép đi ở cặp6a'),('stop','đèn đỏ yêu cầu dừng ở cặp6b')])+
 entries('Lệnh lớp học',[('Take out your pencil.','bé lấy bút chì ra, hình1 Classroom Commands'),('Put away your pencil.','bé cất bút chì vào hộp, hình2'),('Open your book.','bé mở sách, hình3'),('Close your book.','bé đóng sách, hình4')]),
 phrases=['Take out your pencil.','Put away your pencil.','Open your book.','Close your book.','Please take out your pencil.'],
 model='Please take out your pencil.',meaning='Vui lòng lấy bút chì ra.',model_wrong=['Vui lòng cất bút chì đi.','Vui lòng đóng sách lại.'],
 cloze=[('________ out your pencil.','Take','🖼️lấy bút chì ra'),('________ away your pencil.','Put','🖼️cất bút chì đi'),('________ your book.','Open','🖼️bé đang mở sách'),('________ your book.','Close','🖼️bé đang đóng sách'),('Please take ________ your pencil.','out','🖼️lấy bút chì ra')],
 mixed=[('Nhìn nhóm3a: gọi hình và chọn số lượng.','triangle / 4',['circle / 4','triangle / 5']),('Nhìn nhóm3b: gọi hình và chọn số lượng.','circle / 5',['triangle / 5','circle / 4']),('Nhìn nhóm4a: gọi hình và chọn số lượng.','diamond / 6',['oval / 6','diamond / 7']),('Nhìn nhóm4b: gọi hình và chọn số lượng.','oval / 7',['diamond / 7','oval / 6'])],
 audit='Nguồn có4 tam giác,5 hình tròn,6 hình thoi,7 oval. Các nhóm ký hiệu1–3 bên dưới là biến thể luyện đếm, không phải cặp gốc CD1_71. Open/Close có cùng đuôi your book nên bài điền phải kèm ngữ cảnh để chỉ có một đáp án. Please take out your pencil. giữ như mẫu lịch sự trong nguồn.',
 cue='Bé đóng vai giáo viên: nhìn người lớn sắp lấy bút chì, nói lệnh có Please.',
 translations={'circle':'hình tròn','square':'hình vuông','star':'ngôi sao','heart':'trái tim','triangle':'hình tam giác','diamond':'hình thoi','oval':'hình bầu dục','walk':'đi bộ','run':'chạy','go':'đi / bắt đầu di chuyển','stop':'dừng lại','Take out your pencil.':'Lấy bút chì ra.','Put away your pencil.':'Cất bút chì đi.','Open your book.':'Mở sách ra.','Close your book.':'Đóng sách lại.'}),
'5-6':dict(file='Review 5-6(2).md',tracks=['CD2_35','CD2_36'],pages='54–55',
 vocab=entries('Con vật',[('cat','một con mèo, biến thể luyện số ít'),('cats','nhóm mèo ở cặp1a hoặc1b'),('rabbit','một con thỏ, biến thể luyện số ít'),('rabbits','nhóm thỏ ở cặp2a hoặc2b')])+
 entries('Thức ăn',[('ice cream','kem ở cặp3a'),('cake','bánh ở cặp3b'),('bread','lát bánh mì ở cặp4a'),('rice','bát cơm ở cặp4b')])+
 entries('Hành động',[('skip','bé nhảy chân sáo ở cặp5a'),('jump','bé nhảy bằng hai chân ở cặp5b'),('make a line','các bạn xếp thành hàng ở cặp6a'),('make a circle','các bạn xếp thành vòng tròn ở cặp6b')])+
 entries('Thời tiết',[('sunny','cảnh có nắng, hình1 The Weather'),('cloudy','cảnh nhiều mây, hình2'),('windy','cảnh gió làm lá/khăn bay, hình3'),('rainy','cảnh mưa, hình4'),('snowy','cảnh có tuyết, hình5')]),
 phrases=['ice cream','Make a line.','Make a circle.',"It's sunny."],model="It's sunny.",meaning='Trời có nắng.',model_wrong=['Trời có mưa.','Trời có tuyết.'],
 cloze=[('cat_','s','🖼️nhóm3 con mèo'),('rabbit_','s','🖼️nhóm2 con thỏ'),('ice ________','cream','🖼️kem'),('Make a ________.','line','🖼️các bạn xếp thành hàng'),('Make a ________.','circle','🖼️các bạn xếp thành vòng tròn'),("It's ________.",'sunny','🖼️cảnh có nắng')],
 mixed=[('Nhóm1a có3 con mèo. Chọn từ số nhiều và số lượng.','cats / 3',['cat / 3','cats / 4']),('Nhóm1b có4 con mèo. Chọn cặp đúng.','cats / 4',['cats / 3','rabbits / 4']),('Nhóm2a có2 con thỏ. Chọn cặp đúng.','rabbits / 2',['rabbit / 2','rabbits / 5']),('Nhóm2b có5 con thỏ. Chọn cặp đúng.','rabbits / 5',['cats / 5','rabbits / 2']),('Nhìn hình kem và cảnh có gió. Chọn cặp từ đúng.','ice cream / windy',['cake / windy','ice cream / cloudy'])],
 audit='Giữ lượng nguồn3/4 mèo và2/5 thỏ. Hình1 con vật là biến thể luyện số ít, không gán cho nhóm gốc. Windy cần dấu hiệu gió, không dùng đám mây đơn để thay. Jump và skip có động tác khác nhau. Câu in trong nguồn chỉ là It\'s sunny.; không tuyên bố các câu thời tiết khác đã in hoặc có audio. Nhãn hành động là cách gọi tranh để luyện, chưa phải bản chép MP3.',
 cue='Người lớn chỉ cảnh có nắng trong trang The Weather, bé nói một câu đầy đủ.',
 translations={'cat':'con mèo','cats':'các con mèo','rabbit':'con thỏ','rabbits':'các con thỏ','ice cream':'kem','cake':'bánh','bread':'bánh mì','rice':'cơm','skip':'nhảy chân sáo','jump':'nhảy bằng hai chân','make a line':'xếp thành hàng','make a circle':'xếp thành vòng tròn','sunny':'có nắng','cloudy':'có mây','windy':'có gió','rainy':'có mưa','snowy':'có tuyết'}),
'7-8':dict(file='Review 7-8(2).md',tracks=['CD2_70','CD2_71','CD2_72'],pages='72–73',
 vocab=entries('Hành động',[('wink','bé nháy một mắt ở cặp1a'),('touch your knees','bé đặt hai tay lên đầu gối ở cặp1b'),('touch your toes','bé chạm được tới ngón chân giày ở cặp2a'),('ride a bicycle','bé đi xe đạp ở cặp3a'),('fly a kite','bé thả diều ở cặp3b'),('swim','bé bơi ở cặp4a'),('dance','bé nhảy múa ở cặp4b'),('Stamp your feet.','bé giậm chân ở cặp5a'),('Clap your hands.','bé vỗ tay ở cặp5b'),('Point to the board.','bé chỉ vào bảng ở cặp6a'),('Stand up.','bé đứng lên ở cặp6b')])+
 entries('Ngày trong tuần',[(w,f'thẻ ngày số{i+1} ở mục Say these.') for i,w in enumerate(['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])]),
 phrases=['Touch your toes.','Ride a bicycle.','Fly a kite.','Point to the board.','Stamp your feet.','Clap your hands.',"It's Monday."],model="It's Monday.",meaning='Hôm nay là thứ Hai.',model_wrong=['Hôm nay là thứ Ba.','Hôm nay là Chủ nhật.'],
 cloze=[('ride a ________','bicycle','🖼️đi xe đạp'),('fly a ________','kite','🖼️thả diều'),('touch your ________','toes','🖼️chạm ngón chân giày'),('Point to the ________.','board','🖼️chỉ vào bảng'),('Clap your ________.','hands','🖼️vỗ tay'),("It's ________.",'Monday','🖼️thẻ ngày thứ Hai')],
 mixed=[('Nhìn thẻ ngày2 và hình3a. Chọn cặp đúng.','Monday / ride a bicycle',['Tuesday / ride a bicycle','Monday / fly a kite']),('Nhìn thẻ ngày4 và hình4a. Chọn cặp đúng.','Wednesday / swim',['Thursday / swim','Wednesday / dance']),('Nhìn thẻ ngày7 và hình5b. Chọn cặp đúng.','Saturday / Clap your hands.',['Sunday / Clap your hands.','Saturday / Stamp your feet.']),('Cặp2: hình nào chạm được tới giày?','2a',['2b','Cả hai hình đều chạm được'])],
 audit='Hình1b là tay lên đầu gối, không phải wink. Cụm touch your knees là cách gọi hình để luyện, không phải chữ in/bản chép audio. Cặp2a chạm được giày;2b chưa chạm được. Cặp5a giậm chân,5b vỗ tay: đưa vào bài chính, không thay bằng dance. Thẻ ngày có Sunday1 đến Saturday7; số này là thứ tự THẺ, không phải số thứ trong tiếng Việt hay ngày tháng. Lịch tháng nhỏ có ngày1 ở cộtMonday, khác với thẻMonday số2. CD2_72 không có lời hát in trong PDF, không thêm lời hát tự viết.',
 cue='Người lớn chỉ thẻ Monday hoặc ô lịch nằm trong cộtMonday, bé nói một câu đầy đủ.',
 translations={'wink':'nháy một mắt','touch your knees':'đặt/chạm hai tay lên đầu gối','touch your toes':'chạm vào ngón chân','ride a bicycle':'đi xe đạp','fly a kite':'thả diều','swim':'bơi','dance':'nhảy múa','Stamp your feet.':'Giậm chân.','Clap your hands.':'Vỗ tay.','Point to the board.':'Chỉ vào bảng.','Stand up.':'Đứng lên.','Sunday':'Chủ nhật','Monday':'thứ Hai','Tuesday':'thứ Ba','Wednesday':'thứ Tư','Thursday':'thứ Năm','Friday':'thứ Sáu','Saturday':'thứ Bảy'})}

NAMES=['Vocabulary Master','Listen & Understand','Fill & Recall','Build & Match','Final Boss']
LEVELS=['Recognition','Recognition → Comprehension','Recall','Comprehension','Production']

class Guide:
    def __init__(self,pair,data):
        self.pair=pair;self.data=data;self.lines=[];self.questions=[];self.c=0;self.n=0
        self.rng=random.Random(100+int(pair[0]));self.audio=set()
    def add(self,*s):self.lines.extend(s)
    def chapter(self,c):
        self.c=c;self.n=0
        self.add('---','',f'# Challenge {c} — {NAMES[c-1]}',f'**Level: {LEVELS[c-1]}**','')
    def q(self,prompt,answer,options=None,kind='short',audio=None):
        self.n+=1;qid=f'R{self.pair.replace("-","")}-C{self.c}-{self.n:02}'
        self.add(f'### {qid}',prompt,'')
        q={'id':qid,'challenge':self.c,'prompt':prompt,'answer':answer,'type':kind}
        if kind=='match':q['accepted_answers']=[answer.split(' — ',1)[0]]
        if options is not None:
            choices=list(dict.fromkeys([answer,*options]));self.rng.shuffle(choices)
            assert len(choices)>=2 and choices.count(answer)==1
            q['choices']=[{'id':chr(65+i),'text':v} for i,v in enumerate(choices)]
            q['correct_choice_id']=chr(65+choices.index(answer))
            for choice in q['choices']:self.add(f"- [ ] {choice['id']}. {choice['text']}")
        else:self.add('→ ______________________________')
        if audio:
            self.audio.add(audio);q['audio_script']=audio
            self.add('',f'> Người lớn/clip riêng đọc **{audio}**; khi cho bé làm, ẩn dòng này.')
        self.add('');self.questions.append(q)
        return qid
    def distract(self,vocab,target):
        pool=[v['word'] for v in vocab if v['word']!=target]
        self.rng.shuffle(pool);return pool[:3]
    def scramble(self,phrase):
        tokens=phrase.split()
        if len(tokens)<2:return phrase
        original=tokens[:]
        while tokens==original:self.rng.shuffle(tokens)
        assert Counter(tokens)==Counter(original)
        return ' / '.join(tokens)

def normalize(s):return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_')

def author(pair,d):
    doc=ROOT/d['file'];original=doc.read_text(encoding='utf-8-sig')
    initial_digest=hashlib.sha256(doc.read_bytes()).hexdigest()
    folder=ROOT/f'Review {pair} - Lesson Pages'
    backup=folder/'references/challenge-before-pattern-update.md'
    if not backup.exists():backup.write_text(original,encoding='utf-8')
    g=Guide(pair,d);linkbase=quote(folder.name,safe='/')+'/'
    g.add(f'# Review {pair} — Ôn tập theo 5 Challenge','',
      f'**Nguồn đối chiếu:** Review {pair}.pdf, trang sách {d["pages"]}; các hình được kiểm trực quan trên hai trang nguồn.',
      '**Lộ trình:** Recognition → Recall → Comprehension → Production.','',
      '## Bộ trang học và cách dùng','',
      f'- [Ảnh + audio + câu hỏi theo track]({linkbase}preview.html) · [Xem cả bộ]({linkbase}preview.jpg).',
      f'- [Metadata]({linkbase}review.regenerated.metadata) · [Câu hỏi theo trang]({linkbase}questions.md).',
      f'- Mục học chính: **{", ".join(d["tracks"])}**. Mỗi mục vẫn có một câu trắc nghiệm sau nghe; các Challenge dưới đây là bài luyện tổng hợp riêng.',
      '- Người lớn chỉ đúng hình/diễn động tác theo mô tả 🖼️; hình không gắn sẵn là yêu cầu chọn hình, không phải asset đã tạo riêng. Không dùng emoji mơ hồ thay cho đồ dùng/động tác.',
      '- Chọn mỗi lần một nhóm câu vừa sức; không bắt bé làm hết trong một lượt. Ưu tiên nói/chọn/diễn, viết khi phù hợp.',
      '- Ở bài nhớ và tự nói, che nhãn tiếng Anh, kho từ và đáp án. Câu nghe dùng clip riêng hoặc người lớn đọc; giấu script audio với bé.',
      '- Đáp án cuối file dùng cho người lớn, không hiển thị trước khi bé trả lời. Chấp nhận phát âm hiểu được; phần nói không bắt buộc đúng dấu câu.',
      '- Đây là đáp án bài luyện bổ sung, **không phải đáp án đã nghe xác nhận của Listen and circle**. MP3 CD chưa được nghe/transcribe độc lập.','',
      '## Nội dung cần nắm','')
    groups=list(dict.fromkeys(v['group'] for v in d['vocab']))
    for group in groups:g.add(f'### {group}',' · '.join('`'+v['word']+'`' for v in d['vocab'] if v['group']==group),'')
    if pair=='3-4':g.add('### Số lượng','1–7; nhóm nguồn gồm4 tam giác,5 hình tròn,6 hình thoi,7 oval.','')
    if pair=='7-8':g.add('**Thứ tự thẻ nguồn:** Sunday1 → Monday2 → Tuesday3 → Wednesday4 → Thursday5 → Friday6 → Saturday7.','')
    g.add('### Câu mẫu',f'`{d["model"]}`','', '### Ghi chú đối chiếu',d['audit'],'')

    # C1: all vocabulary covered through identifiable contexts.
    g.chapter(1)
    for group in groups:
        vs=[v for v in d['vocab'] if v['group']==group]
        g.add(f'## Nhìn hình → chọn từ: {group}','')
        for v in vs:g.q('🖼️'+v['picture']+'. Chọn từ/cụm từ đúng.',v['word'],g.distract(vs,v['word']),kind='choice')
    if pair=='3-4':
        g.add('## Đếm nhóm ký hiệu → chọn số','', 'Nhóm ký hiệu là biến thể luyện đếm, không phải lựa chọn/đáp án của track gốc.','')
        for n in range(1,8):g.q('Đếm: '+'△ '*n,str(n),[str(x) for x in range(1,8) if x!=n][:2],kind='choice')
    g.add('## Vòng nghe bổ sung','',
      'Người lớn chọn một từ trong nhóm đang học, đọc mà không cho bé thấy chữ; bé chọn hình tương ứng. Ghi từ đã chọn trước lượt nghe, chấm theo từ thực sự được đọc. Không có một đáp án cố định cho vòng chọn ngẫu nhiên.','')

    # C2: spread all topic groups; commands have actual action distractors.
    g.chapter(2)
    for group in groups:
        vs=[v for v in d['vocab'] if v['group']==group]
        for v in vs[:2]:g.q('Nghe từ/cụm từ và chọn đúng mục.',v['word'],g.distract(vs,v['word']),kind='choice',audio=v['word'])
    action_words=[v for v in d['vocab'] if v['group'] in ['Hành động','Lệnh lớp học']]
    g.add('## Nghe → chọn ý nghĩa/hành động','')
    for v in action_words:
        others=[d['translations'][a['word']] for a in action_words if a['word']!=v['word']]
        g.q('Chọn ý nghĩa của câu/lệnh vừa nghe.',d['translations'][v['word']],others[:2],kind='choice',audio=v['word'])
    g.q('Nghe câu mẫu và chọn ý nghĩa.',d['meaning'],d['model_wrong'],kind='choice',audio=d['model'])
    if pair=='3-4':
        for n,word in [(4,'four'),(6,'six'),(7,'seven')]:g.q('Nghe số lượng và chọn số.',str(n),[str(n-1),str(n+1)],kind='choice',audio=word)
    if pair=='7-8':
        for n,day in enumerate(['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],1):
            g.q('Nghe tên ngày: chọn số THẺ trong mục Say these., không chọn ngày tháng.',str(n),[str(x) for x in [1,2,3,4,5,6,7] if x!=n][:2],kind='choice',audio=day)

    # C3: real missing letters and context disambiguates identical stems.
    g.chapter(3)
    g.add('## Điền chữ còn thiếu','')
    short_words=[v['word'] for v in d['vocab'] if ' ' not in v['word'] and '.' not in v['word']]
    for word in short_words:
        index=next((i for i,c in enumerate(word) if c.lower() in 'aeiou'),1)
        masked=word[:index]+'_'+word[index+1:]
        g.q(f'Hoàn thành từ: `{masked}`.',word,kind='spelling')
    g.add('## Điền theo ngữ cảnh','')
    g.add('**Kho từ/chữ:** '+' · '.join('`'+v+'`' for v in dict.fromkeys(a for _,a,_ in d['cloze'])),
          'Dùng kho ở lượt đầu; lượt ôn sau che kho. Mỗi chỗ trống đã có hình/ngữ cảnh để xác định một đáp án.','')
    for sentence,answer,context in d['cloze']:g.q(f'{context}. Điền: `{sentence}`.',answer)
    if pair=='3-4':
        for n in [4,5,6,7]:g.q('Đếm và điền số: '+'◆ '*n,str(n))
    if pair=='5-6':
        g.q('Điền từ số ít/số nhiều: 🖼️1 con mèo → ________.','cat')
        g.q('Điền từ số ít/số nhiều: 🖼️5 con thỏ → ________.','rabbits')
    if pair=='7-8':
        for seq,answer in [('Sunday → ___ → Tuesday','Monday'),('Tuesday → ___ → Thursday','Wednesday'),('Thursday → ___ → Saturday','Friday')]:g.q('Điền ngày còn thiếu: '+seq,answer)
    g.q('Nghe câu mẫu và điền: '+('`I have ________.`' if pair=='1-2' else '`'+d['model'].replace(d['cloze'][-1][1],'________')+'`' if pair in ['5-6','7-8'] else '`Please take ________ your pencil.`'),
        'paper' if pair=='1-2' else 'out' if pair=='3-4' else d['cloze'][-1][1],audio=d['model'])

    # C4: shuffled source phrases plus real matching and mixed topics.
    g.chapter(4)
    g.add('## Sắp xếp thẻ → ghép câu/cụm từ','', 'Dùng đúng các thẻ, thêm/chỉnh viết hoa ở đầu câu khi cần; không cần thêm từ.','')
    for phrase in d['phrases']:g.q('Các thẻ: `'+g.scramble(phrase)+'`.',phrase,kind='order')
    g.add('## Ghép hình/ngữ cảnh với từ','')
    selected=[next(v for v in d['vocab'] if v['group']==group) for group in groups]
    options=[v['word'] for v in selected];g.rng.shuffle(options)
    if options==[v['word'] for v in selected]:options=options[1:]+options[:1]
    g.add('**Các thẻ từ:** '+' · '.join(f'{chr(65+i)}. {w}' for i,w in enumerate(options)),'')
    for v in selected:
        letter=chr(65+options.index(v['word']))
        g.q('🖼️'+v['picture']+'. Điền chữ cái của thẻ phù hợp.',letter+' — '+v['word'],kind='match')
    g.add('## Ghép kiến thức giữa các nhóm','')
    for prompt,correct,wrong in d['mixed']:g.q(prompt,correct,wrong,kind='choice')

    # C5: no-hint retrieval and source-backed model application.
    g.chapter(5)
    g.add('## Quick Recognition tổng hợp','')
    for prompt,correct,wrong in d['mixed'][:3]:g.q(prompt,correct,wrong,kind='choice')
    g.add('## Nhìn hình → tự nói, không kho từ','')
    for group in groups:
        vs=[v for v in d['vocab'] if v['group']==group]
        # Final Boss retains no-hint recall of every vocabulary item, like Unit1.
        for v in vs:g.q('Người lớn chỉ/diễn: '+v['picture']+'. Bé tự nói từ/cụm phù hợp.',v['word'],kind='production')
    if pair=='3-4':
        for name,n in [('triangle',4),('circle',5),('diamond',6),('oval',7)]:g.q(f'Người lớn chỉ nhóm nguồn {n} hình {name}, che nhãn/số. Bé nói hình và số lượng.',f'{name} — {n}',kind='production')
    if pair=='5-6':g.q('Che nhãn: chỉ nhóm mèo ở1b và nhóm thỏ ở2b. Bé gọi số nhiều và đếm mỗi nhóm.','cats — 4; rabbits — 5',kind='production')
    if pair=='7-8':g.q('So sánh cặp2a/2b: chỉ hình chạm được giày, rồi gọi đúng động tác.','2a — touch your toes',kind='production')
    g.add('## Nghe → thực hiện/chỉ hình','',
      'Người lớn đọc ngẫu nhiên một lệnh/hành động trong kho của Review; bé thực hiện hoặc chỉ hình đúng, rồi nói lại. Động tác cần đồ dùng có thể chỉ hình/diễn minh họa. Chấm theo lệnh thực sự được đọc, không theo thứ tự in trong file.','')
    g.add('**Kho lệnh:** '+' · '.join('`'+v['word']+'`' for v in action_words),'')
    g.q('Nói câu đầy đủ theo tình huống, không nhìn câu mẫu: '+d['cue'],d['model'],kind='production')
    g.add('## Cách chấm phần tự nói','',
      '- Nhận biết: chọn đúng hình/từ/nhóm. Nhớ lại: nói đúng từ hoặc điền đúng nội dung; bài đếm phải đúng lượng thực tế.',
      '- Ghép câu: đúng từ và thứ tự; không thêm từ ngoài thẻ. Tự nói: chấp nhận cách viết hoa/dấu câu tương đương; ưu tiên câu hiểu được.',
      '- Mỗi câu chưa đúng cho bé thử lại sau gợi ý ngắn; lượt đầu của Final Boss không mở kho từ/đáp án.','')

    # Answer bank is complete for every fixed task; variable rounds are specified separately.
    g.add('---','', '# Đáp án dành cho người lớn','',
      'Ẩn phần này khi bé làm bài. Đây là đáp án bài luyện bổ sung, không gán đáp án cho track Listen and circle chưa được nghe xác nhận.','')
    for c in range(1,6):
        g.add(f'## Challenge {c}','', '| Mã câu | Đáp án / câu mẫu |','|---|---|')
        for q in g.questions:
            if q['challenge']==c:
                ans=(q['correct_choice_id']+'. ' if 'correct_choice_id' in q else '')+q['answer']
                g.add('| '+q['id']+' | '+ans.replace('|','\\|')+' |')
        g.add('')
    g.add('Vòng nghe ngẫu nhiên và thực hiện động tác: đáp án là từ/lệnh người lớn đã chọn trước lượt; không có bảng đáp án cố định.','',
      '# Coverage Check','', '| Nhóm nội dung | Bài luyện đối chiếu |','|---|---|')
    for group in groups:g.add(f'| {group} | C1 nhận biết; vòng nghe theo kho; C3/C4/C5 chọn nội dung phù hợp nhóm |')
    if pair=='3-4':g.add('| Số1–7 và4 nhóm hình nguồn | C1 đếm; C2 nghe số; C3 đếm; C4/C5 ghép hình–lượng |')
    g.add(f'| Câu mẫu `{d["model"]}` | C2 nghe nghĩa; C3 điền; C4 ghép; C5 tự nói |','',
      '**Phạm vi kiểm tra:** đã đọc trực quan hai trang nguồn, kiểm từ/câu/ngữ cảnh, lượng và thứ tự thẻ trong bài luyện. Không tuyên bố đã kiểm chứng lời nói toàn bộ MP3.','')

    # Translation is optional support, removed from the core challenge sequence.
    g.add('# Phụ lục tùy chọn — Hỗ trợ nghĩa tiếng Việt','',
      'Dùng khi bé cần hiểu nghĩa; không bắt làm toàn bộ bảng dịch và không tính như một Challenge riêng.','', '| Từ/cụm | Nghĩa hỗ trợ |','|---|---|')
    for w,meaning in d['translations'].items():g.add(f'| {w} | {meaning} |')
    g.add(f'| {d["model"]} | {d["meaning"]} |','')

    # Reuse existing recording names whenever the same script already has a note.
    old_clips={}
    for row in original.splitlines():
        if '.mp3`' not in row:continue
        cells=[s.strip() for s in row.strip('|').split('|')]
        for i,cell in enumerate(cells):
            if re.fullmatch(r'`[^`]+\.mp3`',cell) and i+1<len(cells):old_clips[normalize(cells[i+1])]=cell.strip('`')
    pool=[v['word'] for v in d['vocab']]+[d['model']]
    if pair=='3-4':pool+=['one','two','three','four','five','six','seven','Please take out your pencil.']
    unique={}
    for script in pool:unique.setdefault(normalize(script),script)
    g.add('<!-- challenge-audio-notes -->','# Audio clip riêng cần chủ dự án bổ sung','',
      '**Chủ dự án tự chuẩn bị audio.** Mọi file dưới đây là tên gợi ý, vẫn chưa hoàn thành; không tự sinh audio trong lần cập nhật nội dung này. Track CD nguồn phục vụ trang học chính, không mặc định thay các clip ngắn.',
      'Mỗi nội dung thu một clip dùng chung. Kho từ dùng cho vòng nghe ngẫu nhiên C1; câu nghe cố định có script ở C2/C3; kho hành động dùng cho C5. Chọn clip phải nằm trong đúng tập lựa chọn.',
      'Các cách gọi tranh như touch your knees/Stamp your feet./Clap your hands. là script luyện bổ sung, không khẳng định MP3 CD nói đúng các cụm này.','',
      '| Đã có | File gợi ý | Nội dung đọc | Mức / nơi dùng |','|---|---|---|---|')
    audio_rows=[]
    for slug,script in unique.items():
        filename=old_clips.get(slug,f'r{pair.replace("-","")}_{slug}.mp3')
        used=script in g.audio or any(normalize(v['word'])==slug for v in action_words)
        usage='Cần cho câu nghe cố định C2/C3 hoặc lệnh C5; dùng chung vòng C1' if used else 'Cần nếu chạy vòng nghe ngẫu nhiên C1 đầy đủ; tùy chọn làm mẫu phát âm'
        g.add(f'| ☐ | `{filename}` | {script} | {usage} |')
        audio_rows.append({'filename':filename,'script':script,'usage':usage,'status':'not_supplied'})
    g.add('', 'Giọng Boss riêng, hướng dẫn tiếng Việt và phát mẫu sau câu tự nói là tùy chọn. Không cần thu lặp cùng câu cho từng bài. Nếu có file sau này, nối đường dẫn thực tế rồi mới đánh dấu đã có.')
    if pair=='7-8':g.add('Không tự viết lời hát cho Review 7–8: nguồn không in lời hát; bài hát chính vẫn dùng CD2_72.')
    g.add('Nếu cần clip hội thoại/biến thể mới, ghi rõ script và nguồn trước khi thu.', '<!-- /challenge-audio-notes -->','')

    content='\n'.join(g.lines)+'\n'
    content=re.sub(r'(cặp|hình|nhóm|thẻ ngày|Challenge|Review|Unit)(\d)',r'\1 \2',content)
    assert hashlib.sha256(doc.read_bytes()).hexdigest()==initial_digest,'Concurrent document edit; re-read before writing'
    doc.write_text(content,encoding='utf-8')
    # A standalone copy inside the package uses local links and shares the same content.
    (folder/'challenge-guide.md').write_text(content.replace(linkbase,''),encoding='utf-8')
    structured={'review':pair,'source_pdf':f'Review {pair}.pdf','tracks':d['tracks'],'pattern':NAMES,'questions':g.questions,'audio_notes':audio_rows,'audio_status':'not independently transcribed','source_audit':d['audit']}
    (folder/'challenge-content.json').write_text(json.dumps(structured,ensure_ascii=False,indent=2),encoding='utf-8')
    readme=folder/'README.md';r=readme.read_text(encoding='utf-8')
    marker='<!-- five-challenge-guide -->'
    if marker in r:r=r[:r.index(marker)].rstrip()+'\n'
    r+='\n'+marker+'\n## Bài luyện theo5 Challenge\n\n[Hướng dẫn/bài luyện/đáp án/audio notes](challenge-guide.md) · [Nội dung câu luyện có mã](challenge-content.json).\n\nChuẩn hóa Recognition → Listen & Understand → Recall → Build & Match → Final Boss. Dịch nghĩa là phụ lục hỗ trợ. Kho câu luyện bổ sung riêng với câu trắc nghiệm theo track; preview hiện tại vẫn phục vụ trang học chính, chưa có giao diện chạy toàn bộ Challenge.\n'
    readme.write_text(r,encoding='utf-8')
    verify(pair,folder,doc,structured)
    return {'review':pair,'questions':len(g.questions),'audio_notes':len(audio_rows),'document':str(doc)}

def verify(pair,folder,doc,structured):
    text=doc.read_text(encoding='utf-8')
    assert re.findall(r'^# Challenge (\d) — (.+)$',text,re.M)==[(str(i),name) for i,name in enumerate(NAMES,1)]
    qs=structured['questions'];ids=[q['id'] for q in qs]
    assert len(ids)==len(set(ids))
    for q in qs:
        assert text.count('### '+q['id']+'\n')==1
        assert re.search(r'^\| '+re.escape(q['id'])+r' \|',text,re.M),'Missing answer'
        assert q['answer']
        if 'choices' in q:
            assert len({c['text'] for c in q['choices']})==len(q['choices'])
            assert next(c['text'] for c in q['choices'] if c['id']==q['correct_choice_id'])==q['answer']
    for path in [doc,folder/'challenge-guide.md',folder/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):assert (path.parent/unquote(target)).exists(),(path,target)
    assert all(a['status']=='not_supplied' for a in structured['audio_notes'])
    assert 'Translate & Build' not in text
    if pair=='7-8':assert 'touch your knees' in text
    report={'result':'pass','review':pair,'scope':'Challenge content only; existing image/audio validation unchanged','chapter_count':5,'fixed_question_count':len(qs),'checks':['unique IDs','answer for every fixed question','distinct choices with a valid key','five requested challenge stages','all document links resolve','audio notes remain unfulfilled'],'source_review':'Both source PDF page renders inspected visually; new labels and counting variants explicitly marked.','limitations':['CD speech not independently audited','Challenge UI not implemented; current preview is the track lesson preview']}
    (folder/'challenge-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    dest=ROOT/f'Review_{pair}_regenerated.zip'
    temporary=dest.with_suffix('.writing.zip')
    with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(folder))
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        for p in ['challenge-guide.md','challenge-content.json','challenge-validation.json']:assert p in z.namelist()
        assert z.read('challenge-guide.md').decode('utf-8').replace('\r\n','\n')==(folder/'challenge-guide.md').read_text(encoding='utf-8')
    temporary.replace(dest)

if __name__=='__main__':
    results=[author(pair,d) for pair,d in DATA.items()]
    for r in results:print(json.dumps(r,ensure_ascii=True))
