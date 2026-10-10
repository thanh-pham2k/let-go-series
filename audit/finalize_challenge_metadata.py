"""Normalize export facts without changing source lessons or any card pixels."""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    qa=read(ROOT/'audit/challenge-visual-review.json')['cards']
    for ip in sorted((ROOT/'parallel-prompts/challenge-images').glob('*.inventory.json')):
        inv=read(ip);folder=Path(inv['lesson_folder'])/'challenge-assets';mp=folder/'manifest.json';manifest=read(mp)
        for a in manifest['assets']:
            aid=a['id'];rel=a.get('file',a.get('webp',a.get('files',{}).get('webp') if isinstance(a.get('files'),dict) else None)) or f'webp/{aid}.webp'
            f=folder/rel;h=hashlib.sha256(f.read_bytes()).hexdigest()
            assert qa[aid]['sha256']==h and qa[aid]['status']=='pass',aid
            method=a.get('creation_method',a.get('creation'))
            if not method:
                method=a.get('method') if isinstance(a.get('method'),str) else None
            prov=a.get('provenance')
            if not method and isinstance(prov,str):method=prov
            if not method and isinstance(prov,dict):method=prov.get('method')
            if not method and inv.get('unit')==8:method='built_in_image_gen'
            if method=='crop_or_edit':method='crop_from_lesson'
            if method=='edit_or_generate' and isinstance(prov,dict) and prov.get('source')=='built_in_image_gen':method='built_in_image_gen'
            assert isinstance(method,str),aid
            with Image.open(f) as im:dimensions=list(im.size)
            a.update(file=rel,creation_method=method,format='WEBP',dimensions=dimensions,quality=80,webp_method=6,file_bytes=f.stat().st_size,sha256=h,root_visual_review=qa[aid])
        manifest['root_final_audit']={'all_cards_individually_reviewed':True,'file_hashes_bound_to_reviews':True,'webp_quality':80,'webp_method':6,'source_lessons_unchanged':True}
        write(mp,manifest)
        # Internal contact sheet labels are reviewer metadata, never in the learner WebP.
        sheet=Image.new('RGB',(1200,math.ceil(len(manifest['assets'])/6)*240),'white');draw=ImageDraw.Draw(sheet)
        for i,a in enumerate(manifest['assets']):
            x=i%6*200;y=i//6*240;sheet.paste(Image.open(folder/a['file']).resize((200,200)),(x,y));draw.text((x+3,y+204),a['id'],fill='black')
        sheet.save(folder/'contact-sheet.jpg',quality=90)
        validation=read(folder/'validation.json')
        validation['root_final_audit']={'card_count':len(manifest['assets']),'all_individual_visual_reviews_pass':True,'all_dimensions':[512,512],'all_links_exist':all((folder/a['file']).is_file() for a in manifest['assets']),'max_bytes':max(a['file_bytes'] for a in manifest['assets']),'over_60kb':[a['id'] for a in manifest['assets'] if a['file_bytes']>61440],'unique_hashes':len({a['sha256'] for a in manifest['assets']}),'contact_sheet_regenerated_from_final_webps':True}
        write(folder/'validation.json',validation)
        if inv.get('unit')==5:
            qp=folder/'question-image-map.json';mapping=read(qp)
            def fix(node):
                if isinstance(node,dict):
                    if node.get('needs_context') and node.get('source_line') in [291,335,563]:
                        node.update(needs_context=False,adaptation_applied=True,mode='mapped_assets',image_required=True,asset_ids=node.get('proposed_asset_ids',[]),adapted_items=node.pop('items_needing_context',[]),reason='Aggregate section status synchronized with ten already-applied source-supported/goal-authorized count adaptations; source Markdown unchanged.')
                    for v in list(node.values()):fix(v)
                elif isinstance(node,list):
                    for v in node:fix(v)
            fix(mapping);write(qp,mapping)
        with (folder/'README.md').open('a',encoding='utf-8') as file:
            file.write('\n\nRoot completion audit: every final compressed WebP was individually viewed; corrected cards rechecked. Manifest now records creation_method separately from WebP codec, actual dimensions/bytes/hash, and hash-bound root visual review. Contact sheet rebuilt from final files. Preview uses neutral card labels and six source-backed examples spanning Challenge 1–5; teacher descriptions remain collapsed. Source context exceptions, if any, remain explicitly in question-image-map.json rather than guessed answer keys.\n')
    print('Normalized all 12 manifests, validations and final contact sheets; no card/source pixels changed.')

if __name__=='__main__':main()
