# Regenerate Challenge — batch 06

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
| 1,1 | `u04_kangaroo` | unit-04 | `E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\challenge-assets\webp\u04_kangaroo.webp` |
| 1,2 | `u04_lion` | unit-04 | `E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\challenge-assets\webp\u04_lion.webp` |
| 1,3 | `u05_dog_01` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_dog_01.webp` |
| 1,4 | `u05_dog_02` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_dog_02.webp` |
| 2,1 | `u05_cat_01` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_cat_01.webp` |
| 2,2 | `u05_cat_02` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_cat_02.webp` |
| 2,3 | `u05_bird_01` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_bird_01.webp` |
| 2,4 | `u05_bird_02` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_bird_02.webp` |
| 3,1 | `u05_cow_01` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_cow_01.webp` |
| 3,2 | `u05_cow_02` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_cow_02.webp` |
| 3,3 | `u05_rabbit_01` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_rabbit_01.webp` |
| 3,4 | `u05_rabbit_02` | unit-05 | `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\challenge-assets\webp\u05_rabbit_02.webp` |

## Nguồn nội dung và tham khảo

- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\unit-04.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\unit-05.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- `E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\pages\png\CD1_69.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\pages\png\CD2_07.png`
- `E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\pages\png\CD2_11.png`

## Prompt nội dung cho một lần generate

Create ONE master sheet of 12 square cells in exactly 4 columns and 3 rows, following the shared style and supplied references. No labels or panel numbers.
Row 1, column 1: Một kangaroo theo phonics I–L. Igloo là nhà băng vòm (không nhà tranh dù emoji là 🛖); jump rope là vật dây nhảy, không cảnh bé nhảy.
Row 1, column 2: Một lion theo phonics I–L. Igloo là nhà băng vòm (không nhà tranh dù emoji là 🛖); jump rope là vật dây nhảy, không cảnh bé nhảy.
Row 1, column 3: Đúng 1 con dog; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 1, column 4: Đúng 2 con dog; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 2, column 1: Đúng 1 con cat; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 2, column 2: Đúng 2 con cat; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 2, column 3: Đúng 1 con bird; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 2, column 4: Đúng 2 con bird; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 3, column 1: Đúng 1 con cow; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 3, column 2: Đúng 2 con cow; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 3, column 3: Đúng 1 con rabbit; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.
Row 3, column 4: Đúng 2 con rabbit; mỗi con thấy toàn thân, nhóm tách rõ, không con khác hoặc con phụ trong nền. Cùng thiết kế ở bản đơn/nhóm.

Staging riêng: `E:\let-go-series\audit\challenge-regeneration-staging\batch-06`.
