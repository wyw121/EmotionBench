from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from visualization.confusion_matrix import plot_confusion_matrix


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def set_style() -> None:
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#D0D0D0",
            "axes.labelcolor": "#222222",
            "text.color": "#222222",
            "xtick.color": "#222222",
            "ytick.color": "#222222",
            "font.size": 11,
            "axes.titlesize": 16,
            "axes.labelsize": 12,
            "legend.fontsize": 10,
        }
    )


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def save_figure(fig: plt.Figure, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def load_dataset_distribution(dataset_dir: Path) -> tuple[Counter, Counter, int]:
    metadata_path = dataset_dir / "metadata.json"
    if metadata_path.exists():
        metadata = load_json(metadata_path)
        label_counts = Counter(metadata["label_counts"])
        type_counts = Counter(metadata["type_counts"])
        total = int(metadata["num_samples"])
        return label_counts, type_counts, total

    samples = load_json(dataset_dir / "all.json")
    assert isinstance(samples, list)
    label_counts = Counter(item["label"] for item in samples)
    type_counts = Counter(item["type"] for item in samples)
    return label_counts, type_counts, len(samples)


def plot_distribution_bar(title: str, ylabel: str, counts: Counter, palette: list[str], output_path: Path) -> Path:
    ordered_items = list(counts.items())
    labels = [item[0] for item in ordered_items]
    values = [int(item[1]) for item in ordered_items]
    total = sum(values)
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    bars = ax.bar(labels, values, color=palette[: len(labels)], width=0.62, edgecolor="#FFFFFF", linewidth=1.0)
    ax.set_xlabel("Category")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(values) * 1.22)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, count in zip(bars, values):
        pct = count / total if total else 0.0
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.03,
            f"{count}\n({format_percent(pct)})",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.text(
        0.99,
        0.02,
        f"N = {total}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        color="#555555",
    )
    return save_figure(fig, output_path)


def build_project_tree() -> str:
    lines = [
        "EmotionBench/",
        "├── dataset/",
        "│   ├── adversarial.json",
        "│   ├── metaphor.json",
        "│   ├── normal.json",
        "│   └── sarcasm.json",
        "├── dataset_expanded/",
        "│   ├── all.json",
        "│   ├── metadata.json",
        "│   └── *.json (type-wise splits)",
        "├── evaluation/",
        "├── prompts/",
        "├── results/",
        "│   ├── expanded/",
        "│   ├── runs/",
        "│   ├── charts/",
        "│   └── *.json / *.csv",
        "├── scripts/",
        "├── src/emotionbench/",
        "├── visualization/",
        "├── reports/",
        "├── main.py",
        "└── README.md",
    ]
    return "\n".join(lines)


def plot_project_structure(output_path: Path) -> Path:
    tree_text = build_project_tree()
    fig = plt.figure(figsize=(12.5, 8))
    ax = fig.add_subplot(111)
    ax.axis("off")
    fig.text(
        0.04,
        0.96,
        tree_text,
        family="monospace",
        fontsize=12,
        ha="left",
        va="top",
        linespacing=1.45,
    )
    return save_figure(fig, output_path)


def load_summary(path: Path) -> dict:
    return load_json(path)


def extract_metric(summary: dict, key: str) -> float:
    return float(summary.get(key, 0.0))


def extract_type_metric(summary: dict, category: str) -> float:
    per_type = summary.get("per_type_accuracy", {})
    return float(per_type.get(category, 0.0))


def plot_grouped_comparison(
    title: str,
    records: list[dict[str, object]],
    category_key: str,
    metrics: list[tuple[str, str]],
    output_path: Path,
    rotate_x: bool = False,
) -> Path:
    rows = []
    for record in records:
        label = str(record[category_key])
        for metric_name, metric_key in metrics:
            rows.append({"Label": label, "Metric": metric_name, "Value": float(record[metric_key])})
    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(max(11, len(records) * 1.6), 6.8))
    palette = sns.color_palette("Set2", n_colors=len(metrics))
    sns.barplot(data=df, x="Label", y="Value", hue="Metric", palette=palette, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)
    ax.legend(title="Metric", frameon=True, loc="upper left", bbox_to_anchor=(1.02, 1.0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if rotate_x:
        plt.setp(ax.get_xticklabels(), rotation=20, ha="right")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=2, fontsize=8)

    return save_figure(fig, output_path)


def load_rule_based_baselines(results_root: Path) -> list[dict[str, object]]:
    specs = [
        ("Majority-Negative", results_root / "expanded" / "majority_negative_summary.json"),
        ("Literal Keyword", results_root / "expanded" / "literal_keyword_summary.json"),
        ("Prompt-Aware", results_root / "expanded" / "prompt_aware_summary.json"),
    ]
    records: list[dict[str, object]] = []
    for name, path in specs:
        summary = load_summary(path)
        records.append(
            {
                "Method": name,
                "Accuracy": extract_metric(summary, "accuracy"),
                "Macro-F1": extract_metric(summary, "macro_f1"),
                "Normal Accuracy": extract_metric(summary, "normal_accuracy"),
                "Adversarial Accuracy": extract_metric(summary, "adversarial_accuracy"),
                "Robustness": extract_metric(summary, "robustness_score"),
            }
        )
    return records


def load_real_models(runs_root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(runs_root.glob("compatible/*/level2_paper/compatible_summary.json")):
        summary = load_summary(path)
        model = str(summary.get("model", path.parent.parent.name))
        records.append(
            {
                "Model": model,
                "Accuracy": extract_metric(summary, "accuracy"),
                "Macro-F1": extract_metric(summary, "macro_f1"),
                "Robustness": extract_metric(summary, "robustness_score"),
                "Normal Accuracy": extract_metric(summary, "normal_accuracy"),
                "Sarcasm Accuracy": extract_type_metric(summary, "sarcasm"),
                "Metaphor Accuracy": extract_type_metric(summary, "metaphor"),
                "Adversarial Accuracy": extract_metric(summary, "adversarial_accuracy"),
            }
        )
    records.sort(key=lambda item: float(item["Accuracy"]), reverse=True)
    return records


def load_prompt_comparison(results_root: Path) -> list[dict[str, object]]:
    specs = [
        ("Baseline", results_root / "runs" / "openrouter" / "gemini-2.5-pro" / "baseline_20" / "openrouter_summary.json"),
        ("CoT", results_root / "runs" / "openrouter" / "gemini-2.5-pro" / "cot_20" / "openrouter_summary.json"),
    ]
    records: list[dict[str, object]] = []
    for name, path in specs:
        summary = load_summary(path)
        records.append(
            {
                "Prompt": name,
                "Accuracy": extract_metric(summary, "accuracy"),
                "Macro-F1": extract_metric(summary, "macro_f1"),
                "Normal Accuracy": extract_metric(summary, "normal_accuracy"),
                "Adversarial Accuracy": extract_metric(summary, "adversarial_accuracy"),
                "Robustness": extract_metric(summary, "robustness_score"),
            }
        )
    return records


def plot_real_model_heatmap(records: list[dict[str, object]], output_path: Path) -> Path:
    df = pd.DataFrame(
        [
            {
                "Model": record["Model"],
                "Normal": record["Normal Accuracy"],
                "Sarcasm": record["Sarcasm Accuracy"],
                "Metaphor": record["Metaphor Accuracy"],
                "Adversarial": record["Adversarial Accuracy"],
            }
            for record in records
        ]
    )
    heatmap_df = df.set_index("Model")

    fig, ax = plt.subplots(figsize=(12.5, max(5.0, 0.65 * len(records) + 2.6)))
    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        vmin=0,
        vmax=1,
        linewidths=0.6,
        linecolor="#F2F2F2",
        cbar_kws={"label": "Accuracy"},
        ax=ax,
    )
    ax.set_xlabel("Text Category")
    ax.set_ylabel("Model")
    return save_figure(fig, output_path)


def build_figures(dataset_dir: Path, results_root: Path, output_dir: Path) -> list[Path]:
    set_style()
    output_dir = ensure_output_dir(output_dir)

    label_counts, type_counts, _ = load_dataset_distribution(dataset_dir)

    figure_paths: list[Path] = []
    figure_paths.append(
        plot_distribution_bar(
            "Dataset Label Distribution",
            "Number of Samples",
            label_counts,
            ["#C44E52", "#8172B3", "#4C72B0"],
            output_dir / "dataset_label_distribution.png",
        )
    )
    figure_paths.append(
        plot_distribution_bar(
            "Dataset Type Distribution",
            "Number of Samples",
            type_counts,
            ["#4C72B0", "#55A868", "#C44E52", "#8172B3"],
            output_dir / "dataset_type_distribution.png",
        )
    )
    figure_paths.append(plot_project_structure(output_dir / "project_directory_structure.png"))

    baseline_records = load_rule_based_baselines(results_root)
    figure_paths.append(
        plot_grouped_comparison(
            "Rule-based Baseline Comparison",
            baseline_records,
            "Method",
            [
                ("Accuracy", "Accuracy"),
                ("Macro-F1", "Macro-F1"),
                ("Robustness", "Robustness"),
                ("Adversarial Acc.", "Adversarial Accuracy"),
            ],
            output_dir / "rule_based_baseline_comparison.png",
            rotate_x=True,
        )
    )

    for _, summary_path, filename in [
        ("Majority-Negative", results_root / "expanded" / "majority_negative_summary.json", "majority_negative_confusion_matrix.png"),
        ("Literal-Keyword", results_root / "expanded" / "literal_keyword_summary.json", "literal_keyword_confusion_matrix.png"),
        ("Prompt-Aware", results_root / "expanded" / "prompt_aware_summary.json", "prompt_aware_confusion_matrix.png"),
    ]:
        summary = load_summary(summary_path)
        figure_paths.append(
            plot_confusion_matrix(
                summary["confusion_matrix"],
                summary["labels"],
                output_dir / filename,
            )
        )

    real_model_records = load_real_models(results_root / "runs")
    figure_paths.append(
        plot_grouped_comparison(
            "Real Model Overall Comparison",
            real_model_records,
            "Model",
            [
                ("Accuracy", "Accuracy"),
                ("Macro-F1", "Macro-F1"),
                ("Robustness", "Robustness"),
            ],
            output_dir / "real_model_overall_comparison.png",
            rotate_x=True,
        )
    )
    figure_paths.append(plot_real_model_heatmap(real_model_records, output_dir / "model_type_wise_accuracy_heatmap.png"))

    prompt_records = load_prompt_comparison(results_root)
    figure_paths.append(
        plot_grouped_comparison(
            "Prompt Comparison on Gemini 2.5 Pro (20-sample subset)",
            prompt_records,
            "Prompt",
            [
                ("Accuracy", "Accuracy"),
                ("Macro-F1", "Macro-F1"),
                ("Robustness", "Robustness"),
                ("Adversarial Acc.", "Adversarial Accuracy"),
            ],
            output_dir / "prompt_comparison.png",
            rotate_x=True,
        )
    )

    return figure_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate paper-ready EmotionBench figures")
    parser.add_argument("--dataset-dir", default=str(ROOT / "dataset_expanded"), help="Dataset directory used for distribution plots")
    parser.add_argument("--results-root", default=str(ROOT / "results"), help="Results directory used for comparison plots")
    parser.add_argument("--output-dir", default=str(ROOT / "reports" / "figures"), help="Directory for generated PNG figures")
    parser.add_argument("--write-index", action="store_true", help="Write a short figure index markdown next to the PNGs")
    return parser.parse_args()


def write_index(output_dir: Path, figures: list[Path]) -> Path:
    index = output_dir / "figure_index.md"
    lines = [
        "# EmotionBench Figure Index\n",
        "All figure captions and on-chart text are in English for paper submission.\n",
        "\n| File | Purpose |\n|---|---|\n",
    ]
    descriptions = {
        "dataset_label_distribution.png": "Class distribution over sentiment labels.",
        "dataset_type_distribution.png": "Distribution over benchmark sample types.",
        "project_directory_structure.png": "Condensed repository tree for the project overview section.",
        "rule_based_baseline_comparison.png": "Comparison of rule-based baselines on the expanded benchmark.",
        "majority_negative_confusion_matrix.png": "Confusion matrix for the majority-negative baseline.",
        "literal_keyword_confusion_matrix.png": "Confusion matrix for the literal-keyword baseline.",
        "prompt_aware_confusion_matrix.png": "Confusion matrix for the prompt-aware baseline.",
        "real_model_overall_comparison.png": "Overall performance comparison across real models.",
        "model_type_wise_accuracy_heatmap.png": "Per-type accuracy heatmap for each real model.",
        "prompt_comparison.png": "Baseline versus CoT prompt comparison on the Gemini 2.5 Pro subset.",
    }
    for fig in figures:
        lines.append(f"| `{fig.name}` | {descriptions.get(fig.name, 'Generated figure.')} |\n")
    index.write_text("".join(lines), encoding="utf-8")
    return index


def main() -> int:
    args = parse_args()
    dataset_dir = Path(args.dataset_dir)
    results_root = Path(args.results_root)
    output_dir = Path(args.output_dir)

    figures = build_figures(dataset_dir, results_root, output_dir)
    print("Generated figures:")
    for path in figures:
        print(path)
    if args.write_index:
        index = write_index(output_dir, figures)
        print(index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())