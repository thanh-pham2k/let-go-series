"""Build source-anchored Challenge image briefs; does not generate media."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / 'Let_s Go Begin/Units'
OUT = ROOT / 'parallel-prompts/challenge-images'
TOPICS = ['Toys', 'Colors', 'Shapes', 'Numbers', 'Animals', 'Food', 'My Body', 'Abilities']
REG = {n: {} for n in range(1, 9)}

def add(n, key, description, tracks, method='crop_or_edit', note=''):
    REG[n][key] = dict(id=f'u{n:02d}_{key}', brief=description, reference_tracks=tracks,
                       method=method, note=note, uses=[])

toys = [('ball', 'Một quả bóng'), ('jump_rope', 'Một dây nhảy với hai tay cầm'),
        ('yo_yo', 'Một yo-yo, dây rõ'), ('bicycle', 'Một xe đạp đủ hai bánh'),
        ('train', 'Một tàu hỏa đồ chơi'), ('car', 'Một ô tô đồ chơi'),
        ('doll', 'Một búp bê'), ('teddy_bear', 'Một gấu bông')]
for i, (k, d) in enumerate(toys):
    add(1, k, d + '; giữ thiết kế/màu của hình từ vựng Unit 1, không có người hoặc món khác.',
        ['CD1_07' if i < 4 else 'CD1_11'])

colors = ['red', 'blue', 'yellow', 'green', 'brown', 'purple', 'orange', 'black', 'white', 'pink']
for c in colors:
    add(2, 'color_'+c, f'Mảng màu {c}, cùng hình dạng/kích thước với 9 mảng còn lại; màu trắng có viền xám mảnh để nhìn được trên nền trắng.',
        ['CD1_24', 'CD1_28'], 'native_graphic')
for k,d in [('red_train','Tàu hỏa đồ chơi màu đỏ'),('blue_ball','Bóng màu xanh dương'),
            ('brown_teddy_bear','Gấu bông màu nâu'),('green_yo_yo','Yo-yo màu xanh lá'),('green_car','Ô tô đồ chơi màu xanh lá')]:
    add(2,k,d+'; một vật, giữ thiết kế trang mẫu, không nhãn.', ['CD1_35' if k=='green_car' else 'CD1_34'])
for k in ['apple','bird','cat','dog']:
    add(2,k,f'Một {k} giống minh họa phonics A–D; không chữ cái, không tên từ.', ['CD1_33'])

shapes = ['circle','square','triangle','heart','star','rectangle','diamond','oval']
for k in shapes:
    add(3,k,f'Một hình {k}, hình học chính xác và rõ; màu không phải mục tiêu câu hỏi. Giữ hình dạng/màu cơ bản theo trang Words; diamond là hình thoi, không phải đá quý.',
        ['CD1_43' if k in shapes[:4] else 'CD1_47'], 'native_graphic')
for c,k in [('blue','square'),('purple','heart'),('orange','triangle'),('yellow','circle'),('green','square'),('pink','heart')]:
    add(3,f'{c}_{k}',f'Một hình {k} màu {c} thuần, không vật phụ; giữ cùng nét viền/hình học của bộ Shapes.', ['CD1_53','CD1_54'], 'native_graphic')
for k in ['egg','fish','gorilla']:
    add(3,k,f'Một {k} giống phonics E–H; fish là cá sống, gorilla rõ dáng khỉ đột; không chữ.', ['CD1_52'])
# Phonics H uses the same heart as the shape task, not a second duplicate.

for count in range(1,6):
    add(4,f'dots_{count:02d}',f'Đúng {count} chấm tròn đặc ●, tách rời và dễ đếm. Đây là ký hiệu chấm trong bài luyện, không tự đổi thành bóng đồ chơi.', ['CD1_60'], 'native_graphic')
for k,count in [('rings',5),('triangles',6),('stars',7),('circles',8),('hearts',9),('squares',10)]:
    add(4,f'{k}_{count:02d}',f'Đúng {count} hình {k}, giống ký hiệu nhóm trong bài luyện (rings = ◎; circles = ○), không số/nhãn, không chồng lên nhau.', ['CD1_64','CD1_67'], 'native_graphic')
for k,count in [('cars',3),('teddy_bears',4),('cars',7)]:
    add(4,f'{k}_{count:02d}',f'Đúng {count} {k}, từng vật trọn vẹn, tách nhau, dễ đếm; không số, không vật cùng loại trong nền.', ['CD1_60','CD1_62'], 'compose_from_crops')
for k in ['igloo','jump_rope','kangaroo','lion']:
    add(4,k,f'Một {k} theo phonics I–L. Igloo là nhà băng vòm (không nhà tranh dù emoji là 🛖); jump rope là vật dây nhảy, không cảnh bé nhảy.', ['CD1_69'])

animals = {'🐶':'dog','🐱':'cat','🐦':'bird','🐄':'cow','🐇':'rabbit','🦆':'duck'}
for k in animals.values():
    for count in [1,2]:
        add(5,f'{k}_{count:02d}',f'Đúng {count} con {k}; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.',
            ['CD2_07' if k in ['dog','cat','bird'] else 'CD2_11'], 'compose_from_crops')
for k,count in [('bird',3),('duck',3),('cow',8),('car',8)]:
    add(5,f'{k}_{count:02d}',f'Đúng {count} {k}; không thêm vật cùng loại, không số hoặc nhãn. Không sao chép cả cảnh nguồn nếu cảnh có số lượng khác.', ['CD2_13','CD2_19'], 'compose_from_crops')
for k in ['moon','nest','octopus','peach']:
    add(5,k,f'Một {k} theo phonics M–P; nest là tổ chim, không thêm chim làm thay đổi đối tượng chính; octopus đủ 8 tay, peach là đào.', ['CD2_17'])

food = {'🍦':'ice_cream','🍕':'pizza','🎂':'cake','🍗':'chicken','🥛':'milk','🐟':'fish','🍞':'bread','🍚':'rice'}
for k in food.values():
    add(6,k,f'Một món {k} theo tranh Food; không nhãn. Chicken là món thịt gà, fish là món cá theo trang Food (không lấy cá sống của phonics Unit 3).', ['CD2_25','CD2_29'])
for k in ['queen','rabbit','sun','tiger']:
    add(6,k,f'Một {k} theo phonics Q–T, không chữ.', ['CD2_33'])
add(6,'birds','Nhóm chim để thể hiện birds, không số lượng cố định trong câu. Có thể dùng 2 con tách rõ, ghi là adaptation cho số nhiều, không biến câu thành bài đếm.', ['CD2_07'], 'compose_from_crops')
add(6,'likes_milk','Bé với ly sữa, biểu cảm và cử chỉ thích rõ; dùng cho tình huống mẫu Yes, I do. Không in câu trả lời hoặc dấu tick.', ['CD2_31'], 'edit_or_generate')
add(6,'dislikes_fish','Bé với món cá, cử chỉ nhẹ nhàng từ chối rõ; dùng cho tình huống mẫu No, I don’t. Không in câu trả lời hoặc dấu X.', ['CD2_31'], 'edit_or_generate')

for k in ['head','shoulders','knees','toes','eyes','ears','mouth','nose']:
    add(7,k,f'Bộ phận {k} trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.', ['CD2_42','CD2_46'], 'edit_or_generate')
for k in ['head','nose','eyes']:
    add(7,'touch_'+k,f'Bé đang chạm đúng {k}; động tác rõ, bàn tay tự nhiên, không che mất vùng cần nhận diện. Chạm mắt nhẹ ở vùng cạnh mắt, không chọc vào nhãn cầu.', ['CD2_44','CD2_48'], 'edit_or_generate')
add(7,'red_circle','Một hình tròn màu đỏ, không chữ, để bé chỉ/chạm trong câu I can touch the red circle.', ['CD2_52','CD2_53'], 'native_graphic')
for k in ['umbrella','violin','watch']:
    add(7,k,f'Một {k} theo phonics U–W; watch là đồng hồ đeo tay, không đồng hồ treo tường; không chữ.', ['CD2_51'])

abilities = {'🚲':'ride_bicycle','🎤':'sing_song','🎵':'sing_song','🪁':'fly_kite','🏀':'bounce_ball','🏊':'swim','😊':'smile','😉':'wink','💃':'dance'}
details = {'ride_bicycle':'Bé thực sự đang đạp xe, chân trên bàn đạp, hai bánh rõ',
 'sing_song':'Bé đang hát, miệng mở, cử chỉ hát và nốt nhạc phụ vừa đủ',
 'fly_kite':'Bé đang thả diều bay, dây nối tay với diều rõ',
 'bounce_ball':'Bé đập bóng xuống đất, tay/bóng/vệt chuyển động thể hiện bounce, không chỉ cầm bóng',
 'swim':'Bé bơi trong nước, cử động rõ', 'smile':'Cận mặt bé cười, cả hai mắt mở',
 'wink':'Cận mặt bé nháy đúng một mắt, mắt kia mở; không giống smile', 'dance':'Bé đang múa/nhảy với tư thế rõ, khác chạy hoặc đứng'}
for k,d in details.items():
    add(8,k,d+'; cùng nhân vật/thiết kế trang Words; không nhãn.', ['CD2_59' if k in list(details)[:4] else 'CD2_63'], 'edit_or_generate')
add(8,'cannot_fly_kite','Cùng bé/diều với fly_kite nhưng diều nằm dưới đất, dây chùng, bé bối rối không thả được; hình diễn đạt can’t, không chỉ dấu X hoặc chữ can’t.', ['CD2_61'], 'edit_or_generate')
for k,d in [('play_ball','Hai bé chơi bóng cùng nhau; khác một bé đập bóng'),('play_tag','Các bé chơi đuổi bắt, một bé đưa tay đuổi/chạm bạn; không chỉ một người chạy'),('jump_rope','Bé đang nhảy qua dây, hai tay cầm và dây đúng chuyển động; khác ảnh vật dây nhảy')]:
    add(8,k,d+'; không lời thoại hay nhãn.', ['CD2_54','CD2_55'], 'edit_or_generate')
for k in ['fox','yarn','zebra']:
    add(8,k,f'Một {k} theo phonics X–Z; yarn là cuộn sợi len, không dây nhảy; không chữ.', ['CD2_68'])
# These two are conditional until the ambiguous fill-in items have an approved cue.
for k in ['make_circle','make_line']:
    add(8,k,'Nhóm bé '+('xếp thành vòng tròn khép kín' if k=='make_circle' else 'xếp thành một hàng thẳng')+'; không chữ.', ['CD2_69'], 'edit_or_generate', 'Đã chốt cue theo yêu cầu người dùng: câu5 circle, câu6 line; dùng lại ảnh hiện có.')

ISSUES = {
 1: [],
 2: [],
 3: ['C3§6: hai câu square và hai câu heart trùng dạng; dùng bộ 6 hình của C5§3 theo thứ tự blue square, purple heart, orange triangle, yellow circle, green square, pink heart. Đây là đề xuất nối context dựa trên C5, phải ghi adaptation_notes.'],
 4: ['C5§4 tình huống 2 nói 7 cars nhưng chỉ có emoji một xe ở tiêu đề: cần nhóm đúng 7 xe. Chấm ● và vòng ◎ là ký hiệu của bài luyện, không tự suy diễn thành ball/yo-yo.'],
 5: ['C3§3 câu 3–5 How many ____? chưa có context phân biệt ducks/cows/cars. Có thể nối lần lượt nhóm 3 ducks, 8 cows, 8 cars theo thứ tự C3§4/C3§5; ghi là đề xuất adaptation, không khẳng định nguồn đã có hình.', 'C3§5 và C5 hội thoại đếm dùng lại duck_03/cow_08/car_08; không tạo nhóm mới mỗi lần.', 'C3§6 1 train, 2 trains, 3 trains là điền số nhiều bằng text; không yêu cầu thêm ba nhóm tàu.'],
 6: ['C3§2: I like ____ / Do you like ____ lặp lại nhưng chưa có context. Dùng đồ ăn đã có để thêm context nếu cần; không tự quyết định đáp án trước khi xác định thứ tự.', 'C3§3 bốn câu I’m ____ chỉ khác thứ tự lựa chọn: không xác định được tuổi bằng khuôn mặt. Giữ là luyện nói tuổi tự chọn hoặc bổ sung cue tuổi/audio trước khi gán đáp án; chữ số 5/6/7/10 render bằng font, không cần 4 tranh sinh nhật.', 'likes_milk/dislikes_fish chỉ dùng tình huống mẫu cố định C5§9. C5§4 và tình huống birds cho phép trả lời sở thích thật: không ép Yes/No theo ảnh.'],
 7: ['C3§2 câu 3–5 touch my ____ và C3§5 hai câu What can you do? thiếu context; dùng lại touch_head/touch_nose/touch_eyes khi đã chọn thứ tự, ghi adaptation; không đoán đáp án từ bộ phận trống.', 'C5§3 icon bộ phận yêu cầu nói I can touch my...: dùng ảnh động tác tương ứng, không chỉ chân dung/vật tĩnh.'],
 8: ['C3§2 câu 5–8 trống hoàn toàn: đề xuất nối swim, smile, wink, dance theo thứ tự từ vựng C1/C3§1; ghi adaptation.', 'C3§3 hai câu I ____ fly a kite thiếu cue: đề xuất nối fly_kite / cannot_fly_kite theo thứ tự bài; hai câu Can you ____ cũng cần cue dance/swim nếu có đáp án cố định.', 'C3§6 play ball/tag và C3§7 Make a circle/line cần context để phân biệt hai câu giống nhau. Hai ảnh make_circle/make_line là CONDITIONAL, không tính vào bộ bắt buộc khi vẫn giữ bài điền mở.', 'Câu Can you swim/dance/jump hỏi khả năng của chính bé có thể Yes hoặc No: không suy diễn đáp án bằng ảnh.'],
}

MARKERS = set('⬛⬜🍎🐦🐱🐶🖼🚗🟥🟦🟧🟨🟩🟪🟫🩷▭◆❤⬭⭐⭕🐟💜🔺🟡🥚🦍□△○◎●☆♡🛖🦁🦘🧸🪢🌙🍑🐄🐇🐙🦆🪺☀🍕🍗🍚🍞🍦🎂🐅👸🥛⌚☂🎻👀👂👃👄👤🙌🦵🦶🧍⚽🎤🎵🏀🏃🏊💃😉😊🚲🦊🦓🧶🪁')
COLOR_MARKS = dict(zip(['🟥','🟦','🟨','🟩','🟫','🟪','🟧','⬛','⬜','🩷'], colors))

def keys_for(n, line, challenge, section):
    keys=[]
    if n==1:
        synonyms={'ball':['ball','quả bóng'],'jump_rope':['jump rope','dây nhảy'],'yo_yo':['yo-yo'], 'bicycle':['bicycle','xe đạp'],'train':['train','tàu hỏa'],'car':['car','ô tô'],'doll':['doll','búp bê'],'teddy_bear':['teddy bear','gấu bông']}
        keys=[k for k,terms in synonyms.items() if any(t in line.lower() for t in terms)]
    elif n==2:
        if '🖼' in line or '🚗' in line:
            keys=['red_train' if 'tàu' in line or 'red train' in line else 'blue_ball' if 'bóng' in line or 'blue ball' in line else 'brown_teddy_bear' if 'gấu' in line or 'brown teddy bear' in line else 'green_yo_yo' if 'yo-yo' in line else 'green_car']
        else:
            keys=['color_'+c for marker,c in COLOR_MARKS.items() if marker in line]
            keys += [k for marker,k in {'🍎':'apple','🐦':'bird','🐱':'cat','🐶':'dog'}.items() if marker in line]
    elif n==3:
        pairs={'🟦':'blue_square','💜':'purple_heart','🟧':'orange_triangle','🟡':'yellow_circle','🟩':'green_square','🩷':'pink_heart'}
        keys=[k for m,k in pairs.items() if m in line]
        if not keys:
            keys=[k for m,k in {'⭕':'circle','⬜':'square','🔺':'triangle','❤':'heart','⭐':'star','▭':'rectangle','◆':'diamond','⬭':'oval','🥚':'egg','🐟':'fish','🦍':'gorilla'}.items() if m in line]
    elif n==4:
        for m,k in {'●':'dots','◎':'rings','△':'triangles','☆':'stars','○':'circles','♡':'hearts','□':'squares','🚗':'cars','🧸':'teddy_bears'}.items():
            if m in line:
                count=line.count(m)
                if m=='🚗' and challenge==5 and section.startswith('4.'):count=7
                keys.append(f'{k}_{count:02d}')
        keys += [k for m,k in {'🛖':'igloo','🪢':'jump_rope','🦘':'kangaroo','🦁':'lion'}.items() if m in line]
    elif n==5:
        for m,k in {**animals,'🚗':'car'}.items():
            if m in line:
                count=line.count(m)
                if section.startswith('7.') and challenge==5:
                    if k in ['duck','cow','car']:count={'duck':3,'cow':8,'car':8}[k]
                keys.append(f'{k}_{count:02d}')
        keys += [k for m,k in {'🌙':'moon','🪺':'nest','🐙':'octopus','🍑':'peach'}.items() if m in line]
    elif n==6:
        keys=[k for m,k in {**food,'👸':'queen','🐇':'rabbit','☀':'sun','🐅':'tiger','🐦':'birds'}.items() if m in line]
        if challenge==5 and section.startswith('9.'):
            keys=['likes_milk' if k=='milk' else 'dislikes_fish' if k=='fish' else k for k in keys]
    elif n==7:
        keys=[k for m,k in {'👤':'head','🧍':'shoulders','🦵':'knees','🦶':'toes','👀':'eyes','👂':'ears','👄':'mouth','👃':'nose','🙌':'head','☂':'umbrella','🎻':'violin','⌚':'watch'}.items() if m in line]
        if (challenge==1 and section.startswith('3.')) or (challenge==5 and section.startswith('3.')):
            keys=['touch_'+k if k in ['head','eyes','nose'] else k for k in keys]
    else:
        keys=[k for m,k in abilities.items() if m in line]
        if '✗' in line:keys=['cannot_fly_kite' if k=='fly_kite' else k for k in keys]
        keys += [k for m,k in {'⚽':'play_ball','🏃':'play_tag','🪢':'jump_rope','🦊':'fox','🧶':'yarn','🦓':'zebra'}.items() if m in line]
    return list(dict.fromkeys(keys))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    decisions_path=ROOT/'audit/challenge-cue-decisions.json'
    decisions=json.loads(decisions_path.read_text(encoding='utf-8'))['decisions'] if decisions_path.exists() else []
    for n in [6,7,8]:
        if any(r['unit']==n for r in decisions):
            ISSUES[n]=[note for note in ISSUES[n] if not note.startswith(('C3§2:', 'C3§2 câu 3–5', 'C3§6 play ball/tag'))]
            ISSUES[n].append('Đã chốt 8 cue theo quyết định được người dùng giao; đọc audit/challenge-cue-decisions.json. Các câu đã gắn hình có expected_answer duy nhất trong mapping, không coi là context mở.')
    summary=[]
    all_records=[]
    for n,topic in enumerate(TOPICS,1):
        source=next(UNITS.glob(f'Unit {n} - *(*).md'))
        lesson=UNITS/f'Unit {n} - {topic} - Lesson Pages'
        lines=source.read_text(encoding='utf-8-sig').splitlines()
        sections=[]; records=[]; challenge=0; section=''; sub=''; current=None
        for i,line in enumerate(lines,1):
            if line.startswith('# Challenge'):
                challenge=int(re.search(r'Challenge (\d)',line)[1]);section='';sub='';current=None
            elif line.startswith('# ') and challenge:
                challenge=0;current=None
            if not challenge:continue
            if re.match(r'#{2,3} \d+\. ',line):
                section=re.sub(r'^#+ ','',line);sub=''
                current={'challenge':challenge,'section':section,'line':i,'visual_lines':[]}
                sections.append(current)
            elif re.match(r'### \d+\.\d+',line):sub=line[4:]
            if any(m in line for m in MARKERS):
                keys=keys_for(n,line,challenge,section)
                assert keys, (n,i,line)
                rec=dict(line=i,challenge=challenge,section=section,item=sub,source_text=line,
                         asset_ids=[REG[n][k]['id'] for k in keys])
                records.append(rec)
                if current:current['visual_lines'].append(i)
                for k in keys:REG[n][k]['uses'].append(i)
        def bind(key,line_number,why):
            REG[n][key]['uses'].append(line_number)
            records.append(dict(line=line_number,challenge=None,section='Context bổ sung / dùng chung',item='',
                source_text=lines[line_number-1],asset_ids=[REG[n][key]['id']],note=why))
        if n==1:
            for k,line_number in zip([k for k,d in toys],range(195,203)):bind(k,line_number,'C2§2 chọn đồ vật: cả 8 hình là lựa chọn dùng chung.')
        if n==3:
            for k,ln in zip(['blue_square','purple_heart','orange_triangle','yellow_circle','green_square','pink_heart'],range(359,365)):
                bind(k,ln,'Đề xuất context theo C5§3; nguồn chưa gắn hình tại đây.')
        if n==4:bind('cars_07',406,'C5§4 tình huống 2: câu mẫu 7 cars cần đúng nhóm 7 xe.')
        if n==5:
            for k,ln in [('duck_03',340),('cow_08',343),('car_08',346)]:bind(k,ln,'C3§5: nhóm đếm đã được xác định ở C5§3, dùng chung.')
        if n==7:
            bind('red_circle',524,'Vật thật/hình tròn để bé chạm: không cần thêm một tranh riêng mỗi câu.')
        for r in decisions:
            if r['unit']==n and n in [6,7]:bind(r['asset_id'][4:],r['question_line'],'Fixed cue selected by user-authorized decision; answer '+r['expected_answer'])
        if n==8:
            bind('make_circle',390,'Đã chốt cue và đáp án theo yêu cầu người dùng; giữ nguyên stem nguồn.')
            bind('make_line',391,'Đã chốt cue và đáp án theo yêu cầu người dùng; giữ nguyên stem nguồn.')
        for sec in sections:
            sec['status']='has_visual_mapping' if sec['visual_lines'] else 'text_audio_action_or_context_review'
        assets=list(REG[n].values())
        for a in assets:
            a['uses']=sorted(set(a['uses']))
            assert a['uses'], (n,a['id'])
            a['references']=[str(lesson/'pages/png'/f'{track}.png') for track in a['reference_tracks']]
            # Some safe, immutable cross-unit sources are reused; no task depends on another task's future output.
            if n==6 and a['id']=='u06_birds':
                a['references']=[str(UNITS/'Unit 5 - Animals - Lesson Pages/pages/png/CD2_07.png')]
            assert all(Path(p).is_file() for p in a['references']), a
            a['expected_files']=[f'webp/{a["id"]}.webp']
            a['export']={'format':'webp','size':[512,512],'quality':80,'method':6,'target_bytes':61440,'png_optional':True}
            a['existing_challenge_files']=[str(lesson/'challenge-assets'/p) for p in a['expected_files'] if (lesson/'challenge-assets'/p).is_file()]
            a['status']='existing_dedicated_asset' if len(a['existing_challenge_files'])==len(a['expected_files']) else 'conditional_context' if a['method']=='conditional' else 'missing_dedicated_asset_or_mapping'
        data=dict(schema_version=1,unit=n,topic=topic,source=str(source),lesson_folder=str(lesson),
                  scope='Challenge 1–5 only; lesson pages are immutable references',
                  sections=sections,visual_occurrences=records,assets=assets,context_issues=ISSUES[n])
        (OUT/f'unit-{n:02d}.inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        prompt=make_prompt(data)
        (OUT/f'unit-{n:02d}.md').write_text(prompt,encoding='utf-8')
        summary.append(dict(unit=n,topic=topic,required=len([a for a in assets if a['method']!='conditional']),
                            conditional=len([a for a in assets if a['method']=='conditional']),
                            visual_occurrences=len(records),sections=len(sections)))
        all_records.append(data)
    ids=[a['id'] for d in all_records for a in d['assets']]
    assert len(ids)==len(set(ids))
    for d in all_records:
        valid={a['id'] for a in d['assets']}
        assert all(set(r['asset_ids']) <= valid for r in d['visual_occurrences'])
    report=dict(date='2026-10-10',units=summary,required=sum(s['required'] for s in summary),
                conditional=sum(s['conditional'] for s in summary),
                checks={'unit_count':8,'unique_asset_ids':len(ids),'unmapped_visual_marker_lines':0,
                        'dangling_asset_ids':0,'all_reference_images_exist':True,'all_assets_have_source_evidence':True},
                limitations=['Counts describe planned dedicated assets, not images already generated.',
                  'Marker coverage is not proof that every exercise has unambiguous pedagogy; see context_issues.',
                  'Same visual is reused within a Unit. Cross-unit IDs may have the same noun, but distinct source artwork/context; reuse immutable lesson art where safe. Do not create another asset per exercise.'])
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows='\n'.join(f'| {s["unit"]} — {s["topic"]} | {s["required"]} | {s["conditional"]} | [Prompt](unit-{s["unit"]:02d}.md) |' for s in summary)
    readme=f'''# Prompt ảnh Challenge — Unit 1–8

Kiểm kê ngày 2026-10-10. **Bộ ảnh Challenge của 8 Unit đã có đầy đủ; các cue được chốt theo yêu cầu người dùng.** Xem trạng thái hiện tại ở audit/challenge-images-completion.md; không sinh lại ảnh đã đạt. Bộ trang học chính đã có: 133 trang Unit + 9 trang Review. Các prompt dưới đây chỉ bổ sung Challenge 1–5, không regenerate bộ trang học hoặc 4 Review.

**Format mới cho cả 12 prompt:** ưu tiên batch **8–12 hình** (8: 4×2, 9: 3×3, 12: 4×3; 10/11 để ô dư trắng). Sau khi xem và cắt từng ô, xuất **WebP 512×512**, quality 80/method 6, mục tiêu thường **15–60 KB/thẻ**. PNG từng thẻ không bắt buộc; giữ ảnh batch gốc để xuất lại. Tranh đếm/động tác cần chi tiết có thể xuất 640×640 hoặc tách batch ít ô hơn, ghi lý do. Không thêm ảnh dư để đủ batch; mapping/preview dùng WebP. Kiểm tra chất lượng sau nén, ghi bytes thực tế và ngoại lệ trên 60 KB.

| Unit | Asset bắt buộc trong kế hoạch | Asset có điều kiện | Prompt độc lập |
|---|---:|---:|---|
{rows}

Tổng **{report['required']} asset bắt buộc + {report['conditional']} asset có điều kiện**. Đây là số mã hình cần chuẩn bị/tách và nối bài tập, **không phải số hình bắt buộc sinh mới bằng AI**. Phần lớn hình có thể cắt từ tranh chuẩn, ghép nhóm đúng số lượng, hoặc dựng mảng màu/hình học bằng đồ họa xác định. Số lần image_gen thực tế chỉ biết sau khi xem từng crop.

Copy toàn bộ nội dung một file `unit-NN.md` vào một chat riêng. Mỗi chat chỉ ghi `Unit N - TOPIC - Lesson Pages/challenge-assets/`; không sửa các file Unit gốc, script dùng chung hoặc output Unit khác. Các file `unit-NN.inventory.json` là nguồn danh sách/mapping cùng line và câu nguồn; chỉ đọc. Các chat không phụ thuộc vào ảnh mới sinh của chat khác.

Chữ bài học vẫn giữ ở bộ trang học. Với Challenge nhìn hình đoán từ/đếm/nói không hint, chữ câu hỏi và lựa chọn đặt ngoài bitmap; ảnh không chứa nhãn đáp án. Các đoạn thoại, tên, chữ cái và số dùng để học được render riêng bằng font. Không biến bài text/audio/hành động thực tế thành một loạt tranh không cần thiết.

Đã kiểm tra: đủ 8 Unit; mỗi asset có dẫn chứng nguồn; toàn bộ dòng có ký hiệu hình trong Challenge được nối ít nhất một asset; không ID trùng, không tham chiếu asset mồ côi, tất cả ảnh tham khảo tồn tại. Dòng tiêu đề/câu mẫu cũng được ghi để truy vết, nên số `visual_occurrences` không phải số câu hỏi. Các câu chưa đủ context được liệt kê riêng trong từng prompt: chưa thể khẳng định mỗi câu có đáp án duy nhất.

Chống trùng: một ID dùng lại trong mọi Challenge của cùng Unit, H–heart của Unit 3 dùng luôn hình heart, nhóm đếm phân biệt bằng loại vật + số lượng, Unit 8 tách vật dây nhảy khỏi hành động nhảy dây. Cùng từ ở Unit khác không tự động là cùng tranh: cá Food khác cá sống phonics; xe đạp Toys khác hành động ride. Phonics và đối tượng chung ưu tiên lấy lại nguồn lesson hiện hữu thay vì sinh thêm bản mới. Không yêu cầu global shared assets mới để tránh phụ thuộc giữa các chat song song.

Unit8 make_circle/make_line đã được chốt dùng cho câu5 circle/câu6 line và trở thành bắt buộc; không cần tạo lại ảnh hiện có. Audio Challenge vẫn do chủ dự án bổ sung; công việc này không tạo audio. Báo cáo validation.json chỉ kiểm kê Unit; Review có báo cáo riêng bên dưới.

## Challenge của 4 Review — thêm 4 prompt độc lập

Cả 4 Review có 5 Challenge riêng và đã có đủ bộ challenge-assets; các prompt dưới đây dùng để kiểm tra/tiếp tục khi nguồn thay đổi. Copy một prompt vào một chat riêng; có thể chạy song song với 8 Unit vì mỗi chat chỉ ghi thư mục Review của mình. Không dùng các prompt Review cũ ở thư mục cha để làm việc này: chúng là prompt trang lesson.

| Review | Asset cần chuẩn bị | Prompt |
|---|---:|---|
| 1–2: Toys, Colors, School Supplies, Commands | 17 | [Review 1–2](review-1-2.md) |
| 3–4: Shapes, Counts, Classroom Commands | 27 | [Review 3–4](review-3-4.md) |
| 5–6: Animals, Food, Weather, Commands | 19 | [Review 5–6](review-5-6.md) |
| 7–8: Body Actions, Abilities, Days of the Week | 19 | [Review 7–8](review-7-8.md) |

Tổng Review: **82 asset**, nhiều hình có thể crop/ghép/native thay vì sinh mới. Inventory Review có bản ghi cho mọi question_id trong Challenge 1–5, cả câu không cần raster. Nhóm đếm dùng một ảnh cho mọi câu lặp; cặp ghép kiến thức dùng nhiều ID riêng thay vì sinh một tranh mới cho mỗi cặp. Thẻ ngày dùng graphic/font và chế độ giấu tên khi kiểm tra; phân biệt thứ tự thẻ Sunday1–Saturday7 với lịch tháng. Xem [reviews-validation.json](reviews-validation.json). Dựng lại bằng `python audit/build_review_challenge_prompts.py`.

Để dựng lại danh sách từ các bản Markdown hiện tại: `python audit/build_challenge_prompt_inventory.py`. Xem [validation.json](validation.json) để biết kết quả kiểm tra danh sách; đây không phải chứng nhận chất lượng ảnh chưa tạo.
'''
    (OUT/'README.md').write_text(readme,encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

def make_prompt(d):
    n=d['unit'];topic=d['topic'];dest=Path(d['lesson_folder'])/'challenge-assets'
    inventory=OUT/f'unit-{n:02d}.inventory.json'
    required=sum(a['method']!='conditional' for a in d['assets'])
    rows=[]
    for a in d['assets']:
        evidence=', '.join(str(i) for i in a['uses'])
        refs=', '.join(a['reference_tracks'])
        rows.append(f'| `{a["id"]}` | {a["brief"]} | {a["method"]} | {refs} | {evidence} |')
    issues='\n'.join('- '+s for s in d['context_issues']) or '- Không thấy câu visual cần thêm loại hình ngoài danh sách. Vẫn đọc lại câu nguồn trước khi nối.'
    return f'''# Prompt độc lập — Unit {n}: {topic} — ảnh Challenge

Hãy hoàn thiện bộ ảnh riêng cho **Challenge 1–5 của Unit {n} — {topic}** trong repo `E:\\let-go-series`. Làm đến khi có ảnh thật và mapping kiểm tra được, không chỉ đưa kế hoạch. Chỉ làm Unit này; các chat Unit khác chạy song song.

## Nguồn phải đọc

- Bài luyện chuẩn: `{d['source']}`. Đọc đầy đủ Challenge 1–5; các số dòng bên dưới chỉ giúp tìm, có thể đổi sau khi source được sửa.
- Inventory chỉ đọc: `{inventory}`. Dùng `assets` và `visual_occurrences` để nối ID→mọi chỗ dùng. Kiểm tra lại nội dung nguồn nếu đã có thay đổi, cập nhật manifest trong thư mục output của mình, không sửa inventory chung.
- Ảnh/phong cách chuẩn: `{d['lesson_folder']}\\pages\\png`, manifest và PDF Unit cùng thư mục Units. Các đường dẫn tuyệt đối của ảnh tham khảo có sẵn trong inventory.
- Mẫu phong cách chung chỉ đọc: `E:\\let-go-series\\Let_s Go Begin\\Units\\Unit 1 - Toys - Lesson Pages\\pages\\png\\CD1_07.png` và `E:\\let-go-series\\Let_s Go Begin\\Units\\Unit 2 - Colors - Lesson Pages\\pages\\png\\CD1_34.png`.

## Phạm vi ghi riêng và chạy song song

Chỉ tạo/sửa trong `{dest}`. Tạo `png/`, `webp/`, `batches/`, `references/` nếu cần, `manifest.json`, `question-image-map.json`, `preview.html`, `contact-sheet.jpg`, `validation.json`, `README.md`. Không sửa Markdown Unit gốc, trang lesson, audio, ZIP lesson, root helpers, file prompt/inventory chung, Unit khác. Không commit/push. Không cần chờ chat khác; tất cả nguồn tham khảo hiện đã có. Nếu phát hiện bài nguồn thiếu cue, ghi trong README và mapping chứ không tự ghi đè source.

Trước khi làm, đọc manifest/output đã có để tiếp tục đúng trạng thái; không tạo lại asset đã đạt yêu cầu. Mỗi ID một WebP nhẹ, PNG thẻ riêng là tùy chọn; giữ ảnh batch gốc để xuất lại. Mọi câu trùng dùng cùng ID. Không sinh một bản mới cho mỗi Challenge. Không xóa ảnh nguồn. Chỉ dọn bản output bỏ trong phạm vi mình sau khi xác nhận không còn được tham chiếu.

## Format và chữ

Giữ textbook cartoon như ảnh mẫu: màu sáng, nét viền đậm gọn, soft shading, nhân vật trẻ em cùng thiết kế, thân thiện; không đổi sang ảnh thật, 3D hoặc icon emoji. Nền trắng/sáng, chủ thể rõ, không trang trí gây nhầm, khoảng trống an toàn. Xuất thẻ **WebP 512×512** mặc định, contain giữ tỷ lệ, không kéo méo/cắt vật. Nếu nhóm đếm/động tác mất chi tiết, được dùng 640×640 và ghi lý do riêng trong manifest. Đây là thẻ hình đơn nhỏ cho câu luyện, không phải trang lesson 1200×1200. Không phóng crop nguồn nhỏ để giả chi tiết.

WebP lightweight: bắt đầu quality=80, method=6, bỏ metadata không cần thiết; mục tiêu thường 15–60 KB/thẻ. Nếu quá 60 KB, thử quality 75 rồi 70, xem lại ở kích thước hiển thị thật; không giảm chất lượng đến mức khó nhận vật/màu/ngón tay/số lượng. Nếu vẫn lớn, giữ bản rõ và ghi ngoại lệ cùng bytes thực tế, không tuyên bố đã đạt ngân sách. PNG thẻ không bắt buộc; giữ batch/crop master trong batches/references để có thể xuất lại. Preview/mapping chỉ dùng WebP.

Giữ chữ bài học ở bộ lesson. Trong ảnh Challenge để đoán từ/đếm/nói không hint: **không nhãn từ vựng, không câu trả lời, không tên file/ID, không lựa chọn, không speech bubble trả lời sẵn**. Câu hỏi/câu thoại cần hiện và lựa chọn giữ nguyên văn, đặt ngoài bitmap trong preview/mapping. Chữ cái, số, chỗ trống render bằng font ở UI để chính xác; không tạo ảnh AI chỉ để viết chữ. Dấu ✓/✗ của bài khả năng có thể thay bằng cảnh làm được/không làm được rõ, không dùng một vật tĩnh cho cả hai trạng thái.

## Danh sách duy nhất cần xử lý

**{required} ID bắt buộc**{'; có asset conditional được liệt kê riêng' if any(a['method']=='conditional' for a in d['assets']) else ''}. `native_graphic`: đồ họa xác định hợp lệ cho mảng màu/hình học, không placeholder. `compose_from_crops`: ghép từ một hình thật chuẩn thành nhóm đúng số. `crop_or_edit`: ưu tiên cắt nguồn khi không mất nội dung/không còn nhãn; nếu không đủ thì sửa hoặc sinh bằng built-in image_gen. `edit_or_generate`: chỉ dùng lại crop nếu thật sự có đúng cảnh/động tác; cần sửa/sinh nếu thiếu. `conditional`: đọc ghi chú trước khi làm.

| ID / tên file | Nội dung cần thấy | Cách ưu tiên | Track tham khảo | Dòng nguồn dùng chung |
|---|---|---|---|---|
{chr(10).join(rows)}

## Context và chỗ cần chú ý

{issues}

Các bài nghe→chọn chữ, ghép từ/câu, điền ngữ pháp, hỏi tuổi/tên/sở thích/khả năng của chính bé và nghe→bé thực hiện động tác không mặc định cần thêm raster. Ghi `image_required=false` với lý do cho các mục đó. Không tạo thêm cảnh chỉ vì một từ xuất hiện trong đáp án nhiễu. Các câu thiếu cue mà chưa xác định được phải có `needs_context=true`, không báo mapping toàn bộ câu đã hoàn chỉnh.

## Cách tạo, gom 8–12 hình nhỏ/lần

1. Đọc và xem trực quan ảnh tham khảo đúng track trong inventory. Chọn crop sạch nếu giữ nguyên chủ thể; ghi file nguồn và box pixel. Không dùng cả trang có nhãn làm hình đoán đáp án. Không coi tham khảo đã đúng chỉ vì file tồn tại.
2. Khi cần sinh/sửa minh họa, đọc skill imagegen và dùng **built-in image_gen**. Không chuyển sang CLI/API ngoài hoặc tự vẽ thay minh họa nhân vật/đồ vật. Đồ họa mảng màu/hình học và ghép crop nhóm đếm có thể dùng Pillow/SVG rồi raster theo yêu cầu trên. Nếu built-in không dùng được, báo đúng ID còn thiếu.
3. Ưu tiên batch 8–12 ID: 8 hình = 4 cột × 2 hàng; 9 = 3×3; 12 = 4×3. Với 10/11 dùng lưới 4×3, các ô dư để trắng; không sinh hình dư. Đánh số hàng/cột trong prompt/log theo thứ tự đọc, không in số/ID lên ảnh. Mỗi ô vuông, gutter trắng thẳng, cùng style, không lẫn nội dung. Dùng kích thước batch lớn nhất phù hợp tool, ưu tiên 2048×2048 nếu được hỗ trợ; kiểm độ phân giải thực của từng ô sau cắt. Lưới 4×3 ô vuông không kéo giãn để lấp canvas vuông: giữ khoảng trắng ngoài lưới. Không ép batch đủ 8 nếu chỉ còn ít ID hoặc nhiều ID đã crop sạch. Nếu nhóm đếm/anatomy quá nhỏ hoặc lẫn ô, tách riêng nhóm lỗi thành batch ít ô hơn. Không giả định mỗi ô gốc đủ 512px; xuất nhỏ không bổ sung chi tiết bị mất.
4. Khung prompt: “Create [N] independent square educational illustration cards, arranged in [columns] columns and [rows] rows with straight white gutters and safe outer margins, matching the supplied Let’s Go Begin references: bright textbook cartoon, clean bold outlines, soft shading. Keep all cells square, use blank margins rather than stretching, and leave unused cells empty. Each panel contains only its specified subject/action/count, no labels, words, numbers, answer hints, watermarks or panel IDs. Row 1, column 1: [full brief]. Row 1, column 2: [full brief]. Continue with one explicit row/column brief for EVERY requested ID. Keep subjects fully visible; no cross-panel objects.” Trước khi gọi tool, thay hết placeholder và liệt kê đủ 8–12 ô đúng vị trí. Nhóm đếm nhắc lại số lượng, không thêm vật cùng loại ở nền.
5. Log batch gồm IDs, prompt chính xác, tool, refs, rows/columns, occupied_cells, kết quả, crop_boxes thực tế và trạng thái xem. Giữ ảnh batch gốc. Xem từng ô, sửa lỗi bằng built-in, cắt theo gutter thực tế (không chia pixel mù), bỏ ô trắng, contain về 512×512 rồi xuất `webp/ID.webp` theo thông số nén trên. PNG thẻ tùy chọn, không phải cổng hoàn tất.
6. Manifest mỗi asset ghi semantic (loại, màu, lượng, hành động, trạng thái), WebP, cách tạo, refs/crop box, provenance/batch, kích thước, quality, method, file_bytes và visual_review thật. Mapping theo Challenge/section/item và câu nguồn; số dòng chỉ là locator phụ. Một câu có thể nhiều ID (lựa chọn hình), giữ đủ lựa chọn, không chỉ hình đáp án đúng.
7. Preview phải cho xem tất cả ảnh ở kích thước thẻ và thử các câu tiêu biểu: câu hỏi/blank và text choices nằm ngoài ảnh; answer key giáo viên tách riêng, không hiển thị sẵn. Cùng ID có thể dùng nhiều câu. Ghi các câu thiếu cue như trong phần Context; không âm thầm đoán hoặc đổi bài.

## Kiểm tra trước khi báo xong

- Đủ toàn bộ ID bắt buộc, không ID trùng/ngoài danh sách; conditional báo riêng. Mọi occurrence trong inventory được nối hoặc có lý do rõ nếu nguồn đã đổi. Mọi section Challenge 1–5 có mapping ảnh hoặc `image_required=false` / `needs_context=true` trung thực.
- Xem **mọi WebP sau cắt và nén**, không chỉ batch/contact sheet. Đối chiếu vật/màu/động tác/lượng ở 512px và kích thước thẻ UI; đếm thực tế từng vật, anatomy đúng, smile khác wink, bounce khác cầm bóng, tag khác chạy, can khác can’t. Nếu nén mất chi tiết phải xuất lại.
- Không còn chữ/đáp án gợi ý, không mất vật; WebP 512×512 mặc định (640×640 có lý do), quality/bytes được ghi, mọi link mapping/preview tồn tại. Báo số thẻ vượt 60 KB và lý do; không buộc PNG riêng cho từng thẻ.
- Kiểm tra duplicate hash: cùng nội dung trong Unit phải dùng cùng ID; nếu hai ID khác semantic nhưng pixel giống nhau là lỗi cần sửa. Không dùng ảnh tĩnh của đồ vật thay động tác.
- validation ghi required/complete/missing/conditional, occurrence coverage, unresolved context, dimensions, links và visual review. Check kỹ thuật không thay thế kiểm tra nội dung. Không khẳng định Challenge sẵn sàng tích hợp nếu còn `needs_context` chưa xử lý.

Cuối cùng báo số ID xong/thiếu, số sinh mới/crop/ghép/native, preview và mapping, cùng các context còn mở. Không tạo audio: chủ dự án sẽ tự bổ sung.
'''

if __name__ == '__main__':
    main()
