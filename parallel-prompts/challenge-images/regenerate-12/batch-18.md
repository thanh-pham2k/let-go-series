# Regenerate Challenge — batch 18

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
| 1,1 | `r78_day_01_sunday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_01_sunday.webp` |
| 1,2 | `r78_day_02_monday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_02_monday.webp` |
| 1,3 | `r78_day_03_tuesday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_03_tuesday.webp` |
| 1,4 | `r78_day_04_wednesday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_04_wednesday.webp` |
| 2,1 | `r78_day_05_thursday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_05_thursday.webp` |
| 2,2 | `r78_day_06_friday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_06_friday.webp` |
| 2,3 | `r78_day_07_saturday` | review-7-8 | `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\challenge-assets\webp\r78_day_07_saturday.webp` |

## Nguồn nội dung và tham khảo

- Inventory và mapping: `E:\let-go-series\parallel-prompts\challenge-images\review-7-8.inventory.json`; đọc nguồn và question-image-map.json trong challenge-assets tương ứng.
- `E:\let-go-series\Let_s Go Begin\Units\Review 7-8(2).md`
- `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\pages\png\CD2_70.png`
- `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\pages\png\CD2_71.png`
- `E:\let-go-series\Let_s Go Begin\Units\Review 7-8 - Lesson Pages\pages\png\CD2_72.png`

## Prompt nội dung cho một lần generate

Create ONE master sheet of 12 square cells in exactly 4 columns and 3 rows, following the shared style and supplied references. No labels or panel numbers.
Row 1, column 1: Thẻ thứ tự nguồn 1 — Sunday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 1, column 2: Thẻ thứ tự nguồn 2 — Monday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 1, column 3: Thẻ thứ tự nguồn 3 — Tuesday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 1, column 4: Thẻ thứ tự nguồn 4 — Wednesday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 2, column 1: Thẻ thứ tự nguồn 5 — Thursday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 2, column 2: Thẻ thứ tự nguồn 6 — Friday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 2, column 3: Thẻ thứ tự nguồn 7 — Saturday. Sunday=1 đến Saturday=7; không phải số thứ trong tiếng Việt hoặc ngày tháng. Native graphic/font, không cần image_gen.
Row 2, column 4: Completely empty white cell. No subject.
Row 3, column 1: Completely empty white cell. No subject.
Row 3, column 2: Completely empty white cell. No subject.
Row 3, column 3: Completely empty white cell. No subject.
Row 3, column 4: Completely empty white cell. No subject.

Staging riêng: `E:\let-go-series\audit\challenge-regeneration-staging\batch-18`.
