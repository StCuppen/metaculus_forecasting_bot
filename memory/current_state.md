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
Set 2026-06-06 (user-chosen, IDs verified live against the OpenRouter catalog). 5 distinct families,
1 run each, for ensemble diversity. Prices are per 1M tokens (in/out) as of 2026-06-06.

| Label | Model ID | Runs | max_tokens | Price in/out |
|-------|----------|------|-----------|--------------|
| DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` | 1 | 10000 | $0.43 / $0.87 |
| GPT-5.4 Mini | `openai/gpt-5.4-mini` | 1 | 9000 | $0.75 / $4.50 |
| Kimi K2.6 | `moonshotai/kimi-k2.6` | 1 | 10000 | $0.68 / $3.42 |
| Gemini 3 Flash | `google/gemini-3-flash-preview` | 1 | 9000 | $0.50 / $3.00 |
| Claude Haiku 4.5 | `anthropic/claude-haiku-4.5` | 1 | 9000 | $1.00 / $5.00 |

Utility-call models (env-overridable), all still default `google/gemini-2.5-flash` as of 2026-06-06:
`EVIDENCE_EXTRACTION_MODEL`, `SEARCH_PLANNER_MODEL`, `RED_TEAM_MODEL`, `CLAIM_AUDIT_MODEL`,
`SIGNPOST_MODEL`. (Cheaper option for cost: `google/gemini-2.5-flash-lite` @ $0.10/$0.40.)

Model-ID gotchas (as of 2026-06-06): `moonshotai/kimi-k2.6:free` exists but `:free` Kimi variants have
historically 404'd — use the paid slug above.

## Improvement backlog
See `docs/forecast_workflow_review_2026-06-06.md` for the full review + prioritized backlog. Top items
(as of 2026-06-06): **P0** AskNews retrieval client (winning bots' provider; keys already templated,
no client yet) + roster refresh; **P1** outside-view/inside-view prompt split, hybrid LLM judge;
**P2** outcome-driven Platt calibration from `forecast_records/`.

## Search provider
- Local default (no dedicated search key): **Perplexity Sonar via OpenRouter** fallback, wired into
  `lean_ensemble.py` 2026-06-06. Provisional quality — a dedicated key is the upgrade path.
- CI (`run_tournament.yaml`) has `EXA_API_KEY` (+ Serper/Brave/Tavily) secrets → uses **Exa** primary.

## Caps / counts
- Rolling forecast cap: **25 predictions per 7-day window** (`league.toml`, as of 2026-02-12).
- 7-day league `dry_run_default = true` (as of 2026-02-12).

## Cost-control defaults (env-tunable; set 2026-06-06)
- Per-run completion tokens (defaults in roster): Kimi **12000**, GPT-5 Mini **10000**,
  Gemini **10000**. Global cap via `FORECAST_RUN_MAX_TOKENS` (0 = use per-model default).
- `FORECAST_MAX_SEARCH_QUERIES` default **6** (was 10) — fewer queries = fewer Sonar/Exa calls.
- `FORECAST_MAX_EVIDENCE_DOCS` default **8** (was 12) — caps per-doc extraction LLM calls.
- Sonar per-query `max_tokens` = 600. Lower all of these further before large batch runs.

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
