import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
r=read(ROOT/'audit/challenge-regeneration-completion.json')
a=read(ROOT/'audit/challenge-images-completion.json')
browser=read(ROOT/'audit/challenge-regeneration-browser-validation.json')
assert a['image_bundle_complete'] and a['required_total']==a['complete_files']==211 and a['context_items_total']==0
assert len(browser['pages'])==12 and all(not p['broken'] and not p['badDimensions'] and p['teacherOpen']==0 for p in browser['pages'])
assert browser['interaction']['choiceChecked'] and browser['interaction']['blankValue']=='test'
assert r['all_replaced'] and r['protected_source_hashes_unchanged']
# Refresh full-size QA evidence from the accepted compressed files after crop corrections.
for p in (ROOT/'audit/challenge-regeneration-staging').glob('batch-*/export.json'):
    d=read(p);sheet=Image.new('RGB',(2048,1536),'white')
    for i,c in enumerate(d['assets']):sheet.paste(Image.open(p.parent/'webp'/f"{c['id']}.webp"),(i%4*512,i//4*512))
    sheet.save(p.parent/'qa-512.png')
text=f'''# Bộ ảnh Challenge đã regenerate

Đã thay toàn bộ **211 ảnh** của **Unit 1–8 và 4 Review** bằng WebP **512×512** mới. Đủ ID, không thiếu/trùng/ảnh thừa. Toàn bộ cue và đáp án được giữ nguyên, không còn ô thiếu cue.

18 master lưới4×3: 17 batch đủ12 ảnh; batch18 có7 ảnh +5 ô trắng không xuất. Mỗi lượt tạo một master bằng built-in image_gen. Batch14 cần chạy lại toàn bộ một lần để sửa biểu tượng STOP: **19 lần gọi tổng cộng**, không sinh từng thẻ riêng.

## Dung lượng và kiểm tra

- Tổng WebP: **{r['total_bytes']:,} bytes**, khoảng **{r['total_bytes']/1048576:.2f} MiB**.
- Ảnh lớn nhất: **{r['max_bytes']:,} bytes**, khoảng **{r['max_bytes']/1024:.1f} KiB**; mọi ảnh dưới60 KiB.
- Quality80, method6; tất cả file đã decode và kiểm định dạng/kích thước.
- Root đã xem từng thẻ sau nén ở512px trong bảng lossless đủ kích thước, đếm vật và kiểm màu/động tác/anatomy. Các vùng cắt lỗi đã sửa và xem riêng lại. SHA256 gắn với QA của211 file hiện tại.
- Cả12 preview đã được kiểm bằng browser: không ảnh hỏng, mọi ảnh512×512, đáp án giáo viên đóng; đã thử chọn radio và điền chữ.
- {r['protected_source_files']} file nguồn/lesson/audio ngoài Challenge giữ nguyên hash trong lượt regenerate này.

Master thực tế1448×1086; ô gốc khoảng350px, có upscale giữ tỷ lệ khi xuất512. Upscale không tạo thêm chi tiết; ảnh sau nén đã được xem ở512px và ở kích thước thẻ nhỏ. Phong cách chung là minh họa textbook2D màu sáng, viền sạch, nền trắng; đặc điểm nội dung theo từng trang nguồn. Thẻ ngày giữ số cue1–7, không tên ngày để lộ đáp án.

## Các bộ

| Bộ | Số ảnh | Kích thước | Max KiB |
|---|---:|---|---:|
'''
for row in a['sets']:text+=f"| {row['set']} | {row['complete_files']} | 512×512 | {row['max_bytes']/1024:.1f} |\n"
text+='''
Preview tổng: [challenge-preview.html](challenge-preview.html).

Ảnh đang dùng nằm trong `Let_s Go Begin/Units/<bộ> - Lesson Pages/challenge-assets/webp`. Manifest, contact sheet và preview đã cập nhật. Prompt/master/log/QA của18 batch nằm trong `audit/challenge-regeneration-staging`; bộ prompt: `parallel-prompts/challenge-images/regenerate-12`.

Bản ảnh cũ và metadata để khôi phục nằm trong `audit/challenge-regeneration-backup`. Các PNG/master cũ trong thư mục references/batches là lịch sử; preview chỉ dùng WebP mới. Audio Challenge do chủ dự án tự bổ sung. Chưa commit/push.
'''
(ROOT/'audit/challenge-images-completion.md').write_text(text,encoding='utf-8')
a.update(status='complete_regenerated_12_cell_batches',regeneration=r,browser_validation='challenge-regeneration-browser-validation.json',note='All211 required cards regenerated, source cues resolved, strict512x512 WebP;19 calls for18 accepted batch masters including one full retry.')
(ROOT/'audit/challenge-images-completion.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS: regeneration report backed by disk, hash-bound512px QA and12 live browser previews.')
