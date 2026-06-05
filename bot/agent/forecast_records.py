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


def write_forecast_record(record: dict[str, Any], record_dir: str | None = None) -> str:
    """Persist a durable rich JSON forecast record inside the repository."""
    root = Path(record_dir or os.getenv("FORECAST_RECORD_DIR") or DEFAULT_RECORD_DIR)
    root.mkdir(parents=True, exist_ok=True)

    question = str(record.get("question_title") or record.get("question") or "forecast")
    timestamp = str(record.get("generated_at_utc") or utc_now_iso())
    digest_input = json.dumps(jsonable(record), sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()[:12]
    filename = f"{timestamp.replace(':', '').replace('-', '')}_{safe_slug(question)}_{digest}.json"
    path = root / filename

    enriched = dict(record)
    enriched.setdefault("schema_version", "forecast-record/v1")
    enriched.setdefault("written_at_utc", utc_now_iso())
    enriched["record_file"] = str(path)

    path.write_text(
        json.dumps(jsonable(enriched), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    return str(path)
