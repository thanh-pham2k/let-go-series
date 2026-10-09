Hoàn thiện RIÊNG Review 1-2 của Let's Go Begin tại E:\let-go-series, theo bộ ảnh Unit1/2/3 đã regenerate. Công việc này chạy song song với các Review và Unit khác. Hãy thực hiện đến khi có bộ Review hoàn chỉnh, không dừng ở kế hoạch.

## Phạm vi file riêng

Bạn được tạo/sửa:
- E:\let-go-series\Let_s Go Begin\Units\Review 1-2 - Lesson Pages (tạo thư mục nếu chưa có).
- E:\let-go-series\Let_s Go Begin\Units\Review 1-2(3).md (giữ bài luyện người dùng đã có, cập nhật liên kết/trạng thái/audio notes).
- E:\let-go-series\Let_s Go Begin\Units\Review 1-2 - Cau hoi theo trang.md (tạo nếu chưa có).
- E:\let-go-series\Let_s Go Begin\Units\Review_1-2_regenerated.zip.

Chỉ ghi trong phạm vi này. Không sửa Unit1–8, Review khác hoặc scripts/root/progress file dùng chung. Không chạy prepare_lesson_units.py; không gọi build_lesson_unit.py/complete_unit_docs.py cho Review vì hai script hiện chỉ hỗ trợ Unit số nguyên. Nếu cần helper, đặt riêng trong thư mục Review của bạn. Không commit/push, không hoàn tác thay đổi của chat khác, không tạo thêm chat/agent.

## Nguồn chuẩn và mapping

- PDF chuẩn: E:\let-go-series\Let_s Go Begin\Units\Review 1-2.pdf.
- Bài luyện có sẵn: E:\let-go-series\Let_s Go Begin\Units\Review 1-2(3).md.
- Mapping chỉ đọc: E:\let-go-series\Let_s Go Begin\lets_go_audio_mapping.metadata. Lọc source_pdf đúng Review 1-2.pdf, không lấy toàn bộ track của Unit liền kề.
- Bộ mẫu chỉ đọc: E:\let-go-series\Let_s Go Begin\Units\Unit 2 - Colors - Lesson Pages và Unit 3 - Shapes - Lesson Pages; tham khảo preview.html, manifest.json, metadata, questions.md, validation.json.
- MP3 nguồn: E:\let-go-series\Let_s Go Begin\Oxford - Let_s Go Begin Student_s Book 3rd Edition CD1 hoặc CD2, tên TrackNN.mp3 theo mã tương ứng. Tất cả track dưới đây đã xác nhận có file, nhưng phải kiểm tra lại và so sánh bản copy.

Review này có **2 mục theo audio**:
- CD1_36: PDF trang1, trang sách18, Listen and circle.
- CD1_37: PDF trang2, trang sách19, Say these.

Đọc đầy đủ hai trang PDF. Cả Listen and Review lẫn Let's Learn About đều thuộc phạm vi, kể cả hoạt động cùng trang không có marker audio riêng. Không chia mỗi cặp lựa chọn của Listen and circle thành track mới. Hoạt động không có audio riêng giữ trong ảnh/tài liệu phụ phù hợp, ghi rõ dùng chung hay không có audio, không bịa track.

Ôn đồ chơi, màu sắc và động tác của Unit1–2; trang Let's Learn About có School Supplies. Đọc và giữ đúng từng đồ dùng học tập và từ/câu trong PDF. Không chỉ dùng lại ảnh Toys/Colors rồi bỏ trang School Supplies. Kiểm tra màu, tên đồ vật, vị trí/số các lựa chọn của Listen and circle. Đồ dùng học tập bổ sung có thể cần audio clip riêng cho Challenge, ghi checklist để chủ dự án tự cung cấp.

## Yêu cầu thực hiện

1. Đọc skill imagegen và PDF. Render/đọc trực quan nguồn trước khi tạo prompt. Không chỉ suy diễn từ Markdown hoặc tên bài. Khi PDF và bài luyện mâu thuẫn, PDF là nguồn đối chiếu; sửa điểm sai trong bài luyện và ghi rõ thay đổi thực tế.
2. Dùng **built-in image_gen**, KHÔNG fallback CLI/API, không dùng ảnh sách gốc/screenshot/SVG/placeholder để thay cho ảnh regenerate. Nếu tool không khả dụng, ghi phần chưa làm và lý do; không chuyển fallback. Giữ phong cách textbook cartoon sáng, nét rõ, soft shading tương ứng Unit1–3.
3. Gom nhiều ảnh/mục vào cùng một batch: Review2 mục dùng2 ô trái/phải; Review3 mục có thể2x2 với ô cuối trống. Prompt xác định rõ title, track và nội dung từng ô, không trộn. Yêu cầu gutter thẳng và ô độc lập. Giữ đầy đủ chữ bài học, từ, câu, lời hát in trong nguồn, số/màu/đồ vật và thứ tự lựa chọn. Chỗ cần circle/điền vẫn để trống, không tô đáp án. Không in câu trắc nghiệm bổ sung lên ảnh học.
4. Giữ nguyên số các lựa chọn và ý nghĩa mỗi cặp trên trang Listen and circle. Không suy ra đáp án bài nghe gốc từ ảnh hay đặt đáp án khi chưa nghe. Câu trắc nghiệm bổ sung có thể hỏi nhận biết rõ trong hình/mẫu câu; phải có đúng1 câu với đáp án xác định cho mỗi mục audio. Không yêu cầu nhớ thứ tự xuất hiện trong MP3 nếu chưa kiểm chứng lời nói.
5. Lưu ảnh sinh từ built-in vào workspace. Tạo references/source-pages để đối chiếu, assets/batches để lưu batch và prompt/reference/track/tool/source-output. Không print base64. Sau sinh xem kỹ tất cả chữ, vật, số lượng, ngữ nghĩa; sửa bằng built-in khi cần và xem lại. Ghép lớp chữ bằng font khi cần độ chính xác như Unit1, không thay minh họa bằng đồ họa lập trình.
6. Cắt theo ranh giới ô THỰC TẾ, không mặc định luôn đúng giữa. Mỗi mục audio có một PNG và một WebP riêng, tất cả canvas **1200×1200**; contain giữ tỷ lệ, không kéo méo, không cắt chữ/vật. Đối chiếu mọi ảnh sau cắt với nguồn, kiểm contact sheet.
7. Copy MP3 nguồn vào audio/ của Review và kiểm tra từng byte; không tự tạo/đổi audio. Người dùng sẽ tự bổ sung các clip Challenge riêng. Không báo đã nghe/transcribe độc lập nếu mới kiểm file.

## Bộ đầu ra

- pages/png/TRACK.png và pages/webp/TRACK.webp: đủ2 mục, tất cả1200×1200.
- audio/TrackNN.mp3, đúngCD nguồn.
- manifest.json: track, exercise, PDF page/book page, source/reference, output path, canvas, lớp ảnh/chữ cần dựng, question(id/prompt/choices/correct_choice_id/show_after_audio=true/render_in_lesson_image=false), adaptation_notes.
- review.regenerated.metadata: nối track→image→audio_file→question, đường dẫn tương đối và kích thước thực.
- preview.html: chọn mục, xem ảnh/chữ, nghe audio, hiện một câu trắc nghiệm sau khi audio kết thúc hoặc bấm ôn tập; đáp án phản hồi sau lựa chọn. Dùng template Unit2/3 làm mẫu nhưng copy riêng, không sửa bộ mẫu.
- preview.jpg, questions.md, README.md, generation.json và validation.json; ghi bằng chứng kiểm tra và hạn chế thực tế, không tự ghi reviewed/pass trước khi kiểm.
- Review 1-2 - Cau hoi theo trang.md: link ảnh/audio/metadata mới thực sự tồn tại, đủ2 câu và bảng đáp án; không phụ thuộc ZIP mapping cũ.
- Review 1-2(3).md: giữ bài luyện cũ, sửa lỗi đã chứng minh, thêm link bộ chuẩn; checklist các audio clip riêng cần bổ sung, tên file gợi ý/câu cần đọc và nội dung dùng chung. Người dùng tự thu, chưa có thì để chưa hoàn thành. Phân biệt cần thiết/tùy chọn. Không khẳng định coverage100% nếu chưa đối chiếu đủ.
- Review_1-2_regenerated.zip: gói bộ Review, metadata/ảnh/audio/preview/tài liệu; kiểm ZIP mở được và file nội bộ đủ.

Nếu nội dung mới của Let's Learn About chưa có asset Unit tương ứng, phải regenerate riêng theo nguồn, không bỏ hoặc đổi sang nội dung Unit cũ. Có thể tham khảo style của Unit đã có, nhưng không phụ thuộc vào file tạm của chat Unit đang chạy.

Runtime PDF sẵn có: C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe có pypdf/pdfplumber/Pillow, pdftoppm trong PATH. Python hệ thống có Pillow. Helper riêng của bạn có thể render/cắt/contain/export/validate, không sửa scripts dùng chung.

## Cổng hoàn tất

Chỉ báo hoàn thiện khi đủ2/2 mục audio và nguồn cả2 trang được adapt: mọi ảnh đã kiểm trực quan sau cắt; chữ, câu, số, lượng, thứ tự lựa chọn đúng; đủ1 câu trắc nghiệm mỗi audio với đáp án hợp lệ; PNG/WebP1200×1200; audio copy khớp nguồn; metadata/link/preview hoạt động; ZIP hợp lệ; hai file Markdown ngoài thư mục đã cập nhật và audio notes trung thực. Các check kỹ thuật không thay việc đối chiếu nội dung.

Cuối cùng báo số mục hoàn thiện, đường dẫn preview/ZIP, kiểm tra đã chạy và hạn chế còn lại. Không xin xác nhận lại cho những bước đã được phép. Nếu thiếu, nêu rõ track/nội dung/lỗi; không gọi Review hoàn chỉnh chỉ vì script export pass.
