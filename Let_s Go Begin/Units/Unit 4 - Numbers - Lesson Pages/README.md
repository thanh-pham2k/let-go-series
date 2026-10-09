# Unit 4 – Numbers: Bộ bài học chuẩn

Đủ 16 ảnh + audio + câu trắc nghiệm. Ảnh PNG/WebP đều **1200 × 1200**, giữ tỷ lệ minh họa và chữ. Regenerate bằng **image_gen tích hợp**, theo nhóm nhiều trang rồi cắt riêng; không dùng fallback.

- [Preview học và làm bài](preview.html)
- [Xem cả bộ](preview.jpg)
- [Metadata tích hợp](unit.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Báo cáo kiểm tra](validation.json)

Ảnh chuẩn dùng cho app: pages/webp. Bản PNG tương ứng: pages/png. assets giữ lớp ảnh phục vụ dựng lại; references và source-pages giữ nguồn PDF đối chiếu. assets/batches lưu prompt, ảnh ghép và đánh giá từng batch; không dùng ảnh ghép làm trang học.

Giữ chữ bài học, số chỉ hình, câu thoại và chỗ trống; câu trắc nghiệm nằm riêng. Các mục chỉ có tiêu đề được bổ sung bằng nội dung của mục cùng trang. Nên hỗ trợ phóng to để đọc lời bài hát trên điện thoại.

Audio khớp file CD nguồn, chưa nghe/transcribe độc lập. Tài liệu Challenge luyện thêm có checklist audio riêng do chủ dự án tự bổ sung.

Dựng lại từ thư mục gốc repo: python build_lesson_unit.py --unit 4 --render --export

Điều chỉnh đối chiếu nguồn: CD1_60 khôi phục mẫu “Let's count. 1, 2, 3.” bằng lớp font; CD1_63 thêm từ one–five; CD1_67 thêm nhãn five/seven/ten và sửa đáp án thành 5. CD1_66 bố trí lại nhóm 9 mèo, 8 chó, 7 táo, 6 trái tim, 5 sao để đếm rõ; CD1_70 bố trí mười bóng thành hai hàng, giữ đúng mã nhóm/số và hai hội thoại, thêm nhãn CD1 70 bằng font. Không thêm lời bài hát.

Đã xem riêng cả 16 PNG sau cắt và contact sheet, đối chiếu source-pages/reference từ PDF; kiểm số lượng, màu nhóm hình, glyph và chữ.
