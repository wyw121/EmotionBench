from __future__ import annotations

from pathlib import Path
import json

from .metrics import ResultRow, normalize_label


def parse_label_from_text(text: str) -> str:
    return normalize_label(text)


def load_result_rows(path: str | Path) -> list[ResultRow]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict) and "predictions" in payload:
        payload = payload["predictions"]
    return [
        ResultRow(
            id=str(item["id"]),
            prediction=parse_label_from_text(str(item.get("prediction", item.get("label", "")))),
            raw_output=str(item.get("raw_output", "")),
        )
        for item in payload
    ]
