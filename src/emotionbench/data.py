from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import json


@dataclass(frozen=True)
class BenchmarkSample:
    id: str
    text: str
    label: str
    type: str
    difficulty: str = "medium"
    context: str = ""


def _read_json_file(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "samples" in data:
        data = data["samples"]
    if not isinstance(data, list):
        raise ValueError(f"Unsupported JSON format in {path}")
    return data


def load_samples(dataset_dir: str | Path) -> list[BenchmarkSample]:
    dataset_dir = Path(dataset_dir)
    samples: list[BenchmarkSample] = []
    combined = dataset_dir / "all.json"
    files = [combined] if combined.exists() else [p for p in sorted(dataset_dir.glob("*.json")) if p.name != "metadata.json"]
    for file_path in files:
        payload = _read_json_file(file_path)
        for item in payload:
            samples.append(
                BenchmarkSample(
                    id=str(item["id"]),
                    text=str(item["text"]),
                    label=str(item["label"]).lower(),
                    type=str(item.get("type", file_path.stem)),
                    difficulty=str(item.get("difficulty", "medium")),
                    context=str(item.get("context", "")),
                )
            )
    return samples


def group_by_type(samples: Iterable[BenchmarkSample]) -> dict[str, list[BenchmarkSample]]:
    grouped: dict[str, list[BenchmarkSample]] = {}
    for sample in samples:
        grouped.setdefault(sample.type, []).append(sample)
    return grouped
