from pathlib import Path
import json
r=Path(__file__).resolve().parent
p=r/'assets/batches/batch1.json'
d=json.loads(p.read_text(encoding='utf-8'));d['status']='generated_needs_review';d['source_output']="C:\\Users\\Admin\\.codex\\generated_images\\01a11c50-9e97-74c3-b487-055d453dea0f\\exec-7bd86c92-bbf0-467b-a9c5-f6758d57c35e.png";d['selected_asset']='assets/batches/batch1.png';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

