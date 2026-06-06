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

## Search providers (set 2026-06-06)
Lean search combines providers by capability, each active only with a **real** key (template
placeholders like `1234567890`/`your_*` are ignored via `_real_key()`):
- **Linkup** (primary) — factual + fresh full-text; SimpleQA factuality leader. `LinkupClient` in
  `utils.py`. Returns diverse kinds (Wikipedia/background, Polymarket/market, .gov/authoritative).
  Queries capped by `FORECAST_LINKUP_QUERIES` (default 4); depth via `LINKUP_DEPTH` (default standard).
- **Serper** (free Google breadth + news + `site:` queries) — secondary, via `multi_provider_search`.
- **Sonar** (free via OpenRouter) — fallback/top-up only when evidence is still thin (<3 docs).
- **Exa** — OPTIONAL, only if a real `EXA_API_KEY` is set; covers semantic base-rate/reference-class
  discovery. Decision 2026-06-06: not needed yet; add only if base-rate retrieval feels weak.
- **`.env` key-name note:** the Linkup key is currently stored as `LINKEUP_API_KEY` (typo); code reads
  both `LINKUP_API_KEY` and `LINKEUP_API_KEY`. `EXA_API_KEY`/`BRAVE_API_KEY`/`TAVILY_API_KEY` in `.env`
  are still template placeholders (inactive).
- Live verification (US/Iran question, 2026-06-06): `search_provider=serper+linkup`, 8 evidence items,
  2 primary sources, mean relevance ~0.8, action publish.

## Caps / counts
- Rolling forecast cap: **25 predictions per 7-day window** (`league.toml`, as of 2026-02-12).
- 7-day league `dry_run_default = true` (as of 2026-02-12).

## Cost-control + experiment defaults (env-tunable; updated 2026-06-06)
- Per-run completion tokens (roster defaults): per `current roster` table; global cap via
  `FORECAST_RUN_MAX_TOKENS` (0 = use per-model default).
- `FORECAST_MAX_SEARCH_QUERIES` default **8**; `FORECAST_LINKUP_QUERIES` default **8**;
  `FORECAST_MAX_EVIDENCE_DOCS` default **10** (was 16; dialed back for ~30% cost cut).
- Measured cost ≈ **$0.40/forecast** at depth 16 (~$0.28 at 10). Linkup ~$0.05/forecast.
- `FORECAST_EXTREMIZE_K` default **1.0** (no extremization until validated on resolved corpus).
- `FORECAST_SHRINK_TO_CROWD` default **0** — low-confidence forecasts shrink toward 0.5, not the
  crowd, so skill-vs-crowd stays measurable. Set 1 to anchor to the community prior.
- `FORECAST_SECOND_PASS` default **1** — conditional extra Linkup round only when no resolution/
  primary source was found (not blind 2x search).
- Sonar per-query `max_tokens` = 600. Lower these before large batch runs if cost matters.

## Record schema + layout (2026-06-06, forecast-record/v1)
- Records live in `forecast_records/<platform>/` with name
  `<date>_<platform>_<runtype>_<question>_<digest>.json`; each has a **companion `.md`** (human-readable
  view) written at forecast time. Re-render with `scripts/render_record_markdown.py` (e.g. after enrich).
- Records carry: `run_config` (pipeline_version, as_of_utc, models, aggregation, search caps),
  `crowd_benchmark`, `outside_view_probability` + `base_rate_texts` (binary only), `search_provider`,
  `platform`, `run_type`. `LEAN_PIPELINE_VERSION` in `lean_ensemble.py` — bump on behavior changes.
- **Community prediction is hidden while open on bot-benchmark Qs.** Enrich captures
  `outcome.community_prediction_at_resolution` + top-level `crowd_brier` once revealed at resolution,
  enabling the skill-vs-crowd head-to-head post-hoc.

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
