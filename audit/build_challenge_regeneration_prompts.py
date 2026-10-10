import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'parallel-prompts/challenge-images'
OUT = BASE / 'regenerate-12'
OUT.mkdir(exist_ok=True)
names = [f'unit-{n:02}' for n in range(1,9)] + ['review-1-2','review-3-4','review-5-6','review-7-8']
cards = []
for name in names:
    inv = json.loads((BASE / f'{name}.inventory.json').read_text(encoding='utf-8'))
    for asset in inv['assets']:
        cards.append(dict(id=asset['id'], brief=asset['brief'], note=asset.get('note',''),
            set=name, source=inv['source'], references=asset.get('references',[]),
            uses=asset.get('uses',[]), output=str(Path(inv['lesson_folder']) / 'challenge-assets/webp' / (asset['id']+'.webp'))))
ids = [a['id'] for a in cards]
assert len(cards)==211 and len(set(ids))==211
assert all(Path(a['source']).exists() and all(Path(r).exists() for r in a['references']) for a in cards)
style_refs = [str(ROOT / 'Let_s Go Begin/Units/Unit 1 - Toys - Lesson Pages/pages/png/CD1_07.png'),
              str(ROOT / 'Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/pages/png/CD1_34.png')]
common = '''Tạo lại TOÀN BỘ các ID trong batch này, kể cả ảnh hiện có. Không dùng crop ảnh cũ để thay cho việc regenerate. Đọc nguồn và mapping hiện tại để giữ nguyên ý nghĩa, số lượng, màu và đáp án đã chốt. Không sửa bài, đáp án hoặc audio. Không commit/push.

Dùng built-in image_gen: đúng MỘT lần gọi tạo master cho toàn bộ batch, không gọi từng ảnh. Xem các ảnh tham khảo trước khi gọi, đính kèm hai mẫu phong cách chung và các trang nội dung cần thiết. Mỗi batch là lưới 4 cột × 3 hàng gồm 12 ô vuông, thứ tự trái→phải, trên→dưới. Không in ID hoặc số ô lên master. Ô trống cuối danh sách phải trắng hoàn toàn.

Phong cách chung: minh họa sách Let's Go Begin, hoạt hình 2D cho trẻ, màu sáng, viền đậm sạch, đổ bóng mềm nhẹ, nền trắng, không ảnh thật/3D/emoji. Cùng đồ vật và nhân vật phải giữ cùng thiết kế, màu và trang phục theo mẫu lesson; Review dùng cùng thiết kế của Unit tương ứng. Chủ thể nằm trọn trong ô với khoảng an toàn ít nhất 8%; không cắt đầu, tay, chân, dây, bánh xe; không vật xuyên ô. Nhóm đếm phải đúng số lượng, không thêm vật cùng loại ở nền. Hành động và trạng thái can/can't phải phân biệt rõ; giữ nguyên cue đã chốt. Không chữ, nhãn đáp án, lựa chọn, watermark hoặc lời thoại gợi đáp án trong bitmap. Câu hỏi và chữ đặt ngoài ảnh trong UI; chi tiết chữ/số thực sự cần cho câu hỏi giữ theo mapping bằng font ngoài ảnh.

Xuất master lớn nhất tool hỗ trợ, ưu tiên canvas ngang tỷ lệ 4:3 với ô vuông và gutter trắng. Nếu canvas khác tỷ lệ, thêm lề trắng ngoài lưới; không kéo méo ô. Không hứa kích thước master mà tool không hỗ trợ. Sau một lần generate, xem đủ từng ô, cắt theo gutter thực tế rồi contain giữ tỷ lệ về ĐÚNG 512×512, nền trắng. Xuất WebP quality=80, method=6, bỏ metadata; mục tiêu ≤60 KiB mỗi ảnh, thử quality 75/70 nếu cần và kiểm tra chi tiết. Không xuất 640×640. Phải ghi kích thước ô gốc thực tế; upscale không bổ sung chi tiết. Nếu master có lỗi hoặc độ nét không đạt, báo batch cần chạy lại, không âm thầm gọi thêm trong cùng lượt.

Lưu master, prompt thực tế, references, vị trí ô, crop boxes, thông số export, bytes và nhận xét từng ảnh vào thư mục riêng của batch. Xuất trước vào thư mục staging của batch, chưa ghi đè ảnh đang dùng. Kiểm tra đủ ID, không trùng/thiếu/ảnh thừa, nội dung khớp nguồn, không lẫn ô và đủ 512×512 WebP nhẹ. Chỉ sau QA mới thay các file đúng đường dẫn đích trong bảng; giữ bản cũ có thể khôi phục, cập nhật manifest/mapping/preview liên quan mà không đổi ID hoặc đáp án. Các batch khác chỉ đọc nguồn dùng chung và ghi staging riêng; việc tích hợp manifest chung thực hiện tuần tự sau khi tất cả batch được duyệt.
'''
batches=[]
for offset in range(0,len(cards),12):
    number=offset//12+1
    subset=cards[offset:offset+12]
    positions=[]
    for i in range(12):
        row,col=i//4+1,i%4+1
        if i<len(subset):
            a=subset[i]
            positions.append(f"Row {row}, column {col}: {a['brief']}" + (f" Lưu ý: {a['note']}" if a['note'] else ''))
        else:
            positions.append(f'Row {row}, column {col}: Completely empty white cell. No subject.')
    prompt='Create ONE master sheet of 12 square cells in exactly 4 columns and 3 rows, following the shared style and supplied references. No labels or panel numbers.\n'+'\n'.join(positions)
    filename=f'batch-{number:02}.md'
    body=f'# Regenerate Challenge — batch {number:02}\n\n{common}\n## Mẫu phong cách chung\n\n'+''.join(f'- `{r}`\n' for r in style_refs)
    body+='\n## Danh sách ô và đường dẫn đích\n\n| Ô | ID | Bộ | File đích |\n|---|---|---|---|\n'
    for i,a in enumerate(subset):
        body+=f"| {i//4+1},{i%4+1} | `{a['id']}` | {a['set']} | `{a['output']}` |\n"
    body+='\n## Nguồn nội dung và tham khảo\n\n'
    for name in dict.fromkeys(a['set'] for a in subset):
        body+=f'- Inventory và mapping: `{BASE / (name+".inventory.json")}`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.\n'
    for p in dict.fromkeys([a['source'] for a in subset]+[r for a in subset for r in a['references']]):
        body+=f'- `{p}`\n'
    body+='\n## Prompt nội dung cho một lần generate\n\n'+prompt+'\n\nStaging riêng: `'+str(ROOT / 'audit/challenge-regeneration-staging' / f'batch-{number:02}')+'`.\n'
    (OUT / filename).write_text(body,encoding='utf-8')
    batches.append(dict(batch=number,prompt_file=filename,rows=3,columns=4,occupied_cells=len(subset),blank_cells=12-len(subset),cards=subset))
flat=[a['id'] for b in batches for a in b['cards']]
assert Counter(flat)==Counter(ids) and len(batches)==18
data=dict(total_assets=len(cards),total_batches=len(batches),batch_capacity=12,export=dict(format='WebP',width=512,height=512,quality=80,method=6,target_bytes=61440),style_references=style_refs,batches=batches)
(OUT/'batch-index.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps(dict(status='pass',scope='Prompt coverage and existing source/reference paths only; images have not been regenerated',assets=211,unique_ids=211,missing_ids=[],duplicate_ids=[],extra_ids=[],batches=18,full_batches=17,last_batch_assets=7,last_batch_blank_cells=5,source_and_reference_paths_exist=True),ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Bộ prompt regenerate toàn bộ Challenge — 12 ô/lần

Bộ mới này thay hướng dẫn tạo ảnh trước đây: regenerate toàn bộ 211 ID của Unit 1–8 và 4 Review, không bỏ qua ảnh hiện có, không ngoại lệ 640px. Mỗi file batch là một prompt độc lập và đúng một lần gọi image_gen tạo master 4×3. Sau đó cắt ra WebP 512×512 lightweight, giữ nguyên ID và ý nghĩa nguồn. Hai mẫu lesson chung áp dụng cho mọi batch để giữ phong cách.

211 không chia hết cho 12: 17 batch đầy đủ 12 ảnh, batch 18 có 7 ảnh + 5 ô trắng. Không tạo 5 ảnh dư. Batch có thể đi qua ranh giới Unit/Review để gom đủ 12; đường dẫn từng ID đã ghi rõ. Có thể chạy các batch song song trong staging riêng; tích hợp manifest/mapping chung tuần tự sau QA để tránh ghi đè nhau.

Đây là bộ prompt, chưa phải bộ ảnh regenerate đã hoàn thành. Một lần generate là một master, không phải tool trả trực tiếp 12 file WebP. Phải cắt và nén sau khi tạo. Nếu batch lỗi, báo cần chạy lại; không coi lần tạo là bảo đảm chất lượng.

'''
for b in batches:
    readme+=f"- [Batch {b['batch']:02}]({b['prompt_file']}): {b['occupied_cells']} ảnh, {b['blank_cells']} ô trắng.\n"
readme+='\nĐối chiếu đầy đủ: `batch-index.json`; kiểm tra coverage: `validation.json`. Không cần tạo audio.\n'
(OUT/'README.md').write_text(readme,encoding='utf-8')
print(json.dumps(dict(assets=len(cards),batches=len(batches),output=str(OUT)),ensure_ascii=False))
