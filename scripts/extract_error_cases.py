from __future__ import annotations

import json
from pathlib import Path
import sys
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]

def load_dataset(path: Path):
    return {item['id']: item for item in json.loads(path.read_text(encoding='utf-8'))}

def load_predictions(path: Path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'predictions' in data:
        data = data['predictions']
    return {str(item['id']): item for item in data}

def extract_mismatches(dataset, preds, max_per_type=2):
    grouped = defaultdict(list)
    for sid, sample in dataset.items():
        gold = sample.get('label', 'neutral')
        pred = preds.get(sid, {}).get('prediction', 'neutral')
        raw = preds.get(sid, {}).get('raw_output', '')
        if pred != gold:
            t = sample.get('type', 'unknown')
            grouped[t].append({
                'id': sid,
                'text': sample.get('text',''),
                'context': sample.get('context',''),
                'gold': gold,
                'prediction': pred,
                'raw_output': raw,
            })
    # trim
    out = {}
    for k, v in grouped.items():
        out[k] = v[:max_per_type]
    return out

def main():
    if len(sys.argv) < 4:
        print('Usage: extract_error_cases.py <dataset_all.json> <output_md> <pred1>=<label> [<pred2>=<label> ...] [--max N]')
        sys.exit(1)
    args = sys.argv[1:]
    max_per_type = 2
    if '--max' in args:
        i = args.index('--max')
        try:
            max_per_type = int(args[i+1])
        except Exception:
            pass
        # remove the two args
        del args[i:i+2]
    dataset_path = Path(args[0])
    out_md = Path(args[1])
    pairs = args[2:]
    dataset = load_dataset(dataset_path)
    summary = {}
    results = []
    for p in pairs:
        if '=' in p:
            pred_path, label = p.split('=',1)
        else:
            pred_path = p
            label = Path(p).stem
        pred_path = Path(pred_path)
        preds = load_predictions(pred_path)
        mism = extract_mismatches(dataset, preds, max_per_type=max_per_type)
        summary[label] = {k: len(v) for k,v in mism.items()}
        results.append({'model': label, 'mismatches': mism})

    out_json_dir = ROOT / 'results' / 'temp'
    out_json_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_json_dir / 'error_cases.json'
    out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')

    # write markdown
    lines = ['# 错误案例摘录（自动提取）\n']
    for r in results:
        lines.append(f"## 模型：{r['model']}\n")
        for t, items in r['mismatches'].items():
            lines.append(f"### 类型：{t}\n")
            for item in items:
                lines.append(f"- id: {item['id']}")
                lines.append(f"  - text: {item['text']}")
                lines.append(f"  - context: {item['context']}")
                lines.append(f"  - gold: {item['gold']}")
                lines.append(f"  - prediction: {item['prediction']}")
                lines.append(f"  - raw_output: >\n    {item['raw_output'].replace('\n','\n    ')}\n")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text('\n'.join(lines), encoding='utf-8')
    # write CSV
    csv_lines = ['model,type,id,text,context,gold,prediction,raw_output']
    for r in results:
        for t, items in r['mismatches'].items():
            for item in items:
                ro = item['raw_output'].replace('\n','\\n').replace('"','""')
                csv_lines.append(f'"{r["model"]}","{t}","{item["id"]}","{item["text"].replace("\"","\"\"")}","{item["context"].replace("\"","\"\"")}","{item["gold"]}","{item["prediction"]}","{ro}"')
    out_csv = out_json_dir / 'error_cases.csv'
    out_csv.write_text('\n'.join(csv_lines), encoding='utf-8')
    print('Wrote', out_json, out_md, out_csv)

if __name__ == '__main__':
    main()
