from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_pct(v: float) -> str:
    return f"{v * 100:.2f}%"


def fmt_pp(v: float) -> str:
    return f"{v * 100:+.2f}pp"


def build_markdown(baseline: dict, cot: dict) -> str:
    rows = [
        ("Accuracy", baseline["accuracy"], cot["accuracy"]),
        ("Macro-F1", baseline["macro_f1"], cot["macro_f1"]),
        ("Normal", baseline.get("normal_accuracy", 0.0), cot.get("normal_accuracy", 0.0)),
        ("Sarcasm", baseline.get("per_type_accuracy", {}).get("sarcasm", 0.0), cot.get("per_type_accuracy", {}).get("sarcasm", 0.0)),
        ("Metaphor", baseline.get("per_type_accuracy", {}).get("metaphor", 0.0), cot.get("per_type_accuracy", {}).get("metaphor", 0.0)),
        ("Adversarial", baseline.get("adversarial_accuracy", 0.0), cot.get("adversarial_accuracy", 0.0)),
        ("Robustness", baseline.get("robustness_score", 0.0), cot.get("robustness_score", 0.0)),
    ]

    md = [
        "# EmotionBench Prompt 对比结果\n",
        "## 实验设置\n",
        f"- Model: `{cot.get('model', 'unknown')}`\n",
        f"- Provider: `{cot.get('provider', 'unknown')}`\n",
        f"- Dataset size: `{cot.get('num_samples', 'unknown')}`\n",
        f"- Baseline prompt: `{baseline.get('prompt', 'baseline.txt')}`\n",
        f"- CoT prompt: `{cot.get('prompt', 'cot_prompt.txt')}`\n",
        "- Shuffle: fixed seed, same sample order\n",
        "- Temperature: 0\n\n",
        "## 对比表\n",
        "| Metric | Baseline | CoT | Delta (CoT - Baseline) |",
        "|---|---:|---:|---:|",
    ]
    for metric, b, c in rows:
        md.append(f"| {metric} | {fmt_pct(b)} | {fmt_pct(c)} | {fmt_pp(c - b)} |")

    md += [
        "\n## 结论\n",
        f"- Accuracy delta: {fmt_pp(cot['accuracy'] - baseline['accuracy'])}\n",
        f"- Macro-F1 delta: {fmt_pp(cot['macro_f1'] - baseline['macro_f1'])}\n",
        f"- Robustness delta: {fmt_pp(cot.get('robustness_score', 0.0) - baseline.get('robustness_score', 0.0))}\n",
    ]
    return "\n".join(md)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two EmotionBench run summaries")
    parser.add_argument("--baseline", required=True, help="Baseline summary JSON path")
    parser.add_argument("--cot", required=True, help="CoT summary JSON path")
    parser.add_argument("--output", required=True, help="Output markdown path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    baseline = load_summary(Path(args.baseline))
    cot = load_summary(Path(args.cot))
    md = build_markdown(baseline, cot)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
