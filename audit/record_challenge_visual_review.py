"""Record explicit human/model visual judgments against current file hashes."""
from pathlib import Path
import json,hashlib,argparse

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--set',required=True);parser.add_argument('--fail',action='append',default=[]);parser.add_argument('--pending',action='store_true');parser.add_argument('--ids',nargs='*');parser.add_argument('--note',default='Individually viewed final compressed WebP by root: semantic/color/count/action and complete target contours checked; no answer labels.')
    args=parser.parse_args();p=ROOT/'audit/challenge-visual-review.json'
    data=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'reviewer':'root','cards':{}}
    inv=json.loads((ROOT/f'parallel-prompts/challenge-images/{args.set}.inventory.json').read_text(encoding='utf-8'));folder=Path(inv['lesson_folder'])/'challenge-assets'
    for a in inv['assets']:
        if args.ids and a['id'] not in args.ids:continue
        f=folder/f'webp/{a["id"]}.webp'
        data['cards'][a['id']]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'status':'pending' if args.pending else 'fail' if a['id'] in args.fail else 'pass','notes':args.note}
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(args.set,'recorded')

if __name__=='__main__':main()
