from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
m['lesson_specs']=json.loads((ROOT/'lesson_specs.json').read_text(encoding='utf-8'))
notes={
'CD2_41':'Source E is title-only. Adapt stamping feet and clapping hands from source D on same PDF page 2.',
'CD2_43':'Source B is title-only. Reuse four numbered body cards and header model from A on PDF page 3.',
'CD2_45':'No chant lyrics printed in PDF. Retain four body-part illustrations; labels are vocabulary support from preceding page, not a transcription.',
'CD2_47':'Source B is title-only. Reuse four numbered face-part cards and header model dialogue from A on PDF page 5.',
'CD2_49':'No song lyrics printed in PDF. Retain nose/shoulders/toes/knees actions; supplementary ears practice inset comes from C on same page, not from invented lyrics.',
'CD2_50':'Complete 26 upper/lowercase pairs reformatted into columns; Uu/Vv/Ww highlighted.',
'CD2_51':'Include untracked C. Find the letters as supporting activity on same lesson page; preserve Uu Vv Ww glyphs without marking answers.'}
for p in m['items']:
 if p['track'] in notes:p['adaptation_notes']=notes[p['track']]
m['batches']=[{'id':'batch'+str(i+1),'tracks':[p['track'] for p in m['items'][i*4:(i+1)*4]],'status':'reviewed' if i==0 else 'pending_generation'} for i in range(5)]
(ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

