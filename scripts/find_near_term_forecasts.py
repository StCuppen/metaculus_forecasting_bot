"""Find forecastable Metaculus and Polymarket questions resolving soon."""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


METACULUS_API = "https://www.metaculus.com/api/posts/"
POLYMARKET_MARKETS_API = "https://gamma-api.polymarket.com/markets"


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def metaculus_session() -> requests.Session:
    session = requests.Session()
    token = os.getenv("METACULUS_TOKEN")
    if token:
        session.headers["Authorization"] = f"Token {token}"
    session.headers["User-Agent"] = "forecast-candidate-finder"
    return session


def question_url(post: dict[str, Any]) -> str:
    slug = quote(str(post.get("slug") or "question"))
    return f"https://www.metaculus.com/questions/{post['id']}/{slug}/"


def project_names(post: dict[str, Any]) -> list[str]:
    projects = post.get("projects") or {}
    names: list[str] = []
    for value in projects.values():
        if isinstance(value, list):
            names.extend(str(item["name"]) for item in value if isinstance(item, dict) and item.get("name"))
        elif isinstance(value, dict) and value.get("name"):
            names.append(str(value["name"]))
    return sorted(set(names))


def find_metaculus(now: datetime, window_start: datetime, window_end: datetime, limit: int) -> list[dict[str, Any]]:
    session = metaculus_session()
    results: list[dict[str, Any]] = []
    offset = 0

    while len(results) < limit and offset < 500:
        response = session.get(
            METACULUS_API,
            params={
                "limit": 100,
                "offset": offset,
                "statuses": "open",
                "order_by": "scheduled_resolve_time",
            },
            timeout=30,
        )
        response.raise_for_status()
        posts = response.json().get("results", [])
        if not posts:
            break

        for post in posts:
            question = post.get("question") or {}
            resolve_time = parse_dt(post.get("scheduled_resolve_time") or question.get("scheduled_resolve_time"))
            close_time = parse_dt(post.get("scheduled_close_time") or question.get("scheduled_close_time"))
            actual_close_time = parse_dt(post.get("actual_close_time") or question.get("actual_close_time"))
            if not resolve_time:
                continue
            if resolve_time <= now:
                continue
            if resolve_time < window_start:
                continue
            if resolve_time > window_end:
                return results[:limit]
            if actual_close_time and actual_close_time <= now:
                continue
            if close_time and close_time <= now:
                continue
            if str(post.get("status")) != "open" or str(question.get("status")) != "open":
                continue

            aggregations = question.get("aggregations") or {}
            unweighted = aggregations.get("unweighted") or {}
            results.append(
                {
                    "source": "metaculus",
                    "id": post.get("id"),
                    "question_id": question.get("id"),
                    "title": post.get("title"),
                    "url": question_url(post),
                    "type": question.get("type"),
                    "scheduled_close_time": iso_z(close_time) if close_time else None,
                    "scheduled_resolve_time": iso_z(resolve_time),
                    "projects": project_names(post),
                    "nr_forecasters": post.get("nr_forecasters"),
                    "forecasts_count": post.get("forecasts_count"),
                    "community_latest": unweighted.get("latest"),
                }
            )
            if len(results) >= limit:
                break

        offset += len(posts)
        time.sleep(0.2)

    return results[:limit]


def polymarket_url(market: dict[str, Any]) -> str:
    events = market.get("events") or []
    if events and isinstance(events[0], dict) and events[0].get("slug"):
        return f"https://polymarket.com/event/{events[0]['slug']}?tid={market.get('id')}"
    slug = market.get("slug") or market.get("id")
    return f"https://polymarket.com/market/{slug}"


def parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def is_intraday_up_down(question: str | None) -> bool:
    text = (question or "").lower()
    return " up or down - " in text


def find_polymarket(
    now: datetime,
    window_start: datetime,
    window_end: datetime,
    limit: int,
    include_intraday: bool,
) -> list[dict[str, Any]]:
    response = requests.get(
        POLYMARKET_MARKETS_API,
        params={
            "active": "true",
            "closed": "false",
            "limit": max(100, limit * 20),
            "end_date_min": iso_z(window_start),
            "end_date_max": iso_z(window_end),
            "order": "endDate",
            "ascending": "true",
        },
        headers={"User-Agent": "forecast-candidate-finder"},
        timeout=30,
    )
    response.raise_for_status()
    candidates: list[dict[str, Any]] = []
    for market in response.json():
        end_date = parse_dt(market.get("endDate"))
        if not end_date or end_date < window_start or end_date > window_end:
            continue
        if market.get("closed") or not market.get("active"):
            continue
        if not include_intraday and is_intraday_up_down(market.get("question")):
            continue
        outcomes = parse_json_list(market.get("outcomes"))
        prices = parse_json_list(market.get("outcomePrices"))
        if len(outcomes) != 2:
            continue
        candidates.append(
            {
                "source": "polymarket",
                "id": market.get("id"),
                "question": market.get("question"),
                "url": polymarket_url(market),
                "end_time": iso_z(end_date),
                "outcomes": outcomes,
                "outcome_prices": prices,
                "liquidity": float(market.get("liquidityNum") or market.get("liquidity") or 0),
                "volume": float(market.get("volumeNum") or market.get("volume") or 0),
                "accepting_orders": market.get("acceptingOrders"),
                "description": market.get("description"),
            }
        )

    candidates.sort(key=lambda item: (item["end_time"], -item["liquidity"]))
    return candidates[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--limit", type=int, default=10)
    # Floor of 24h excludes near-determined questions (<1 day to close), whose outcomes carry
    # little forecasting signal and would inflate Brier scores in the empirical test.
    parser.add_argument("--min-hours", type=float, default=24.0)
    parser.add_argument("--include-intraday", action="store_true")
    parser.add_argument("--output-dir", default="forecast_candidates")
    parser.add_argument("--as-of", help="UTC ISO datetime override, e.g. 2026-06-05T00:00:00Z")
    args = parser.parse_args()

    now = parse_dt(args.as_of) if args.as_of else datetime.now(timezone.utc)
    if now is None:
        raise ValueError("--as-of must be an ISO datetime")
    window_start = now + timedelta(hours=args.min_hours)
    window_end = now + timedelta(days=args.days)

    metaculus = find_metaculus(now, window_start, window_end, args.limit)
    polymarket = find_polymarket(now, window_start, window_end, args.limit, args.include_intraday)
    combined = (metaculus + polymarket)[: args.limit]

    output = {
        "generated_at_utc": iso_z(datetime.now(timezone.utc)),
        "as_of_utc": iso_z(now),
        "window_start_utc": iso_z(window_start),
        "window_end_utc": iso_z(window_end),
        "days": args.days,
        "min_hours": args.min_hours,
        "include_intraday": args.include_intraday,
        "counts": {
            "metaculus": len(metaculus),
            "polymarket": len(polymarket),
            "selected": len(combined),
        },
        "selected": combined,
        "metaculus_candidates": metaculus,
        "polymarket_candidates": polymarket,
    }

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"near_term_{now:%Y%m%d}.json"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True, sort_keys=True), encoding="utf-8")
    print(output_path)
    print(json.dumps(output["counts"], indent=2))


if __name__ == "__main__":
    main()
