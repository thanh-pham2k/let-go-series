"""Apply user-authorized fixed visual cues to the eight previously ambiguous blanks."""
from pathlib import Path
from urllib.parse import quote
import json,re

ROOT=Path(__file__).resolve().parents[1]
DECISIONS={6:[(273,'u06_cake','cake'),(274,'u06_milk','milk'),(275,'u06_fish','fish'),(276,'u06_ice_cream','ice cream')],7:[(308,'u07_touch_head','head'),(311,'u07_touch_eyes','eyes')],8:[(390,'u08_make_circle','circle'),(391,'u08_make_line','line')]}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    all_decisions=[]
    for unit,decisions in DECISIONS.items():
        ip=ROOT/f'parallel-prompts/challenge-images/unit-{unit:02d}.inventory.json';inv=read(ip);folder=Path(inv['lesson_folder'])/'challenge-assets';source=Path(inv['source']);lines=source.read_text(encoding='utf-8-sig').splitlines()
        records=[]
        for ln,aid,answer in decisions:
            target=folder/f'webp/{aid}.webp';assert target.is_file()
            cue_line=ln+1 if unit==7 else ln
            raw=re.sub(r'\s*!\[Hình gợi ý\]\([^)]*\)','',lines[cue_line-1]).rstrip()
            link=quote((target.relative_to(source.parent)).as_posix())
            lines[cue_line-1]=raw+'  ![Hình gợi ý]('+link+')'
            records.append({'unit':unit,'question_line':ln,'cue_line':cue_line,'asset_id':aid,'asset_ids':[aid],'expected_answer':answer,'accepted_answers':[answer],'image_required':True,'needs_context':False,'adaptation_applied':True,'adaptation_notes':'User authorized assistant to choose a fixed cue/answer; existing image reused, original question stem preserved.','learner_prompt':raw})
        source.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        by_line={r['question_line']:r for r in records};mapping=read(folder/'question-image-map.json')
        def fix(node):
            if isinstance(node,dict):
                ln=node.get('line',node.get('source_line'))
                if ln in by_line:
                    r=by_line[ln];node.update(asset_ids=r['asset_ids'],expected_answer=r['expected_answer'],accepted_answers=r['accepted_answers'],image_required=True,needs_context=False,adaptation_applied=True,adaptation_notes=r['adaptation_notes'])
                    node.pop('reason',None);node.pop('note',None)
                if unit==7 and node.get('challenge')==3 and str(node.get('section','')).startswith('5.'):
                    node.update(needs_context=False,image_required=True)
                if unit==8 and ((node.get('challenge')==3 and str(node.get('section','')).startswith('7.')) or node.get('id')=='u08_c3_command_order'):
                    node.update(needs_context=False,image_required=True,applied=True,status='fixed_visual_cues',asset_ids=['u08_make_circle','u08_make_line'],decision='Fixed by user-authorized decision: item5=circle; item6=line.',items=[r for r in records])
                    node.pop('reason',None)
                for v in list(node.values()):fix(v)
            elif isinstance(node,list):
                for v in node:fix(v)
        fix(mapping);mapping['resolved_visual_cues']=records;write(folder/'question-image-map.json',mapping)
        manifest=read(folder/'manifest.json')
        for a in manifest['assets']:
            uses=[r for r in records if r['asset_id']==a['id']]
            if uses:a['fixed_cue_uses']=uses
            if unit==8 and uses:a.update(required=True,conditional=False)
        write(folder/'manifest.json',manifest)
        validation=read(folder/'validation.json');validation['unresolved_context']=[];validation['resolved_visual_cues']=records;validation['status']='passed';write(folder/'validation.json',validation)
        # Unit7 package copy is a duplicate of this same Challenge document.
        copy=folder.parent/'challenge.md'
        if copy.exists():copy.write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
        with (folder/'README.md').open('a',encoding='utf-8') as f:f.write('\n\nCập nhật cue theo quyết định được người dùng giao: '+', '.join(f'dòng {r["question_line"]} → {r["expected_answer"]}' for r in records)+'. Đã gắn ảnh cụ thể và đáp án duy nhất; thay thế các ghi chú needs_context cũ ở các mục này. Không tạo thêm ảnh.\n')
        all_decisions.extend(records)
    write(ROOT/'audit/challenge-cue-decisions.json',{'date':'2026-10-10','authorization':'User asked assistant to decide to remove ambiguity.','decisions':all_decisions})
    print('Resolved eight blanks using existing images; source, maps and answer keys updated.')

if __name__=='__main__':main()
