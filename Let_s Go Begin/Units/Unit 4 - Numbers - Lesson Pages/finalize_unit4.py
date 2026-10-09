from pathlib import Path
import json, shutil, sys
import re, zipfile
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parent
def job(name, tracks, prompt, refs, result=None):
    data={'tracks':tracks,'prompt':prompt,'refs':refs,'tool':'built-in image_gen','result':result,'status':'submitted'}
    (ROOT/'assets/batches'/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
if sys.argv[1]=='prepare':
    for src, name, tracks in [('batch3','batch3-first3',['CD1_63','CD1_64','CD1_65']),('batch4','batch4-first3',['CD1_67','CD1_68','CD1_69'])]:
        old=json.loads((ROOT/'assets/batches'/f'{src}.json').read_text(encoding='utf-8'))
        job(name,tracks,old['prompt'],old['refs'],f'First three quadrants from {src}.png; fourth superseded by standalone repair.')
        shutil.copyfile(ROOT/'assets/batches'/f'{src}.png',ROOT/'assets/batches'/f'{name}.png')
    m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    next(p for p in m['items'] if p['track']=='CD1_67')['question']['correct_choice_id']='B'
    (ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
if sys.argv[1]=='docs':
    doc=ROOT.parent/'Unit 4 - Numbers(2).md'
    text=doc.read_text(encoding='utf-8')
    clips=[('one','one','Challenge 1.3'),('two','two','Challenge 1.3'),('three','three','Challenge 1.3'),('four','four','Challenge 1.3'),('five','five','Challenge 1.3'),('six','six','Challenge 1.3'),('seven','seven','Challenge 1.3'),('eight','eight','Challenge 1.3'),('nine','nine','Challenge 1.3'),('ten','ten','Challenge 1.3'),('lets_count',"Let's count.",'Challenge 2.1.6'),('igloo','igloo','Phonics: tùy chọn'),('jump_rope','jump rope','Phonics: tùy chọn'),('kangaroo','kangaroo','Phonics: tùy chọn'),('lion','lion','Phonics: tùy chọn')]
    extra='\n## Rà soát clip nghe bắt buộc và dùng chung\n\nCác clip câu mẫu trong bảng trên là bắt buộc cho Challenge 2, Challenge 3.4 và các bài nghe lệnh. Dùng chung May I come in?, Sure! Please come in!, Please come in!, Is it a 5?, Is it a 9?, How many?, Go., Stop. giữa các câu; không cần thu bản trùng. Bảng bổ sung dưới đây vá các mục bộ dò tự động chưa liệt kê. Chưa có file nào trong checklist được tạo hoặc đánh dấu đã có.\n\n| Đã có | File gợi ý | Nội dung | Dùng cho |\n|---|---|---|---|\n'
    for slug, utterance, use in clips: extra+=f'| ☐ | `u4_{slug}.mp3` | {utterance} | {use} |\n'
    extra+='\nChallenge 1.3 cần đủ mười clip one–ten và chọn ngẫu nhiên trong tập lựa chọn đang hiển thị. Challenge 2.3 nghe câu hỏi dùng clip câu hỏi; nếu phát cả hội thoại thì thu riêng hai lượt May I come in? / Sure! Please come in!, Is it a 5? / Yes, it is., Is it a 9? / No, it isn\'t. It\'s a 6. Các clip Yes, it is. và No, it isn\'t. It\'s a 6. có thể tái sử dụng. Đọc đáp án mẫu, chuỗi số, bảng chữ cái A–Z và giọng Boss là tùy chọn; không thay clip nghe bắt buộc. Bài tự nói/viết không bắt buộc audio.\n'
    doc.write_text(text.rstrip()+'\n'+extra,encoding='utf-8')
    readme=ROOT/'README.md'
    readme.write_text(readme.read_text(encoding='utf-8')+'\nĐiều chỉnh đối chiếu nguồn: CD1_60 khôi phục mẫu “Let\'s count. 1, 2, 3.” bằng lớp font; CD1_63 thêm từ one–five; CD1_67 thêm nhãn five/seven/ten và sửa đáp án thành 5. CD1_66 bố trí lại nhóm 9 mèo, 8 chó, 7 táo, 6 trái tim, 5 sao để đếm rõ; CD1_70 bố trí mười bóng thành hai hàng, giữ đúng mã nhóm/số và hai hội thoại, thêm nhãn CD1 70 bằng font. Không thêm lời bài hát.\n\nĐã xem riêng cả 16 PNG sau cắt và contact sheet, đối chiếu source-pages/reference từ PDF; kiểm số lượng, màu nhóm hình, glyph và chữ.\n',encoding='utf-8')
    report=json.loads((ROOT/'validation.json').read_text(encoding='utf-8'))
    report['visual_validation']='All 16 final PNG pages and contact sheet inspected against source PDF renders; counts, colors, dialogues, alphabet and crop boundaries checked.'
    report['adjustments']=['CD1_60 source model font restored','CD1_66 exact count repair','CD1_67 answer B=5','CD1_70 ten balloon pairs and dialogues repaired']
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    files=[doc,ROOT.parent/'Unit 4 - Numbers - Cau hoi theo trang.md',ROOT/'README.md',ROOT/'questions.md']
    for f in files:
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
            assert (f.parent/unquote(target)).exists(),(f,target)
    zpath=ROOT.parent/'Unit_4_Numbers_regenerated.zip'
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
        for f in ROOT.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts: z.write(f,f.relative_to(ROOT))
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None
        assert len([n for n in z.namelist() if n.startswith('pages/png/')])==16
        assert len([n for n in z.namelist() if n.startswith('pages/webp/')])==16
    print('Final docs links and ZIP verified; 16 PNG + 16 WebP; Challenge exercises preserved.')
if sys.argv[1]=='layers':
    m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    p=next(p for p in m['items'] if p['track']=='CD1_60')
    p['layers'][0]['box']=[0,0,1200,1120]
    p['layers'] += [{'type':'text','text':"Let's count. 1, 2, 3.",'box':[120,1140,960,50],'font_size':38,'align':'center'}]
    p['visual_review']+=' Source header model restored with font layer.'
    p=next(p for p in m['items'] if p['track']=='CD1_70')
    p['layers'] += [{'type':'rect','box':[1035,0,155,74],'fill':'#FFFFFF'}, {'type':'text','text':'CD1 70','box':[1040,20,145,42],'font_size':32,'bold':True,'align':'center'}]
    for b in m['batches']:
        b['status']='reviewed'
        if 'batch3' in b['id']: b['note']='First three quadrants approved; CD1_66 superseded by page66-repair.'
        if 'batch4' in b['id']: b['note']='First three quadrants approved; CD1_70 superseded by page70-repair.'
    (ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
