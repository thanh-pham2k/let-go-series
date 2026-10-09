Hoàn thiện RIÊNG Unit 5 – Animals trong repo E:\let-go-series. Đây là một phần của công việc Unit2–8 đang chạy song song; hãy làm đến khi Unit này hoàn thiện và kiểm tra được, không chỉ lập kế hoạch.

Phạm vi ghi file của bạn:
- E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages
- E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Cau hoi theo trang.md
- E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals(2).md
- ZIP Unit_5_Animals_regenerated.zip trong E:\let-go-series\Let_s Go Begin\Units.

Không sửa Unit khác, không chạy prepare_lesson_units.py hoặc script cấu hình Unit khác. Không sửa các script dùng chung ở root (build_lesson_unit.py, complete_unit_docs.py, prepare_lesson_units.py) hoặc render.py của Unit1. Nếu cần helper mới, đặt trong thư mục Unit của bạn. Không cập nhật remaining-units-progress.json toàn cục, không commit/push. Các chat khác có thể sửa file ngoài phạm vi; không hoàn tác thay đổi của chúng.

Nguồn và bộ mẫu:
- PDF chuẩn: E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals.pdf.
- Manifest/mapping hiện có: E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Lesson Pages\manifest.json. Đọc trạng thái thực tế trước khi làm, vì file có thể đã tiến thêm sau khi prompt này được viết.
- E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals - Cau hoi theo trang.md và E:\let-go-series\Let_s Go Begin\Units\Unit 5 - Animals(2).md: câu hỏi theo track và bài luyện thêm.
- Mapping tổng chỉ đọc: E:\let-go-series\Let_s Go Begin\lets_go_audio_mapping.metadata.
- Mẫu đã hoàn thiện để tham khảo chỉ đọc: Unit2 – Colors – Lesson Pages và Unit3 – Shapes – Lesson Pages (preview.html, manifest.json, validation.json).
- Yêu cầu chính xác: đủ **18 trang cho CD2_02–CD2_19**, mỗi trang có hình và chữ bài học, audio đúng track, đúng1 câu trắc nghiệm riêng trong metadata.

Trạng thái đã kiểm tra:
- assets/batches/batch1.png và batch2.png đã sinh, gồm8 trang CD2_02–09. Chưa trang nào nhập/xuất/chốt. Bắt đầu bằng kiểm tra hai batch này, không tạo lại nếu không cần.
- Batch1 đã có câu thoại, hai tình huống chỗ trống, đủ8 dòng lời hát Here You Are. Thank You., Jump/Skip; vẫn cần kiểm tra và cắt.
- Batch2: hai trang CD2_07 và08 đang vẽ6 con chim trong ô plural birds, trong khi nguồn có5. Sửa thành đúng5 chim trên dây ở cả hai trang; giữ badge6 vì đó là mã nhóm. Trang09 có2 mèo,3 chó,5 chim; kiểm tra lại sau sửa.
- Còn thiếu10 trang CD2_10–19. configure_unit5.py đã chuẩn bị lesson_specs và reference crops cho đủ18 trang. Đọc các spec và đối chiếu PDF, dùng các nhóm10–13,14–17,18–19 hoặc nhóm tương đương không làm lại các trang đã có.

Các lượng nguồn phải giữ:
- CD2_07/08: ô1dog có1 chó; ô2dogs có3 chó; ô3cat có1 mèo; ô4cats có2 mèo; ô5bird có1 chim; ô6birds có5 chim. Badge là mã nhóm.
- CD2_09:2 mèo,3 chó,5 chim; câu Let's count the cats. /1 cat,2 cats.
- CD2_10:2 chim,3 chó,2 mèo, nhóm cuối làcats.
- CD2_11/12:1cow,3cows,1rabbit,6rabbits,1duck,4ducks. Header3ducks là ví dụ nhỏ riêng, không đổi đàn vịt chính thành3.
- CD2_13/14: nhóm1 gồm8 bò; nhóm4 có1 bò riêng; nhóm2 có1 vịt trên bờ, nhóm3 có6 vịt trong ao; nhóm5 có3 thỏ chạy, nhóm6 có1 thỏ ngồi. Câu How many cows? /8 cows.
- CD2_15:2 vịt,3 bò,5 thỏ,7 chó,10 chim theo nguồn; nhóm chim cuối. Không tự thêm lời hát không có trong PDF.
- CD2_17: Mm moon, Nn nest, Oo octopus, Pp peach; giữ Find the letters.
- CD2_18:3 đầu tàu với toa đi kèm,1 bóng,6 gấu,9yo-yo. Không đếm toa thành đầu tàu.
- CD2_19:8 ô tô,10 thẻ chữ nhật xanh,4 dây nhảy,2 thỏ,5 bóng,1 xe đạp; câu How many cars? /8 cars.

Sửa đúng số ít/số nhiều, số lượng và chữ; không đánh dấu reviewed chỉ vì ảnh nhìn đẹp.

Quy trình bắt buộc:
1. Đọc skill imagegen; dùng built-in image_gen cho mọi lần sinh/sửa minh họa. KHÔNG dùng fallback CLI/API, không thay bằng ảnh gốc, screenshot PDF, SVG hay placeholder để tuyên bố regenerate xong. Nếu built-in không khả dụng, ghi đúng phần chưa làm, không âm thầm chuyển cách sinh.
2. Đọc trực quan PDF/reference trước khi đưa vào image_gen. Giữ đầy đủ từ vựng, câu thoại, lời hát IN TRONG NGUỒN, số, lượng, màu, tên, chỗ trống và người nói. Không thêm lời hát chưa có nguồn. Chỗ trống của bài gốc không điền đáp án. Các nhãn font cần độ chính xác có thể ghép bằng font như Unit1.
3. Gom khoảng4 trang trong một ảnh ghép2x2, yêu cầu ô độc lập, gutter thẳng, title và track rõ; nhóm cuối có thể2/3/1 trang. Prompt từng ô độc lập, không trộn nội dung giữa các track. Giữ phong cách textbook cartoon sáng, nét rõ, soft shading theo Unit1/2/3.
4. Lưu prompt, đường dẫn reference, danh sách track, tool và kết quả vào assets/batches/batchN.json; lưu ảnh batchN.png từ kết quả built-in vào workspace. Không print base64. File job phải có ít nhất tracks (mảng mã), prompt, refs và tool. Khi sửa ghi log riêng, kiểm tra ảnh hiện tại để tránh làm lại việc đã sửa.
5. Xem kết quả, đối chiếu đầy đủ nội dung và chữ/đồ vật; sửa lỗi bằng built-in rồi xem lại. Với bài đếm, đếm từng vật thực tế, phân biệt badge nhóm với số lượng. Với chữ cái, kiểm đủ glyph. Validation file kỹ thuật không chứng minh nội dung tranh đúng.
6. Cắt RIÊNG từng trang theo đường chia thực tế, không mặc định luôn đúng giữa ảnh. Xuất tất cả PNG/WebP canvas **1200×1200**, contain giữ tỷ lệ, không kéo méo/cắt mất chữ hoặc vật. Kiểm tra bản sau cắt và cả contact sheet.

Các lệnh dùng chung (chạy ở E:\let-go-series; có thể dùng python hệ thống cho Pillow):
```powershell
python build_lesson_unit.py --unit 5 --import-batch batchN --note "Ghi rõ nội dung đã kiểm tra" --render
# Nếu đường chia lệch, thêm --split-x X --split-y Y theo pixel thực tế.
python build_lesson_unit.py --unit 5 --render --export
python complete_unit_docs.py --unit 5
```
Đọc script trước khi dùng. Import chỉ gọi sau khi đã kiểm tra batch; --note phải trung thực. Job2 trang được cắt trái/phải; job3/4 trang dùng2x2; job1 trang dùng toàn ảnh. Nếu tổ chức khác, dùng helper riêng và ghi box vào manifest. Các script dùng chung là read-only, không sửa để giảm yêu cầu hoặc bỏ check.

PDF runtime sẵn có nếu cần:
`C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` có pypdf/pdfplumber/Pillow; pdftoppm có trong PATH. Không cần cài dịch vụ tạo ảnh.

Hoàn thiện tài liệu:
- Metadata nối track→ảnh WebP→audio→question; giữ đáp án và bài trắc nghiệm khỏi ảnh học, hiện sau nghe.
- File câu hỏi bên ngoài phải link file ảnh/audio mới tồn tại, không phụ thuộc ZIP mapping cũ.
- File Challenge giữ nội dung người dùng đã sửa, thêm link bộ chuẩn và checklist audio clip cần bổ sung. Chủ dự án tự bổ sung audio; KHÔNG tự tạo audio hay đánh dấu đã có. Rà checklist tự động từ complete_unit_docs.py để bổ sung những câu nghe bị bỏ sót, phân biệt bắt buộc/tùy chọn và các clip dùng chung. Bỏ khẳng định coverage100% nếu chưa chứng minh.
- README ghi rõ ảnh chuẩn ở pages/webp, PNG tương ứng, điều chỉnh so với nguồn, giới hạn audio chưa nghe độc lập. Không báo đã nghe/transcribe nếu mới so sánh file.

Cổng hoàn tất:
- 18/18 track có đúng ảnh PNG +WebP1200×1200, file audio khớp nguồn,1 câu trắc nghiệm với đáp án hợp lệ.
- Xem lại MỌI ảnh sau cắt, đối chiếu PDF, số lượng/màu/nhãn/câu thoại/glyph đúng, không lỗi gutter/cắt chữ.
- Preview, metadata, questions.md, README, validation.json và ZIP có đủ nội dung; mọi link tồn tại; PNG khớp manifest; ZIP kiểm tra mở được.
- Hai file Markdown ngoài thư mục đã cập nhật, không thay mất bài luyện cũ. Giữ nguồn đối chiếu và asset cần dựng; xóa file sửa bỏ/preview cũ chỉ trong phạm vi Unit mình khi không còn tham chiếu.

Cuối cùng báo số trang hoàn thiện, đường dẫn preview/ZIP, checks đã chạy và hạn chế thực tế. Nếu còn thiếu, nêu rõ track/lỗi cụ thể; không gọi Unit hoàn thiện chỉ vì export pass. Không cần chờ lại người dùng cho các bước đã được phép trong prompt này.
