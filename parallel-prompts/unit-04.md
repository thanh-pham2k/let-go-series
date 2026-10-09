Hoàn thiện RIÊNG Unit 4 – Numbers trong repo E:\let-go-series. Đây là một phần của công việc Unit2–8 đang chạy song song; hãy làm đến khi Unit này hoàn thiện và kiểm tra được, không chỉ lập kế hoạch.

Phạm vi ghi file của bạn:
- E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages
- E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Cau hoi theo trang.md
- E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers(2).md
- ZIP Unit_4_Numbers_regenerated.zip trong E:\let-go-series\Let_s Go Begin\Units.

Không sửa Unit khác, không chạy prepare_lesson_units.py hoặc script cấu hình Unit khác. Không sửa các script dùng chung ở root (build_lesson_unit.py, complete_unit_docs.py, prepare_lesson_units.py) hoặc render.py của Unit1. Nếu cần helper mới, đặt trong thư mục Unit của bạn. Không cập nhật remaining-units-progress.json toàn cục, không commit/push. Các chat khác có thể sửa file ngoài phạm vi; không hoàn tác thay đổi của chúng.

Nguồn và bộ mẫu:
- PDF chuẩn: E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers.pdf.
- Manifest/mapping hiện có: E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Lesson Pages\manifest.json. Đọc trạng thái thực tế trước khi làm, vì file có thể đã tiến thêm sau khi prompt này được viết.
- E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers - Cau hoi theo trang.md và E:\let-go-series\Let_s Go Begin\Units\Unit 4 - Numbers(2).md: câu hỏi theo track và bài luyện thêm.
- Mapping tổng chỉ đọc: E:\let-go-series\Let_s Go Begin\lets_go_audio_mapping.metadata.
- Mẫu đã hoàn thiện để tham khảo chỉ đọc: Unit2 – Colors – Lesson Pages và Unit3 – Shapes – Lesson Pages (preview.html, manifest.json, validation.json).
- Yêu cầu chính xác: đủ **16 trang cho CD1_55–CD1_70**, mỗi trang có hình và chữ bài học, audio đúng track, đúng1 câu trắc nghiệm riêng trong metadata.

Trạng thái đã kiểm tra:
- Đã sinh batch1–batch4.png trong assets/batches, tương ứng đủ16 trang dạng ảnh ghép. Chỉ CD1_55–58 đã nhập vào manifest và xuất pages/png + pages/webp. Không tạo lại batch1 nếu kiểm tra không phát hiện lỗi.
- Bản sửa batch2.png hiện có đủ5 yo-yo ở CD1_61 và đủ5 bóng tổng cộng ở CD1_62 (1 bé trái cầm +3 trên sàn +1 bé phải cầm phía sau). Phải đếm xác nhận lại, không suy ra từ tên file hay batch2-repair.json.
- Bản sửa batch3.png, CD1_66: hiện có7 táo, nhưng đàn mèo nhìn thấy8 con (2+3+3), dây tường5 trái tim. Cần sửa thành9 mèo (3x3),6 trái tim; giữ8 chó,5 sao,7 táo và lời đáp7. Đếm lại toàn bộ sau mỗi sửa.
- Batch4.png đã sinh nhưng chưa nhập/xuất/chốt. Kiểm tra5 trái tim,7 sao,10 hình thoi; đủ26 cặp chữ ở CD1_68, Ii/Jj/Kk/Ll và hoạt động Find the letters ở69. CD1_70 giữ hai hội thoại: Is it a5? / Yes, it is. và Is it a9? / No, it isn't. It's a6.; không nhầm6/9; giữ Find the numbers.
- configure_unit4.py đã tạo lesson_specs và reference crops. Đọc chúng, nhưng PDF là chuẩn khi có mâu thuẫn.

Các lượng cần kiểm tra:
- CD1_60/61:1 bóng,2 búp bê,3 ô tô,4 gấu bông,5 yo-yo.
- CD1_62:5 bóng tổng cộng,2 búp bê,4 yo-yo,3 xe đạp,1 đoàn tàu. Badge xanh1–5 là mã nhóm, không phải số lượng.
- CD1_64/65:6 tam giác,7 sao,8 hình tròn,9 trái tim,10 hình vuông.
- CD1_66:7 táo,8 chó,9 mèo,6 trái tim,5 sao; badge1–5 là mã nhóm.
- CD1_67:5 trái tim,7 sao,10 hình thoi.

Hoàn thiện bằng cách sửa batch3 hoặc riêng trang66 với image_gen, kiểm tra batch2/batch4 rồi nhập những batch đạt. Không đánh dấu reviewed cho ảnh sai hoặc chỉ dựa vào validation file cũ.

Quy trình bắt buộc:
1. Đọc skill imagegen; dùng built-in image_gen cho mọi lần sinh/sửa minh họa. KHÔNG dùng fallback CLI/API, không thay bằng ảnh gốc, screenshot PDF, SVG hay placeholder để tuyên bố regenerate xong. Nếu built-in không khả dụng, ghi đúng phần chưa làm, không âm thầm chuyển cách sinh.
2. Đọc trực quan PDF/reference trước khi đưa vào image_gen. Giữ đầy đủ từ vựng, câu thoại, lời hát IN TRONG NGUỒN, số, lượng, màu, tên, chỗ trống và người nói. Không thêm lời hát chưa có nguồn. Chỗ trống của bài gốc không điền đáp án. Các nhãn font cần độ chính xác có thể ghép bằng font như Unit1.
3. Gom khoảng4 trang trong một ảnh ghép2x2, yêu cầu ô độc lập, gutter thẳng, title và track rõ; nhóm cuối có thể2/3/1 trang. Prompt từng ô độc lập, không trộn nội dung giữa các track. Giữ phong cách textbook cartoon sáng, nét rõ, soft shading theo Unit1/2/3.
4. Lưu prompt, đường dẫn reference, danh sách track, tool và kết quả vào assets/batches/batchN.json; lưu ảnh batchN.png từ kết quả built-in vào workspace. Không print base64. File job phải có ít nhất tracks (mảng mã), prompt, refs và tool. Khi sửa ghi log riêng, kiểm tra ảnh hiện tại để tránh làm lại việc đã sửa.
5. Xem kết quả, đối chiếu đầy đủ nội dung và chữ/đồ vật; sửa lỗi bằng built-in rồi xem lại. Với bài đếm, đếm từng vật thực tế, phân biệt badge nhóm với số lượng. Với chữ cái, kiểm đủ glyph. Validation file kỹ thuật không chứng minh nội dung tranh đúng.
6. Cắt RIÊNG từng trang theo đường chia thực tế, không mặc định luôn đúng giữa ảnh. Xuất tất cả PNG/WebP canvas **1200×1200**, contain giữ tỷ lệ, không kéo méo/cắt mất chữ hoặc vật. Kiểm tra bản sau cắt và cả contact sheet.

Các lệnh dùng chung (chạy ở E:\let-go-series; có thể dùng python hệ thống cho Pillow):
```powershell
python build_lesson_unit.py --unit 4 --import-batch batchN --note "Ghi rõ nội dung đã kiểm tra" --render
# Nếu đường chia lệch, thêm --split-x X --split-y Y theo pixel thực tế.
python build_lesson_unit.py --unit 4 --render --export
python complete_unit_docs.py --unit 4
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
- 16/16 track có đúng ảnh PNG +WebP1200×1200, file audio khớp nguồn,1 câu trắc nghiệm với đáp án hợp lệ.
- Xem lại MỌI ảnh sau cắt, đối chiếu PDF, số lượng/màu/nhãn/câu thoại/glyph đúng, không lỗi gutter/cắt chữ.
- Preview, metadata, questions.md, README, validation.json và ZIP có đủ nội dung; mọi link tồn tại; PNG khớp manifest; ZIP kiểm tra mở được.
- Hai file Markdown ngoài thư mục đã cập nhật, không thay mất bài luyện cũ. Giữ nguồn đối chiếu và asset cần dựng; xóa file sửa bỏ/preview cũ chỉ trong phạm vi Unit mình khi không còn tham chiếu.

Cuối cùng báo số trang hoàn thiện, đường dẫn preview/ZIP, checks đã chạy và hạn chế thực tế. Nếu còn thiếu, nêu rõ track/lỗi cụ thể; không gọi Unit hoàn thiện chỉ vì export pass. Không cần chờ lại người dùng cho các bước đã được phép trong prompt này.
