from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
import logging
from openai import APIConnectionError, OpenAI, PermissionDeniedError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Configure HTTPX / httpcore debug logging to a file for diagnosing connection issues.
log_file = ROOT / "http_debug.log"
if not logging.getLogger().handlers:
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(fh)
    # set libraries to debug
    logging.getLogger("httpx").setLevel(logging.DEBUG)
    logging.getLogger("httpcore").setLevel(logging.DEBUG)
    logging.getLogger("openai").setLevel(logging.DEBUG)

from evaluation.metrics import ResultRow, load_dataset  # noqa: E402
from evaluation.robustness import merge_summary  # noqa: E402
from emotionbench.prompts import render_prompt  # noqa: E402


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    env_key: str
    model_env: str
    base_url_env: str
    default_base_url: str | None = None


PROVIDERS = {
    "gpt": ProviderConfig(
        name="GPT",
        env_key="OPENAI_API_KEY",
        model_env="OPENAI_MODEL",
        base_url_env="OPENAI_BASE_URL",
        default_base_url=None,
    ),
    "deepseek": ProviderConfig(
        name="DeepSeek",
        env_key="DEEPSEEK_API_KEY",
        model_env="DEEPSEEK_MODEL",
        base_url_env="DEEPSEEK_BASE_URL",
        default_base_url="https://api.deepseek.com",
    ),
    "qwen": ProviderConfig(
        name="Qwen",
        env_key="QWEN_API_KEY",
        model_env="QWEN_MODEL",
        base_url_env="QWEN_BASE_URL",
        default_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    "openrouter": ProviderConfig(
        name="OpenRouter",
        env_key="OPENROUTER_API_KEY",
        model_env="OPENROUTER_MODEL",
        base_url_env="OPENROUTER_BASE_URL",
        default_base_url="https://openrouter.ai/api/v1",
    ),
    "siliconflow": ProviderConfig(
        name="SiliconFlow",
        env_key="SILICONFLOW_API_KEY",
        model_env="SILICONFLOW_MODEL",
        base_url_env="SILICONFLOW_BASE_URL",
        default_base_url="https://api.siliconflow.cn/v1",
    ),
    "compatible": ProviderConfig(
        name="OpenAI-Compatible",
        env_key="COMPATIBLE_API_KEY",
        model_env="COMPATIBLE_MODEL",
        base_url_env="COMPATIBLE_BASE_URL",
        default_base_url="https://api.openai.com/v1",
    ),
    "mock": ProviderConfig(
        name="Mock",
        env_key="",
        model_env="",
        base_url_env="",
        default_base_url=None,
    ),
}


SYSTEM_PROMPT = (
    "You are an expert benchmark assistant for complex emotional semantics. "
    "Return only one final label from: positive, neutral, negative."
)


def build_client(provider: str, model_override: str | None = None) -> tuple[OpenAI, str, str]:
    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")

    cfg = PROVIDERS[provider]
    if provider == "mock":
        raise RuntimeError("Mock provider does not use an API client.")

    api_key = os.getenv(cfg.env_key, "").strip()
    if not api_key:
        raise RuntimeError(
            f"Missing API key for provider '{provider}'. Please set {cfg.env_key} in .env."
        )

    base_url = os.getenv(cfg.base_url_env, cfg.default_base_url or "").strip() or None
    model = (model_override or os.getenv(cfg.model_env, "")).strip()
    if not model:
        raise RuntimeError(f"Missing model name for provider '{provider}'. Please set {cfg.model_env} in .env.")

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=120.0, max_retries=0)
    return client, model, cfg.name


def normalize_label(text: str) -> str:
    value = (text or "").strip().lower()
    if "positive" in value:
        return "positive"
    if "negative" in value:
        return "negative"
    if "neutral" in value or "mixed" in value or "uncertain" in value:
        return "neutral"
    return "neutral"


def call_model(client: OpenAI, model: str, prompt: str, temperature: float = 0.0) -> str:
    # Perform a single request attempt. Retry logic (with client recreation) is handled
    # by the caller to allow recreating the underlying HTTP client between attempts.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=64,
    )
    return response.choices[0].message.content or ""


def mock_generate(sample: dict) -> str:
    text = f"{sample['text']} {sample.get('context', '')}".lower()
    sarcasm_tokens = ["谢谢你哈", "真贴心", "真周到", "真会安排", "great,", "nice job", "呵呵", "‘", "’", "🙂", "太妙了", "真不错"]
    positive_tokens = ["开心", "高兴", "满意", "轻松", "喜欢", "温暖", "顺利", "认可", "感谢", "稳定", "good", "great", "nice"]
    negative_tokens = ["烦", "坏", "糟", "沮丧", "崩溃", "迟到", "停电", "删光", "故障", "broken", "crashed", "失败"]

    sarcasm_hit = any(tok in text for tok in sarcasm_tokens)
    pos_hit = sum(tok in text for tok in positive_tokens)
    neg_hit = sum(tok in text for tok in negative_tokens)

    if sarcasm_hit and neg_hit >= pos_hit:
        label = "negative"
    elif pos_hit > neg_hit:
        label = "positive"
    elif neg_hit > pos_hit:
        label = "negative"
    else:
        label = "neutral"

    return f"reasoning: mock smoke test\nlabel: {label}"


def run_provider(provider: str, dataset_path: Path, prompt_name: str, limit: int | None = None, model_override: str | None = None) -> dict:
    samples = load_dataset(dataset_path)
    if limit:
        samples = samples[:limit]

    predictions: list[ResultRow] = []
    if provider == "mock":
        provider_name = PROVIDERS[provider].name
        model = "heuristic-mock"
        for sample in samples:
            prompt = render_prompt(prompt_name, sample)
            raw_output = mock_generate(sample)
            predictions.append(ResultRow(id=str(sample["id"]), prediction=normalize_label(raw_output), raw_output=raw_output))
    else:
        # Build client per-sample to avoid persistent connection pool issues
        # (some compatible endpoints may drop long-lived connections after N requests).
        total = len(samples)
        for idx, sample in enumerate(samples, start=1):
            prompt = render_prompt(prompt_name, sample)
            # Try multiple times, recreating the client each attempt to avoid persistent
            # connection/pool issues observed with this compatible endpoint.
            last_exc: Exception | None = None
            max_attempts = 4
            for attempt in range(1, max_attempts + 1):
                client, model, provider_name = build_client(provider, model_override=model_override)
                print(f"[PROGRESS] provider={provider_name} model={model} start sample={idx}/{total} attempt={attempt}/{max_attempts}")
                try:
                    raw_output = call_model(client, model, prompt)
                    predictions.append(ResultRow(id=str(sample["id"]), prediction=normalize_label(raw_output), raw_output=raw_output))
                    # close underlying client if possible to avoid leaking sockets
                    try:
                        if hasattr(client, "close"):
                            client.close()
                        elif hasattr(client, "_client") and hasattr(client._client, "close"):
                            client._client.close()
                    except Exception:
                        pass
                    break
                except PermissionDeniedError as exc:
                    message = str(exc)
                    if "token quota" in message or "pre_consume_token_quota_failed" in message:
                        raise RuntimeError(
                            "API quota is insufficient for this run. Please top up the account or reduce the sample count / switch to a cheaper model."
                        ) from exc
                    raise
                except APIConnectionError as exc:
                    last_exc = exc
                    print(f"[WARN] transient connection error on attempt {attempt}/{max_attempts}; retrying after backoff...")
                    # exponential backoff, longer waits to avoid repeated disconnect at fixed count
                    try:
                        if hasattr(client, "close"):
                            client.close()
                        elif hasattr(client, "_client") and hasattr(client._client, "close"):
                            client._client.close()
                    except Exception:
                        pass
                    time.sleep(1.0 * attempt)
                    continue
                except Exception as exc:
                    # unexpected error, record and re-raise
                    raise
            else:
                # all attempts failed
                raise RuntimeError("API connection failed after multiple retries. Please check the proxy/server stability.") from last_exc

            # brief pause to reduce request burst and avoid server-side rate/keep-alive limits
            try:
                time.sleep(1.0)
            except Exception:
                pass

            if idx == 1 or idx == total or idx % 10 == 0:
                print(f"[PROGRESS] provider={provider_name} model={model} sample={idx}/{total}")

    summary = merge_summary(samples, predictions)
    summary.update(
        {
            "provider": provider_name,
            "model": model,
            "num_samples": len(samples),
            "prompt": prompt_name,
        }
    )
    return {
        "summary": summary,
        "predictions": [row.__dict__ for row in predictions],
    }


def save_outputs(provider: str, payload: dict, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / f"{provider}_summary.json"
    preds_path = output_dir / f"{provider}_predictions.json"
    manifest_path = output_dir / "manifest.json"
    summary_path.write_text(json.dumps(payload["summary"], ensure_ascii=False, indent=2), encoding="utf-8")
    preds_path.write_text(json.dumps(payload["predictions"], ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "schema_version": "1.0",
        "benchmark": "EmotionBench",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": payload["summary"].get("provider"),
        "model": payload["summary"].get("model"),
        "prompt": payload["summary"].get("prompt"),
        "num_samples": payload["summary"].get("num_samples"),
        "output_files": {
            "summary": summary_path.name,
            "predictions": preds_path.name,
        },
        "metrics": ["accuracy", "macro_f1", "per_type_accuracy", "robustness_score", "confusion_matrix"],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary_path, preds_path


def append_csv_row(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["provider", "model", "num_samples", "accuracy", "strict_accuracy", "macro_f1", "normal_accuracy", "adversarial_accuracy", "robustness_score", "format_valid_rate", "invalid_output_count"]
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({k: summary.get(k, "") for k in fieldnames})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EmotionBench on real LLM APIs")
    parser.add_argument("--provider", choices=PROVIDERS.keys(), required=True, help="Which provider to use")
    parser.add_argument("--model", default=None, help="Override model name instead of reading from .env")
    parser.add_argument("--dataset", default="dataset_expanded", help="Dataset directory or combined JSON file")
    parser.add_argument("--prompt", default="baseline.txt", help="Prompt template file in prompts/")
    parser.add_argument("--limit", type=int, default=None, help="Optional sample limit for a cheap smoke test")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle samples with a fixed seed before applying the limit")
    parser.add_argument("--seed", type=int, default=42, help="Random seed used when shuffling samples")
    parser.add_argument("--output", default="results/real_models", help="Output directory")
    return parser.parse_args()


def main() -> int:
    load_dotenv(ROOT / ".env")
    args = parse_args()
    dataset_path = (ROOT / args.dataset) if not Path(args.dataset).is_absolute() else Path(args.dataset)
    output_dir = (ROOT / args.output) if not Path(args.output).is_absolute() else Path(args.output)

    if args.shuffle:
        rng = __import__("random").Random(args.seed)
        samples = load_dataset(dataset_path)
        rng.shuffle(samples)
        tmp_path = output_dir / "_shuffled_dataset.json"
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
        dataset_path = tmp_path

    payload = run_provider(args.provider, dataset_path, args.prompt, args.limit, model_override=args.model)
    summary_path, preds_path = save_outputs(args.provider, payload, output_dir)
    append_csv_row(output_dir / "leaderboard.csv", payload["summary"])

    run_config = {
        "provider": args.provider,
        "dataset": str(dataset_path),
        "prompt": args.prompt,
        "limit": args.limit,
        "shuffle": args.shuffle,
        "seed": args.seed,
        "output_dir": str(output_dir),
    }
    (output_dir / "run_config.json").write_text(json.dumps(run_config, ensure_ascii=False, indent=2), encoding="utf-8")

    if payload["summary"].get("format_valid_rate", 1.0) < 0.8:
        print(f"[WARN] Low format_valid_rate={payload['summary'].get('format_valid_rate'):.2f}; raw outputs are not well-formed labels.")

    print(f"Summary saved to: {summary_path}")
    print(f"Predictions saved to: {preds_path}")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
