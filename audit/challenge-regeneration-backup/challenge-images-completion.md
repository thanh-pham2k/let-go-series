# Báo cáo hoàn thiện ảnh Challenge — Unit 1–8 và 4 Review

**Đã hoàn thiện bộ ảnh:** **211 ID bắt buộc = 211 WebP**, tất cả **512×512**, tổng **2.47 MiB**, file lớn nhất **51.6 KiB**. Không có ảnh vượt 60 KB hoặc ID bắt buộc còn thiếu.

[Mở trang tổng hợp 12 bộ](<E:/let-go-series/audit/challenge-preview.html>) · [Audit JSON](<E:/let-go-series/audit/challenge-images-completion.json>) · [Kiểm tra trình duyệt](<E:/let-go-series/audit/challenge-preview-browser-validation.json>)

| Bộ | Bắt buộc đạt | Có điều kiện | Crop | Ghép | Native | AI sinh/sửa | Lớn nhất KiB | Preview |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| unit-01 | 8/8 | 0 | 7 | 0 | 0 | 1 | 22.7 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 1 - Toys - Lesson Pages/challenge-assets/preview.html>) |
| unit-02 | 19/19 | 0 | 3 | 0 | 10 | 6 | 18.7 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 2 - Colors - Lesson Pages/challenge-assets/preview.html>) |
| unit-03 | 17/17 | 0 | 3 | 0 | 14 | 0 | 8.3 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 3 - Shapes - Lesson Pages/challenge-assets/preview.html>) |
| unit-04 | 18/18 | 0 | 2 | 3 | 11 | 2 | 18.3 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 4 - Numbers - Lesson Pages/challenge-assets/preview.html>) |
| unit-05 | 20/20 | 0 | 6 | 10 | 0 | 4 | 29.5 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 5 - Animals - Lesson Pages/challenge-assets/preview.html>) |
| unit-06 | 15/15 | 0 | 6 | 1 | 0 | 8 | 24.7 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 6 - Food - Lesson Pages/challenge-assets/preview.html>) |
| unit-07 | 15/15 | 0 | 5 | 0 | 1 | 9 | 24.4 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 7 - My Body - Lesson Pages/challenge-assets/preview.html>) |
| unit-08 | 17/17 | 0 | 0 | 0 | 0 | 17 | 51.6 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Unit 8 - Abilities - Lesson Pages/challenge-assets/preview.html>) |
| review-1-2 | 17/17 | 0 | 8 | 0 | 0 | 9 | 35.3 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Review 1-2 - Lesson Pages/challenge-assets/preview.html>) |
| review-3-4 | 27/27 | 0 | 8 | 0 | 19 | 0 | 21.8 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Review 3-4 - Lesson Pages/challenge-assets/preview.html>) |
| review-5-6 | 19/19 | 0 | 5 | 0 | 0 | 14 | 34.9 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Review 5-6 - Lesson Pages/challenge-assets/preview.html>) |
| review-7-8 | 19/19 | 0 | 0 | 0 | 7 | 12 | 16.3 | [Xem](<E:/let-go-series/Let_s Go Begin/Units/Review 7-8 - Lesson Pages/challenge-assets/preview.html>) |

Tổng cách tạo: crop **53**, ghép **14**, native **62**, AI sinh/sửa **82**. Các ảnh ghép có thể dùng master AI; không đếm chúng thêm lần nữa vào cột AI. Đây là số thẻ cuối, không phải số lần gọi tool. Các job nhỏ hơn8 được dùng khi chỉ còn ít hình cần sửa; batch/crop masters và prompt thực tế được giữ trong mỗi bộ.

## Kiểm tra đã thực hiện

- Root xem riêng từng **211 WebP sau cắt/nén**, đối chiếu vật, màu, lượng, anatomy và động tác; những bản sửa được xem lại và ràng buộc review với SHA256 file cuối.
- Đếm lại các nhóm hình/con vật/xe; sửa mảnh vật bên cạnh, mép nơ/giày/đuôi/tai/miệng ly, marker nhầm mouth/nose và cặp can/can’t. Không dùng kiểm tra file/hash thay cho việc xem tranh.
- 12 bộ có đủ manifest, mapping, preview, contact-sheet.jpg, README và validation. Mỗi ID chỉ có một WebP runtime; source/master/debug không được đưa thành ảnh luyện thừa.
- 364 câu Review khớp ID bài nguồn. Unit có đủ mapping section/visual occurrences; những adaptation được lưu trong output, không sửa bài gốc.
- Trình duyệt đã tải đủ12 preview, không ảnh hỏng; mỗi bộ có câu mẫu cho cả5 Challenge; tổng80 câu, bao phủ Challenge1–5. Câu hỏi, lựa chọn và ô điền nằm ngoài bitmap; mã ảnh mặc định ẩn, teacher details đóng. Radio/text input đã thử hoạt động.
- Pixel không đổi trong bước chuẩn hóa metadata; dimensions/bytes/SHA256 được đọc lại từ file thật. Prompt/crop/batch/generation provenance được lưu riêng.
- Git xác nhận chỉ các Challenge nguồn được sửa để gắn8 cue đã chốt; lesson images/audio không đổi. Không add/commit/push. Bốn file Challenge Markdown được bổ sung cue theo yêu cầu mới; ảnh lesson và audio không đổi.

## 8 ô điền đã được chốt cue và đáp án

**Không còn ô thiếu cue trong danh sách này.** Người dùng đã giao assistant tự chốt: Unit6 cake/milk/fish/ice cream; Unit7 head/eyes; Unit8 circle/line. Đã gắn ảnh vào bài nguồn, mapping có expected_answer duy nhất và needs_context=false. Tuổi, sở thích và khả năng cá nhân vẫn giữ là câu trả lời mở. Xem audit/challenge-cue-decisions.json.

| Bộ | Vị trí | Câu nguồn | Ghi chú |
|---|---|---|---|

Unit8 câu5 dùng make_circle, câu6 dùng make_line; hai ảnh này đã trở thành bắt buộc và có đáp án cố định. Unit5 các nhóm3 ducks/8 cows/8 cars đã nối bằng adaptation được goal cho phép; các summary flags cũ được đồng bộ với item mapping.

## Hạn chế và cách dùng

- Audio Challenge vẫn do chủ dự án bổ sung; lượt này không tạo audio hay tự nhận đã nghe/transcribe các MP3 lesson.
- Một số crop gốc nhỏ được contain lên512 để giữ style; provenance ghi rõ, không khẳng định thêm chi tiết mới. Bản hỏng/thiếu contour được sửa bằng built-in image_gen.
- Review5–6 make_circle dùng4 bé thay3 bé nguồn như action adaptation; không dùng số lượng trẻ để làm claim bài đếm.
- Prompt/inventory là snapshot kế hoạch trước khi làm. Trạng thái ảnh hiện tại lấy từ manifest/validation và báo cáo này; không chạy lại generation chỉ vì inventory còn ghi “missing”.

## Bằng chứng hoàn thành goal

- Yêu cầu 1: **proved** — Initial outputs inspected before work; existing clean source art reused and revised only when visual QA failed.
- Yêu cầu 2: **proved** — 12 inventory ID sets matched; Only user-authorized eight cue insertions in Challenge sources; original lesson images/audio unchanged.
- Yêu cầu 3: **proved** — Creation provenance separates native/crop/compose and built-in image_gen. Exact tool prompts/results persisted for all 10 sets using AI.
- Yêu cầu 4: **proved** — Actual 12-card action and 9-card body batches retained; smaller remainder/repair jobs documented; no surplus runtime IDs.
- Yêu cầu 5: **proved** — 211 actual WebP files decoded at 512×512, quality80/method6 documented, largest 52864 bytes; zero above60KB.
- Yêu cầu 6: **proved** — 211 mandatory IDs (the two prior conditional cues are now selected), one file per ID, repeated exercises reuse IDs; no within-set exact duplicates or orphan runtime WebP.
- Yêu cầu 7: **proved** — All12 manifest/mapping/preview/contact-sheet/README/validation deliverables exist. 364 Review IDs exactly covered; Unit source sections and visual occurrences mapped; 80 representative preview samples span all5 Challenges in all12 sets.
- Yêu cầu 8: **proved_after_user_authorized_cue_decisions** — Authorized count/color/action adaptations recorded without rewriting source. Eight formerly unknown blanks now have explicit user-authorized cue decisions and unique keys; personal answers stay open.

[Danh mục provenance](<E:/let-go-series/audit/challenge-generation-provenance-index.json>) · [Review ảnh ràng buộc hash](<E:/let-go-series/audit/challenge-visual-review.json>)

![Preview trong trình duyệt](<E:/let-go-series/audit/challenge-preview-browser.png>)
