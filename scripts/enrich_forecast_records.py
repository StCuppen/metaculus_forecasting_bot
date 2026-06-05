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

    return None


def enrich_file(path: Path, sleep_seconds: float) -> bool:
    record = json.loads(path.read_text(encoding="utf-8"))
    post_id = _post_id(record)
    if not post_id:
        return False

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

    path.write_text(json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich forecast_records JSON files with Metaculus outcomes and scores.")
    parser.add_argument("--records-dir", default="forecast_records")
    parser.add_argument("--sleep-seconds", type=float, default=1.0)
    args = parser.parse_args()

    records_dir = Path(args.records_dir)
    updated = 0
    skipped = 0
    failed = 0
    for path in sorted(records_dir.glob("*.json")):
        try:
            if enrich_file(path, sleep_seconds=args.sleep_seconds):
                updated += 1
            else:
                skipped += 1
        except Exception as exc:
            failed += 1
            print(f"failed {path}: {exc}")
    print({"updated": updated, "skipped_no_metaculus_post": skipped, "failed": failed})


if __name__ == "__main__":
    main()
