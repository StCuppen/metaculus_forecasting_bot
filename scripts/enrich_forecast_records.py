from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bot.agent.forecast_records import render_record_markdown

try:
    import dotenv

    dotenv.load_dotenv()
except Exception:
    pass


POST_RE = re.compile(r"metaculus\.com/questions/(\d+)")
POLY_EVENT_RE = re.compile(r"polymarket\.com/event/([A-Za-z0-9_-]+)")


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


def _polymarket_event_slug(record: dict[str, Any]) -> str | None:
    for key in ("question_url", "url", "question", "question_title", "background_info", "resolution_criteria"):
        value = str(record.get(key) or "")
        match = POLY_EVENT_RE.search(value)
        if match:
            return match.group(1)
    event = record.get("event") if isinstance(record.get("event"), dict) else {}
    for key in ("url", "slug"):
        value = str(event.get(key) or "")
        match = POLY_EVENT_RE.search(value)
        if match:
            return match.group(1)
        if value and "/" not in value and " " not in value:
            return value
    return None


def _headers() -> dict[str, str]:
    headers = {"User-Agent": "metaculus-forecast-record-enricher"}
    token = os.getenv("METACULUS_TOKEN")
    if token:
        headers["Authorization"] = f"Token {token}"
    return headers


def _polymarket_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "User-Agent": "forecast-record-enricher/1.0",
    }


def _fetch_post(post_id: str) -> dict[str, Any]:
    response = requests.get(
        f"https://www.metaculus.com/api/posts/{post_id}/",
        headers=_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _fetch_polymarket_event(slug: str) -> dict[str, Any]:
    response = requests.get(
        "https://gamma-api.polymarket.com/events",
        params={"slug": slug},
        headers=_polymarket_headers(),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list) and payload:
        return payload[0]
    if isinstance(payload, dict):
        return payload
    raise ValueError(f"No Polymarket event found for slug={slug}")


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


def _parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def _market_label(market: dict[str, Any]) -> str:
    label = str(market.get("groupItemTitle") or "").strip()
    if label:
        return label
    question = str(market.get("question") or "").strip()
    if question.lower().startswith("will "):
        return question[5:].split(" win ", 1)[0].strip(" ?") or question
    return question or str(market.get("slug") or market.get("id") or "unknown")


def _market_binary_resolution(market: dict[str, Any]) -> str | None:
    winning = market.get("winningOutcome") or market.get("outcome")
    if isinstance(winning, str):
        normalized = winning.strip().lower()
        if normalized in {"yes", "true", "1"}:
            return "Yes"
        if normalized in {"no", "false", "0"}:
            return "No"

    # Some Gamma records omit winningOutcome but carry final one-hot prices.
    outcomes = [str(x).strip().lower() for x in _parse_json_list(market.get("outcomes"))]
    prices = [_to_float(x) for x in _parse_json_list(market.get("outcomePrices"))]
    if len(outcomes) == len(prices) and "yes" in outcomes and "no" in outcomes:
        yes_i = outcomes.index("yes")
        no_i = outcomes.index("no")
        yes_p = prices[yes_i]
        no_p = prices[no_i]
        if yes_p is not None and no_p is not None:
            if yes_p >= 0.999 and no_p <= 0.001:
                return "Yes"
            if no_p >= 0.999 and yes_p <= 0.001:
                return "No"
    return None


def _polymarket_markets_subset(event: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for market in event.get("markets") or []:
        if not isinstance(market, dict):
            continue
        rows.append(
            {
                "id": market.get("id"),
                "slug": market.get("slug"),
                "question": market.get("question"),
                "label": _market_label(market),
                "closed": market.get("closed"),
                "resolved": market.get("resolved"),
                "winningOutcome": market.get("winningOutcome"),
                "outcome": market.get("outcome"),
                "outcomePrices": market.get("outcomePrices"),
                "endDate": market.get("endDate"),
            }
        )
    return rows


def _polymarket_resolution(record: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    markets = [m for m in (event.get("markets") or []) if isinstance(m, dict)]
    q_type = str(record.get("question_type") or "").lower()
    if q_type == "mc":
        q_type = "multiple_choice"

    if q_type == "binary":
        title = str(record.get("question_title") or record.get("question") or "").split("\n", 1)[0].strip()
        selected = None
        if len(markets) == 1:
            selected = markets[0]
        else:
            for market in markets:
                if str(market.get("question") or "").strip() == title:
                    selected = market
                    break
        selected = selected or (markets[0] if markets else None)
        if not selected:
            return {"resolved": False, "resolution": None, "question_type": "binary", "computed_brier": None}
        is_terminal = bool(selected.get("resolved") or selected.get("closed"))
        resolution = _market_binary_resolution(selected) if is_terminal else None
        computed = _brier(record, {"type": "binary", "resolution": resolution}) if resolution else None
        return {
            "resolved": bool(resolution),
            "resolution": resolution,
            "question_type": "binary",
            "market_id": selected.get("id"),
            "market_slug": selected.get("slug"),
            "computed_brier": computed,
        }

    # Grouped Polymarket events are represented as one binary market per option.
    yes_labels: list[str] = []
    terminal_count = 0
    for market in markets:
        is_terminal = bool(market.get("resolved") or market.get("closed"))
        if is_terminal:
            terminal_count += 1
        if _market_binary_resolution(market) == "Yes":
            yes_labels.append(_market_label(market))
    resolution = yes_labels[0] if len(yes_labels) == 1 else None
    computed = _brier(record, {"type": "multiple_choice", "resolution": resolution}) if resolution else None
    return {
        "resolved": bool(resolution),
        "resolution": resolution,
        "question_type": "multiple_choice",
        "resolved_option_count": len(yes_labels),
        "terminal_market_count": terminal_count,
        "computed_brier": computed,
    }


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


def _community_prediction(question: dict[str, Any]) -> dict[str, Any] | None:
    """Community prediction (hidden while open on bot-benchmark Qs; revealed at resolution)."""
    agg = (question.get("aggregations") or {}).get("recency_weighted") or {}
    latest = agg.get("latest") or {}
    centers = latest.get("centers")
    if centers is None:
        centers = question.get("community_prediction")
    if centers is None:
        return None
    return {"centers": centers, "forecaster_count": latest.get("forecaster_count")}


def _crowd_brier(question: dict[str, Any], community: dict[str, Any] | None) -> dict[str, Any] | None:
    """Crowd's own Brier on a resolved binary question, for the head-to-head vs our forecast."""
    if not community or question.get("type") != "binary":
        return None
    res = str(question.get("resolution") or "").lower()
    if res not in {"yes", "no", "true", "false", "1", "0"}:
        return None
    centers = community.get("centers")
    p = _to_float(centers[0]) if isinstance(centers, list) and centers else None
    if p is None:
        return None
    y = 1.0 if res in {"yes", "true", "1"} else 0.0
    return {"type": "binary", "p_yes": p, "y": y, "brier": (p - y) ** 2}


def _already_resolved(record: dict[str, Any]) -> bool:
    """True if a prior enrich pass already captured a terminal resolution for this record."""
    outcome = record.get("outcome") if isinstance(record.get("outcome"), dict) else {}
    return bool(outcome.get("resolved")) and outcome.get("resolution") not in (None, "")


def enrich_file(path: Path, sleep_seconds: float, force: bool = False) -> str:
    """Returns a status: 'updated' | 'skipped_no_source' | 'skipped_already_resolved'."""
    record = json.loads(path.read_text(encoding="utf-8"))
    post_id = _post_id(record)
    event_slug = None if post_id else _polymarket_event_slug(record)
    if not post_id and not event_slug:
        return "skipped_no_source"

    # Idempotency: terminally-resolved records don't change, so don't re-hit the API for them.
    if not force and _already_resolved(record):
        return "skipped_already_resolved"

    if post_id:
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
            "community_prediction_at_resolution": _community_prediction(question),
            "computed_brier": _brier(record, question),
            "raw_post_subset": {
                "nr_forecasters": post.get("nr_forecasters"),
                "forecasts_count": post.get("forecasts_count"),
                "projects": post.get("projects"),
            },
        }

        # Top-level queryable signals for the scoreboard.
        record["resolved"] = bool(post.get("resolved")) and question.get("resolution") not in (None, "")
        # Head-to-head: the crowd's own Brier (available once a hidden-CP question resolves).
        record["crowd_brier"] = _crowd_brier(question, record["outcome"]["community_prediction_at_resolution"])
    else:
        assert event_slug is not None
        event = _fetch_polymarket_event(event_slug)
        resolution = _polymarket_resolution(record, event)
        record["outcome"] = {
            "source": "polymarket_gamma_api",
            "event_slug": event_slug,
            "event_id": event.get("id"),
            "title": event.get("title"),
            "event_closed": event.get("closed"),
            "event_active": event.get("active"),
            "endDate": event.get("endDate"),
            "resolved": resolution.get("resolved"),
            "resolution": resolution.get("resolution"),
            "question_type": resolution.get("question_type"),
            "market_id": resolution.get("market_id"),
            "market_slug": resolution.get("market_slug"),
            "resolved_option_count": resolution.get("resolved_option_count"),
            "terminal_market_count": resolution.get("terminal_market_count"),
            "computed_brier": resolution.get("computed_brier"),
            "raw_markets_subset": _polymarket_markets_subset(event),
        }
        record["resolved"] = bool(record["outcome"]["resolved"])
        record["crowd_brier"] = None

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
    path.with_suffix(".md").write_text(render_record_markdown(record), encoding="utf-8")
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    return "updated"


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich forecast_records JSON files with outcomes and scores.")
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
        "skipped_no_source": 0,
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
