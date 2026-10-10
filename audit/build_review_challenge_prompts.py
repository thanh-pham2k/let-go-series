"""Inventory all Review Challenge question IDs and create independent briefs."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
UNITS=ROOT/'Let_s Go Begin/Units'
OUT=ROOT/'parallel-prompts/challenge-images'

DEFS={
'1-2':[
 ('car','Ô tô đồ chơi ở 1a'),('train','Đoàn tàu đồ chơi ở 1b'),('bicycle','Xe đạp ở 2a'),('ball','Bóng ở 2b'),
 ('green','Mảng xanh lá 3a'),('red','Mảng đỏ 3b'),('purple','Mảng tím 4a'),('yellow','Mảng vàng 4b'),
 ('paper','Một tờ giấy, hình 1 School Supplies'),('scissors','Kéo học sinh, hình 2'),
 ('glue','Lọ keo có đầu nhọn, hình 3, không chai mỹ phẩm'),('paint','Lọ màu vẽ và cọ, hình 4'),
 ('tape','Hộp/cuộn băng keo đúng hình 5, không giấy vệ sinh'),
 ('stand_up','Bé đứng dậy, 5a'),('sit_down','Bé ngồi xuống ghế, 5b'),
 ('come_here','Bé đi về phía cô giáo/người đang gọi, 6a; có người gọi để thấy hướng'),
 ('turn_around','Bé quay người, 6b; vệt xoay nhẹ rõ')],
'3-4':[(k,f'Một hình {k} chính xác theo Review; không số/nhãn') for k in ['circle','square','star','heart','triangle','diamond','oval']]+[
 ('walk','Bé đi bộ, 5a; khác chạy'),('run','Bé chạy, 5b; khác đi bộ'),
 ('go','Đèn xanh cho phép đi, 6a; không chữ GO'),('stop','Đèn đỏ yêu cầu dừng, 6b; không chữ STOP'),
 ('take_out_pencil','Bé lấy bút chì ra khỏi hộp, hình 1 Classroom Commands; hướng tay/vật rõ'),
 ('put_away_pencil','Bé cất bút chì vào hộp, hình 2; khác lấy ra'),
 ('open_book','Bé đang mở sách, hình 3; chuyển động mở rõ'),
 ('close_book','Bé đang đóng sách, hình 4; khác mở')]+
 [(f'triangles_{i:02d}',f'Đúng {i} tam giác △ tách rõ, không số/nhãn; biến thể luyện đếm') for i in range(2,8)]+
 [(f'diamonds_{i:02d}',f'Đúng {i} hình thoi ◆, không đá quý, không số/nhãn') for i in range(4,8)]+
 [('circles_05','Đúng 5 hình tròn, nhóm nguồn 3b'),('ovals_07','Đúng 7 oval, nhóm nguồn 4b')],
'5-6':[
 ('cat_01','Đúng 1 mèo; biến thể luyện số ít, không gán vào nhóm nguồn'),
 ('cat_03','Đúng 3 mèo, nhóm 1a'),('cat_04','Đúng 4 mèo, nhóm 1b'),
 ('rabbit_01','Đúng 1 thỏ; biến thể luyện số ít'),('rabbit_02','Đúng 2 thỏ, nhóm 2a'),('rabbit_05','Đúng 5 thỏ, nhóm 2b'),
 ('ice_cream','Kem 3a'),('cake','Bánh 3b'),('bread','Lát bánh mì 4a'),('rice','Bát cơm 4b'),
 ('skip','Bé nhảy chân sáo 5a, chân luân phiên; khác jump'),('jump','Bé nhảy bằng hai chân 5b; khác skip'),
 ('make_line','Các bé xếp một hàng thẳng, 6a'),('make_circle','Các bé xếp vòng tròn khép kín, 6b'),
 ('sunny','Cảnh có nắng, hình 1 Weather'),('cloudy','Cảnh nhiều mây, hình 2'),
 ('windy','Cảnh có gió làm lá/khăn bay, hình 3; không chỉ một đám mây'),
 ('rainy','Cảnh mưa với hạt mưa rõ, hình 4'),('snowy','Cảnh tuyết với bông tuyết/tuyết phủ rõ, hình 5')],
'7-8':[
 ('wink','Bé nháy một mắt, mắt kia mở, 1a'),('touch_knees','Bé đặt hai tay lên đầu gối, 1b'),
 ('touch_toes','Bé cúi chạm được tới ngón chân giày, 2a; tay tiếp xúc rõ'),
 ('cannot_touch_toes','Cùng bé cúi nhưng tay chưa chạm được giày, 2b; khoảng hở rõ, không dấu X'),
 ('ride_bicycle','Bé thực sự đạp xe, 3a'),('fly_kite','Bé thả diều bay, dây nối tay và diều, 3b'),
 ('swim','Bé bơi trong nước, 4a'),('dance','Bé đang nhảy múa, 4b'),
 ('stamp_feet','Bé giậm chân, 5a; chuyển động chân rõ'),('clap_hands','Bé vỗ tay, 5b; hai bàn tay đúng'),
 ('point_board','Bé chỉ vào bảng, 6a; không đi tới bảng'),('stand_up','Bé đứng lên, 6b')]+
 [(f'day_{i:02d}_{day.lower()}',f'Thẻ thứ tự nguồn {i} — {day}. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.')
  for i,day in enumerate(['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],1)]
}

def match(pair,text):
    keys=[]
    def hit(key,*terms):
        if any(t in text for t in terms):keys.append(key)
    if pair=='1-2':
        for key,terms in {
          'car':['ô tô','cặp 1a'],'train':['đoàn tàu','cặp 1b'],'bicycle':['xe đạp','cặp 2a'],
          'ball':['quả bóng','cặp 2b'],'green':['xanh lá','ô màu3a'],'red':['ô màu đỏ'],
          'purple':['ô màu tím'],'yellow':['ô màu vàng','ô màu4b'],
          'paper':['tờ giấy'],'scissors':['chiếc kéo'],'glue':['lọ keo','hình 3 School Supplies'],
          'paint':['lọ màu vẽ'],'tape':['băng keo'],
          'stand_up':['đứng dậy','đứng lên','cặp 5a'],'sit_down':['ngồi xuống','cặp 5b'],
          'come_here':['phía cô giáo','phía người gọi'],'turn_around':['quay người','hình 6b']}.items():hit(key,*terms)
    elif pair=='3-4':
        if '△' in text: keys.append('triangle' if text.count('△')==1 else f'triangles_{text.count("△"):02d}')
        elif '◆' in text: keys.append(f'diamonds_{text.count("◆"):02d}')
        elif 'gọi hình và chọn số lượng' in text or 'nhóm nguồn' in text:
            for marker,key in {'3a':'triangles_04','3b':'circles_05','4a':'diamonds_06','4b':'ovals_07',
                               '4 hình triangle':'triangles_04','5 hình circle':'circles_05','6 hình diamond':'diamonds_06','7 hình oval':'ovals_07'}.items():hit(key,marker)
        else:
            for key,terms in {'circle':['hình tròn'],'square':['hình vuông'],'star':['ngôi sao'],'heart':['trái tim'],
              'triangle':['tam giác'],'diamond':['hình thoi'],'oval':['bầu dục'],
              'walk':['đi bộ'],'run':['bé chạy'],'go':['đèn xanh'],'stop':['đèn đỏ'],
              'take_out_pencil':['lấy bút chì'],'put_away_pencil':['cất bút chì'],'open_book':['mở sách'],'close_book':['đóng sách']}.items():hit(key,*terms)
    elif pair=='5-6':
        for species,word in [('cat','mèo'),('rabbit','thỏ')]:
            if word not in text:continue
            found=re.search(r'(\d+)\s*con '+word,text)
            if found:keys.append(f'{species}_{int(found[1]):02d}')
            elif 'một con' in text:keys.append(f'{species}_01')
            elif 'nhóm '+word in text:keys.extend(['cat_03','cat_04'] if species=='cat' else ['rabbit_02','rabbit_05'])
        if 'nhóm mèo ở1b' in text:keys=['cat_04','rabbit_05']
        for key,terms in {'ice_cream':['kem'],'cake':['bánh ở'],'bread':['bánh mì'],'rice':['bát cơm'],
          'skip':['chân sáo'],'jump':['hai chân'],'make_line':['thành hàng'],'make_circle':['vòng tròn'],
          'sunny':['có nắng'],'cloudy':['nhiều mây'],'windy':['gió','có gió'],'rainy':['cảnh mưa'],'snowy':['có tuyết']}.items():hit(key,*terms)
    else:
        if 'So sánh cặp 2a/2b' in text or 'Cặp2:' in text:keys.extend(['touch_toes','cannot_touch_toes'])
        for key,terms in {'wink':['nháy một mắt'],'touch_knees':['đầu gối'],'touch_toes':['chạm được tới','chạm ngón chân'],
          'ride_bicycle':['đi xe đạp','hình 3a'],'fly_kite':['thả diều'],'swim':['bé bơi','hình 4a'],
          'dance':['nhảy múa'],'stamp_feet':['giậm chân'],'clap_hands':['vỗ tay','hình 5b'],
          'point_board':['chỉ vào bảng'],'stand_up':['đứng lên']}.items():hit(key,*terms)
        for idx in re.findall(r'thẻ ngày (?:số)?\s*(\d)',text):
            keys.append(next(k for k,d in DEFS[pair] if k.startswith(f'day_{int(idx):02d}_')))
        if 'thẻ ngày thứ Hai' in text or 'thẻ Monday' in text:keys.append('day_02_monday')
    return list(dict.fromkeys(keys))

def main():
    OUT.mkdir(parents=True,exist_ok=True);summary=[]
    for pair,definitions in DEFS.items():
        source=next(UNITS.glob(f'Review {pair}(*).md'));folder=UNITS/f'Review {pair} - Lesson Pages'
        whole=source.read_text(encoding='utf-8-sig');text=whole.split('# Đáp án dành')[0]
        lesson=json.loads((folder/'manifest.json').read_text(encoding='utf-8-sig'))
        refs=[str(folder/i['output']['png']) for i in lesson['items']]
        assert all(Path(r).is_file() for r in refs)
        assets={k:dict(id='r'+pair.replace('-','')+'_'+k,brief=d,uses=[],references=refs,
                      method='native_graphic' if (k in ['green','red','purple','yellow','circle','square','star','heart','triangle','diamond','oval'] or k.startswith(('day_','triangles_','diamonds_','circles_','ovals_'))) else 'crop_or_edit',
                      export={'format':'webp','size':[512,512],'quality':80,'method':6,'target_bytes':61440,'png_optional':True},
                      files=[f'webp/r{pair.replace("-","")}_{k}.webp']) for k,d in definitions}
        questions=[]
        blocks=list(re.finditer(r'^### (R\d+-C(\d)-(\d+))\s*$',text,re.M))
        for j,b in enumerate(blocks):
            block=text[b.end():blocks[j+1].start() if j+1<len(blocks) else len(text)]
            first=next(s.strip() for s in block.splitlines() if s.strip())
            keys=match(pair,first)
            # Text/listening grammar items do not acquire images because their distractors name objects.
            visual=any(t in first for t in ['🖼','Nhìn','nhìn','chỉ/diễn','Đếm','△','◆','Nhóm','Che nhãn','So sánh','Cặp2:']) or ('Nghe tên ngày:' in first)
            if not visual:keys=[]
            if pair=='7-8' and 'Nghe tên ngày:' in first:
                keys=[k for k,d in definitions if k.startswith('day_')]
            if visual:assert keys,(pair,b[1],first)
            assert set(keys)<=assets.keys(),(pair,b[1],keys)
            for k in keys:assets[k]['uses'].append(b[1])
            questions.append(dict(question_id=b[1],challenge=int(b[2]),line=text[:b.start()].count('\n')+1,
              source_prompt=first,image_required=visual,asset_ids=[assets[k]['id'] for k in keys],
              mode='choose_one_variant' if pair=='5-6' and ('hoặc1b' in first or 'hoặc2b' in first) else 'all_required' if visual else 'text_audio_or_live_roleplay'))
        assert all(a['uses'] for a in assets.values()),[(k,a['uses']) for k,a in assets.items() if not a['uses']]
        assert len(questions)==len({q['question_id'] for q in questions})
        assert {q['challenge'] for q in questions}==set(range(1,6))
        data=dict(review=pair,source=str(source),lesson_folder=str(folder),assets=list(assets.values()),questions=questions,
          source_notes=whole.split('### Ghi chú đối chiếu')[1].split('---')[0].strip(),
          status='missing_dedicated_challenge_assets_and_mapping' if not (folder/'challenge-assets').exists() else 'recheck_existing_outputs')
        inventory=OUT/f'review-{pair}.inventory.json'
        inventory.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        rows='\n'.join(f'| `{a["id"]}` | {a["brief"]} | {a["method"]} | '+', '.join(a['uses'])+' |' for a in assets.values())
        days='''
Đặc biệt Days of the Week: ảnh học có thể có chữ Sunday…Saturday bằng font. Ở bài đoán từ/không hint, không đưa nguyên thẻ chứa tên ngày vào câu hỏi. Dùng cùng thiết kế 7 thẻ nhưng giấu tên, giữ số thứ tự THẺ 1–7; hoặc dải tuần 7 ô đánh dấu vị trí tương ứng, Sunday ở ô đầu theo nguồn. Preview có chế độ learning bật tên và assessment giấu tên; không cần sinh hai bitmap khác nhau chỉ vì có/không chữ. Đây là adaptation cho bài luyện và phải ghi rõ. Không đánh đồng Sunday1/Monday2 với lịch tháng có ngày1 ở cộtMonday. Nghe→chọn số THẺ có thể render các số bằng font, không ép phải hiển thị cả 7 ảnh. Cặp2 phải giữ cả chạm được/chưa chạm được, cùng bé/giày/khung cảnh; hiển thị nhãn 2a/2b bằng UI bên ngoài bitmap để khớp lựa chọn của câu so sánh, không ghi nhãn đúng/sai. Không tự thêm lời hát CD2_72.
''' if pair=='7-8' else ''
        prompt=f'''# Prompt độc lập — Review {pair} — ảnh Challenge 1–5

Hoàn thiện RIÊNG bộ ảnh Challenge của Review {pair} trong repo `E:\\let-go-series`. Các Review/Unit khác chạy song song. Làm ảnh thật, mapping và preview đến khi kiểm tra được; không chỉ lập kế hoạch, không regenerate bộ trang học chính đã có.

Nguồn bài luyện: `{source}`. Đọc cả 5 Challenge và đáp án dành cho người lớn để hiểu ngữ cảnh; không đưa đáp án vào tranh. Inventory chỉ đọc: `{inventory}`, gồm mọi question_id, câu nguồn, dòng và asset cần dùng. Tham khảo trực quan PDF `{UNITS / ('Review '+pair+'.pdf')}`, manifest và các PNG sau:

{chr(10).join('- `'+r+'`' for r in refs)}

Phạm vi ghi duy nhất: `{folder/'challenge-assets'}`. Tạo `png/`, `webp/`, `batches/`, `manifest.json`, `question-image-map.json`, `preview.html`, `contact-sheet.jpg`, `validation.json`, `README.md`. Không sửa Markdown nguồn, lesson pages/metadata, audio, ZIP, script chung, prompt/inventory chung hoặc thư mục Review/Unit khác. Không commit/push. Không cần output mới của chat khác; dùng nguồn lesson hiện đã tồn tại. Đọc output hiện tại trước khi làm để tiếp tục, không tạo lại ảnh đã đạt.

## Danh sách duy nhất — {len(assets)} asset

| ID/tên file | Nội dung phải thấy | Cách ưu tiên | Câu dùng chung |
|---|---|---|---|
{rows}

Một ID một WebP nhẹ; PNG thẻ riêng tùy chọn, giữ batch/crop master để xuất lại. Mọi câu lặp dùng cùng ảnh. Nhóm đếm khác loại/số là ID khác; hình 1 tam giác dùng `triangle`, không thêm triangles_01. Câu nhiều ID giữ đủ hình so sánh/ghép, không chỉ ảnh đáp án. Với nhóm mèo/thỏ ghi “hoặc”: chọn một biến thể đúng câu, không cộng dồn hai nhóm. Câu text/audio/live roleplay không cần raster giữ `image_required=false`; không tạo cảnh từ đáp án nhiễu.

## Nội dung riêng của Review

{data['source_notes']}
{days}
Cặp từ ở bài ghép hai nhóm là hai hình riêng, không tự biến thành một đối tượng có cả hai đặc điểm (ví dụ car/green không có nghĩa phải tô ô tô xanh). Các biến thể luyện đếm/số ít được ghi là adaptation, không tuyên bố đã có trong PDF. Giữ lệnh/câu mẫu đúng nội dung nguồn. Audio Challenge do chủ dự án bổ sung: không tạo audio, không đoán đáp án MP3 Listen and circle từ tranh.

## Format, phong cách và chữ

Giữ style theo ảnh Review chuẩn và Unit hiện có: textbook cartoon màu sáng, nét viền rõ, soft shading, nhân vật trẻ em cùng thiết kế; nền trắng/sáng, chủ thể đủ lớn, không trang trí gây nhầm. Xuất **WebP 512×512** mặc định, contain không méo/cắt mất vật; được dùng 640×640 nếu nhóm đếm/động tác cần chi tiết và ghi lý do. Mỗi file là thẻ nhỏ đúng ID, không trang lesson 1200×1200 hoặc emoji. Không upscale để giả chi tiết.

WebP lightweight: bắt đầu quality=80, method=6, bỏ metadata thừa; mục tiêu thường 15–60 KB/thẻ. Nếu quá 60 KB thử quality 75 rồi 70 và xem lại sau nén ở kích thước dùng thật. Ưu tiên nhận diện/đếm/anatomy đúng; nếu vẫn lớn giữ bản rõ và ghi ngoại lệ cùng bytes thực tế. PNG thẻ tùy chọn; giữ batch gốc/crop master, preview và mapping dùng WebP.

Ảnh cho đoán từ/đếm/không hint không có nhãn đáp án, speech bubble trả lời, chữ ID, watermark, số lượng in sẵn hay lựa chọn. Câu hỏi, chữ cái lựa chọn, từ/thẻ câu/chỗ trống render bằng font ngoài bitmap. Giữ đủ chữ nguồn trong lesson; không xóa chữ khỏi bộ trang học. Những nội dung học bằng chữ như ngày trong tuần dùng font/UI với chế độ giấu tên khi kiểm tra, không nhờ image_gen viết chữ.

## Quy trình, gom 8–12 hình nhỏ/lần

1. Xem trực quan các PNG nguồn và đối chiếu PDF/mô tả. Ưu tiên crop sạch đúng hình, bỏ nhãn a/b, số câu và text mà không cắt mất chủ thể. Ghi source file và box pixel. Với nhóm đếm giữ đúng lượng; bản đơn có thể cắt một con từ nhóm và ghi adaptation. Không lấy nguyên trang làm ảnh câu hỏi.
2. Nếu crop không đủ, đọc skill imagegen và dùng **built-in image_gen** để sửa/sinh minh họa. Không CLI/API ngoài. Mảng màu/hình học/thẻ ngày được dựng xác định bằng graphic/font; nhóm có thể ghép crop thật theo đúng số lượng. Không thay cảnh người/đồ vật bằng placeholder/SVG để báo đã regenerate.
3. Ưu tiên batch 8–12 ID: 8 = 4 cột × 2 hàng; 9 = 3×3; 12 = 4×3; 10/11 dùng 4×3 và để ô dư trắng. Mỗi ô vuông, gutter trắng thẳng, cùng style, không chữ/ID và không lẫn vật. Batch dùng độ phân giải lớn nhất phù hợp tool, ưu tiên 2048×2048 nếu hỗ trợ; lưới 4×3 trên canvas vuông giữ khoảng trắng ngoài, không kéo méo ô. Kiểm kích thước crop thực tế, không giả định đủ 512px/ô. Chỉ gom ID cần sinh/sửa, không sinh lại crop sạch để đủ nhóm, nhóm cuối được ít hơn 8. Nếu đếm/anatomy mất chi tiết, tách riêng nhóm lỗi thành batch ít ô hơn.
4. Khung prompt: “Create [N] independent square educational cards in [columns] columns and [rows] rows, separated by straight white gutters with safe outer margins, matching the supplied Let’s Go Begin Review references: bright textbook cartoon, bold clean outlines, soft shading, consistent children and objects. Keep cells square and leave unused cells empty. Each panel shows exactly its specified subject/action/count, fully visible. No labels, answer text, numbers, IDs, speech bubbles or watermarks. Row 1, column 1: [full brief]. Row 1, column 2: [full brief]. Continue with one explicit row/column brief for EVERY requested ID. No objects cross panels; no extra countable objects.” Thay hết placeholder và liệt kê đủ các ô trước khi gọi tool. Nhóm đếm nhắc số chính xác; động tác thấy rõ chuyển động/hướng.
5. Log batch gồm IDs, prompt, refs, tool, rows/columns, occupied_cells, crop_boxes thực tế, kết quả/review; giữ ảnh batch gốc. Xem từng ô, sửa bằng built-in, cắt theo gutter thực tế (không chia mù), bỏ ô trắng, contain về 512×512 và xuất `webp/ID.webp` theo thông số nén trên; PNG thẻ tùy chọn.
6. Manifest ghi semantic loại/màu/lượng/hành động/trạng thái, WebP, nguồn/crop hoặc provenance/batch, kích thước, quality, method, file_bytes, visual_review thật. Mapping theo question_id/câu nguồn; cho phép nhiều ID/alternate variants. Mọi câu trong 5 Challenge có bản ghi, kể cả câu không cần ảnh; số dòng chỉ là locator.
7. Preview có toàn bộ thẻ và các câu tiêu biểu, text/câu hỏi đặt ngoài ảnh; answer key/script audio giáo viên giấu trước khi trả lời. Tình huống người lớn diễn/đưa giấy và bài nghe→bé thực hiện dùng lại asset đã có nếu cần minh họa; không tự sinh thêm cảnh không bắt buộc. Nếu nguồn có thêm/mất câu so với inventory, ghi rõ và cập nhật mapping output, không ghi đè nguồn.

## Cổng kiểm tra

- Đủ {len(assets)} ID bắt buộc, không ID trùng/thừa; tất cả question_id source có mapping hoặc lý do không cần ảnh. Kiểm source hiện tại, không chỉ số đếm trong inventory.
- Xem mọi WebP sau cắt và nén ở 512px và kích thước thẻ UI; đối chiếu type/color/count/action, đếm từng vật thật, anatomy tự nhiên. Phân biệt take out/put away, open/close, go/stop, skip/jump, line/circle, weather, touch knees/toes và chạm được/chưa chạm được khi có trong Review này.
- Không nhãn đáp án/đánh dấu đúng sai, không mất vật; WebP 512×512 mặc định (640×640 có lý do), quality/file_bytes ghi đủ, mọi link tồn tại. Báo số thẻ vượt 60 KB và lý do, PNG thẻ không bắt buộc. Duplicate hash giữa hai ID khác semantic phải kiểm tra/sửa; cùng nội dung nhiều câu dùng một ID.
- validation ghi số ID có/thiếu, số câu mapped/không cần ảnh/context chưa rõ, dimensions, links và review trực quan. Không báo hoàn chỉnh nếu còn missing/context chưa giải quyết; check kỹ thuật không chứng minh tranh đúng.

Cuối cùng báo asset xong/thiếu, số crop/ghép/native/sinh mới, đường dẫn preview/mapping và hạn chế còn lại. Chỉ làm ảnh Challenge Review {pair}; không tạo audio hoặc thêm lời hát.
'''
        (OUT/f'review-{pair}.md').write_text(prompt,encoding='utf-8')
        summary.append(dict(review=pair,assets=len(assets),questions=len(questions),visual_questions=sum(q['image_required'] for q in questions),
          all_questions_have_record=True,unmapped_visual_questions=0,all_references_exist=True,status=data['status']))
    (OUT/'reviews-validation.json').write_text(json.dumps(dict(date='2026-10-10',reviews=summary,total_assets=sum(s['assets'] for s in summary)),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
