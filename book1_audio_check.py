"""Sample ASR only: assists mapping QA, never substitutes for source CD icons."""
from pathlib import Path
import json, subprocess
import numpy as np
import torch,whisper

root=Path(__file__).parent/'Let_s Go 1'
torch.set_num_threads(4)
model=whisper.load_model('tiny.en',device='cpu')
samples=[(1,t) for t in [1,2,4,24,50,73,97,99]]+[(2,t) for t in [1,2,25,51,74,95,96,97,98,99]]
out=[]
for d,t in samples:
    folder=next(root.glob(f'*Students Book*CD{d}'))
    audio=next(p for p in folder.glob('*.mp3') if int(p.name.split(' ')[0])==t)
    raw=subprocess.run(['ffmpeg','-v','error','-i',str(audio),'-t','18','-ar','16000','-ac','1','-f','f32le','pipe:1'],check=True,capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32)
    result=model.transcribe(x,language='en',fp16=False,temperature=0,condition_on_previous_text=False)
    row=dict(id=f'CD{d}_{t:02}',sample_seconds=min(18,len(x)/16000),text=result['text'],source=audio.name)
    out.append(row);print(row['id'],row['text'],flush=True)
    (root/'Units/Audio Pages/audio-prefix-check.json').write_text(json.dumps(dict(method='tiny.en ASR of first 18 seconds; sampled tracks only; machine output may contain errors',samples=out),ensure_ascii=False,indent=2),encoding='utf-8')
