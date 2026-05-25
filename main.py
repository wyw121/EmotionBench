from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from evaluation.metrics import evaluate, load_dataset, load_predictions  # noqa: E402
from evaluation.robustness import merge_summary  # noqa: E402
from visualization.confusion_matrix import plot_confusion_matrix  # noqa: E402
from visualization.radar_chart import plot_radar_chart  # noqa: E402


def _dataset_dir(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else (ROOT / p)


def build_dataset(output: str | Path) -> Path:
    output = Path(output)
    if not output.is_absolute():
        output = ROOT / output
    output.mkdir(parents=True, exist_ok=True)

    dataset_dir = ROOT / "dataset"
    combined: list[dict] = []
    for file_path in sorted(dataset_dir.glob("*.json")):
        data = load_dataset(file_path)
        shutil.copy2(file_path, output / file_path.name)
        combined.extend(data)

    (output / "all.json").write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {
        "num_samples": len(combined),
        "types": sorted({str(item.get("type", "unknown")) for item in combined}),
    }
    (output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def evaluate_predictions(dataset: str | Path, predictions: str | Path) -> dict:
    dataset_path = _dataset_dir(dataset)
    if dataset_path.is_dir():
        samples = load_dataset(dataset_path)
    else:
        samples = load_dataset(dataset_path)
    preds = load_predictions(predictions)
    return merge_summary(samples, preds)


def save_summary(summary: dict, output: str | Path) -> Path:
    output = Path(output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def visualize(dataset: str | Path, predictions: str | Path, output_dir: str | Path) -> list[Path]:
    summary = evaluate_predictions(dataset, predictions)
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    radar_scores = {
        "accuracy": summary["accuracy"],
        "macro_f1": summary["macro_f1"],
        "normal": summary.get("normal_accuracy", 0.0),
        "adversarial": summary.get("adversarial_accuracy", 0.0),
        "robustness": summary.get("robustness_score", 0.0),
    }
    paths = [
        plot_radar_chart(radar_scores, output_dir / "radar_chart.png"),
        plot_confusion_matrix(summary["confusion_matrix"], summary["labels"], output_dir / "confusion_matrix.png"),
    ]
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="EmotionBench: complex emotional semantics evaluation framework")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-dataset", help="Copy sample dataset files and create a combined dataset")
    build.add_argument("--output", default="dataset_out", help="Output directory for generated dataset artifacts")

    eval_parser = subparsers.add_parser("evaluate", help="Evaluate predictions against the benchmark")
    eval_parser.add_argument("--dataset", default="dataset", help="Dataset directory or combined dataset file")
    eval_parser.add_argument("--predictions", required=True, help="Prediction JSON file")
    eval_parser.add_argument("--output", default="results/summary.json", help="Where to save the summary JSON")

    vis = subparsers.add_parser("visualize", help="Generate charts from evaluation results")
    vis.add_argument("--dataset", default="dataset", help="Dataset directory or combined dataset file")
    vis.add_argument("--predictions", required=True, help="Prediction JSON file")
    vis.add_argument("--output", default="results/charts", help="Output directory for charts")

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.command == "build-dataset":
        output = build_dataset(args.output)
        print(f"Dataset artifacts written to: {output}")
        return 0

    if args.command == "evaluate":
        summary = evaluate_predictions(args.dataset, args.predictions)
        save_summary(summary, args.output)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    if args.command == "visualize":
        summary = evaluate_predictions(args.dataset, args.predictions)
        save_summary(summary, ROOT / "results" / "latest_summary.json")
        paths = visualize(args.dataset, args.predictions, args.output)
        print("\n".join(str(path) for path in paths))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
