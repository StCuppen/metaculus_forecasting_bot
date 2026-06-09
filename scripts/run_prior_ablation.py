from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bot.agent.agent_experiment import run_ensemble_forecast


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _question_from_record(path: Path) -> dict[str, Any]:
    record = _load_json(path)
    return {
        "id": path.stem,
        "question": record.get("question_title") or record.get("question"),
        "question_type": record.get("question_type", "binary"),
        "options": record.get("options") or [],
        "lower_bound": (record.get("numeric_bounds") or {}).get("lower_bound"),
        "upper_bound": (record.get("numeric_bounds") or {}).get("upper_bound"),
        "unit": (record.get("numeric_bounds") or {}).get("unit"),
        "source_record": str(path),
    }


def _load_spec(path: Path) -> dict[str, Any]:
    spec = _load_json(path)
    questions: list[dict[str, Any]] = []
    for item in spec.get("questions") or []:
        if item.get("record_path"):
            q = _question_from_record(Path(item["record_path"]))
            q.update({k: v for k, v in item.items() if k != "record_path"})
        else:
            q = dict(item)
        questions.append(q)
    spec["questions"] = questions
    return spec


def _token_totals(result: dict[str, Any]) -> dict[str, int]:
    """Aggregate prompt/completion/total tokens across all usage labels."""
    totals = {"prompt": 0, "completion": 0, "total": 0}
    for usage in (result.get("token_usage") or {}).values():
        if isinstance(usage, dict):
            for key in totals:
                totals[key] += int(usage.get(key, 0) or 0)
    return totals


async def _run_arm(question: dict[str, Any], arm: dict[str, Any]) -> dict[str, Any]:
    started = time.time()
    old_run_type = os.environ.get("FORECAST_RUN_TYPE")
    os.environ["FORECAST_RUN_TYPE"] = f"prior_ablation_{arm['name']}"
    try:
        result = await run_ensemble_forecast(
            question=str(question["question"]),
            publish_to_metaculus=False,
            question_type=str(question.get("question_type") or "binary"),
            options=question.get("options") or None,
            lower_bound=question.get("lower_bound"),
            upper_bound=question.get("upper_bound"),
            unit=question.get("unit"),
            prior_packet=arm.get("prior_packet"),
        )
    finally:
        if old_run_type is None:
            os.environ.pop("FORECAST_RUN_TYPE", None)
        else:
            os.environ["FORECAST_RUN_TYPE"] = old_run_type

    token_totals = _token_totals(result)
    return {
        "arm": arm["name"],
        "question_id": question.get("id"),
        "runtime_s": time.time() - started,
        "final_probability": result.get("final_probability"),
        "mc_probabilities": result.get("mc_probabilities"),
        "numeric_percentiles": result.get("numeric_percentiles"),
        "publish_action": result.get("publish_action"),
        "forecast_record_path": result.get("forecast_record_path"),
        "token_total": token_totals["total"],
        "token_prompt": token_totals["prompt"],
        "token_completion": token_totals["completion"],
        "token_usage_by_label": result.get("token_usage") or {},
        "summary_text": result.get("summary_text"),
    }


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run prior/base-rate packet ablations on forecast records.")
    parser.add_argument("--spec", required=True, help="Ablation JSON spec.")
    parser.add_argument("--out", default="forecasts/prior_ablation_results.json")
    parser.add_argument("--dry-run", action="store_true", help="Print expanded spec without calling models.")
    args = parser.parse_args()

    spec = _load_spec(Path(args.spec))
    if args.dry_run:
        print(json.dumps(spec, indent=2, ensure_ascii=False))
        return

    rows = []
    for question in spec.get("questions") or []:
        arms = question.get("arms") or spec.get("arms") or []
        for arm in arms:
            if arm.get("skip"):
                continue
            print(f"running question={question.get('id')} arm={arm.get('name')}")
            rows.append(await _run_arm(question, arm))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"spec": spec, "results": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"saved {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
