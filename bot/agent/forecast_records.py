from __future__ import annotations

import dataclasses
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_RECORD_DIR = "forecast_records"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_slug(value: str, max_len: int = 80) -> str:
    cleaned = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in value.strip())
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    return (cleaned or "forecast")[:max_len]


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    if dataclasses.is_dataclass(value):
        return jsonable(dataclasses.asdict(value))
    if hasattr(value, "to_dict"):
        try:
            return jsonable(value.to_dict())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return jsonable(vars(value))
        except Exception:
            pass
    return repr(value)


def _platform_for(record: dict[str, Any]) -> str:
    """Infer the platform from the record (URL or question text)."""
    explicit = str(record.get("platform") or "").strip().lower()
    if explicit in {"metaculus", "polymarket"}:
        return explicit
    blob = " ".join(
        str(record.get(k) or "")
        for k in ("question_url", "url", "question", "question_title")
    ).lower()
    if "metaculus" in blob:
        return "metaculus"
    if "polymarket" in blob:
        return "polymarket"
    return "other"


def write_forecast_record(record: dict[str, Any], record_dir: str | None = None) -> str:
    """Persist a durable rich JSON forecast record inside the repository.

    Records are organized for easy human inspection: one subfolder per platform, and a
    descriptive filename of the form `<date>_<platform>_<runtype>_<question>_<digest>.json`.
    """
    root = Path(record_dir or os.getenv("FORECAST_RECORD_DIR") or DEFAULT_RECORD_DIR)

    platform = _platform_for(record)
    run_type = safe_slug(str(record.get("run_type") or os.getenv("FORECAST_RUN_TYPE") or "oneoff"), 24)
    question = str(record.get("question_title") or record.get("question") or "forecast")

    timestamp = str(record.get("generated_at_utc") or utc_now_iso())
    try:
        date_str = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y%m%d-%H%M%S")
    except ValueError:
        date_str = timestamp.replace(":", "").replace("-", "")[:15]

    digest_input = json.dumps(jsonable(record), sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()[:8]

    subdir = root / platform
    subdir.mkdir(parents=True, exist_ok=True)
    filename = f"{date_str}_{platform}_{run_type}_{safe_slug(question, 60)}_{digest}.json"
    path = subdir / filename

    enriched = dict(record)
    enriched.setdefault("schema_version", "forecast-record/v1")
    enriched.setdefault("written_at_utc", utc_now_iso())
    enriched["platform"] = platform
    enriched["run_type"] = run_type
    enriched["record_file"] = str(path)

    path.write_text(
        json.dumps(jsonable(enriched), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    return str(path)
