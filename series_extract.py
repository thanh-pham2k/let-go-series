from pathlib import Path
import pymupdf as fitz
import subprocess, os, json
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).parent
CACHE=ROOT/'tmp/series'
CACHE.mkdir(parents=True,exist_ok=True)
BOOKS={n:next(p for p in ROOT.glob(f'Let_s Go {n}*/*.pdf') if 'student' in p.name.lower()) for n in range(1,7)}
RANGES={
1:[(3,10),(11,18),(21,28),(29,36),(39,46),(47,54),(57,64),(65,72)],
2:[(5,12),(13,20),(23,30),(31,38),(41,46),(47,56),(59,66),(67,74)],
3:[(5,12),(13,20),(23,30),(31,38),(41,48),(49,56),(59,66),(67,74)],
4:[(4,11),(12,19),(22,29),(30,37),(40,45),(46,55),(58,65),(66,73)],
5:[(4,11),(12,19),(22,29),(30,37),(40,47),(48,55),(58,65),(66,73)],
6:[(4,11),(12,19),(22,29),(30,37),(40,47),(48,55),(58,65),(66,73)]}

def ocr(job):
    n,i=job
    dest=CACHE/f'b{n}-p{i:02}.txt'
    if dest.exists() and (CACHE/f'b{n}-p{i:02}-sparse.txt').exists(): return
    d=fitz.open(BOOKS[n]); page=d[i-1]
    img=CACHE/f'b{n}-p{i:02}.png'
    page.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(img)
    env=dict(os.environ,OMP_THREAD_LIMIT='1')
    subprocess.run([r'C:\Program Files\Tesseract-OCR\tesseract.exe',str(img),str(dest.with_suffix('')),'-l','eng','--psm','3'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    subprocess.run([r'C:\Program Files\Tesseract-OCR\tesseract.exe',str(img),str(dest.with_suffix(''))+'-sparse','-l','eng','--psm','11'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    return str(dest)

if __name__=='__main__':
    jobs=[(n,i) for n,rr in RANGES.items() for i in range(rr[0][0],rr[-1][1]+3)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for k,_ in enumerate(pool.map(ocr,jobs)):
            if k%24==0: print(f'OCR {k+1}/{len(jobs)}',flush=True)
    print('OCR complete',flush=True)
