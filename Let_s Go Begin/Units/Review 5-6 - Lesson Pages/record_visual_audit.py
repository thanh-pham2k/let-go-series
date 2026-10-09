from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
notes={
'CD2_35':"Visually compared PDF page1/book54 with final 1200x1200 PNG and contact sheet: 1a three individually countable cats;1b four;2a two rabbits;2b five. 3a white cone/3b yellow layered cake blue plate;4a bread/4b pink yellow blue rice bowl.5a boy skipping one grounded foot/5b jumping both feet airborne.6a exactly3 children diagonally one behind another/6b same3 holding hands in circle, original clothing/glasses. Complete header/instruction/CD2_35, pair numbers1-6, twelve a/b labels/footer54 readable. Choices unmarked, no supplementary quiz printed, no gutter or clipped text/objects.",
'CD2_36':"Visually compared PDF page2/book55 with final 1200x1200 PNG and contact sheet: numbered labels1 sunny2 cloudy3 windy4 rainy5 snowy exact; original yellow house, blue shutters, pink curtains, ponytail girl/clothing retained. Sunny sun/upright trees, cloudy gray clouds/no wind or precipitation, windy moving scarf/hair/leaves/wind strokes and bent tree outlines, rainy visible raindrops, snowy white flakes/accumulation/purple shivering girl. Complete large sunny window scene and It's sunny. bubble retained; header/instruction/CD2_36/footer55 readable. No invented weather sentences, no supplementary quiz printed, no gutter or clipping. Slight decorative white clouds in large sunny sky; still clearly sunny, source scene composition compacted."
}
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for p in m['items']:
 p['visual_review']=notes[p['track']]
 p['final_crop_review']='Inspected final PNG and full contact sheet after actual gutter crop and contain.'
 if p['track']=='CD2_36':p['adaptation_notes'].append('Large sunny background includes faint decorative white cloud shading; sunshine and lesson meaning unchanged.')
(ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
report={'method':'Model visual inspection, not OCR-only or technical validation; no claim of independent listening.','source_pages_inspected':['source-pages/page-1.png','source-pages/page-2.png'],'final_images_inspected':['pages/png/CD2_35.png','pages/png/CD2_36.png'],'contact_sheet_inspected':'preview.jpg','gutter':'Straight vertical gutter near x887 on1774x887 sheet; individual boxes exclude separator.','items':[{'track':p['track'],'source_crop_box':p['source_crop_box'],'png_sha256':sha(ROOT/p['output']['png']),'observations':notes[p['track']],'question_basis':'Visible illustration recognition, not original audio selection.'} for p in m['items']],'unverified':['Original CD2_35 a/b listening answers','Independent speech/transcription audit of either MP3'],'corrections_to_challenge':['Source name Review 5-6(2) corrected to Review 5-6.pdf','Blanket coverage statement narrowed; exercise body preserved byte-equivalent after newline normalization.']}
(ROOT/'visual.audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Recorded source/final/contact-sheet content audit for both tracks; no audio-answer claims.')
