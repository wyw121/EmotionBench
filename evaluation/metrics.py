from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Iterable

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

LABELS = ["negative", "neutral", "positive"]


@dataclass(frozen=True)
class ResultRow:
    id: str
    prediction: str
    raw_output: str = ""


def normalize_label(value: str) -> str:
    text = (value or "").strip().lower()
    if not text:
        return "neutral"
    exact = re.search(r"(?<![a-zA-Z])(negative|neutral|positive)(?![a-zA-Z])", text)
    if exact:
        return exact.group(1)
    if any(token in text for token in ["负", "消极", "负面", "悲", "怒", "糟", "坏", "讨厌"]):
        return "negative"
    if any(token in text for token in ["正", "积极", "正面", "喜", "乐", "好", "开心"]):
        return "positive"
    if any(token in text for token in ["neutral", "mixed", "unclear", "unknown", "中性", "平静", "普通"]):
        return "neutral"
    return "neutral"


def is_strict_label_output(value: str) -> bool:
    text = (value or "").strip().lower()
    return text in LABELS


def extract_strict_label(value: str) -> str | None:
    text = (value or "").strip().lower()
    return text if text in LABELS else None


def _load_json(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_predictions(path: str | Path) -> list[ResultRow]:
    data = _load_json(path)
    if isinstance(data, dict) and "predictions" in data:
        data = data["predictions"]
    rows: list[ResultRow] = []
    for item in data:
        rows.append(
            ResultRow(
                id=str(item["id"]),
                prediction=normalize_label(str(item.get("prediction", ""))),
                raw_output=str(item.get("raw_output", "")),
            )
        )
    return rows


def load_dataset(path: str | Path) -> list[dict]:
    samples: list[dict] = []
    path = Path(path)
    if path.is_dir():
        combined = path / "all.json"
        if combined.exists():
            samples = _load_json(combined)
        else:
            for file_path in sorted(path.glob("*.json")):
                if file_path.name in {"metadata.json"}:
                    continue
                payload = _load_json(file_path)
                if isinstance(payload, list):
                    samples.extend(payload)
    else:
        samples = _load_json(path)
    if not isinstance(samples, list):
        raise ValueError(f"Unsupported dataset format: {path}")
    return samples


def align_labels(samples: Iterable[dict], predictions: Iterable[ResultRow]) -> tuple[list[str], list[str]]:
    pred_map = {row.id: row.prediction for row in predictions}
    y_true, y_pred = [], []
    for sample in samples:
        y_true.append(normalize_label(str(sample.get("label", "neutral"))))
        y_pred.append(pred_map.get(str(sample.get("id", "")), "neutral"))
    return y_true, y_pred


def evaluate(samples: Iterable[dict], predictions: Iterable[ResultRow]) -> dict:
    samples = list(samples)
    predictions = list(predictions)
    y_true, y_pred = align_labels(samples, predictions)
    cm = confusion_matrix(y_true, y_pred, labels=LABELS)
    type_acc: dict[str, list[int]] = {}
    pred_map = {row.id: row.prediction for row in predictions}
    for sample in samples:
        sample_type = str(sample.get("type", "unknown"))
        ok = int(pred_map.get(str(sample.get("id", "")), "neutral") == normalize_label(str(sample.get("label", "neutral"))))
        type_acc.setdefault(sample_type, []).append(ok)
    per_type_accuracy = {k: float(sum(v) / len(v)) for k, v in type_acc.items() if v}
    format_valid_flags = [is_strict_label_output(row.raw_output) for row in predictions]
    format_valid_rate = float(sum(format_valid_flags) / len(format_valid_flags)) if format_valid_flags else 0.0
    strict_correct_flags = []
    pred_map = {row.id: row.prediction for row in predictions}
    raw_map = {row.id: row.raw_output for row in predictions}
    for sample in samples:
        sid = str(sample.get("id", ""))
        gold = normalize_label(str(sample.get("label", "neutral")))
        strict_pred = extract_strict_label(raw_map.get(sid, ""))
        strict_correct_flags.append(int(strict_pred is not None and strict_pred == gold))
    strict_accuracy = float(sum(strict_correct_flags) / len(strict_correct_flags)) if strict_correct_flags else 0.0
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "strict_accuracy": strict_accuracy,
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "labels": LABELS,
        "confusion_matrix": cm.tolist(),
        "per_type_accuracy": per_type_accuracy,
        "format_valid_rate": format_valid_rate,
        "invalid_output_count": int(len(format_valid_flags) - sum(format_valid_flags)),
        "support": {label: int(np.sum(np.array(y_true) == label)) for label in LABELS},
    }


def format_metrics_table(metrics: dict) -> str:
    lines = [
        f"Accuracy: {metrics['accuracy']:.3f}",
        f"Macro-F1: {metrics['macro_f1']:.3f}",
    ]
    for name, value in sorted(metrics.get("per_type_accuracy", {}).items()):
        lines.append(f"{name}: {value:.3f}")
    return "\n".join(lines)
