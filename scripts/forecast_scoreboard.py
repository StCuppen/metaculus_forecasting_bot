"""Read-only calibration scoreboard over forecast_records/*.json.

Summarizes the durable forecast-record corpus: how many forecasts exist, how many have
resolved, mean Brier by question type, numeric interval coverage, and the worst-calibrated
resolved binary/MC forecasts. Pure reporting — it never mutates records or calls an LLM.

Outcomes are written by scripts/enrich_forecast_records.py (top-level `resolved` + `brier`,
plus outcome.computed_brier). Run that first so resolved questions are scored.

# TODO(feedback-loop): post-resolution LLM analysis is a deliberate future extension. When a
# corpus of resolved records exists, add a step that asks an LLM to compare forecast vs outcome
# and emit a structured lesson (what was missed, calibration note). Deferred on purpose.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load(records_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(records_dir.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # corrupt/partial file shouldn't kill the report
            print(f"  (skipped unreadable {path.name}: {exc})")
            continue
        data["_file"] = path.name
        records.append(data)
    return records


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only scoreboard over forecast_records.")
    parser.add_argument("--records-dir", default="forecast_records")
    parser.add_argument("--top", type=int, default=5, help="How many worst-calibrated to list.")
    args = parser.parse_args()

    records = _load(Path(args.records_dir))
    total = len(records)
    resolved = [r for r in records if r.get("resolved")]
    pending = total - len(resolved)

    # Brier by type (binary + MC carry a scalar top-level `brier`).
    brier_by_type: dict[str, list[float]] = {"binary": [], "multiple_choice": []}
    numeric_cover_80: list[bool] = []
    for r in resolved:
        scored = (r.get("outcome") or {}).get("computed_brier")
        if not isinstance(scored, dict):
            continue
        t = scored.get("type")
        if t == "binary" and r.get("brier") is not None:
            brier_by_type["binary"].append(float(r["brier"]))
        elif t == "multiple_choice" and r.get("brier") is not None:
            brier_by_type["multiple_choice"].append(float(r["brier"]))
        elif t == "numeric" and scored.get("within_80pct_interval") is not None:
            numeric_cover_80.append(bool(scored["within_80pct_interval"]))

    # Provider / action distributions over the whole corpus.
    providers: dict[str, int] = {}
    actions: dict[str, int] = {}
    for r in records:
        providers[str(r.get("search_provider"))] = providers.get(str(r.get("search_provider")), 0) + 1
        actions[str(r.get("publish_action"))] = actions.get(str(r.get("publish_action")), 0) + 1

    print("=" * 60)
    print(f"FORECAST SCOREBOARD  ({args.records_dir})")
    print("=" * 60)
    print(f"Total records:     {total}")
    print(f"Resolved:          {len(resolved)}")
    print(f"Pending:           {pending}")
    print()
    mb = _mean(brier_by_type["binary"])
    mm = _mean(brier_by_type["multiple_choice"])
    print("Mean Brier (lower is better):")
    print(f"  binary:          {mb:.4f}  (n={len(brier_by_type['binary'])})" if mb is not None else "  binary:          n/a")
    print(f"  multiple_choice: {mm:.4f}  (n={len(brier_by_type['multiple_choice'])})" if mm is not None else "  multiple_choice: n/a")
    if numeric_cover_80:
        cover = sum(numeric_cover_80) / len(numeric_cover_80)
        print(f"  numeric 80% interval coverage: {cover:.0%}  (n={len(numeric_cover_80)}; target ~80%)")
    print()
    print("Search provider distribution:", providers)
    print("Publish action distribution: ", actions)

    # Worst-calibrated resolved forecasts (highest scalar Brier).
    scored_records = [r for r in resolved if r.get("brier") is not None]
    scored_records.sort(key=lambda r: float(r["brier"]), reverse=True)
    if scored_records:
        print()
        print(f"Worst-calibrated resolved (top {args.top}):")
        for r in scored_records[: args.top]:
            title = (r.get("question_title") or r.get("question") or r["_file"])[:70]
            print(f"  brier={float(r['brier']):.3f}  {title}")


if __name__ == "__main__":
    main()
