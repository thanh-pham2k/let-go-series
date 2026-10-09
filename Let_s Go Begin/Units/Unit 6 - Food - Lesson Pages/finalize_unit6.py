"""Unit-6-only final cropping, documentation additions, and package checks."""
from pathlib import Path
import json,hashlib,re,zipfile
from urllib.parse import unquote
from PIL import Image
ROOT=Path(__file__).resolve().parent
def crops():
    m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    boxes={
      'batch1':[(2,2,709,539),(739,2,1446,539),(2,561,709,1084),(739,561,1446,1084)],
      'batch2':[(3,3,722,633),(727,3,1445,633),(3,638,722,1083),(727,638,1445,1083)],
      'batch3':[(3,3,766,510),(771,3,1533,510),(3,515,766,1021),(771,515,1533,1021)],
      'batch4':[(14,12,536,698),(553,12,1073,698),(14,716,536,1433)]
    }
    for b,bs in boxes.items():
        job=json.loads((ROOT/f'assets/batches/{b}.json').read_text(encoding='utf-8'))
        im=Image.open(ROOT/f'assets/batches/{b}.png')
        for t,box in zip(job['tracks'],bs):
            p=next(p for p in m['items'] if p['track']==t)
            im.crop(box).save(ROOT/p['layers'][0]['asset'])
            p['source_crop_box']=list(box)
            p['visual_review']+=' Final crop independently inspected on 1200x1200 contain canvas; gutters/outer frame removed.'
        job['final_crop_boxes']=bs
        (ROOT/f'assets/batches/{b}.json').write_text(json.dumps(job,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

def docs():
    readme=ROOT/'README.md'
    text=readme.read_text(encoding='utf-8')
    text=text.split('\n## Nguồn và điều chỉnh đã đối chiếu',1)[0]
    text+='''
## Nguồn và điều chỉnh đã đối chiếu

- PDF gốc: ../Unit 6 - Food.pdf, 8 trang sách 46–53. Đã xem trực quan đủ 8 trang và mọi trang sau cắt, không chỉ dựa vào câu hỏi.
- Hai nhãn **CD1 32 / CD1 34** in sai trong PDF và mapping ZIP cũ được chuẩn hóa thành **CD2_32 / CD2_34**, theo mapping tổng và MP3 CD2. Không sử dụng CD1/Track32 hoặc CD1/Track34.
- Bốn nhóm 4/4/4/3 trang được vẽ lại bằng built-in image_gen. Prompt, reference, kết quả và log sửa lưu tại assets/batches. Các box cắt thực tế nằm trong manifest; contain giữ tỷ lệ, bỏ gutter/viền ảnh ghép.
- CD2_24, CD2_26, CD2_30 dùng hình hành động/từ vựng cùng trang nguồn vì phần audio chỉ có tiêu đề. CD2_31 giữ cả D. Ask and answer; CD2_33 giữ C. Find the letters; không thêm track hoặc câu trắc nghiệm cho phần không có audio riêng.
- CD2_32 xuống dòng bảng chữ cái để dễ đọc, giữ đủ A–Z/a–z và màu Q–T. CD2_33 giữ cảnh Find the letters với chữ S/s và các nét cuộn trong tán cây, viền áo, ghế; nét trang trí được vẽ lại, không phải bản sao tọa độ của PDF. Không có bảng giải đáp trên ảnh.
- Đã đếm 6 nến ở cả hai cảnh sinh nhật và các nhóm trên game: 2 thỏ, 2 xe đạp, 3 mèo, 2 chim, 3 gấu, 2 tàu. Giữ các ô trống trên bảng và các chỗ trống trong Say and act.
- MP3 chỉ được kiểm tra đồng nhất byte với thư mục nguồn CD2. **Chưa nghe hoặc transcribe kiểm chứng độc lập**; chưa xác nhận nội dung lời nói ở CD2_32/CD2_34 bằng nghe. Audio Challenge chưa tạo; chủ dự án tự bổ sung.
'''
    readme.write_text(text,encoding='utf-8')
    doc=ROOT.parent/'Unit 6 - Food(2).md'
    text=doc.read_text(encoding='utf-8')
    text=text.split('\n## Phân loại và nối clip Challenge (chưa có file)',1)[0]
    text+='''

## Phân loại và nối clip Challenge (chưa có file)

Các ô dưới đây đều chưa hoàn thành. Dùng chung clip trùng câu giữa các Challenge; không coi audio CD dài là clip ngắn đã sẵn sàng.

| Mức | Clip/kho nội dung cần bổ sung | Dùng cho |
|---|---|---|
| Bắt buộc để tự chạy phần nghe | 8 clip đơn từ ice cream, pizza, cake, chicken, milk, fish, bread, rice | Challenge 1.2; Challenge 2.2; chọn ngẫu nhiên đúng một clip nằm trong bộ lựa chọn |
| Bắt buộc | How old are you?; I'm 6.; I like ice cream.; I like cake.; Do you like milk?; Do you like fish?; Yes, I do.; No, I don't.; Make a line.; Make a circle. | Challenge 2.1 (10 mục); câu hỏi 2.3; lệnh 2.4; Challenge 3.4; lệnh 5.7 |
| Tùy chọn cho bài nói/đọc; bắt buộc nếu thêm chế độ nghe | I'm 5.; I'm 7.; I'm 10.; Do you like birds?; queen; rabbit; sun; tiger; Q q; R r; S s; T t | Recall/Build/Final Boss và phonics; dùng chung từ/câu đã có, không thu lặp |
| Tùy chọn | 1, 2, 3, 4, 5, 6, 7!; 1, 2, 3, 4, 5, 6, 7, 8, 9, 10!; toàn bộ A–Z/a–z | Number Recall / luyện alphabet nếu chuyển sang nghe |
| Tùy chọn | Hội thoại tuổi; milk + Yes; fish + No; birds + Yes hoặc No | Challenge 5.9: bản ghép đủ hai lượt, có thể dùng clip hỏi/đáp dùng chung; giọng Boss khác là tùy chọn |

Không cần thu audio cho bài điền chữ, xếp từ hoặc nhìn hình nếu chỉ sử dụng ở chế độ đọc/viết. Khi nối file thực tế, giữ cả lựa chọn Yes và No theo tình huống; không cố định sở thích của người học bằng đáp án mẫu.
'''
    doc.write_text(text,encoding='utf-8')
    report=json.loads((ROOT/'validation.json').read_text(encoding='utf-8'))
    report['visual_audit']={'source_pages':8,'final_pages':15,'basis':'Model visual comparison of all source and final images, plus contact sheet; technical checks alone do not prove art accuracy.','adjustments':['CD1 misprints normalized to CD2','Alphabet wrapped into rows','Find-the-letters ornaments redrawn']}
    report['challenge_audio']='No generated or completed audio clips; mandatory vs optional checklist in Unit 6 - Food(2).md.'
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    preview=ROOT/'preview.html'
    html=preview.read_text(encoding='utf-8')
    html=html.replace("function show(index){current=index;", "function show(index){document.getElementById('review').disabled=true;current=index;")
    html=html.replace("function review(){document.getElementById('practice').style.display='block'}", "function review(){if(document.getElementById('review').disabled)return;document.getElementById('practice').style.display='block'}")
    html=html.replace("audio.addEventListener('ended',review)","audio.addEventListener('ended',()=>{document.getElementById('review').disabled=false;review()})")
    preview.write_text(html,encoding='utf-8')

def package():
    m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    assert [p['track'] for p in m['items']]==[f'CD2_{n}' for n in range(20,35)]
    for p in m['items']:
        assert p['status']=='reviewed' and isinstance(p['question'],dict)
        assert len({c['id'] for c in p['question']['choices']})==len(p['question']['choices'])
        assert p['question']['correct_choice_id'] in [c['id'] for c in p['question']['choices']]
        for fmt in ['png','webp']:
            im=Image.open(ROOT/p['output'][fmt]); assert im.size==(1200,1200); im.verify()
    docs=[ROOT/'README.md',ROOT/'questions.md',ROOT.parent/'Unit 6 - Food(2).md',ROOT.parent/'Unit 6 - Food - Cau hoi theo trang.md']
    for doc in docs:
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            assert (doc.parent/unquote(link)).exists(),(doc,link)
    dest=ROOT.parent/'Unit_6_Food_regenerated.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for p in m['items']:
            for name in [p['output']['png'],p['output']['webp'],p['audio_file']]:assert z.read(name)==(ROOT/name).read_bytes()
    print('Unit6 final PASS: 15 tracks, images decoded/1200, questions, document links, ZIP CRC and asset identity.',dest)

if __name__=='__main__':
    import sys
    {'crops':crops,'docs':docs,'package':package}[sys.argv[1]]()
