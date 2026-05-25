from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEVELS = {
    0: {"limit": 10, "label": "smoke"},
    1: {"limit": 20, "label": "diagnostic"},
    2: {"limit": 101, "label": "paper"},
}

DEFAULT_PROMPT = "baseline.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EmotionBench Level 0/1/2 suite for multiple models")
    parser.add_argument("--provider", default="siliconflow", help="Provider name supported by run_real_model_benchmark.py")
    parser.add_argument("--models", nargs="+", required=True, help="Model IDs to test")
    parser.add_argument("--levels", nargs="+", type=int, default=[0, 1, 2], choices=[0, 1, 2], help="Levels to run")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt template used for all levels")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle samples before applying the level limit")
    parser.add_argument("--seed", type=int, default=42, help="Shuffle seed")
    parser.add_argument("--dataset", default="dataset_expanded", help="Dataset directory or JSON file")
    parser.add_argument("--output-root", default="results/runs", help="Root folder for results")
    return parser.parse_args()


def run_one(provider: str, model: str, level: int, prompt: str, dataset: str, output_root: str, shuffle: bool, seed: int) -> None:
    spec = LEVELS[level]
    model_dir = model.replace("/", "__").replace(" ", "_")
    out_dir = Path(output_root) / provider / model_dir / f"level{level}_{spec['label']}"
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_real_model_benchmark.py"),
        "--provider",
        provider,
        "--model",
        model,
        "--dataset",
        dataset,
        "--prompt",
        prompt,
        "--limit",
        str(spec["limit"]),
        "--output",
        str(out_dir),
        "--seed",
        str(seed),
    ]
    if shuffle:
        cmd.append("--shuffle")
    print(f"[RUN] provider={provider} model={model} level={level} prompt={prompt} -> {out_dir}")
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()
    failures: list[tuple[str, int, str]] = []
    for model in args.models:
        for level in args.levels:
            try:
                run_one(args.provider, model, level, args.prompt, args.dataset, args.output_root, args.shuffle, args.seed)
            except subprocess.CalledProcessError as exc:
                failures.append((model, level, str(exc)))
                print(f"[FAIL] provider={args.provider} model={model} level={level}: {exc}")
                continue
    if failures:
        print("\n[SUMMARY] Some runs failed:")
        for model, level, err in failures:
            print(f"- model={model} level={level}: {err}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
