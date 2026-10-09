Hoàn thiện RIÊNG Unit 6 – Food trong repo E:\let-go-series. Đây là một phần của công việc Unit2–8 đang chạy song song; hãy làm đến khi Unit này hoàn thiện và kiểm tra được, không chỉ lập kế hoạch.

Phạm vi ghi file của bạn:
- E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Lesson Pages
- E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Cau hoi theo trang.md
- E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food(2).md
- ZIP Unit_6_Food_regenerated.zip trong E:\let-go-series\Let_s Go Begin\Units.

Không sửa Unit khác, không chạy prepare_lesson_units.py hoặc script cấu hình Unit khác. Không sửa các script dùng chung ở root (build_lesson_unit.py, complete_unit_docs.py, prepare_lesson_units.py) hoặc render.py của Unit1. Nếu cần helper mới, đặt trong thư mục Unit của bạn. Không cập nhật remaining-units-progress.json toàn cục, không commit/push. Các chat khác có thể sửa file ngoài phạm vi; không hoàn tác thay đổi của chúng.

Nguồn và bộ mẫu:
- PDF chuẩn: E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food.pdf.
- Manifest/mapping hiện có: E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Lesson Pages\manifest.json. Đọc trạng thái thực tế trước khi làm, vì file có thể đã tiến thêm sau khi prompt này được viết.
- E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food - Cau hoi theo trang.md và E:\let-go-series\Let_s Go Begin\Units\Unit 6 - Food(2).md: câu hỏi theo track và bài luyện thêm.
- Mapping tổng chỉ đọc: E:\let-go-series\Let_s Go Begin\lets_go_audio_mapping.metadata.
- Mẫu đã hoàn thiện để tham khảo chỉ đọc: Unit2 – Colors – Lesson Pages và Unit3 – Shapes – Lesson Pages (preview.html, manifest.json, validation.json).
- Yêu cầu chính xác: đủ **15 trang cho CD2_20–CD2_34**, mỗi trang có hình và chữ bài học, audio đúng track, đúng1 câu trắc nghiệm riêng trong metadata.

Trạng thái: chưa regenerate trang nào. Đã có manifest15 mục,8 trang PDF render trong source-pages, MP3 trong audio và reference đầy trang. Cần chọn/cắt riêng vùng bài học cho từng track, bổ sung lesson_specs rồi sinh toàn bộ15 trang theo nhóm khoảng4.

Lưu ý đặc biệt: PDF và file câu hỏi cũ ghi CD1_32 và CD1_34 cho hai mục trong Unit6. Mapping tổng và MP3 Unit6 dùng CD2_32/CD2_34. Manifest hiện chuẩn hóa CD2; giữ những mã này, ghi rõ nguồn nhãn sai trong README và file câu hỏi. Không chọn CD1/Track32 hoặc CD1/Track34. Chưa nghe xác nhận nội dung nên báo đúng giới hạn, không khẳng định đã nghe.

Đối chiếu nguồn cho How old are you?, tuổi nhân vật, câu trả lời số tuổi, các món ăn, I like/Do you like và Yes/No. Không đảo chủ thể thích/không thích hoặc làm sai thức ăn. Giữ hoạt động Find the letters và Play a game của trang cuối; một câu trắc nghiệm cho mỗi track, không bỏ bài không có audio phụ nếu nó nằm trong cùng trang hoạt động.

File câu hỏi cũ chỉ ghi15 mục, không ép số lượng thành17. Đọc đủ8 trang PDF để lập prompt giữ toàn bộ chữ và hình; không tạo dựa riêng vào mô tả câu trắc nghiệm.

Quy trình bắt buộc:
1. Đọc skill imagegen; dùng built-in image_gen cho mọi lần sinh/sửa minh họa. KHÔNG dùng fallback CLI/API, không thay bằng ảnh gốc, screenshot PDF, SVG hay placeholder để tuyên bố regenerate xong. Nếu built-in không khả dụng, ghi đúng phần chưa làm, không âm thầm chuyển cách sinh.
2. Đọc trực quan PDF/reference trước khi đưa vào image_gen. Giữ đầy đủ từ vựng, câu thoại, lời hát IN TRONG NGUỒN, số, lượng, màu, tên, chỗ trống và người nói. Không thêm lời hát chưa có nguồn. Chỗ trống của bài gốc không điền đáp án. Các nhãn font cần độ chính xác có thể ghép bằng font như Unit1.
3. Gom khoảng4 trang trong một ảnh ghép2x2, yêu cầu ô độc lập, gutter thẳng, title và track rõ; nhóm cuối có thể2/3/1 trang. Prompt từng ô độc lập, không trộn nội dung giữa các track. Giữ phong cách textbook cartoon sáng, nét rõ, soft shading theo Unit1/2/3.
4. Lưu prompt, đường dẫn reference, danh sách track, tool và kết quả vào assets/batches/batchN.json; lưu ảnh batchN.png từ kết quả built-in vào workspace. Không print base64. File job phải có ít nhất tracks (mảng mã), prompt, refs và tool. Khi sửa ghi log riêng, kiểm tra ảnh hiện tại để tránh làm lại việc đã sửa.
5. Xem kết quả, đối chiếu đầy đủ nội dung và chữ/đồ vật; sửa lỗi bằng built-in rồi xem lại. Với bài đếm, đếm từng vật thực tế, phân biệt badge nhóm với số lượng. Với chữ cái, kiểm đủ glyph. Validation file kỹ thuật không chứng minh nội dung tranh đúng.
6. Cắt RIÊNG từng trang theo đường chia thực tế, không mặc định luôn đúng giữa ảnh. Xuất tất cả PNG/WebP canvas **1200×1200**, contain giữ tỷ lệ, không kéo méo/cắt mất chữ hoặc vật. Kiểm tra bản sau cắt và cả contact sheet.

Các lệnh dùng chung (chạy ở E:\let-go-series; có thể dùng python hệ thống cho Pillow):
```powershell
python build_lesson_unit.py --unit 6 --import-batch batchN --note "Ghi rõ nội dung đã kiểm tra" --render
# Nếu đường chia lệch, thêm --split-x X --split-y Y theo pixel thực tế.
python build_lesson_unit.py --unit 6 --render --export
python complete_unit_docs.py --unit 6
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
- 15/15 track có đúng ảnh PNG +WebP1200×1200, file audio khớp nguồn,1 câu trắc nghiệm với đáp án hợp lệ.
- Xem lại MỌI ảnh sau cắt, đối chiếu PDF, số lượng/màu/nhãn/câu thoại/glyph đúng, không lỗi gutter/cắt chữ.
- Preview, metadata, questions.md, README, validation.json và ZIP có đủ nội dung; mọi link tồn tại; PNG khớp manifest; ZIP kiểm tra mở được.
- Hai file Markdown ngoài thư mục đã cập nhật, không thay mất bài luyện cũ. Giữ nguồn đối chiếu và asset cần dựng; xóa file sửa bỏ/preview cũ chỉ trong phạm vi Unit mình khi không còn tham chiếu.

Cuối cùng báo số trang hoàn thiện, đường dẫn preview/ZIP, checks đã chạy và hạn chế thực tế. Nếu còn thiếu, nêu rõ track/lỗi cụ thể; không gọi Unit hoàn thiện chỉ vì export pass. Không cần chờ lại người dùng cho các bước đã được phép trong prompt này.
