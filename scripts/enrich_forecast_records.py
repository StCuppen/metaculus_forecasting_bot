from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import requests

try:
    import dotenv

    dotenv.load_dotenv()
except Exception:
    pass


POST_RE = re.compile(r"metaculus\.com/questions/(\d+)")


def _post_id(record: dict[str, Any]) -> str | None:
    for key in ("question_url", "url"):
        value = str(record.get(key) or "")
        match = POST_RE.search(value)
        if match:
            return match.group(1)
    event = record.get("event") if isinstance(record.get("event"), dict) else {}
    value = str(event.get("url") or "")
    match = POST_RE.search(value)
    return match.group(1) if match else None


def _headers() -> dict[str, str]:
    headers = {"User-Agent": "metaculus-forecast-record-enricher"}
    token = os.getenv("METACULUS_TOKEN")
    if token:
        headers["Authorization"] = f"Token {token}"
    return headers


def _fetch_post(post_id: str) -> dict[str, Any]:
    response = requests.get(
        f"https://www.metaculus.com/api/posts/{post_id}/",
        headers=_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _brier(record: dict[str, Any], question: dict[str, Any]) -> dict[str, Any] | None:
    resolution = question.get("resolution")
    if resolution in (None, "", "annulled"):
        return None

    q_type = question.get("type")
    if q_type == "binary":
        p_yes = record.get("final_probability")
        if p_yes is None:
            return None
        normalized = str(resolution).lower()
        if normalized in {"yes", "true", "1"}:
            y = 1.0
        elif normalized in {"no", "false", "0"}:
            y = 0.0
        else:
            return None
        p = float(p_yes)
        return {"type": "binary", "p_yes": p, "y": y, "brier": (p - y) ** 2}

    if q_type == "multiple_choice":
        probs = record.get("final_mc_probabilities")
        if not isinstance(probs, dict):
            return None
        total = 0.0
        per_option = []
        for option, raw_p in probs.items():
            p = float(raw_p)
            y = 1.0 if str(option) == str(resolution) else 0.0
            squared_error = (p - y) ** 2
            total += squared_error
            per_option.append(
                {
                    "option": str(option),
                    "p": p,
                    "outcome": y,
                    "squared_error": squared_error,
                }
            )
        return {
            "type": "multiple_choice",
            "resolution": str(resolution),
            "brier_sum": total,
            "brier_normalized_by_2": total / 2.0,
            "per_option": per_option,
        }

    if q_type in {"numeric", "date", "discrete"}:
        # Numeric questions are not Brier-scorable; report interval coverage + median error
        # against the stored 10/25/50/75/90 percentiles. Keys are strings in the JSON record.
        raw_pcts = record.get("final_numeric_percentiles")
        actual = _to_float(resolution)
        if not isinstance(raw_pcts, dict) or actual is None:
            return None
        pcts: dict[int, float] = {}
        for k, v in raw_pcts.items():
            ik, fv = _to_int(k), _to_float(v)
            if ik is not None and fv is not None:
                pcts[ik] = fv
        if not {10, 50, 90}.issubset(pcts):
            return None
        return {
            "type": "numeric",
            "resolution_value": actual,
            "median_p50": pcts[50],
            "abs_error_p50": abs(actual - pcts[50]),
            "within_50pct_interval": pcts[25] <= actual <= pcts[75] if {25, 75}.issubset(pcts) else None,
            "within_80pct_interval": pcts[10] <= actual <= pcts[90],
        }

    return None


def _to_float(value: Any) -> float | None:
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _already_resolved(record: dict[str, Any]) -> bool:
    """True if a prior enrich pass already captured a terminal resolution for this record."""
    outcome = record.get("outcome") if isinstance(record.get("outcome"), dict) else {}
    return bool(outcome.get("resolved")) and outcome.get("resolution") not in (None, "")


def enrich_file(path: Path, sleep_seconds: float, force: bool = False) -> str:
    """Returns a status: 'updated' | 'skipped_no_metaculus_post' | 'skipped_already_resolved'."""
    record = json.loads(path.read_text(encoding="utf-8"))
    post_id = _post_id(record)
    if not post_id:
        return "skipped_no_metaculus_post"

    # Idempotency: terminally-resolved records don't change, so don't re-hit the API for them.
    if not force and _already_resolved(record):
        return "skipped_already_resolved"

    post = _fetch_post(post_id)
    question = post.get("question") or {}
    score_data = ((question.get("my_forecasts") or {}).get("score_data") or {})
    latest = ((question.get("my_forecasts") or {}).get("latest") or {})

    record["outcome"] = {
        "source": "metaculus_api",
        "post_id": post_id,
        "title": post.get("title"),
        "post_status": post.get("status"),
        "resolved": post.get("resolved"),
        "resolution": question.get("resolution"),
        "actual_close_time": post.get("actual_close_time"),
        "scheduled_close_time": post.get("scheduled_close_time"),
        "actual_resolve_time": post.get("actual_resolve_time"),
        "scheduled_resolve_time": post.get("scheduled_resolve_time"),
        "question_id": question.get("id"),
        "question_type": question.get("type"),
        "options": question.get("options"),
        "metaculus_score_data": score_data,
        "my_latest_forecast": latest,
        "computed_brier": _brier(record, question),
        "raw_post_subset": {
            "nr_forecasters": post.get("nr_forecasters"),
            "forecasts_count": post.get("forecasts_count"),
            "projects": post.get("projects"),
        },
    }

    # Top-level queryable signals for the scoreboard.
    record["resolved"] = bool(post.get("resolved")) and question.get("resolution") not in (None, "")
    scored = record["outcome"]["computed_brier"]
    if isinstance(scored, dict):
        if scored.get("type") == "binary":
            record["brier"] = scored.get("brier")
        elif scored.get("type") == "multiple_choice":
            record["brier"] = scored.get("brier_normalized_by_2")
        else:
            record["brier"] = None  # numeric/date: see outcome.computed_brier for coverage metrics
    else:
        record["brier"] = None

    path.write_text(json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    return "updated"


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich forecast_records JSON files with Metaculus outcomes and scores.")
    parser.add_argument("--records-dir", default="forecast_records")
    parser.add_argument("--sleep-seconds", type=float, default=1.0)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-fetch and re-score even records already terminally resolved.",
    )
    args = parser.parse_args()

    records_dir = Path(args.records_dir)
    counts = {
        "updated": 0,
        "skipped_no_metaculus_post": 0,
        "skipped_already_resolved": 0,
        "failed": 0,
    }
    for path in sorted(records_dir.rglob("*.json")):
        try:
            status = enrich_file(path, sleep_seconds=args.sleep_seconds, force=args.force)
            counts[status] = counts.get(status, 0) + 1
        except Exception as exc:
            counts["failed"] += 1
            print(f"failed {path}: {exc}")
    print(counts)


if __name__ == "__main__":
    main()
