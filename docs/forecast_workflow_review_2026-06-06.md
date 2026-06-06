# Forecasting Workflow Review — 2026-06-06

**Author:** Claude (Opus) session. **Status:** review + prioritized backlog. Nothing here is applied
automatically except the two items already shipped this session (Sonar fallback, cost knobs).

## Method
Read the live lean pipeline (`bot/agent/lean_ensemble.py`, `prompts.py`, `aggregation.py`,
`publish_gate.py`, `coherence.py`) and compared it against current best practice from: the Metaculus
AI Benchmark / FutureEval tournament results and writeups, the Q2-2025 winning bot (Panshul), the
Metaculus `forecasting-tools` template, and 2025 research (AIA Forecaster; "approaching human-level
forecasting"/superforecaster-commandments work; RLVR-on-Brier calibration). Sources at the bottom.

## What the pipeline does today (one paragraph)
One adaptive `SEARCH()` planning pass → shared evidence bundle (Exa, now Sonar-via-OpenRouter
fallback) → per-doc LLM extraction + relevance scoring → 5 parallel model runs (2× Kimi K2.5, 2×
GPT-5 Mini, 1× Gemini 2.5 Flash) using a superforecaster-style binary/MC/numeric prompt → deterministic
trimmed-mean aggregation with evidence-weighted extremization → deterministic publish gate with hard
evidence floors → red-team critique, claim audit, signpost extraction → full markdown trace + durable
JSON record. Coherence projection enforces cross-question constraints.

## Strengths (keep these)
- **Structured superforecaster prompt** — status-quo weighting, explicit base-rate/reference-class,
  YES/NO scenarios, deadline reasoning, resolution-criteria misread check. This is exactly the
  "commandments" pattern shown to lift accuracy. Good.
- **Ensemble + trimmed aggregation + extremization** — matches the single most repeated tournament
  lesson ("aggregation and iteration are the key best practices"). AIA also uses post-hoc
  extremization/Platt scaling.
- **Deterministic risk gate with hard floors** — evidence floors, forced abstain at <3 items, neutral
  agreement at n=1. Strong, and aligned with "risk first" repo principle.
- **Full decision traces + durable records** — enables the iteration loop the tournament writeups call
  out as decisive (manually reviewing past reasoning to improve prompts).

## Fundamental flaws / gaps (ranked)
1. **Search quality is the likely binding constraint.** Winning bots overwhelmingly use **AskNews**
   (reported best context precision; the most common provider among prize winners); Perplexity/Sonar
   is second-tier and, per operator memory, weak standalone. We currently run Exa (CI) or Sonar
   (local fallback, shipped today) and have **no AskNews client** despite keys already in
   `.env.template`. Evidence quality caps everything downstream — this is the highest-leverage gap.
2. **No outside-view / inside-view separation.** The Q2 winner explicitly produces a separate
   base-rate "outside view" report and a current-evidence "inside view" report before predicting. Our
   prompt asks for a base rate inline, which models often skip or confabulate. Separating the passes
   is a cheap, evidence-backed structural win.
3. **Aggregation is purely statistical; the LLM `JUDGE_SYNTHESIS_PROMPT` is unused in the lean path.**
   Trimmed mean is robust but discards reasoning about *why* models disagree. AIA's "supervisor
   reconciliation" suggests a hybrid: statistical aggregate as the anchor, with an LLM
   adjudicator allowed to adjust within a bounded band when it can cite which evidence resolves the
   disagreement. (Guard against the known failure of LLM judges over-trusting verbose runs.)
4. **No calibration learned from outcomes.** Extremization `k` is a fixed env constant. AIA and the
   RLVR work both calibrate against realized Brier. Once the record corpus has resolved questions, fit
   a simple Platt/temperature scaling per question-type from `forecast_records/` and feed it back.
   (The scoreboard added this session is the substrate for this.)
5. **Model roster is stale.** Tournament data: "bots using the most up-to-date models rank top-6";
   models matter more than scaffolding. Current roster predates several frontier light releases.
6. **Single search-plan pass, no iterative deepening.** Top agentic bots do 6-7 step research loops;
   we do one planning pass. Cheap to allow 1 conditional follow-up round when evidence is thin/stale,
   gated by token budget (cost-control knobs now exist).

## Update 2026-06-06 (search resolved)
The search-quality gap below has been addressed without AskNews: **Linkup** (SimpleQA factuality
leader) is now the primary retrieval client, combined with **Serper** (free Google breadth) and
**Sonar** fallback, with a real-key guard. Verified: 8 evidence items + 2 primary sources on a live
question (vs 0 primary on Sonar-only). The P0 "AskNews client" item below is therefore superseded;
**Exa** stays an optional add for semantic base-rate discovery only. Remaining backlog items (P1/P2)
stand.

## Prioritized backlog (pick from this; don't do blindly)
- **P0 — AskNews retrieval client** — ~~build~~ **superseded 2026-06-06** by Linkup + Serper + Sonar
  (user opted not to use AskNews). Keep Exa as an optional semantic/base-rate add.
- **P0 — Roster refresh** to frontier light models incl. a cheap DeepSeek-class model (verify live
  OpenRouter IDs first; see proposal below).
- **P1 — Outside-view/inside-view split** in the binary prompt (two short passes or one prompt with
  two mandatory labeled sections + a parser check that the base-rate section is non-empty).
- **P1 — Hybrid judge** layer: bounded LLM reconciliation around the trimmed-mean anchor, logged,
  off by default behind a flag until A/B'd on the resolved corpus.
- **P2 — Outcome-driven calibration**: fit per-type Platt/temperature scaling from resolved records;
  replace the fixed extremization constant once n is meaningful.
- **P2 — Conditional second research round** when freshness/relevance is below a threshold.
- **P3 — Polymarket outcome enrichment** so non-Metaculus forecasts also close the loop.

## Model roster refresh proposal (verify IDs before applying)
Tournament evidence says model freshness is one of the biggest levers. Proposed direction (to be
confirmed against the live OpenRouter catalog — **do not assume any ID string exists**):
- Keep one strong reasoner as anchor (current Gemini 2.5 Flash / GPT-5 Mini class).
- Add a cheap frontier "flash"-class model (the user named a DeepSeek flash variant) as a diversity
  voice — confirm the exact current OpenRouter slug at apply time.
- Maintain ≥3 *genuinely different* model families for ensemble diversity (avoid 2 near-identical
  siblings, which inflates false agreement). Record the chosen roster + date in `current_state.md`.

This is intentionally left as a proposal: the user wants to pick the models. Forecasting is parked
until that choice + go-ahead.

## Sources
- [Q2 AI Benchmark Results: Pros Maintain Clear Lead (EA Forum)](https://forum.effectivealtruism.org/posts/F2stjK9wHSy3HPEC9/q2-ai-benchmark-results-pros-maintain-clear-lead)
- [Winners of Q2 2025 AI Benchmark Tournament (Metaculus)](https://www.metaculus.com/notebooks/39140/winners-of-q2-2025-ai-benchmark-tournament/)
- [FutureEval Methodology (Metaculus)](https://www.metaculus.com/futureeval/methodology/)
- [Panshul Q2 winning bot (GitHub)](https://github.com/Panshul42/Forecasting_Bot_Q2)
- [Metaculus metac-bot-template (GitHub)](https://github.com/Metaculus/metac-bot-template)
- [AskNews documentation](https://docs.asknews.app/en)
- [AIA Forecaster: Technical Report (arXiv 2511.07678)](https://arxiv.org/abs/2511.07678)
- [Superforecasting LLM (EmergentMind overview)](https://www.emergentmind.com/topics/superforecasting-llm)
