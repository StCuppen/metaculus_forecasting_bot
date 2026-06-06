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


def _fmt_pct(p: Any) -> str:
    try:
        return f"{float(p) * 100:.1f}%"
    except (TypeError, ValueError):
        return "n/a"


def _append_text_block(lines: list[str], title: str, value: Any, max_chars: int = 4000) -> None:
    text = str(value or "").strip()
    if not text:
        return
    lines.append(f"### {title}")
    lines.append("")
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n\n[truncated]"
    lines.append(text)
    lines.append("")


def render_record_markdown(record: dict[str, Any]) -> str:
    """Render a human-readable Markdown view of a forecast record."""
    g = record.get("gate_report") or {}
    agg = record.get("aggregated_forecast") or {}
    out = record.get("outcome") or {}
    cb = record.get("crowd_benchmark") or {}
    L: list[str] = []

    L.append(f"# {record.get('question_title') or record.get('question') or 'Forecast'}")
    L.append("")
    L.append(f"- **Platform / run type:** {record.get('platform','?')} / {record.get('run_type','?')}")
    L.append(f"- **Question type:** {record.get('question_type','?')}")
    if record.get("question_url"):
        L.append(f"- **URL:** {record.get('question_url')}")
    L.append(f"- **Forecast date (UTC):** {record.get('generated_at_utc','?')}")
    rc = record.get("run_config") or {}
    if rc:
        L.append(f"- **Pipeline:** {rc.get('pipeline_version','?')} · models: {', '.join(rc.get('models') or [])}")
    L.append("")

    # Source question details
    if any(record.get(k) for k in ("background_info", "resolution_criteria", "fine_print", "canonical_spec")):
        L.append("## Question details")
        _append_text_block(L, "Background / context", record.get("background_info"))
        _append_text_block(L, "Resolution criteria", record.get("resolution_criteria"))
        _append_text_block(L, "Fine print", record.get("fine_print"))
        _append_text_block(L, "Canonical spec", record.get("canonical_spec"))

    # Final forecast
    L.append("## Final forecast")
    qt = record.get("question_type")
    if qt == "multiple_choice" and isinstance(record.get("final_mc_probabilities"), dict):
        L.append("")
        L.append("| Option | Probability |")
        L.append("|---|---|")
        for opt, p in sorted(record["final_mc_probabilities"].items(), key=lambda kv: -float(kv[1])):
            L.append(f"| {opt} | {_fmt_pct(p)} |")
    elif qt in ("numeric", "date", "discrete") and isinstance(record.get("final_numeric_percentiles"), dict):
        L.append("")
        L.append("| Percentile | Value |")
        L.append("|---|---|")
        for k in sorted(record["final_numeric_percentiles"], key=lambda x: int(x)):
            L.append(f"| P{k} | {record['final_numeric_percentiles'][k]} |")
    else:
        L.append(f"- **Probability: {_fmt_pct(record.get('final_probability'))}**")
    L.append(f"- Action: **{record.get('publish_action','?')}** · Confidence: {g.get('confidence_class','?')} "
             f"· Informativeness: {record.get('informativeness','?')}")
    if record.get("outside_view_probability") is not None:
        L.append(f"- Outside-view (base rate) probability: {_fmt_pct(record.get('outside_view_probability'))}")
    L.append("")

    # Outcome / benchmark
    L.append("## Outcome / benchmark")
    L.append(f"- Resolved: {'yes' if record.get('resolved') else 'no (pending)'}"
             + (f" — resolution: **{out.get('resolution')}**" if out.get('resolution') else ""))
    if record.get("brier") is not None:
        crowd_b = (record.get("crowd_brier") or {}).get("brier") if isinstance(record.get("crowd_brier"), dict) else None
        line = f"- Our Brier: {record.get('brier')}"
        if crowd_b is not None:
            line += f"  vs  crowd Brier: {crowd_b}  ({'we win' if record['brier'] < crowd_b else 'crowd wins'})"
        L.append(line)
    cp = cb.get("metaculus_community_prediction")
    cp_res = out.get("community_prediction_at_resolution")
    if cp is not None:
        L.append(f"- Community prediction (at forecast): {_fmt_pct(cp)}")
    if isinstance(cp_res, dict) and cp_res.get("centers") is not None:
        L.append(f"- Community prediction (revealed): centers={cp_res.get('centers')} "
                 f"(n={cp_res.get('forecaster_count')})")
    if cp is None and not (isinstance(cp_res, dict) and cp_res.get("centers") is not None):
        L.append("- Community prediction: not available (hidden for this question while open)")
    L.append("")

    # Gate
    L.append("## Publish gate")
    L.append(f"- evidence={g.get('evidence_count')} · primary_sources={g.get('primary_sources')} "
             f"· distinct={g.get('distinct_sources')} · mean_relevance={g.get('mean_relevance')} "
             f"· freshness_days={g.get('freshness_days')}")
    L.append(f"- gate_score={g.get('gate_score')} · dispersion={agg.get('dispersion')} · n_runs={agg.get('n_runs')}")
    for r in (g.get("reasons") or []):
        L.append(f"  - {r}")
    L.append("")

    # Search
    L.append("## Search")
    L.append(f"- Provider: `{record.get('search_provider')}`")
    if record.get("planned_queries"):
        L.append("- Planned queries:")
        for q in record["planned_queries"]:
            L.append(f"  - {q}")
    if record.get("executed_queries"):
        L.append("- Executed queries:")
        for q in record["executed_queries"]:
            L.append(f"  - {q}")
    L.append("")

    # Evidence
    te = record.get("top_evidence") or []
    if te:
        L.append(f"## Retrieved evidence ({len(te)} items)")
        for e in te:
            if not isinstance(e, dict):
                continue
            rel = e.get("relevance")
            prim = "primary" if e.get("primary") else "secondary"
            src = e.get("source") or e.get("source_name") or ""
            url = e.get("url") or ""
            snip = (e.get("snippet") or e.get("content") or "").strip().replace("\n", " ")
            L.append(f"- **[{rel}]** ({prim}) {src} — {snip[:300]}")
            if url and not str(url).startswith("sonar://") and not str(url).startswith("local://"):
                L.append(f"  <{url}>")
        L.append("")

    # Base rates
    if record.get("base_rate_texts"):
        L.append("## Base rates (per model)")
        for b in record["base_rate_texts"]:
            L.append(f"- {b}")
        L.append("")

    # Model reasoning
    L.append("## Model reasoning")
    for row in (record.get("individual_results") or []):
        if not isinstance(row, dict):
            continue
        cfg = row.get("config") or {}
        res = row.get("result") or {}
        diag = (res.get("diagnostics") or {}) if isinstance(res, dict) else {}
        label = cfg.get("label") or cfg.get("name") or "model"
        p = res.get("probability") if isinstance(res, dict) else None
        ov = diag.get("outside_view_probability")
        head = f"### {label} — p={_fmt_pct(p)}"
        if ov is not None:
            head += f" (outside-view {_fmt_pct(ov)})"
        L.append(head)
        if diag.get("base_rate_text"):
            L.append(f"_Base rate:_ {diag.get('base_rate_text')}")
        expl = res.get("explanation") if isinstance(res, dict) else None
        L.append("")
        L.append((expl or "_(no output)_").strip())
        L.append("")

    # Audits
    if record.get("red_team_artifact"):
        L.append("## Red-team critique")
        L.append(str(record["red_team_artifact"]).strip())
        L.append("")
    if record.get("summary_text"):
        L.append("## Summary")
        L.append(str(record["summary_text"]).strip())
        L.append("")

    # Cost / tokens
    tu = record.get("token_usage") or {}
    if isinstance(tu, dict) and tu:
        tot = sum(int(u.get("total", 0)) for u in tu.values() if isinstance(u, dict))
        L.append("## Tokens")
        L.append(f"- Total tokens across {len(tu)} calls: {tot:,}")
        L.append("")

    return "\n".join(L)


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

    # Companion human-readable Markdown view next to the JSON.
    try:
        path.with_suffix(".md").write_text(render_record_markdown(enriched), encoding="utf-8")
    except Exception:
        pass

    return str(path)
