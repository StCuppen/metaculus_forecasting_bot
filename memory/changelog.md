# Changelog

Rolling log of recent sessions. Keep only the last ~5 sessions. Durable lessons belong in `lessons.md`, not here.

---

## 2026-06-06 - Memory versioning + Sonar fallback + git + feedback hardening (Claude Opus)

- **Git activated**: local checkout is now a git repo (`main`), initial snapshot committed so
  `forecast_records/` can be committed and enriched by CI on resolution. No GitHub remote yet (open item).
- **Memory restructure (durable vs volatile)**: added `current_state.md` for dated/volatile facts
  (season, roster, keys, search provider, caps, cost defaults); stripped the stale "Spring 2026"
  target and moved the roster/model-ID tables out of the topical files; added per-file
  `Last reviewed` stamps and a staleness rule in `README.md`.
- **Search resilience**: lean ensemble now falls back to **Perplexity Sonar via OpenRouter** when no
  `EXA_API_KEY` is set (provisional quality), with a loud warning and `search_provider` recorded.
  Unblocks forecasting on an OpenRouter-only setup. CI Exa behavior unchanged. (41 tests still pass.)
- **Feedback/storage hardening**: enrichment made idempotent + numeric Brier + top-level `resolved`/
  `brier`; added read-only `scripts/forecast_scoreboard.py`.
- **Cost controls**: per-run token + search/evidence limits made env-tunable.
- **Roster** updated to user-chosen frontier light models (DeepSeek V4 Pro, GPT-5.4 Mini, Kimi K2.6,
  Gemini 3 Flash, Claude Haiku 4.5), IDs verified live on OpenRouter; see `current_state.md`.
- **Critical bug fixed**: record-write referenced `GateReport.rationale`/`.warnings` (nonexistent) →
  every ensemble run crashed after gating and **never wrote a v1 record** (the "0 rich records"
  finding). Now uses real fields.
- **Sonar fallback made usable**: synthesis docs (sonar:// URLs) were dropped by the http-only filter
  in `_extract_and_score_single`, and Sonar inside `multi_provider_search` is basket-gated and often
  never fires. Fixed both; sole-provider runs now query Sonar directly on top queries. Smoke forecast
  went from forced-abstain (1 synthetic item) to `publish` with 6 evidence items @ mean_rel 0.95.
- **Smoke-test status**: 1 question (US/Iran, id 43259) forecast end-to-end on Sonar-only; enrich +
  scoreboard verified. Full 10-question batch still pending user go-ahead (only 4 Metaculus questions
  resolve within 7 days — supply constraint to resolve with user).
- **Search providers chosen + wired (user decision)**: minimal set = **Linkup** (primary, factuality
  leader) + **Serper** (free Google breadth) + **Sonar** fallback; **Exa optional**, not needed yet.
  New `LinkupClient`; lean search block combines providers with a `_real_key()` placeholder guard.
  Re-verified US/Iran: `serper+linkup`, 8 evidence items, 2 primary sources, mean_rel ~0.8 (was 0
  primary on Sonar-only). Keys live in `.env` (Linkup stored as `LINKEUP_API_KEY` typo; code reads both).
- **Pre-full-run informativeness pass** (from `llm_forecasting_methods_report.md`): neutralized
  extremization (k=1.0); record `crowd_benchmark` + decoupled low-conf shrink from crowd
  (`FORECAST_SHRINK_TO_CROWD`); stamped `run_config` provenance (version/as_of/models/aggregation/
  search); forced + recorded explicit outside view (`BASE_RATE`/`OUTSIDE_VIEW` → `outside_view_probability`
  + `base_rate_texts`); near-term finder min-hours floor 6→24; conditional second Linkup pass
  (`FORECAST_SECOND_PASS`). Search depth doubled (queries 8, linkup 8, evidence 16). Verified: 12
  evidence items, all new record fields populate; 41 tests pass.

## 2026-02-12 - Memory Sync + New Test Forecast (Codex GPT-5)

- Updated memory source-of-truth docs to reflect current lean architecture:
  - `memory/architecture.md` now documents lean ensemble default path, coherence projection, and signpost-triggered reforecast flow.
  - `memory/conventions.md` now captures planned/executed query logging, gate decomposition expectations, informativeness semantics, and numeric unit validation requirements.
  - `memory/lessons.md` now includes practical guidance from transparency/coherence/audit iterations.
- Generated a new forecast on a different short-horizon question:
  - Question: Metaculus Q41336 (`https://www.metaculus.com/questions/41336/will-openai-api-token-prices-fall-before-march-14-2026/`)
  - Artifact: `forecasts/forecast_20260212_172715_Will_OpenAI_API_token_prices_fall_before_March_14.txt`
  - Result: `4.7%`, action `publish`.

## 2026-02-12 - Ticket Closure Pass (Coherence + Audit + Numeric Validation) (Codex GPT-5)

- Expanded coherence module (`bot/coherence.py`) with family detection for threshold ladders, mutually exclusive pairs, and option-set style groups.
- Added family-level constraint projection (`project_family_constraints`) and wired it into `src/jobs/forecast_open.py` with before/after adjustment logging in forecast context and markdown artifacts.
- Upgraded claim audit in `bot/agent/lean_ensemble.py` to use regex extraction plus LLM-assisted hinge-claim extraction, with explicit `evidence_backed` vs `assumption` labeling.
- Added assumptions-note surfacing in summary output when hinge claims are assumptions-heavy.
- Hardened signpost extraction to guarantee 3-5 usable signposts (repair pass + deterministic fallback templates).
- Added numeric unit/order-of-magnitude validation and unit inference in lean numeric path; parse failures now trigger fallback only when outputs are truly unparseable or unit-invalid.
- Added coherence tests for detection/projection paths in `tests/test_coherence.py`.
- Generated fresh test forecast artifact (resolution in next month): `forecasts/forecast_20260212_170935_Will_US_consumer_sentiment_in_March_2026_be_high.txt`.

## 2026-02-12 - Lean Aggregation Architecture + Near-Term Test Forecast (Codex GPT-5)

- Implemented lean multi-run aggregation modules: `bot/aggregation.py`, `bot/publish_gate.py`, and `bot/coherence.py`.
- Added lean forecast prompt templates in `bot/agent/prompts.py` and switched `run_ensemble_forecast` to a delegated lean path (`bot/agent/lean_ensemble.py`).
- New default roster now follows instructions update: 2x Kimi K2.5, 2x GPT-5 Mini, 1x Gemini 2.5 Flash; Exa-only search pass shared across runs.
- Added deterministic publish gate scoring + low-confidence shrinkage and a lightweight red-team adjustment pass.
- Added unit-test coverage for aggregation math, publish gate behavior, and coherence constraints (`tests/test_aggregation.py`, `tests/test_publish_gate.py`, `tests/test_coherence.py`).
- Generated test forecast on Metaculus Q41699 (resolves March 2026): final 55.7%, gate action `publish`, log at `forecasts/forecast_20260212_132716_Will_US_consumer_sentiment_in_March_2026_be_high.txt`.

## 2026-02-12 - Output Transparency + Adaptive Search Refinements (Codex GPT-5)

- Replaced legacy basket planner output in lean pipeline with adaptive `SEARCH(...)` query generation (`bot/agent/lean_ensemble.py`).
- Added explicit `planned_queries` vs `executed_queries` logging and return artifacts.
- Added compact `Top Evidence` section in logs with source/date/relevance/primary flags and snippet hashes.
- Expanded publish-gate transparency with component and metric breakdown (`evidence_count`, `distinct_sources`, `primary_sources`, `mean_relevance`, `freshness_days`).
- Updated confidence semantics to include signal strength, reducing near-coinflip forecasts from `high` to `medium` when appropriate.
- Added `informativeness` flag (`weak_view`/`strong_view`) for downstream consumers.
- Added post-hoc claim audit and signpost extraction artifacts to forecast output and context; added signpost checks in `update_online`.
- Implemented model-based MC and numeric forecast paths (trimmed aggregation + constraints), keeping deterministic fallbacks only on parse failure.

## 2026-02-12 - Tournament Workflow Reliability (Codex GPT-5)

- Fixed `RuntimeError: Package name not found` crash by setting `folder_to_save_reports_to=None`.
- Added `--max-open-questions` CLI flag and workflow input for controllable tournament runs.
- Local smoke test confirmed tournament path completes with `post_attempts=1`.
- Fixed workflow summary guard: now parses `skipped_already_forecasted` to avoid false failure on skip-only runs.
- Pushed fix, re-ran workflow successfully (run `21927817303`): 8 OPEN, 4 binary, 1 posted, 0 errors.
