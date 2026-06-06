# LLM Forecasting Methods Report

*Suggested repository path: `docs/llm_forecasting_methods_report.md`.*

## Table of contents

- [Overview](#overview)
- [Architectures and methods](#architectures-and-methods)
- [Public systems and recommended pipeline](#public-systems-and-recommended-pipeline)
- [Probability, calibration, and aggregation](#probability-calibration-and-aggregation)
- [Evaluation and repo design](#evaluation-and-repo-design)
- [Checklist and roadmap](#checklist-and-roadmap)
- [Open questions and annotated bibliography](#open-questions-and-annotated-bibliography)

## Overview

**Executive summary**

The current best evidence says that strong LLM forecasting systems are not “just one prompt.” The systems that consistently do better separate retrieval from forecasting, use structured prompts tied to resolution criteria and time horizon, run multiple independent forecasts, and aggregate them. In the published literature, retrieval plus tuned reasoning materially outperforms naive zero-shot prompting; in public bot practice, higher-performing systems also appear to spend more calls on research, decomposition, and aggregation rather than on one long monologue. The strongest academic result here is Halawi et al.’s retrieval-augmented system, which neared competitive human crowd forecasts on a contamination-controlled test set and improved substantially over baseline zero-shot model performance; the strongest public practitioner signal is from Metaculus FutureEval bot-maker surveys, which report that winners typically split work into research, reasoning, and aggregation phases and made materially more LLM calls per question than non-winners. citeturn6view0turn28view0turn28view5turn36search0turn8search1

A second conclusion is more negative: many intuitively appealing ideas are weak or brittle. Naive chain-of-thought alone does not rescue forecasting; Halawi et al. found untuned zero-shot and scratchpad baselines clustered around or worse than the unskilled 0.25 Brier baseline, and their ablations imply that prompting without retrieval and tuning gives only minor gains. Likewise, recent work on dynamic belief updating finds that LLM revisions are often conservative or inconsistent, and that neither verbalized nor logit-based confidence is clearly superior in that setting. Debate-like or multi-agent systems help mainly when they bring genuinely different evidence, tools, or calibrated decision rules; otherwise they often just multiply correlated errors. citeturn27view1turn29view1turn32view1turn32view5turn31view0

A third conclusion is that crowds and markets remain valuable anchors. Metaculus’s current FutureEval leaderboard still places top models below Metaculus Pro Forecasters and below the Metaculus community baseline, and Metaculus states that pros have won every bot season so far. The broader human-forecasting literature also continues to support training, teaming, tracking, and aggregation, while recent hybrid work such as SAGE shows that human-machine combinations can beat human-only baselines when the combination is explicit and calibrated. The practical implication is that an LLM forecaster should treat crowd or market forecasts as a default benchmark, not as contamination to be ignored. citeturn7view4turn8search2turn24search11turn5search17turn26view0

**Key conclusions**

The highest-confidence implementation recommendations are these. First, parse the question and resolution criteria explicitly, because forecasting quality is heavily constrained by whether the system understands what resolves the question and when. Metaculus itself emphasizes careful question specification and resolution criteria, and its public template bots explicitly inject question text, resolution criteria, fine print, and today’s date into the forecast prompt. citeturn39search15turn17view2turn18view5

Second, keep evidence gathering separate from probability synthesis. Public bot-maker advice says the main bottleneck is the information reaching the final model call, not “reasoning itself,” and Metaculus’s template bots and Halawi et al.’s system both use explicit research stages before probability generation. citeturn8search1turn17view0turn28view0

Third, make base-rate retrieval first-class rather than optional. The human forecasting literature strongly supports the outside view and reference-class thinking, while public forecasting-tool repos now explicitly include “Base Rate Researcher,” “Niche List Researcher,” and Fermi-style estimators. The evidence for decomposition is mixed in general, but outside-view discipline is much better supported than free-form “think hard” prompting. citeturn22search1turn22search11turn20view0turn22search3turn34search4

Fourth, use multiple independent forecasts and aggregate conservatively. The best public template bots already run one research report and multiple forecast samples, then aggregate; Halawi et al. report trimmed mean beating their other tested ensemble rules on validation; RTF reports that a small ensemble of calibrated agents improved over individual agents, while ensembling weakly calibrated base LMs did not. citeturn16view1turn18view2turn28view3turn31view0

Fifth, evaluate with leak-resistant protocols. Forecast evaluation is unusually easy to contaminate through outcome leakage, retrieval leakage, or training-cutoff assumptions. ForecastBench, MIRAI, and FutureEval all move toward dynamic or future-generated test sets, and Paleka et al. detail several quiet failure modes in retrospective backtesting. citeturn11search1turn11search13turn6view5turn8search2turn6view3turn27view5

**Source map**

| Source family | What it contributes | Representative sources |
|---|---|---|
| Forecasting papers | Evidence on what improves forecast accuracy, calibration, aggregation, and hybrid systems | Halawi et al.; ForecastBench; SAGE; Mellers et al.; Gneiting & Raftery; Satopää et al. citeturn6view0turn11search1turn26view0turn5search17turn23search4turn24search1 |
| LLM agent / tool-use papers | Evidence for retrieval, ReAct, self-consistency, hierarchical tool use, confidence elicitation | ReAct; RAG; self-consistency; RTF; Just Ask for Calibration; EVOLVECAST citeturn12search1turn12search2turn12search4turn31view0turn13search2turn32view1 |
| Public bot writeups | Concrete design patterns that practitioners actually use under cost and latency constraints | FutureEval methodology; Q1/Q4/Q2 tournament writeups; bot-maker survey; bot advice; automated prompt engineering analysis citeturn8search2turn38search0turn38search1turn34search15turn36search0turn37search0turn40search1 |
| GitHub repos | Observable implementation structure, file layout, and prompts | `Metaculus/forecasting-tools`; `Metaculus/metac-bot-template`; `No-Stream/metaculus-bot`; `forecastbench`; `metaforecast` citeturn15view0turn15view1turn19view0turn15view6turn15view4 |
| Forecasting platforms | Crowd and market APIs, benchmark baselines, and real-world deployment context | Metaculus API/FAQ; Manifold API; Polymarket API; Good Judgment Open citeturn41search0turn39search15turn41search1turn41search2turn41search19 |

## Architectures and methods

**Taxonomy of LLM forecasting architectures**

The field has converged on a small number of architectural patterns. The simplest is **single-shot forecast generation**, where one prompt receives the question plus some context and emits a probability. This is cheap and easy to benchmark, but alone it is weak: Halawi et al. found that raw models with no retrieval mostly scored around or worse than random guessing on their binary benchmark, and Metaculus’s public practice increasingly treats single-shot bots as baselines rather than competitive systems. citeturn27view1turn21search19

A better pattern is **research-then-forecast**. In Metaculus template bots, `run_research` is distinct from `run_forecast`; research providers can be AskNews, searcher tools, or an LLM-based summarizer, while forecast prompts then force the model to reason about time left, status quo, and yes/no scenarios before giving a percentage. Halawi et al.’s system likewise separates query generation, news retrieval, relevance filtering/reranking, and summarization before reasoning. This separation is currently the most implementation-relevant pattern in both literature and practice. citeturn17view0turn17view2turn28view0turn29view5

A third pattern is **tool-using agentic forecasting**, especially hierarchical ReAct. RTF uses a high-level ReAct planner over low-level agents with Google API access and Python simulation, then aggregates three calibrated agent outputs. Their results suggest that tool use and hierarchical specialization matter more than simply asking the same model to “think more”; without hierarchical planning, they report API failures, timeouts, and context exhaustion. citeturn27view3turn30view1turn31view0

A fourth pattern is **human-machine hybrid forecasting**. SAGE provided machine forecasts to humans, allowed interactive use of model aids, and dynamically combined human and machine forecasts with weights adjusted for assessed skill, overconfidence, and propinquity to resolution. In its randomized competition setting, the hybrid system outperformed a human-only baseline. If your repo may later support human review or editing, SAGE is one of the clearest precedents for building that path in from the start. citeturn26view0

A fifth pattern is **ensemble forecasting across prompts, samples, or models**. Metaculus’s in-house bots typically do internet search, run a roughly 30-line prompt, forecast five times, and submit an aggregation. Public repos increasingly extend that idea to multiple providers, stacked ensembles, and disagreement-resolution passes. The key caveat is that simple plurality of correlated agents is not enough; RTF shows ensembling helps when the base agents are already calibrated, while Halawi et al. show only small differences among simple ensemble rules, with trimmed mean modestly best in their setup. citeturn21search19turn19view0turn31view0turn28view3

**Methods that appear to improve accuracy**

The strongest evidence-backed improvements are in the table below.

| Method | Confidence | What the evidence says | Implementation implication |
|---|---|---|---|
| Retrieval augmentation | High | Halawi et al. show a large jump from no-retrieval baselines to their full system; RTF also improves over base models using tool-based retrieval. citeturn29view1turn31view0 | Build a dedicated retrieval stage with query generation, ranking, and summarization. |
| Separation of research from synthesis | High | Public bot-maker advice says information entering the final call is the main bottleneck; template bots encode this separation directly. citeturn8search1turn17view0 | Use separate modules/classes for search, evidence curation, and probability generation. |
| Multiple independent forecasts + aggregation | High | Template bots use repeated forecasts; Halawi et al. and RTF both report gains from aggregation when applied to calibrated members. citeturn16view1turn28view3turn31view0 | Sample 3–7 independent forecasts and aggregate in probability or logit space. |
| Status-quo / outside-view prompting | Moderate to high | Human forecasting literature strongly supports reference-class and outside-view reasoning; Metaculus template prompts also explicitly emphasize status quo. citeturn22search1turn22search11turn17view2 | Add explicit prompt steps: status quo, base rate, reference class, and “what changes must occur.” |
| Training, teaming, tracking, calibrated aggregation | High | Mellers et al. and Good Judgment summarize these as major drivers of superforecasting performance. citeturn5search17turn5search25turn24search11 | Translate into code as versioned updates, multiple forecasters, and post-resolution score tracking. |
| Verbalized confidence elicitation | Moderate | “Just Ask for Calibration” finds verbalized confidences are often better calibrated than token probabilities for RLHF models. citeturn13search2turn13search10 | Ask for explicit probabilities/confidence JSON; do not rely only on token logprobs. |
| Proper scoring and explicit calibration analysis | High | Proper scoring rules are foundational; Brier decomposition cleanly separates reliability and resolution. citeturn23search4turn23search6 | Optimize and monitor Brier, log score, calibration curves, sharpness, and resolution. |
| Hybrid human-machine systems | Moderate | SAGE reports hybrid gains over human-only baselines; LLM-assistant work also reports improvements from superforecasting-style assistance. citeturn26view0turn6view4 | Leave hooks for human review, override, and machine-generated drafts/cruxes. |

Beyond those, several practical ideas are promising but less cleanly proven. **Explicit base-rate search**, **contrarian evidence search**, **scenario generation**, **historical analogues**, and **quantitative submodels** all fit well with the human-forecasting literature and with current bot practice, but the direct experimental evidence comparing these components in LLM forecasting is still sparse. These are good engineering bets, but they should be treated as candidate ablations rather than assumed wins. citeturn22search1turn20view0turn36search1

**Methods that look weak, overrated, or actively risky**

The first weak method is **naive chain-of-thought or “think carefully” prompting without fresh evidence**. Zero-shot and scratchpad prompting help much less than retrieval-plus-tuning in formal evaluations, and Halawi et al.’s no-retrieval ablations essentially fall back to near-baseline performance. citeturn27view1turn29view1

The second is **debate or multi-agent scaffolding without evidence diversity**. There is nothing magical about multiple copies of one model. RTF’s results explicitly state that ensembles help only if members are already calibrated; otherwise sampling can make performance worse. More broadly, Metaculus practitioner notes suggest better information flow, not more rhetorical reasoning, is what separated stronger bots. citeturn31view0turn8search1

The third is **overtrusting recent news**. EVOLVECAST finds that accumulated news context does not reliably improve dynamic update quality and can reduce directional agreement by inducing spurious movement. In a forecasting pipeline, “more articles” is not automatically better unless they are independent, relevant, and resolution-linked. citeturn32view2

The fourth is **uncritical extremization of correlated LLM ensembles**. In human-forecast aggregation, extremization can help when forecasters possess diverse, partly non-overlapping information. But later work also shows anti-extremization can be appropriate, and the theory is explicitly about information diversity rather than “more samples.” For same-model prompt variants, overlap is usually very high, so human-style extremization should be presumed risky unless validated on your own data. citeturn24search1turn24search9turn24search18

The fifth is **evaluation shortcuts that quietly leak answers**. Paleka et al. catalog logical leakage from question selection, leakage through date-restricted retrieval, over-reliance on stated training cutoffs, piggybacking on human forecasts, and skewed benchmark distributions. Any repo that lacks leakage checks should assume its retrospective numbers are optimistic. citeturn6view3turn27view5

**Lessons from human forecasting and superforecasting**

What is genuinely operationalizable from human superforecasting is narrower than many summaries imply. The robust pieces are: start with the outside view; decompose only when the decomposition is clear and recombinable; update frequently; track reasons and cruxes; keep probabilities numeric; aggregate multiple views; train calibration; and maintain humility about edge cases. These themes recur across Good Judgment Project summaries, Mellers et al., Tetlock’s tournament writeups, and reference-class forecasting literature. citeturn5search17turn5search24turn24search11turn22search1turn22search11

The literature does **not** justify unlimited faith in decomposition. MacGregor’s classic work argues decomposition can help judgmental forecasting, but later discussion in the forecasting community correctly notes that the evidence is mixed and that bad decompositions can amplify noise. In code terms: decomposition is best used when the subquestions are conditionally meaningful, independently researchable, and mechanically recombinable. If not, decomposition easily becomes “more prose, same error.” citeturn22search3turn34search4

## Public systems and recommended pipeline

**Lessons from public forecasting bots and repositories**

Publicly observable Metaculus bot architecture is already enough to establish a baseline standard. The official `forecasting-tools` repo exists specifically as a framework for building AI forecasting bots, and the `q1_template_bot.py` flow is explicit: load questions, run research a configurable number of times, run forecasts multiple times per research report, aggregate predictions, and optionally submit or save reports. The simpler `metac-bot-template` retains the same structure and currently defaults to one research report and five forecast samples. citeturn15view0turn15view2turn16view0turn16view1

The template prompt itself is informative. For binary questions it tells the model to consider time left, status quo, a no scenario, and a yes scenario, and only then output `Probability: ZZ%`. This is a practical example of lightly structured reasoning that is probably worth preserving even if you later add decomposition or markets. The critical part is not the prose style; it is the ordered reasoning schema. citeturn17view2

Public Metaculus writeups also reveal what stronger bot builders changed. Metaculus’s Fall 2025 bot-maker survey reports that the median winning bot made about 28 LLM calls per question versus 7 for non-winners, typically by splitting the pipeline into research, reasoning, and aggregation stages. A companion bot-advice article says external research remains necessary no matter how good the bot is, due to model training cutoffs, and that many builders found information quality entering the final call to be the central bottleneck. Internal Metaculus results also report that AskNews outperformed Exa or Perplexity in their own bot comparisons. citeturn36search0turn37search0turn8search1turn39search0

Among public non-official repos, the most implementation-relevant ones are useful mainly as design sketches, not as trustworthy performance evidence. `No-Stream/metaculus-bot` is notable for explicitly documenting a six-LLM fan-out, multi-provider parallel research, disagreement-targeted second-pass research, and a numeric CDF pipeline with strict constraint enforcement. `rpm_forecasting-tools` is valuable because it exposes reusable components like a base-rate researcher, niche list researcher, key-factor analysis, Fermi estimator, cost manager, and benchmark harness. `forecastbench_metaculus_forecasting_bot_q2` is another example of a multi-stage RAG plus ensemble architecture. These are useful to mine for module boundaries and interfaces, but their README performance claims should be treated as author statements unless independently benchmarked. citeturn19view0turn19view2turn20view0turn15view7

**Recommended reference architecture**

For a small personal forecasting repo, the best default is a **structured research-and-synthesis pipeline** with explicit state objects. Not a giant generic agent loop. Not full autonomy. A deterministic orchestration layer that calls tools and models in a fixed order will be simpler to test, cheaper to run, and easier for a coding agent to inspect and improve. That recommendation is an inference from the public bot ecosystem plus the strongest current academic systems, not something any single paper proves outright. citeturn15view2turn28view0turn31view0turn36search0

A good reference pipeline looks like this:

```python
def forecast_question(question: ForecastQuestion, as_of: date) -> ForecastReport:
    parsed = parse_question(
        text=question.text,
        background=question.background,
        resolution_criteria=question.resolution_criteria,
        fine_print=question.fine_print,
        open_date=question.open_date,
        close_date=question.close_date,
        resolve_date=question.resolve_date,
        as_of=as_of,
    )

    resolution = parse_resolution_schema(parsed)
    horizon = compute_time_horizon(parsed, as_of)

    retrieval_plan = plan_research(
        parsed_question=parsed,
        include=[
            "resolution_source",
            "latest_status",
            "base_rates",
            "reference_classes",
            "historical_analogues",
            "prediction_markets",
            "contrarian_evidence",
        ],
    )

    evidence = gather_evidence(retrieval_plan)
    evidence = dedupe_and_rank(evidence)
    evidence_packet = build_evidence_packet(
        parsed=parsed,
        evidence=evidence,
        max_items=20,
        sections=["resolution", "base_rates", "current_state", "markets", "contrarian"]
    )

    subquestions = maybe_decompose(parsed, evidence_packet)
    quantitative = run_quant_models(parsed, evidence_packet, subquestions)
    scenarios = generate_scenarios(parsed, evidence_packet, quantitative)
    cruxes = identify_cruxes(parsed, evidence_packet, scenarios)

    raw_forecasts = []
    for config in independent_forecaster_configs():
        raw_forecasts.append(
            synthesize_probability(
                parsed=parsed,
                evidence_packet=evidence_packet,
                quantitative=quantitative,
                scenarios=scenarios,
                cruxes=cruxes,
                config=config,
            )
        )

    red_team = critique_forecast_set(parsed, evidence_packet, raw_forecasts)
    revised_forecasts = revise_if_needed(raw_forecasts, red_team)

    aggregated = aggregate_forecasts(revised_forecasts)
    calibrated = apply_calibrator(aggregated, model_family=aggregated.model_family)
    final = incorporate_market_anchor_if_appropriate(calibrated, evidence_packet.markets)

    return ForecastReport(
        parsed_question=parsed,
        evidence=evidence,
        subquestions=subquestions,
        quantitative_estimates=quantitative,
        scenarios=scenarios,
        cruxes=cruxes,
        raw_forecasts=raw_forecasts,
        red_team=red_team,
        final_forecast=final,
        provenance=build_audit_trail(),
    )
```

The most important design choice there is the explicit split between `gather_evidence`, `synthesize_probability`, and `aggregate_forecasts`. If your current repo lets one model both search, summarize, decide what matters, assign probabilities, and judge its own answer in a single call, that is the first thing to change. Public bot builders consistently moved in the opposite direction. citeturn8search1turn36search0turn17view0

**Concrete prompt templates**

A practical **question parser / resolution parser** prompt:

```text
System:
You convert forecasting questions into structured data for downstream use.

User:
Parse the following forecasting question into JSON.

Required fields:
- question_type: binary | multiple_choice | numeric | date
- canonical_question
- entity_list
- event_predicate
- resolution_source
- resolution_criteria_summary
- disqualifying_edge_cases
- earliest_relevant_date
- latest_resolution_date
- time_horizon_days
- geographic_scope
- market_ticker_candidates
- base_rate_queries
- current-status queries
- contrarian queries
- quantity_type_if_numeric
- units_if_numeric
- should_decompose: true/false
- proposed_subquestions: []

Question text:
{question_text}

Background:
{background_info}

Resolution criteria:
{resolution_criteria}

Fine print:
{fine_print}

Today:
{today}
```

A practical **research planner** prompt:

```text
System:
You are building a research plan for a forecasting question.
Separate outside-view and inside-view research.

User:
Produce a JSON plan with these arrays:
- resolution_queries
- current_state_queries
- base_rate_queries
- reference_class_queries
- market_queries
- contrarian_queries
- source_type_targets

Rules:
- Include at least one query aimed at the exact resolution source.
- Include at least two outside-view/base-rate queries.
- Include at least one contrarian query that could falsify the leading narrative.
- Prefer primary sources, official statistics, filings, regulator pages, and platform APIs.
- Avoid vague generic searches.

Parsed question:
{parsed_question_json}
```

A practical **probability synthesis** prompt:

```text
System:
You are a calibrated forecaster. Use the evidence packet, not your vague prior.

User:
Forecast the event in JSON.

First reason in this order:
1. What exactly resolves the question?
2. What happens by default if nothing material changes?
3. What outside-view base rate or reference class is most relevant?
4. What are the strongest pro and con pieces of evidence?
5. What are the main cruxes?
6. What scenario split best captures the uncertainty?

Then output JSON:
{
  "probability": 0.00,
  "confidence_in_estimate": 0.00,
  "outside_view": "...",
  "inside_view": "...",
  "cruxes": ["...", "..."],
  "key_assumptions": ["...", "..."],
  "main_failure_modes": ["...", "..."],
  "evidence_used_ids": ["E12", "E03", "M1"],
  "notes_on_calibration": "..."
}

Question:
{parsed_question}

Evidence packet:
{evidence_packet}
```

**Search and retrieval strategy**

The agent should search for five things and do them in roughly this order: the exact resolution source; current status relevant to the resolution criteria; outside-view base rates or reference classes; analogous historical episodes; and current crowd/market forecasts. This order is partly an engineering judgment, but it matches the strongest signals from human forecasting, public bot design, and academic retrieval systems. citeturn22search1turn28view0turn17view0turn41search0turn41search1turn41search2

The quality hierarchy for sources should be explicit in code. A reasonable default is: official statistics, regulators, filings, court rulings, company releases, and direct platform APIs at the top; then reputable specialist reporting; then major general news; then blogs/forum posts; then generic commentary. The evidence packet should store both the source type and a reliability class so that the final synthesizer can reason differently over a SEC filing, a Metaculus market, and a Substack post. That reliability taxonomy is an inference, but it directly addresses the anti-pattern that public bot builders identified: letting low-quality search results dominate the final prompt context. citeturn8search1turn39search0

A cost-effective search plan for a small project is usually one research pass with multiple query families rather than multiple unconstrained agent loops. Halawi et al. generated several search queries and then filtered/reranked; Metaculus template bots often run one research report and several forecast samples; winning public bots then seem to spend extra calls on gap-filling or disagreement resolution rather than brute-force more of the same search. So a good default is: one structured research pass, then one targeted follow-up pass only if the forecasters disagree or the evidence packet lacks a clean resolution source. That is a design hypothesis consistent with the available evidence, not a settled empirical law. citeturn28view0turn16view1turn19view0

When to stop searching should also be explicit. Stop when one of these conditions holds: the top-ranked sources already include a resolution source and at least one strong outside-view source; two extra search batches add no new crux-relevant evidence; or the ensemble variance is already low and recent additional evidence has not moved the median forecast materially. EVOLVECAST’s results are a good warning here: more context can induce spurious updates rather than better updates. citeturn32view2

**Prediction markets and crowd forecasts**

A production forecaster should integrate platform forecasts rather than ignore them. Metaculus provides question and forecast endpoints through its API, its FAQ explains that the community prediction is a recency-weighted median, Manifold provides a programmatic API at `api.manifold.markets`, and Polymarket exposes public market-data REST endpoints that require no auth for discovery. Good Judgment Open offers public probabilistic forecasting questions and reasoning. citeturn41search0turn39search15turn41search1turn41search5turn41search2turn41search6turn41search19

In practice, crowd or market forecasts should be treated as an **anchor feature**, not as an answer key. They should dominate when they are recent, liquid or well-trafficked, tightly matched to your exact resolution criteria, and the question is near resolution. They should be downweighted when the market is stale, thin, clearly proxying a different resolution condition, or when the LLM has found hard evidence the crowd appears not to have incorporated. This is partly inference, but it is supported by two facts: current human crowd baselines still outperform bots on average in public evaluations, and recent work on prediction-market calibration finds that calibration depends materially on domain, time horizon, and trade size rather than being universally trustworthy. citeturn7view4turn38search0turn14search1

The cleanest implementation pattern is:

- fetch relevant platform forecasts;
- normalize them to the same event definition;
- compute age, liquidity/proxy-quality, and resolution-match scores;
- pass these features to the final calibrator or aggregator rather than hard-overriding the model forecast.

For example:

```python
market_anchor = weighted_anchor(
    sources=[
        metaculus_prob,
        manifold_prob,
        polymarket_prob,
        gjopen_prob,
    ],
    weights={
        "resolution_match": 0.45,
        "recency": 0.20,
        "platform_quality": 0.20,
        "liquidity_or_participation": 0.15,
    }
)
```

## Probability, calibration, and aggregation

**Probability estimation and calibration**

Use **numeric probabilities everywhere**. Avoid vague verbal probabilities in storage, internal APIs, and evaluation. Metaculus, Good Judgment Open, and the forecasting-scoring literature are all built around explicit probabilistic forecasts because proper scoring rules require comparable numerical probabilities. citeturn39search15turn41search19turn23search4

The best default elicitation pattern is not “What is the probability?” in one line. It is a structured elicitation that asks for status quo, outside view, inside view, cruxes, and then a probability. This mirrors the Metaculus template prompt and the human-forecasting literature better than generic chain-of-thought, and it reduces the chance that the model jumps directly from anecdote to number. citeturn17view2turn22search1turn24search11

For confidence extraction, prefer **verbalized probabilities** over raw token probabilities unless you have a specific reason not to. “Just Ask for Calibration” found that verbalized confidence from RLHF-tuned LLMs was often much better calibrated than the models’ native conditional probabilities, reducing expected calibration error substantially. But do not assume one representation always wins: EVOLVECAST suggests verbalized and logit-based confidence differ by setting and neither is universally superior in dynamic belief-update tasks. citeturn13search2turn13search10turn32view1

Post-hoc calibration should be a standard module. The classical options remain logistic calibration, isotonic calibration, and reliability-curve monitoring; in LLM-specific work, calibration-tuning and newer decomposition-based methods show that explicit interventions can improve uncertainty estimates, and recent work argues that good uncertainty usually requires training or calibration data rather than emerging automatically. For a small project, post-hoc calibration on resolved historical questions is the right first move; full fine-tuning of uncertainty is not. citeturn13search7turn13search6turn13search3turn13search9

A practical binary calibration stack looks like this:

```python
# fit on resolved historical questions
raw_p = model_outputs["probability"]
y = outcomes["resolved_yes"]

iso = IsotonicRegression(out_of_bounds="clip")
iso.fit(raw_p, y)

# optional per-model-family calibrators
calibrators = {
    "gpt_4o": iso_gpt4o,
    "claude_sonnet": iso_claude,
    "deepseek": iso_deepseek,
}
```

For numeric and date questions, the same principle applies but on distributions. The publicly visible Metaculus template bots already force percentile outputs for numeric and date questions and then convert these into constrained distributions. A personal repo should copy that design choice. Forecasting systems are more useful when they emit percentile or quantile distributions, not just single values. citeturn17view3turn17view4turn17view5

**Forecast aggregation**

The first rule of aggregation is to keep a **simple equal-weight or median baseline**. Decades of forecast-combination literature show that simple combinations are often extremely hard to beat, especially when errors are unstable or highly correlated. That conclusion is more general than LLM forecasting, but it is exactly the right default for a small repo. citeturn23search11turn23search7turn23search18

The second rule is to aggregate on the right scale. Probabilities near 0 and 1 behave badly under straight averaging if the members differ in calibration or extremity. For strongly independent members, logit-space pooling can be useful; for highly correlated prompt variants, a median or trimmed mean is safer. Halawi et al. found trimmed mean marginally best among their tested ensemble methods, and Metaculus internal/public practice also leans on repeated samples plus aggregation rather than learned meta-models as a first step. citeturn28view3turn21search19

The third rule is to separate **diversification** from **duplication**. If you ensemble five outputs from the same model, same prompt, same evidence packet, and same temperature, you do not have five independent forecasters; you have a noisy replicate. Diversity can come from different models, different evidence subsets, different search passes, different explicit priors, and different reasoning templates like inside-view versus outside-view. The public bot ecosystem increasingly implements this kind of structured diversity, for example with disagreement-targeted second-pass research or inside/outside-view prompts. citeturn19view0turn36search1

Extremization deserves caution. Human aggregation theory supports extremization when combining diverse information pools, but anti-extremization can be equally rational when inputs share biased priors or high overlap. For LLMs, where overlap is usually extreme, the default should be **no extremization** until validated, followed by learned extremization or shrinkage only if your backtests justify it. citeturn24search1turn24search9turn24search13

A practical aggregation recipe for a small repo:

```python
def aggregate_binary_forecasts(ps, meta):
    # ps: list[float]
    # meta: diagnostics per forecaster (model family, evidence coverage, self-rated confidence)
    center = trimmed_mean(ps, trim_fraction=0.15)

    # Optional learned correction based on historical calibration of each forecaster family
    adjusted = bias_correct(center, meta)

    # Shrink toward market/crowd anchor only when anchor quality is high
    if meta["anchor_quality"] >= 0.8:
        adjusted = 0.75 * adjusted + 0.25 * meta["anchor_prob"]

    return clip(adjusted, 0.01, 0.99)
```

## Evaluation and repo design

**Evaluation framework**

There are now several useful public benchmarks, but they answer different questions. **ForecastBench** is a dynamic benchmark of about 1,000 forecasting questions with continuously updated data, human comparison groups, and open code/data; its site says new forecasting rounds occur every two weeks and the leaderboard updates nightly. **FutureEval** is Metaculus’s live benchmark and bot tournament ecosystem. **MIRAI** evaluates tool-using agents on international-event forecasting with structured event databases and fresh test splits generated after model cutoffs. **EVOLVECAST** is not a pure accuracy benchmark; it evaluates whether models update beliefs in the right direction and magnitude as new evidence arrives. OpenForecast and OpenForesight extend the space toward open-ended future reasoning and specialized training. citeturn11search1turn11search13turn15view6turn8search2turn6view5turn27view4turn33search10turn33search2

For a private evaluation set, the highest-value practice is to build a **rolling, timestamped question bank** rather than a static backtest CSV. Each question should store `as_of_date`, complete resolution criteria, archived retrieved evidence, and the exact system version that forecast it. If you later replay questions retrospectively, the retrieval layer must be date-restricted and audited, because Paleka et al. show that even nominally date-restricted pipelines can leak future knowledge through retrieval metadata or through human-crafted question selection. citeturn6view3turn27view5

Before resolution, use proxy metrics, but do not confuse them with ground truth. Metaculus’s automated prompt-engineering analysis used **expected baseline score**, effectively a log-score-based expectation under the community forecast, to speed iteration. That is useful because it lets you compare pipelines now, but the limitation is obvious: it penalizes a system for being better than the current crowd. For unresolved long-horizon questions, also track update direction, forecast stability, and evidence quality audits, because those often contain more signal than pseudo-scores. citeturn40search1turn32view1

After resolution, track at least these metrics: Brier score, log score, calibration curve / reliability, sharpness, discrimination or resolution, abstention or invalid-output rate, and update quality over time. For calibration, store both aggregate bias and bucketed curves. For binary questions, use Murphy-style decomposition where possible. For numeric/date questions, score the full distribution or quantiles rather than collapsing to a point estimate. citeturn23search4turn23search6

A good ablation matrix for a personal repo is not huge. Ablate retrieval on/off; base-rate module on/off; crowd anchor on/off; contrarian search on/off; single-shot versus separated research/synthesis; one forecaster versus ensemble; and calibrator on/off. Most current public work suggests these are the levers with the highest chance of mattering. citeturn29view1turn36search0turn8search1

Question counts matter, and the literature here is weaker than people pretend. A reasonable practitioner heuristic is: fewer than about 100 resolved binary questions is usually too noisy for scaffold decisions unless the effect is very large; 200–500 resolved questions is a better minimum for comparing closely related pipelines; and more is needed if you stratify by category or forecast horizon. That guideline is not a theorem; it is an engineering inference from the size of modern evaluations, including Metaculus tournament analyses and the 230-question test set used in prompt-optimization experiments. citeturn38search0turn38search1turn40search1

**Repo and module design**

A practical module layout:

```text
/prompts
  question_parser/
  research_planner/
  evidence_ranker/
  probability_synthesis/
  red_team/
  calibration/

/agents
  parser_agent.py
  retrieval_agent.py
  forecaster_agent.py
  critic_agent.py
  aggregator_agent.py

/retrieval
  search_clients/
    metaculus_api.py
    manifold_api.py
    polymarket_api.py
    web_search.py
  query_generation.py
  evidence_store.py
  ranking.py
  dedupe.py
  summarization.py
  source_scoring.py

/forecasting
  question_schema.py
  resolution_parser.py
  base_rates.py
  decomposition.py
  analogues.py
  scenarios.py
  quantitative_models.py
  synthesis.py
  distributions.py
  aggregation.py

/calibration
  fit.py
  isotonic.py
  logistic.py
  diagnostics.py
  bias_correction.py

/evaluation
  scoring.py
  calibration_metrics.py
  update_metrics.py
  leak_checks.py
  ablations.py
  significance.py

/benchmarks
  public/
    forecastbench/
    futureeval/
    mirai/
  private/
    question_bank/
    resolutions/

/logs
  forecasts/
  evidence/
  traces/
  cost/
  model_versions/

/docs
  llm_forecasting_methods_report.md
  architecture.md
  evaluation.md

/experiments
  configs/
  notebooks/
  prompt_sweeps/
  ablation_runs/

/configs
  models.yaml
  search.yaml
  aggregation.yaml
  calibration.yaml
```

The rationale for this structure is direct. Public bot ecosystems already separate bots from search tools and platform APIs; `forecasting-tools` and `rpm_forecasting-tools` both expose reusable API wrappers, researchers, benchmarking, and bot objects; and the most common weakness in small projects is letting all of that blur into one `main.py`. Keep the forecast object model and the evidence object model separate. citeturn15view0turn19view2

A minimal set of classes and functions worth having:

| Module | Purpose | Likely contents |
|---|---|---|
| `/forecasting/question_schema.py` | Canonical question object | `ForecastQuestion`, `ParsedQuestion`, `ResolutionSchema` |
| `/retrieval/evidence_store.py` | Persist source snippets and metadata | `EvidenceItem`, `EvidencePacket`, `save_evidence()` |
| `/forecasting/base_rates.py` | Outside-view retrieval and estimation | `find_reference_classes()`, `estimate_base_rate()` |
| `/forecasting/synthesis.py` | Probability generation from curated evidence | `synthesize_binary()`, `synthesize_numeric()` |
| `/forecasting/aggregation.py` | Combine multiple forecasts | `trimmed_mean()`, `median_pool()`, `shrink_to_anchor()` |
| `/calibration/fit.py` | Fit post-hoc calibrators | `fit_isotonic()`, `fit_logistic()`, `apply_calibrator()` |
| `/evaluation/scoring.py` | Proper scoring rules | `brier()`, `log_score()`, `crps_or_quantile_loss()` |
| `/evaluation/leak_checks.py` | Catch contamination | `check_future_dates()`, `check_resolution_overlap()`, `check_market_copying()` |
| `/logs/traces/` | Audit trail | raw prompt, evidence IDs, model outputs, parsed JSON, final forecast |

## Checklist and roadmap

**Agentic implementation checklist**

A coding agent inspecting your repo should check the following, in roughly this order.

- [ ] **Question parsing**: Does the repo explicitly parse question type, resolution criteria, fine print, and time horizon, or does it treat the question as a raw string? Metaculus question structure strongly suggests the former. citeturn39search15turn17view2
- [ ] **Evidence separation**: Is evidence retrieval separated from probability synthesis? If not, fix this first. citeturn8search1turn17view0
- [ ] **Base-rate retrieval**: Is there an explicit base-rate / outside-view module? If not, add one. citeturn22search1turn20view0
- [ ] **Resolution-source retrieval**: Does the search layer try to find the exact source that will resolve the question? If not, queries are underspecified. citeturn39search15
- [ ] **Source storage**: Are full source URLs, snippets, publication dates, source types, and retrieval timestamps persisted with the forecast? If not, the audit trail is broken. citeturn28view0turn6view3
- [ ] **Independent forecast samples**: Does the repo generate multiple independent forecasts per question? A single forecast is a baseline, not a serious design. citeturn16view1turn21search19
- [ ] **Principled aggregation**: Is there an explicit aggregation module with a simple validated baseline such as median or trimmed mean? citeturn28view3turn23search11
- [ ] **Contrarian pass**: Is there a red-team or disconfirming-evidence stage? If not, add one after first-pass synthesis. This is more of a design hypothesis than a proven universal win, but it is a good safeguard. citeturn36search1turn40search1
- [ ] **Crowd/market integration**: Can the system fetch Metaculus, Manifold, Polymarket, or Good Judgment Open anchors? citeturn41search0turn41search1turn41search2turn41search19
- [ ] **Calibration tracking**: Does the repo fit and monitor calibrators over time, by model family and by question type? citeturn13search2turn23search6
- [ ] **Versioning**: Are prompts, model names, temperatures, tool configs, and calibrator versions logged per forecast? If not, regression analysis will be impossible. citeturn40search1
- [ ] **Leakage checks**: Are there tests for future-data leakage, retrieval-date errors, and backtest contamination? citeturn6view3turn27view5
- [ ] **Uncertainty representation**: For numeric/date questions, does the repo store distributions or percentiles rather than a single guessed number? citeturn17view3turn17view4
- [ ] **Post-resolution learning**: Is there a job that backfills resolved outcomes, scores old forecasts, and updates calibration reports? If not, the system cannot improve. citeturn24search11turn23search4
- [ ] **Prompt regression tests**: Are there smoke tests ensuring parser prompts still produce valid JSON and scorer functions still match reference implementations? This is plain engineering necessity, not something the literature had to rediscover. citeturn15view1turn15view2

**Prioritized roadmap**

For a small personal project, the highest-ROI path is not to replicate full FutureEval bots. It is to add the missing structural pieces that transform a demo into a testable forecaster.

| Priority | Change | Why it is high ROI | Evidence status |
|---|---|---|---|
| Quick win | Add explicit question/resolution parser | Prevents a large class of dumb failures | High confidence citeturn39search15turn17view2 |
| Quick win | Split retrieval from synthesis | Public bot experience and academic systems both point here | High confidence citeturn8search1turn17view0turn28view0 |
| Quick win | Store evidence packets and snippets | Necessary for audits, debugging, and future training | High confidence citeturn6view3turn28view0 |
| Quick win | Add 3–5 independent forecast samples + trimmed mean | Cheap accuracy gain relative to complexity | High confidence citeturn16view1turn28view3 |
| Quick win | Add a base-rate module | Human literature strongly supports outside view | Moderate-high confidence citeturn22search1turn20view0 |
| Medium term | Integrate Metaculus, Manifold, and Polymarket anchors | Gives strong real-world priors and update signals | High confidence on usefulness, moderate on exact weighting citeturn41search0turn41search1turn41search2turn7view4 |
| Medium term | Add calibration fitting and dashboards | Miscalibration is a persistent LLM weakness | High confidence citeturn13search2turn13search3turn23search6 |
| Medium term | Add contrarian evidence and crux logging | Helps fight narrative lock-in and recency bias | Moderate confidence citeturn36search1turn40search1 |
| Medium term | Build a rolling private eval bank | Needed to avoid leak-prone retrospective tuning | High confidence citeturn6view3turn11search13 |
| Ambitious | Train or fine-tune a forecasting-specialized model | Specialized training can improve accuracy/calibration | Promising but newer evidence citeturn28view5turn33search2 |
| Ambitious | Add human review / hybrid mode | Hybrid systems can outperform human-only baselines | Moderate confidence citeturn26view0turn6view4 |
| Ambitious | Evaluate belief updates, not only final scores | Dynamic forecast revision quality is a real capability | Moderate confidence citeturn32view1turn27view4 |

A reasonable first milestone for a personal repo is this: **one structured research pass, one base-rate pass, one market-anchor pass, three independent synthesis calls, trimmed-mean aggregation, isotonic calibration, and full audit logging**. That is cheap enough to run, simple enough to debug, and close enough to current public best practice to be a serious starting point. citeturn16view1turn28view3turn36search0

## Open questions and annotated bibliography

**Open questions and uncertain claims**

The literature is still weak on several issues, and the report should not be read as stronger than the evidence. It is still unclear exactly how much **decomposition** helps LLM forecasting once you control for better retrieval and better prompts; the human literature is mixed, and public bot builders do not yet expose enough ablations to separate the effect cleanly. citeturn22search3turn34search4

It is also unclear whether **multi-agent debate** has intrinsic value beyond evidence diversification and calibration. The current public signal points toward “no, unless the agents have different tools or evidence,” but dedicated forecasting studies are still limited. citeturn31view0turn8search11

Likewise, the exact best way to combine **LLM probabilities with market probabilities** is underexplored. Public practice often uses markets as anchors, and theory suggests conditional weighting by source quality, but there is little open evidence yet on the best real-world fusion rule for mixed systems. Treat this as an active design problem. citeturn14search1turn7view4

**Annotated bibliography and source list**

**Papers**

- **Halawi et al., *Approaching Human-Level Forecasting with Language Models*** — The central technical paper for LLM forecasting pipelines. Important because it gives a full retrieval-reasoning-aggregation system, ablations showing retrieval and fine-tuning matter, and evidence that the system can complement crowds. citeturn6view0turn29view3
- **Hsieh et al., *Reasoning and Tools for Human-Level Forecasting*** — Important for hierarchical ReAct design, tool use, and the result that a small ensemble of calibrated tool-using agents can outperform base models and roughly match or beat human crowd baselines on that dataset. citeturn31view0turn30view1
- **Karger et al., *ForecastBench*** — Important as an open, dynamic, contamination-aware benchmark with living datasets, human comparisons, and public code. Use it as one public regression suite. citeturn11search1turn15view6
- **Ye et al., *MIRAI*** — Important for evaluating agentic tool use with structured event databases and fresh contamination-resistant splits, especially if you want international-event forecasting tasks. citeturn6view5
- **EVOLVECAST** — Important because it evaluates belief revision, not just end-state accuracy. Use it conceptually when building update-quality metrics. citeturn32view1turn27view4
- **Paleka et al., *Pitfalls in Forecasting Evaluation*** — Essential reading for leakage. Important because many bot repos and papers are probably overclaiming due to exactly the failure modes this paper names. citeturn6view3turn27view5
- **Benjamin et al., *Hybrid Forecasting of Geopolitical Events*** — Important evidence that hybrid human-machine systems can beat human-only baselines, with useful ideas for weighted aggregation and human oversight. citeturn26view0
- **Mellers et al., *Psychological Strategies for Winning a Geopolitical Forecasting Tournament*** — Core human forecasting paper. Operationally important for training, teaming, and tracking. citeturn5search17turn25search8
- **Tetlock et al., *Forecasting Tournaments*** — Important as the concise statement of why forecasting tournaments improve transparency and reveal what methods actually work. citeturn5search24
- **Chang et al., *Developing Expert Political Judgment*** — Important for training effects in forecasting tournaments. citeturn5search25
- **Lovallo and Kahneman, *Delusions of Success* / outside view work** — The canonical source on reference-class forecasting and outside-view discipline. Important because LLMs need exactly this corrective. citeturn22search1turn22search11
- **MacGregor, *Decomposition for Judgmental Forecasting and Estimation*** — Important because it motivates decomposition while also clarifying that decomposition is a methodological choice, not a free lunch. citeturn22search3turn22search13
- **Gneiting and Raftery, *Strictly Proper Scoring Rules, Prediction, and Estimation*** — Mandatory for scoring design. Important because proper scores are the backbone of forecast evaluation. citeturn23search4
- **Siegert, *Simplifying and Generalising Murphy’s Brier Score Decomposition*** — Important for calibration dashboards and reliability/resolution analysis. citeturn23search6
- **Satopää et al., *Combining Probability Forecasts and Understanding Probability Extremizing through Information Diversity*** — Important because it explains when extremization can help. Use it mainly as a caution against naive reuse on correlated LLM ensembles. citeturn24search1
- **Lichtendahl et al., *Extremizing and Antiextremizing in Bayesian Ensembles*** — Important because it shows extremization is not always correct and that anti-extremization can be rational. citeturn24search9
- **Tian et al., *Just Ask for Calibration*** — Important for extracting usable confidence from RLHF LLMs. citeturn13search2turn13search10
- **Kapoor et al., *Calibration-Tuning*** and **Zhang et al., *UF Calibration*** — Important because they make the general point that LLM uncertainty often needs explicit calibration interventions. Transfer to forecasting is plausible but not fully established. citeturn13search7turn13search6
- **Lewis et al., *Retrieval-Augmented Generation*** — Important background for nonparametric memory and provenance-aware generation. citeturn12search2
- **Yao et al., *ReAct*** — Important for tool-use design and interleaving reasoning with action. citeturn12search1turn12search9
- **Wang et al., *Self-Consistency Improves Chain-of-Thought Reasoning*** — Important because sample-and-aggregate can beat greedy decoding, though forecasting benefits depend on calibration and evidence. citeturn12search4
- **Chandak et al., *Scaling Open-Ended Reasoning to Predict the Future*** — Important emerging evidence for specialized forecasting training and RL on open-ended forecasting data. Promising, but newer and less battle-tested than Halawi/ForecastBench. citeturn33search2turn33search3
- **Yuan et al., *FOReCAst*** and **Wang et al., *OpenForecast*** — Important newer benchmarks for open-ended and confidence-aware forecasting tasks. Useful if your repo will go beyond binary event questions. citeturn33search14turn33search10

**Blogs, forum posts, and community writeups**

- **Metaculus, *FutureEval methodology*** — Important because it describes the live benchmark design and human baselines. citeturn8search2
- **Metaculus, *Q1 AI Benchmark Results: Pro Forecasters Crush Bots*** — Important because it shows public tournament-scale evidence that pros were still ahead in 2025. citeturn38search0
- **Metaculus, *Q4 AI Benchmarking: Bots Are Closing the Gap*** — Important because it shows the rate of progress and the scale of question counts. citeturn38search1
- **Metaculus, *Fall 2025 FutureEval Bot-Maker Survey*** — Extremely important implementation source. It is one of the clearest public windows into what winning bots actually changed. citeturn36search0
- **Metaculus, *Advice from Bot Makers to Bot Makers*** — Important because it states directly that external research remains necessary and surfaces practical failure modes. citeturn37search0
- **Metaculus / EA Forum, *Analysis of Automated Prompt Engineering for Forecasting*** — Important because it shows prompt optimization can help some models a lot, others little or not at all, and gives a useful methodology for fast pre-resolution testing. citeturn40search1
- **AI Impacts, *Evidence on Good Forecasting Practices from the Good Judgment Project*** — Good compact operational summary of human forecasting lessons. citeturn34search2turn24search15
- **LessWrong, *The Evidence for Question Decomposition is Weak*** — Important counterweight against cargo-cult decomposition. citeturn34search4
- **Forecasting Research Institute Substack, *How well can large language models predict the future?*** — Useful summary and context around ForecastBench updates. citeturn11search18
- **Mantic, *A new kind of foresight*** — Useful as an industry signal that strong automated forecasting is becoming commercially relevant, but not a rigorous evaluation source by itself. citeturn21search5

**GitHub repositories**

- **`Metaculus/forecasting-tools`** — The most important public codebase for bot builders. Valuable for API wrappers, template bots, and expected workflow separation. citeturn15view0turn15view2
- **`Metaculus/metac-bot-template`** — Important because it shows the minimal competitive scaffold and concrete default prompts. citeturn15view1turn17view2
- **`forecastingresearch/forecastbench`** — Important for benchmark code and public datasets. citeturn15view6
- **`forecastingresearch/forecastbench_metaculus_forecasting_bot_q2`** — Useful reference for a multi-stage RAG bot architecture. Treat README performance claims as author-reported. citeturn15view7
- **`quantified-uncertainty/metaforecast`** — Important for cross-platform market/crowd forecast retrieval. citeturn15view4
- **`gnosis/prediction-market-agent`** — Useful if your project may evolve from forecasting to automated betting or market interaction. citeturn15view5
- **`No-Stream/metaculus-bot`** — Useful for advanced ensemble and disagreement-research patterns. README claims are not independent evidence. citeturn19view0
- **`RichiePim/rpm_forecasting-tools`** — Useful for modular ideas around base rates, niche lists, and Fermi estimation. citeturn19view2turn20view0

**Benchmarks and platforms**

- **ForecastBench** — Dynamic public benchmark with live datasets and human groups. citeturn11search1turn11search13
- **FutureEval** — Live benchmark and tournament ecosystem on Metaculus; practical source of real-world leaderboard signals. citeturn7view4turn8search2
- **Metaculus** — Platform plus API; useful for questions, community forecasts, and structured resolution criteria. citeturn41search0turn39search15
- **Manifold** — Easy-to-query API and data ecosystem; good low-friction market anchor. citeturn41search1turn41search5
- **Polymarket** — Public market data via REST endpoints; useful for liquid market anchors. citeturn41search2turn41search6
- **Good Judgment Open** — Public crowd-forecasting platform with shared reasoning. citeturn41search3turn41search19

**Other resources**

- **Metaculus FAQ and API docs** — Important for exact platform semantics and integration. citeturn39search15turn41search0
- **`awesome-prediction-markets`** — Useful for discovering APIs, datasets, and tooling across platforms. citeturn14search11
- **Metaculus FutureEval resources page / build-a-bot tutorial** — Useful onboarding if you want your repo to be tournament-compatible. citeturn10search1turn36search12

**Bottom line**

If a coding agent compares this report against an existing repo, the first things it should try to add are: explicit resolution parsing, a separate evidence store, a base-rate module, multiple independent forecast samples, a simple aggregation layer, calibrated post-processing, crowd/market anchoring, and leak-resistant evaluation. Those changes are more likely to matter than adding generic agent chatter, more model personas, or longer chain-of-thought. That is the central practical conclusion of the current evidence base. citeturn8search1turn28view0turn31view0turn36search0