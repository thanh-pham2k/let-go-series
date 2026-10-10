# Regenerate Challenge — batch 09

Tạo lại TOÀN BỘ các ID trong batch này, kể cả ảnh hiện có. Không dùng crop ảnh cũ để thay cho việc regenerate. Đọc nguồn và mapping hiện tại để giữ nguyên ý nghĩa, số lượng, màu và đáp án đã chốt. Không sửa bài, đáp án hoặc audio. Không commit/push.

Dùng built-in image_gen: đúng MỘT lần gọi tạo master cho toàn bộ batch, không gọi từng ảnh. Xem các ảnh tham khảo trước khi gọi, đính kèm hai mẫu phong cách chung và các trang nội dung cần thiết. Mỗi batch là lưới 4 cột × 3 hàng gồm 12 ô vuông, thứ tự trái→phải, trên→dưới. Không in ID hoặc số ô lên master. Ô trống cuối danh sách phải trắng hoàn toàn.

Phong cách chung: minh họa sách Let's Go Begin, hoạt hình 2D cho trẻ, màu sáng, viền đậm sạch, đổ bóng mềm nhẹ, nền trắng, không ảnh thật/3D/emoji. Cùng đồ vật và nhân vật phải giữ cùng thiết kế, màu và trang phục theo mẫu lesson; Review dùng cùng thiết kế của Unit tương ứng. Chủ thể nằm trọn trong ô với khoảng an toàn ít nhất 8%; không cắt đầu, tay, chân, dây, bánh xe; không vật xuyên ô. Nhóm đếm phải đúng số lượng, không thêm vật cùng loại ở nền. Hành động và trạng thái can/can't phải phân biệt rõ; giữ nguyên cue đã chốt. Không chữ, nhãn đáp án, lựa chọn, watermark hoặc lời thoại gợi đáp án trong bitmap. Câu hỏi và chữ đặt ngoài ảnh trong UI; chi tiết chữ/số thực sự cần cho câu hỏi giữ theo mapping bằng font ngoài ảnh.

Xuất master lớn nhất tool hỗ trợ, ưu tiên canvas ngang tỷ lệ 4:3 với ô vuông và gutter trắng. Nếu canvas khác tỷ lệ, thêm lề trắng ngoài lưới; không kéo méo ô. Không hứa kích thước master mà tool không hỗ trợ. Sau một lần generate, xem đủ từng ô, cắt theo gutter thực tế rồi contain giữ tỷ lệ về ĐÚNG 512×512, nền trắng. Xuất WebP quality=80, method=6, bỏ metadata; mục tiêu ≤60 KiB mỗi ảnh, thử quality 75/70 nếu cần và kiểm tra chi tiết. Không xuất 640×640. Phải ghi kích thước ô gốc thực tế; upscale không bổ sung chi tiết. Nếu master có lỗi hoặc độ nét không đạt, báo batch cần chạy lại, không âm thầm gọi thêm trong cùng lượt.

Lưu master, prompt thực tế, references, vị trí ô, crop boxes, thông số export, bytes và nhận xét từng ảnh vào thư mục riêng của batch. Xuất trước vào thư mục staging của batch, chưa ghi đè ảnh đang dùng. Kiểm tra đủ ID, không trùng/thiếu/ảnh thừa, nội dung khớp nguồn, không lẫn ô và đủ 512×512 WebP nhẹ. Chỉ sau QA mới thay các file đúng đường dẫn đích trong bảng; giữ bản cũ có thể khôi phục, cập nhật manifest/mapping/preview liên quan mà không đổi ID hoặc đáp án. Các batch khác chỉ đọc nguồn dùng chung và ghi staging riêng; việc tích hợp manifest chung thực hiện tuần tự sau khi tất cả batch được duyệt.

## Mẫu phong cách chung

- `E:\let-go-series\Let_s Go Begin\Units\Unit 1 - Toys - Lesson Pages\pages\png\CD1_07.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 2 - Colors - Lesson Pages\pages\png\CD1_34.png`

## Danh sách ô và đường dẫn đích

| Ô | ID | Bộ | File đích |
|---|---|---|---|
| 1,1 | `u06_dislikes_fish` | unit-06 | `E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Lesson Pages\challenge-assets\webp\u06_dislikes_fish.webp` |
| 1,2 | `u07_head` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_head.webp` |
| 1,3 | `u07_shoulders` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_shoulders.webp` |
| 1,4 | `u07_knees` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_knees.webp` |
| 2,1 | `u07_toes` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_toes.webp` |
| 2,2 | `u07_eyes` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_eyes.webp` |
| 2,3 | `u07_ears` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_ears.webp` |
| 2,4 | `u07_mouth` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_mouth.webp` |
| 3,1 | `u07_nose` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_nose.webp` |
| 3,2 | `u07_touch_head` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_touch_head.webp` |
| 3,3 | `u07_touch_nose` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_touch_nose.webp` |
| 3,4 | `u07_touch_eyes` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_touch_eyes.webp` |

## Nguồn nội dung và tham khảo

- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\unit-06.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\unit-07.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- `E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Lesson Pages\pages\png\CD2_31.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_42.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_46.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_44.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_48.png`

## Prompt nội dung cho một lần generate

Create ONE master sheet of 12 square cells in exactly 4 columns and 3 rows, following the shared style and supplied references. No labels or panel numbers.
Row 1, column 1: Bé với món cá, cử chỉ nhẹ nhàng từ chối rõ; dùng cho tình huống mẫu No, I don’t. Không in câu trả lời hoặc dấu X.
Row 1, column 2: Bộ phận head trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 1, column 3: Bộ phận shoulders trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 1, column 4: Bộ phận knees trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 2, column 1: Bộ phận toes trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 2, column 2: Bộ phận eyes trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 2, column 3: Bộ phận ears trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 2, column 4: Bộ phận mouth trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 3, column 1: Bộ phận nose trên cùng mẫu nhân vật Unit 7, có vòng sáng/mũi tên không chữ chỉ đúng vùng. shoulders/knees/toes/eyes/ears thể hiện số nhiều. Toes là ngón chân, knees là đầu gối; không chỉ toàn chân.
Row 3, column 2: Bé đang chạm đúng head; động tác rõ, bàn tay tự nhiên, không che mất vùng cần nhận diện. Chạm mắt nhẹ ở vùng cạnh mắt, không chọc vào nhãn cầu.
Row 3, column 3: Bé đang chạm đúng nose; động tác rõ, bàn tay tự nhiên, không che mất vùng cần nhận diện. Chạm mắt nhẹ ở vùng cạnh mắt, không chọc vào nhãn cầu.
Row 3, column 4: Bé đang chạm đúng eyes; động tác rõ, bàn tay tự nhiên, không che mất vùng cần nhận diện. Chạm mắt nhẹ ở vùng cạnh mắt, không chọc vào nhãn cầu.

Staging riêng: `E:\let-go-series\audit\challenge-regeneration-staging\batch-09`.
