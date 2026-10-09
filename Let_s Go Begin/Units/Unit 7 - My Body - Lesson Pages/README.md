# Unit 7 – My Body: Bộ bài học chuẩn

Đủ 17 ảnh + audio + câu trắc nghiệm. Ảnh PNG/WebP đều **1200 × 1200**, giữ tỷ lệ minh họa và chữ. Regenerate bằng **image_gen tích hợp**, theo nhóm nhiều trang rồi cắt riêng; không dùng fallback.

- [Preview học và làm bài](preview.html)
- [Xem cả bộ](preview.jpg)
- [Metadata tích hợp](unit.regenerated.metadata)
- [Câu hỏi](questions.md)
- [Báo cáo kiểm tra](validation.json)

Ảnh chuẩn dùng cho app: pages/webp. Bản PNG tương ứng: pages/png. assets giữ lớp ảnh phục vụ dựng lại; references và source-pages giữ nguồn PDF đối chiếu. assets/batches lưu prompt, ảnh ghép và đánh giá từng batch; không dùng ảnh ghép làm trang học.

Giữ chữ bài học, số chỉ hình, câu thoại và chỗ trống; câu trắc nghiệm nằm riêng. Các mục chỉ có tiêu đề được bổ sung bằng nội dung của mục cùng trang. Nên hỗ trợ phóng to để đọc lời bài hát trên điện thoại.

Audio khớp file CD nguồn, chưa nghe/transcribe độc lập. Tài liệu Challenge luyện thêm có checklist audio riêng do chủ dự án tự bổ sung.

Dựng lại từ thư mục gốc repo: python build_lesson_unit.py --unit 7 --render --export

## Điều chỉnh có nguồn đối chiếu

- CD2_41: Source E is title-only. Adapt stamping feet and clapping hands from source D on same PDF page 2.
- CD2_43: Source B is title-only. Reuse four numbered body cards and header model from A on PDF page 3.
- CD2_45: No chant lyrics printed in PDF. Retain four body-part illustrations; labels are vocabulary support from preceding page, not a transcription.
- CD2_47: Source B is title-only. Reuse four numbered face-part cards and header model dialogue from A on PDF page 5.
- CD2_49: No song lyrics printed in PDF. Retain nose/shoulders/toes/knees actions; supplementary ears practice inset comes from C on same page, not from invented lyrics.
- CD2_50: Complete 26 upper/lowercase pairs reformatted into columns; Uu/Vv/Ww highlighted.
- CD2_51: Include untracked C. Find the letters as supporting activity on same lesson page; preserve Uu Vv Ww glyphs without marking answers.

Đã xem từng PNG sau cắt và contact sheet; kiểm tra từ, nhãn, số thứ tự, vị trí chạm và câu thoại với 8 trang PDF nguồn. Mặt đồng hồ là minh họa cho watch, không phải bài đọc giờ. references/lesson-crops giữ vùng bài học đã chọn; lesson_specs.json và manifest lưu đặc tả. Bản thu Challenge cần bổ sung, xem bảng bắt buộc/tùy chọn ở tài liệu bên ngoài.

- [Challenge và checklist audio](challenge.md) (bản đóng gói giữ nguyên bài luyện).

Sau lệnh export dùng chung, chạy complete_unit_docs.py --unit 7 rồi finish_unit7.py trong thư mục Unit này, check_preview.cjs bằng node và pack_unit7.py để giữ các ghi chú, kiểm tra preview và đóng gói tài liệu cập nhật.
