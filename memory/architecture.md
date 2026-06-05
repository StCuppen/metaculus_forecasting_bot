# Architecture

## Pipelines

### Tournament Pipeline
- Entry point: `bot/main_forecast_pipeline.py`
- Target season/tournament is **volatile** → see `current_state.md` (set via `tournament_id` input /
  `TOURNAMENT_ID` env, not hardcoded).
- Triggered by: `.github/workflows/run_tournament.yaml` (scheduled + manual dispatch)
- CLI modes: `--mode tournament`, `--mode urls`, `--mode test_questions`
- Key CLI flags: `--force-repost`, `--max-open-questions`, `--question-types`
- Output: `./forecast_reports.json` (or `--output-file`), `./forecasts/forecast_{timestamp}_{question}.txt`

### 7-Day Feedback Loop League
- Entry point: `src/jobs/tick.py`
- Flow: ingest -> forecast -> resolve -> score -> update
- Config: `league.toml` (`dry_run_default=true` by default)
- Prediction artifacts: `predictions/feedback_loop/`

## Forecasting Engine

### Default Path: Lean Ensemble
- Entry: `bot/agent/agent_experiment.py` -> `run_ensemble_forecast(...)` delegates to `bot/agent/lean_ensemble.py`.
- Search: one adaptive `SEARCH(...)` planning pass + primary source targeting (heuristic domain lookup), then shared evidence bundle.
- Evidence: after search, LLM extraction+scoring per doc (parallel, gemini-2.5-flash) produces `EnrichedEvidence` with extracted claims and real relevance scores (0.0-1.0). Fallback to raw docs if extraction fails.
- Primary sources: question-aware detection via `_PRIMARY_SOURCE_TEMPLATES` lookup + `_is_primary_source_url(url, question_domains)`.
- Runs: roster families expanded into parallel runs (default: 2x Kimi K2.5, 2x GPT-5 Mini, 1x Gemini 2.5 Flash).
- Aggregation: trimmed mean + evidence-weighted extremization (`effective_k = 1.0 + (k-1.0) * evidence_score`) in `bot/aggregation.py`.
- Gate: deterministic publish gate with hard floors (primary_sources=0 caps at 0.5, mean_relevance<0.7 caps at 0.6, <3 evidence items forces abstain, n=1 runs get neutral 0.5 agreement) in `bot/publish_gate.py`.
- Signposts: magnitudes anchored to final probability and clipped to [1%, 99%] via `_anchor_signposts`.
- Critique/audit: red-team critique before gate, plus post-hoc claim audit and signpost extraction.
- Output: structured markdown report with 10 sections (header, search process, evidence summary, model runs with reasoning, aggregation, gate decision, red team, claim audit, signposts, final summary).

### Question Type Handling
- Binary: direct probability extraction per run.
- Multiple-choice: per-option parsing + trimmed aggregation + `enforce_sum_to_one`.
- Numeric: percentile parsing (10/25/50/75/90) + monotonic repair + bounds clamp + unit sanity checks.
- Fallback distributions are used only when model outputs are unparseable/invalid.

### Coherence and Update Loop
- `bot/coherence.py` provides:
  - family detection (threshold ladders, mutually exclusive pairs, option-set pattern groups),
  - projection constraints (`enforce_sum_to_one`, monotonic ladder projection).
- `src/jobs/forecast_open.py` applies projection before persistence and logs before/after probabilities.
- `src/core/updater.py` + `src/jobs/update_online.py` run signpost checks and can trigger re-forecasting when signposts fire.

## Records & Feedback Loop
- Every ensemble run writes a durable rich JSON record (`forecast-record/v1`) to `forecast_records/`
  via `bot/agent/forecast_records.py` — visible model output, token usage, evidence, gate decision,
  `search_provider`, and (when available) the Metaculus URL for later outcome lookup.
- `scripts/enrich_forecast_records.py` fetches the Metaculus resolution + computes Brier (binary/MC/
  numeric) and writes it back into each record. Idempotent: terminally resolved records are skipped.
- `.github/workflows/enrich_forecast_records.yaml` runs this daily and commits enriched records back,
  so outcomes are fetched automatically once questions resolve.
- `scripts/forecast_scoreboard.py` is a read-only summary (counts, resolved vs pending, mean Brier by
  type). LLM-based post-resolution analysis is a deliberate future extension, not yet implemented.

## Key Files
| File | Purpose |
|------|---------|
| `bot/main_forecast_pipeline.py` | Tournament + URL + test mode entry point |
| `bot/agent/agent_experiment.py` | Forecast bridge into lean ensemble |
| `bot/agent/lean_ensemble.py` | Default forecasting runtime |
| `bot/agent/prompts.py` | Lean binary/MC/numeric prompt templates |
| `bot/aggregation.py` | Trimmed aggregation + confidence class |
| `bot/publish_gate.py` | Publish gate scoring + action selection |
| `bot/coherence.py` | Family detection + constraint projection |
| `src/jobs/tick.py` | 7-day league pipeline |
| `league.toml` | League configuration |
| `.github/workflows/run_tournament.yaml` | Tournament CI workflow |
| `scripts/run_forecast_ablation.py` | Ablation runner scaffold |
| `scripts/enrich_forecast_records.py` | Fetch Metaculus outcomes + Brier into `forecast_records/` |
| `scripts/forecast_scoreboard.py` | Read-only calibration summary over `forecast_records/` |
| `bot/agent/forecast_records.py` | Durable per-forecast JSON record writer (`forecast-record/v1`) |
| `tests/test_evidence_pipeline.py` | Regression coverage for primary-source detection, LLM evidence extraction/scoring, and signpost anchoring |
| `tests/test_publish_gate.py` | Regression coverage for evidence floors, forced abstain, and neutral n=1 agreement behavior |
| `tests/test_aggregation.py` | Regression coverage for evidence-weighted extremization (`effective_k`) calibration math |

---
_Last reviewed: 2026-06-06. Volatile facts (season, roster, keys, CI) live in `current_state.md`._
