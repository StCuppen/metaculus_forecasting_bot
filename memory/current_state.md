# Current State (volatile)

> **Last verified: 2026-06-06.** This file is the single home for facts that **expire**: model
> versions, the active season/tournament, rolling counts, search provider, and CI wiring. Every line
> is tagged with the date it was last confirmed. **If `Last verified` is more than ~30 days old, treat
> every entry here as suspect and re-verify against the code/API before trusting it.** Durable
> invariants (pipeline structure, gating rules) live in `architecture.md` / `conventions.md` instead.

## Active forecasting target
- Live Metaculus season: **Metaculus Cup Summer 2026** (as of 2026-06-06).
- The tournament workflow no longer hardcodes a season — target is set via the `tournament_id`
  workflow input or the `TOURNAMENT_ID` env var, else the `forecasting_tools` library default
  (as of 2026-06-06). (Historic note: it used to hardcode `metaculus-cup-spring-2026`.)

## Model roster (in code: `bot/agent/lean_ensemble.py::_default_forecast_model_families`)
As of 2026-06-06 the default ensemble is:

| Slot | Model ID | Runs | Notes |
|------|----------|------|-------|
| Primary researcher | `moonshotai/kimi-k2.5` | 2 | Paid only (`:free` → 404). |
| Budget / third voice | `openai/gpt-5-mini` | 2 | May 400 on some OpenRouter accounts — verify access. |
| Primary reasoner | `google/gemini-2.5-flash` | 1 | Also the default for utility calls below. |

Utility-call models (env-overridable), all default `google/gemini-2.5-flash` as of 2026-06-06:
`EVIDENCE_EXTRACTION_MODEL`, `SEARCH_PLANNER_MODEL`, `RED_TEAM_MODEL`, `CLAIM_AUDIT_MODEL`,
`SIGNPOST_MODEL`.

Model-ID gotchas (as of 2026-02-12, re-verify): `google/gemini-3-flash-preview` valid on OpenRouter;
`moonshotai/kimi-k2.5:free` returns 404 (use paid).

**Pending refresh (requested 2026-06-06):** move to frontier *light* models including cheaper ones
(e.g. a DeepSeek "flash"-class model). Verify actual current OpenRouter IDs before swapping — do not
assume an ID string exists. Tracked in the workflow-review backlog.

## Search provider
- Local default (no dedicated search key): **Perplexity Sonar via OpenRouter** fallback, wired into
  `lean_ensemble.py` 2026-06-06. Provisional quality — a dedicated key is the upgrade path.
- CI (`run_tournament.yaml`) has `EXA_API_KEY` (+ Serper/Brave/Tavily) secrets → uses **Exa** primary.

## Caps / counts
- Rolling forecast cap: **25 predictions per 7-day window** (`league.toml`, as of 2026-02-12).
- 7-day league `dry_run_default = true` (as of 2026-02-12).

## Active CI workflows (`.github/workflows/`)
- `run_tournament.yaml` — tournament forecasts; commits `forecast_records/` back (cron disabled;
  triggered manually / via external cron-job.org). As of 2026-06-06.
- `test_custom_urls.yaml` — ad-hoc URL forecasts. As of 2026-06-06.
- `enrich_forecast_records.yaml` — daily 06:17 UTC; fetches Metaculus outcomes + Brier into
  `forecast_records/` and commits back. As of 2026-06-06.

## Required keys (runtime)
`OPENROUTER_API_KEY` (all LLM calls + Sonar search) and `METACULUS_TOKEN` (questions + outcomes) are
the only two strictly required. Search keys (`EXA_API_KEY`/Serper/Brave/Tavily) are optional upgrades.
As of 2026-06-06.
