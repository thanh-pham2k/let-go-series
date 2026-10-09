# Review 3–4: Bộ bài học chuẩn

Đủ2 mục CD1_71 và CD1_72, adapt toàn bộ2 trang PDF36–37. Minh họa regenerate bằng built-in image_gen, theo batch2 ô rồi cắt theo gutter thực tế; ảnh chuẩn pages/webp và PNG tương ứng pages/png đều1200×1200, contain giữ tỷ lệ.

- [Preview nghe và làm bài](preview.html)
- [Contact sheet](preview.jpg)
- [Metadata](review.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Validation](validation.json)
- [Generation log và prompt](generation.json)
- [PDF đối chiếu](references/source.pdf)

CD1_71 giữ nguyên6 cặp a/b: circle/square; star/heart;4 tam giác/5 hình tròn;6 hình thoi/7 oval;walk/run;go/stop. Các số trong hình3 là nhãn từng vật, đã đối chiếu số lượng thực tế. Square có cạnh bằng nhau; oval có chiều ngang dài hơn chiều cao. Bài circle chưa chọn đáp án; chưa suy ra đáp án bài nghe gốc.

CD1_72 giữ4 lệnh và nghĩa lấy/cất, mở/đóng, màu quần áo/đồ dùng. Câu Please take out your pencil. và tranh giáo viên ở cuối trang được giữ cùng ảnh72; không có marker audio riêng, không bịa thêm track hoặc khẳng định câu đó được đọc trong MP3.

Bố cục được giãn để đọc/đếm rõ; typography và phong cách được vẽ lại. Không thêm lời hát, không tô đáp án bài gốc, câu trắc nghiệm bổ sung và đáp án nằm riêng trong metadata. Trắc nghiệm hiện khi audio kết thúc hoặc bấm Ôn tập; phản hồi sau chọn.

Audio copy đúng từng byte từ CD1 Track71/72.mp3. Chưa nghe/transcribe độc lập. Clip Challenge riêng chưa có, chủ dự án tự bổ sung theo checklist ở Markdown ngoài thư mục. Challenge cũ được giữ; không phát hiện mâu thuẫn nội dung cần thay đổi sau đối chiếu PDF. Bỏ khẳng định coverage tuyệt đối để phân biệt việc đối chiếu nội dung với kiểm chứng audio.

## Bằng chứng kiểm tra preview

[Kiểm tra Edge headless](browser-validation.json), [kiểm tra JavaScript](preview-validation.json) và [tài nguyên HTTP](http-validation.json) ghi kết quả. Hai ảnh chụp preview-browser-1.png/2.png đã được xem trực quan: không cắt chữ hay hình. Edge tải cả2 ảnh và giải mã metadata MP3 với thời lượng62.906667s/66.8s; chọn/chuyển bài, câu hỏi ban đầu ẩn, sự kiện ended và nút Ôn tập hiện câu hỏi, phản hồi đúng/sai đều pass. Sự kiện ended được mô phỏng để kiểm UI; chưa nghe/transcribe lời audio độc lập. Công cụ trình duyệt tích hợp lỗi khởi tạo, nên kiểm bằng Edge headless riêng. Profile kiểm thử .browser-check được giữ cục bộ và loại khỏi ZIP.

references/source-pages giữ ảnh nguồn chỉ để đối chiếu; assets giữ minh họa dựng lại; assets/batches giữ prompt/tool/reference/source-output. Không dùng ảnh nguồn làm ảnh học. build_review.py là helper riêng, không sửa script Unit chung. Chạy lại: python build_review.py --render --export (giữ dấu kiểm trực quan đã ghi trong manifest).

<!-- five-challenge-guide -->
## Bài luyện theo5 Challenge

[Hướng dẫn/bài luyện/đáp án/audio notes](challenge-guide.md) · [Nội dung câu luyện có mã](challenge-content.json).

Chuẩn hóa Recognition → Listen & Understand → Recall → Build & Match → Final Boss. Dịch nghĩa là phụ lục hỗ trợ. Kho câu luyện bổ sung riêng với câu trắc nghiệm theo track; preview hiện tại vẫn phục vụ trang học chính, chưa có giao diện chạy toàn bộ Challenge.
