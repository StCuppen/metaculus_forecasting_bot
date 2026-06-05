# Conventions

> Model roster, model-ID gotchas, and other version-pinned facts are **volatile** and live in
> `current_state.md` (dated). This file holds only durable *rules* that don't expire.

## Lean Pipeline Rules
- Keep legacy staged/ReAct mode available as fallback, but default path is lean ensemble.
- Search planning should be adaptive (`SEARCH(...)` list), not fixed basket decomposition.
- Log both `planned_queries` and `executed_queries` for inspectability.
- Keep evidence visibility high: include top evidence rows with source/date/primary/relevance/bearing/snippet hash.

## Confidence and Gating
- Treat confidence as process quality, not forecast extremity alone.
- Include signal strength (`|p-0.5|`) and an `informativeness` label (`weak_view`/`strong_view`) in summaries.
- Gate logs should include both component scores and raw metrics (`evidence_count`, `distinct_sources`, `freshness_days`, etc.).
- Low-confidence gate action shrinks probability toward base rate/0.5.

## MC/Numeric Rules
- MC: aggregate per-option from model outputs, normalize to sum to 1.
- Numeric: aggregate percentiles 10/25/50/75/90, enforce monotonicity, clamp to bounds.
- Numeric unit and order-of-magnitude checks are required before accepting parsed output.
- Fallback distributions are safety net only when parsing/validation fails.

## Audit/Signpost Rules
- Red-team critique should leave a log artifact even if no change (`ran | no_change`).
- Claim audit must label claims `evidence_backed` vs `assumption`.
- Signpost extraction target is 3-5 events; keep a repair/fallback path when extraction is weak.
- `update_online` should evaluate signposts and trigger re-forecasting when they fire.

## Config
- `league.toml` controls the 7-day league; explicitly set `dry_run` false for live runs.
- Tournament runtime: keep `folder_to_save_reports_to=None` to avoid package-name saver errors.
- A rolling forecast cap applies per 7-day window — current value in `current_state.md`.

## Cost Controls
- Per-run completion caps and search/evidence limits are env-tunable to keep API spend reasonable
  (`FORECAST_RUN_MAX_TOKENS`, `FORECAST_MAX_SEARCH_QUERIES`, `FORECAST_MAX_EVIDENCE_DOCS`); current
  defaults in `current_state.md`. Lower these before large batch runs.

---
_Last reviewed: 2026-06-06. Volatile facts (roster, model IDs, caps, cost defaults) → `current_state.md`._
