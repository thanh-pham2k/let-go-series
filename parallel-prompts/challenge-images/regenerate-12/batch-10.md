# Regenerate Challenge — batch 10

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
| 1,1 | `u07_red_circle` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_red_circle.webp` |
| 1,2 | `u07_umbrella` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_umbrella.webp` |
| 1,3 | `u07_violin` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_violin.webp` |
| 1,4 | `u07_watch` | unit-07 | `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\challenge-assets\webp\u07_watch.webp` |
| 2,1 | `u08_ride_bicycle` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_ride_bicycle.webp` |
| 2,2 | `u08_sing_song` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_sing_song.webp` |
| 2,3 | `u08_fly_kite` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_fly_kite.webp` |
| 2,4 | `u08_bounce_ball` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_bounce_ball.webp` |
| 3,1 | `u08_swim` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_swim.webp` |
| 3,2 | `u08_smile` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_smile.webp` |
| 3,3 | `u08_wink` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_wink.webp` |
| 3,4 | `u08_dance` | unit-08 | `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\challenge-assets\webp\u08_dance.webp` |

## Nguồn nội dung và tham khảo

- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\unit-07.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\unit-08.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_52.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_53.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 7 - My Body - Lesson Pages\pages\png\CD2_51.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\pages\png\CD2_59.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 8 - Abilities - Lesson Pages\pages\png\CD2_63.png`

## Prompt nội dung cho một lần generate

Create ONE master sheet of 12 square cells in exactly 4 columns and 3 rows, following the shared style and supplied references. No labels or panel numbers.
Row 1, column 1: Một hình tròn màu đỏ, không chữ, để bé chỉ/chạm trong câu I can touch the red circle.
Row 1, column 2: Một umbrella theo phonics U–W; watch là đồng hồ đeo tay, không đồng hồ treo tường; không chữ.
Row 1, column 3: Một violin theo phonics U–W; watch là đồng hồ đeo tay, không đồng hồ treo tường; không chữ.
Row 1, column 4: Một watch theo phonics U–W; watch là đồng hồ đeo tay, không đồng hồ treo tường; không chữ.
Row 2, column 1: Bé thực sự đang đạp xe, chân trên bàn đạp, hai bánh rõ; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 2, column 2: Bé đang hát, miệng mở, cử chỉ hát và nốt nhạc phụ vừa đủ; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 2, column 3: Bé đang thả diều bay, dây nối tay với diều rõ; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 2, column 4: Bé đập bóng xuống đất, tay/bóng/vệt chuyển động thể hiện bounce, không chỉ cầm bóng; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 3, column 1: Bé bơi trong nước, cử động rõ; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 3, column 2: Cận mặt bé cười, cả hai mắt mở; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 3, column 3: Cận mặt bé nháy đúng một mắt, mắt kia mở; không giống smile; cùng nhân vật/thiết kế trang Words; không nhãn.
Row 3, column 4: Bé đang múa/nhảy với tư thế rõ, khác chạy hoặc đứng; cùng nhân vật/thiết kế trang Words; không nhãn.

Staging riêng: `E:\let-go-series\audit\challenge-regeneration-staging\batch-10`.
