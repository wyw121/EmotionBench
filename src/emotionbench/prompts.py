from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = ROOT / "prompts"


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def render_prompt(name: str, sample: dict | str) -> str:
    template = load_prompt(name)
    if isinstance(sample, str):
        return template.replace("{{text}}", sample).replace("{{context}}", "")

    text = str(sample.get("text", ""))
    context = str(sample.get("context", ""))
    return template.replace("{{text}}", text).replace("{{context}}", context)
