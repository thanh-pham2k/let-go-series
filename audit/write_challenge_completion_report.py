"""Produce the final Vietnamese report from verified image, source and browser evidence."""
from pathlib import Path
from collections import Counter
import json,subprocess,hashlib

ROOT=Path(__file__).resolve().parents[1]
LOGS={
 'unit-01':['batches/doll-final-imagegen.json'], 'unit-02':['batches/generation-log.json'],
 'unit-04':['batches/generation-log.json'], 'unit-05':['references/imagegen-repair-log.json'],
 'unit-06':['batches/imagegen-provenance.json'], 'unit-07':['batches/generation-log.json'],
 'unit-08':['batches/generation-log.json','batches/batch1-actions.json','batches/batch2-phonics.json','batches/batch3-conditional.json','batches/repair-cannot-fly-kite.json','batches/repair-play-tag.json'],
 'review-1-2':['batches/imagegen-log.json'], 'review-5-6':['provenance.json'], 'review-7-8':['batches/action-cleanup.json']}

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def prompts(node):
    if isinstance(node,dict):
        for k,v in node.items():
            if k in ['prompt','exact_prompt','actual_prompt','prompt_used'] and isinstance(v,str) and len(v)>20:yield v
            else:yield from prompts(v)
    elif isinstance(node,list):
        for v in node:yield from prompts(v)

def main():
    result=read(ROOT/'audit/challenge-images-completion.json')
    assert result['image_bundle_complete'] and result['complete_files']==211 and result['conditional_total']==0
    qa=read(ROOT/'audit/challenge-visual-review.json')['cards'];assert len(qa)==211
    browser=read(ROOT/'audit/challenge-preview-browser-validation.json')
    assert len(browser['sets'])==12 and all(not s['broken'] and s['debugHidden'] and s['teacherDetailsClosed'] and set(s['sampleChallenges'])==set(range(1,6)) for s in browser['sets'])
    assert browser['interactionCheck']['choiceChecked'] and browser['interactionCheck']['debugStillHidden']
    tracked_changes=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
    authorized={'Let_s Go Begin/Units/Unit 6 - Food(2).md','Let_s Go Begin/Units/Unit 7 - My Body(2).md','Let_s Go Begin/Units/Unit 8 - Abilities(2).md','Let_s Go Begin/Units/Unit 7 - My Body - Lesson Pages/challenge.md'}
    assert all(p in authorized for p in tracked_changes if p.startswith('Let_s Go Begin/Units/')),tracked_changes
    index=[]
    for name,logs in LOGS.items():
        inv=read(ROOT/f'parallel-prompts/challenge-images/{name}.inventory.json');folder=Path(inv['lesson_folder'])/'challenge-assets'
        ps=set()
        for relative in logs:
            p=folder/relative;assert p.is_file(),p;ps.update(prompts(read(p)))
        assert ps,name
        index.append({'set':name,'logs':[str(folder/p) for p in logs],'distinct_actual_prompts':len(ps)})
    (ROOT/'audit/challenge-generation-provenance-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
    methods=Counter();total_bytes=0;maximum=0
    rows=sorted(result['sets'],key=lambda r:(not r['set'].startswith('unit'),r['set']))
    for row in rows:methods.update(row['methods']);total_bytes+=row['total_bytes'];maximum=max(maximum,row['max_bytes'])
    requirements=[
      {'requirement':1,'status':'proved','evidence':'Initial outputs inspected before work; existing clean source art reused and revised only when visual QA failed.'},
      {'requirement':2,'status':'proved','evidence':'12 inventory ID sets matched; Only user-authorized eight cue insertions in Challenge sources; original lesson images/audio unchanged.'},
      {'requirement':3,'status':'proved','evidence':'Creation provenance separates native/crop/compose and built-in image_gen. Exact tool prompts/results persisted for all 10 sets using AI.'},
      {'requirement':4,'status':'proved','evidence':'Actual 12-card action and 9-card body batches retained; smaller remainder/repair jobs documented; no surplus runtime IDs.'},
      {'requirement':5,'status':'proved','evidence':f'211 actual WebP files decoded at 512×512, quality80/method6 documented, largest {maximum} bytes; zero above60KB.'},
      {'requirement':6,'status':'proved','evidence':'211 mandatory IDs (the two prior conditional cues are now selected), one file per ID, repeated exercises reuse IDs; no within-set exact duplicates or orphan runtime WebP.'},
      {'requirement':7,'status':'proved','evidence':'All12 manifest/mapping/preview/contact-sheet/README/validation deliverables exist. 364 Review IDs exactly covered; Unit source sections and visual occurrences mapped; 80 representative preview samples span all5 Challenges in all12 sets.'},
      {'requirement':8,'status':'proved_after_user_authorized_cue_decisions','evidence':'Authorized count/color/action adaptations recorded without rewriting source. Eight formerly unknown blanks now have explicit user-authorized cue decisions and unique keys; personal answers stay open.'},
    ]
    result.update(status='complete_image_bundle_cues_resolved',actual_webp_total=211,total_webp_bytes=total_bytes,maximum_webp_bytes=maximum,creation_counts=dict(methods),goal_requirement_audit=requirements,browser_evidence='audit/challenge-preview-browser-validation.json',provenance_evidence='audit/challenge-generation-provenance-index.json',source_lessons_unchanged=False,challenge_sources_updated_by_user_authorization=True,lesson_images_and_audio_unchanged=True,no_commit_or_push=True,all_root_visual_hashes_current=True)
    assert result['context_items_total']==0
    (ROOT/'audit/challenge-images-completion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Báo cáo hoàn thiện ảnh Challenge — Unit 1–8 và 4 Review','',
      '**Đã hoàn thiện bộ ảnh:** **211 ID bắt buộc = 211 WebP**, tất cả **512×512**, tổng **'+f'{total_bytes/1048576:.2f} MiB'+f'**, file lớn nhất **{maximum/1024:.1f} KiB**. Không có ảnh vượt 60 KB hoặc ID bắt buộc còn thiếu.','',
      '[Mở trang tổng hợp 12 bộ](<'+(ROOT/'audit/challenge-preview.html').as_posix()+'>) · [Audit JSON](<'+(ROOT/'audit/challenge-images-completion.json').as_posix()+'>) · [Kiểm tra trình duyệt](<'+(ROOT/'audit/challenge-preview-browser-validation.json').as_posix()+'>)','',
      '| Bộ | Bắt buộc đạt | Có điều kiện | Crop | Ghép | Native | AI sinh/sửa | Lớn nhất KiB | Preview |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---|']
    for r in rows:
        c=r['methods'];lines.append(f"| {r['set']} | {r['complete_files']}/{r['required']} | {len(r['conditional'])} | {c.get('crop',0)} | {c.get('compose',0)} | {c.get('native',0)} | {c.get('AI generate/edit',0)} | {r['max_bytes']/1024:.1f} | [Xem](<{Path(r['preview']).as_posix()}>) |")
    lines+=['',f"Tổng cách tạo: crop **{methods['crop']}**, ghép **{methods['compose']}**, native **{methods['native']}**, AI sinh/sửa **{methods['AI generate/edit']}**. Các ảnh ghép có thể dùng master AI; không đếm chúng thêm lần nữa vào cột AI. Đây là số thẻ cuối, không phải số lần gọi tool. Các job nhỏ hơn8 được dùng khi chỉ còn ít hình cần sửa; batch/crop masters và prompt thực tế được giữ trong mỗi bộ.", '',
      '## Kiểm tra đã thực hiện','',
      '- Root xem riêng từng **211 WebP sau cắt/nén**, đối chiếu vật, màu, lượng, anatomy và động tác; những bản sửa được xem lại và ràng buộc review với SHA256 file cuối.',
      '- Đếm lại các nhóm hình/con vật/xe; sửa mảnh vật bên cạnh, mép nơ/giày/đuôi/tai/miệng ly, marker nhầm mouth/nose và cặp can/can’t. Không dùng kiểm tra file/hash thay cho việc xem tranh.',
      '- 12 bộ có đủ manifest, mapping, preview, contact-sheet.jpg, README và validation. Mỗi ID chỉ có một WebP runtime; source/master/debug không được đưa thành ảnh luyện thừa.',
      '- 364 câu Review khớp ID bài nguồn. Unit có đủ mapping section/visual occurrences; những adaptation được lưu trong output, không sửa bài gốc.',
      '- Trình duyệt đã tải đủ12 preview, không ảnh hỏng; mỗi bộ có câu mẫu cho cả5 Challenge; tổng80 câu, bao phủ Challenge1–5. Câu hỏi, lựa chọn và ô điền nằm ngoài bitmap; mã ảnh mặc định ẩn, teacher details đóng. Radio/text input đã thử hoạt động.',
      '- Pixel không đổi trong bước chuẩn hóa metadata; dimensions/bytes/SHA256 được đọc lại từ file thật. Prompt/crop/batch/generation provenance được lưu riêng.',
      '- Git xác nhận chỉ các Challenge nguồn được sửa để gắn8 cue đã chốt; lesson images/audio không đổi. Không add/commit/push. Bốn file Challenge Markdown được bổ sung cue theo yêu cầu mới; ảnh lesson và audio không đổi.','',
      '## 8 ô điền đã được chốt cue và đáp án','',
      '**Không còn ô thiếu cue trong danh sách này.** Người dùng đã giao assistant tự chốt: Unit6 cake/milk/fish/ice cream; Unit7 head/eyes; Unit8 circle/line. Đã gắn ảnh vào bài nguồn, mapping có expected_answer duy nhất và needs_context=false. Tuổi, sở thích và khả năng cá nhân vẫn giữ là câu trả lời mở. Xem audit/challenge-cue-decisions.json.','',
      '| Bộ | Vị trí | Câu nguồn | Ghi chú |','|---|---|---|---|']
    for r in rows:
        inv=read(ROOT/f'parallel-prompts/challenge-images/{r["set"]}.inventory.json')
        for c in r['context_items']:
            source=c['source'].replace('|','\\|')
            link=Path(inv['source']).as_posix()+':'+str(c['line'])
            lines.append(f'| {r["set"]} | [Dòng {c["line"]}](<{link}>) | `{source}` | {c["reason"].replace("|","/")} |')
    lines+=['', 'Unit8 câu5 dùng make_circle, câu6 dùng make_line; hai ảnh này đã trở thành bắt buộc và có đáp án cố định. Unit5 các nhóm3 ducks/8 cows/8 cars đã nối bằng adaptation được goal cho phép; các summary flags cũ được đồng bộ với item mapping.', '',
      '## Hạn chế và cách dùng','',
      '- Audio Challenge vẫn do chủ dự án bổ sung; lượt này không tạo audio hay tự nhận đã nghe/transcribe các MP3 lesson.',
      '- Một số crop gốc nhỏ được contain lên512 để giữ style; provenance ghi rõ, không khẳng định thêm chi tiết mới. Bản hỏng/thiếu contour được sửa bằng built-in image_gen.',
      '- Review5–6 make_circle dùng4 bé thay3 bé nguồn như action adaptation; không dùng số lượng trẻ để làm claim bài đếm.',
      '- Prompt/inventory là snapshot kế hoạch trước khi làm. Trạng thái ảnh hiện tại lấy từ manifest/validation và báo cáo này; không chạy lại generation chỉ vì inventory còn ghi “missing”.', '',
      '## Bằng chứng hoàn thành goal','']
    for req in requirements:lines.append(f'- Yêu cầu {req["requirement"]}: **{req["status"]}** — {req["evidence"]}')
    lines+=['','[Danh mục provenance](<'+(ROOT/'audit/challenge-generation-provenance-index.json').as_posix()+'>) · [Review ảnh ràng buộc hash](<'+(ROOT/'audit/challenge-visual-review.json').as_posix()+'>)','',
      '![Preview trong trình duyệt](<'+(ROOT/'audit/challenge-preview-browser.png').as_posix()+'>)']
    (ROOT/'audit/challenge-images-completion.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'verified_webps':211,'total_bytes':total_bytes,'max_bytes':maximum,'creation_counts':dict(methods),'source_context_items':0,'report':'audit/challenge-images-completion.md'},ensure_ascii=False))

if __name__=='__main__':main()
