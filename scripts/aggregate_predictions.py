from __future__ import annotations

import json
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

def load_dataset(path: Path):
    data = json.loads(path.read_text(encoding='utf-8'))
    return {item['id']: item for item in data}

def find_prediction_files(root: Path):
    preds = []
    for p in root.rglob('*predictions*.json'):
        preds.append(p)
    return preds

def load_preds(path: Path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'predictions' in data:
        data = data['predictions']
    return data

def main():
    dataset = load_dataset(ROOT / 'dataset_expanded' / 'all.json')
    out_dir = ROOT / 'results' / 'temp'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / 'all_predictions_aggregated.csv'
    files = find_prediction_files(ROOT / 'results')
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['file', 'model', 'provider', 'prompt', 'id', 'gold', 'prediction', 'raw_output'])
        for p in sorted(files):
            # try to infer model/provider/prompt from path
            parts = p.parts
            # default metadata
            model = ''
            provider = ''
            prompt = ''
            # attempt to read a manifest if exists in same dir
            manifest = p.parent / 'manifest.json'
            if manifest.exists():
                try:
                    m = json.loads(manifest.read_text(encoding='utf-8'))
                    model = m.get('model','')
                    provider = m.get('provider','')
                    prompt = m.get('prompt','')
                except Exception:
                    pass
            preds = load_preds(p)
            for item in preds:
                pid = str(item.get('id',''))
                gold = dataset.get(pid, {}).get('label','')
                writer.writerow([str(p), model, provider, prompt, pid, gold, item.get('prediction',''), item.get('raw_output','')])
    print('Wrote', out_csv)

if __name__ == '__main__':
    main()
