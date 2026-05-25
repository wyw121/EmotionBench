from __future__ import annotations

from collections import defaultdict

from .metrics import evaluate, ResultRow


def compare_normal_vs_adversarial(samples: list[dict], predictions: list[ResultRow]) -> dict:
    grouped = defaultdict(list)
    pred_map = {row.id: row.prediction for row in predictions}

    for sample in samples:
        sample_type = str(sample.get("type", "unknown"))
        label = str(sample.get("label", "neutral")).lower()
        pred = pred_map.get(str(sample.get("id", "")), "neutral")
        grouped[sample_type].append(int(label == pred))

    per_type = {k: sum(v) / len(v) for k, v in grouped.items() if v}
    normal = per_type.get("normal", 0.0)
    adversarial_parts = [per_type.get(key, 0.0) for key in ["sarcasm", "metaphor", "adversarial"] if key in per_type]
    adversarial = sum(adversarial_parts) / len(adversarial_parts) if adversarial_parts else 0.0
    return {
        "normal_accuracy": normal,
        "adversarial_accuracy": adversarial,
        "robustness_score": 0.0 if normal <= 0 else max(0.0, min(1.0, adversarial / normal)),
        "per_type_accuracy": per_type,
    }


def merge_summary(samples: list[dict], predictions: list[ResultRow]) -> dict:
    basic = evaluate(samples, predictions)
    robust = compare_normal_vs_adversarial(samples, predictions)
    return {**basic, **robust}
