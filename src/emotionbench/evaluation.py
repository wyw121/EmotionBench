from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

from .data import BenchmarkSample


@dataclass(frozen=True)
class EvaluationRow:
    id: str
    prediction: str
    raw_output: str = ""


LABEL_ORDER = ["negative", "neutral", "positive"]


def normalize_label(text: str) -> str:
    value = (text or "").strip().lower()
    if not value:
        return "neutral"
    if any(token in value for token in ["negative", "neg", "bad", "down", "angry", "sad", "disgust"]):
        return "negative"
    if any(token in value for token in ["positive", "pos", "good", "up", "happy", "joy", "love"]):
        return "positive"
    if any(token in value for token in ["mixed", "neutral", "unclear", "cannot determine", "unknown"]):
        return "neutral"
    return value if value in LABEL_ORDER else "neutral"


def align_predictions(samples: list[BenchmarkSample], predictions: list[EvaluationRow]) -> tuple[list[str], list[str]]:
    pred_map = {row.id: normalize_label(row.prediction) for row in predictions}
    y_true, y_pred = [], []
    for sample in samples:
        y_true.append(normalize_label(sample.label))
        y_pred.append(pred_map.get(sample.id, "neutral"))
    return y_true, y_pred


def compute_basic_metrics(samples: list[BenchmarkSample], predictions: list[EvaluationRow]) -> dict:
    y_true, y_pred = align_predictions(samples, predictions)
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=LABEL_ORDER).tolist(),
        "labels": LABEL_ORDER,
    }


def per_type_accuracy(samples: list[BenchmarkSample], predictions: list[EvaluationRow]) -> dict[str, float]:
    pred_map = {row.id: normalize_label(row.prediction) for row in predictions}
    grouped: dict[str, list[bool]] = {}
    for sample in samples:
        correct = pred_map.get(sample.id, "neutral") == normalize_label(sample.label)
        grouped.setdefault(sample.type, []).append(correct)
    return {name: (sum(items) / len(items) if items else 0.0) for name, items in grouped.items()}


def robustness_score(normal_acc: float, adversarial_acc: float) -> float:
    if normal_acc <= 0:
        return 0.0
    score = adversarial_acc / normal_acc
    return max(0.0, min(1.0, score))


def summarize_results(samples: list[BenchmarkSample], predictions: list[EvaluationRow]) -> dict:
    basic = compute_basic_metrics(samples, predictions)
    type_acc = per_type_accuracy(samples, predictions)
    return {
        **basic,
        "per_type_accuracy": type_acc,
    }
