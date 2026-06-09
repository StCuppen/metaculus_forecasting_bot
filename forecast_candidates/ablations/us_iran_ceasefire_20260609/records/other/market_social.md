# Will the U.S. officially announce an extension of the ceasefire agreement between the U.S. and Iran, or announce a new peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue, by June 30, 2026 at 11:59 PM ET?

Resolution criteria: This resolves YES if, before the deadline, there is clear public confirmation from the U.S. government that the U.S. has either (1) extended its commitment to the ceasefire, either as a dated/time-based extension or through an explicit statement that the ceasefire has been extended, or (2) renewed the existing ceasefire as part of a broader peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue. A qualifying announcement resolves YES regardless of whether the extension later takes effect. Statements that merely say the ceasefire remains in effect, continues to hold, talks are ongoing, the parties are closer to a deal, or de-escalation measures are being discussed do not qualify unless they announce a new extension, renewal, or successor framework. An overwhelming consensus of credible reporting that a qualifying extension or successor agreement has been definitively established also suffices. Confirmation from Iran is not required. Otherwise resolves NO.

- **Platform / run type:** other / prior_ablation_empirical
- **Question type:** binary
- **Forecast date (UTC):** 2026-06-09T17:58:22.606895+00:00
- **Pipeline:** lean-ensemble/v2-2026.06 · models: deepseek/deepseek-v4-pro, openai/gpt-5.4-mini, moonshotai/kimi-k2.6, google/gemini-3-flash-preview, anthropic/claude-haiku-4.5

## Question details
### Canonical spec

- One-line: Will the U.S. officially announce an extension of the ceasefire agreement between the U.S. and Iran, or announce a new peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue, by June 30, 2026 at 11:59 PM ET?
- YES: Clear public confirmation from the U.S. government that the U.S. has either (1) extended its commitment to the ceasefire (dated/time-based or explicit statement) or (2) renewed the existing ceasefire as part of a broader peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue. An overwhelming consensus of credible reporting that a qualifying extension or successor agreement has been definitively established also suffices.
- NO: The U.S. does not make a qualifying announcement by the deadline, or only makes statements that the ceasefire remains in effect, continues to hold, talks are ongoing, the parties are closer to a deal, or de-escalation measures are being discussed without announcing a new extension, renewal, or successor framework.
- Window: by June 30, 2026 at 11:59 PM ET
- Threshold: None
- Metric: None

## Final forecast
- **Probability: 50.0%**
- Action: **publish** · Confidence: medium · Informativeness: weak_view
- Outside-view (base rate) probability: 41.7%

## Prior / base-rate packet
- Status: found
- Canonical prior: 44.5%
- Prior type: empirical_plus_heuristic_plus_social
- Confidence: medium
- Plausible range: [0.3, 0.6]
- Rationale: Combined arm. Start from the weak empirical and structured heuristic priors, then include the current market price as a social prior without forcing exact market copying.

## Model forecasts

| Model | Forecast | Outside view | Tokens | Base rate / short rationale |
|---|---:|---:|---:|---|
| DeepSeek V4 Pro | 40.0% | 44.5% | 8651 | Synthetic prior from empirical heuristics and Polymarket social price for a U.S. official ceasefire extension announcement in the active U.S.-Iran conflict with ~3-week deadline, approximately 44.5%. |
| GPT-5.4 Mini | 58.0% | 33.0% | 5474 | Temporary ceasefire-extension follow-up announcements after short, fragile interstate ceasefires are uncommon; a rough reference-class rate is around 30%. |
| Kimi K2.6 | 40.0% | 42.0% | 22391 | Short-deadline follow-up agreements after temporary ceasefires occur roughly 30% of the time, with a context-adjusted heuristic prior near 42%. |
| Gemini 3 Flash | 42.0% | 44.5% | 3553 | Polymarket social prior for this specific diplomatic event is 44.5%. |
| Claude Haiku 4.5 | 70.0% | 44.5% | 5017 | Temporary ceasefire follow-up agreement within a short deadline (~30% empirical, adjusted to 44.5% via heuristic and market priors); current context suggests April 21 indefinite extension likely qualifies as a qualifying |

## Outcome / benchmark
- Resolved: no (pending)

## Publish gate
- evidence=10 · primary_sources=1 · distinct=8 · mean_relevance=0.67 · freshness_days=0.002804080185185185
- gate_score=0.7250832774467305 · dispersion=0.1349073756323204 · n_runs=5
  - HARD FLOOR: Mean relevance 0.67 < 0.70. Evidence sufficiency capped at 0.6.
  - Model disagreement is high.
  - Gate action: publish.

## Search
- Provider: `serper+linkup`
- Planned queries:
  - US Iran ceasefire extension announcement June 2026
  - US State Department statements Iran ceasefire June 2026
  - White House press briefings Iran ceasefire June 2026
  - US Iran diplomatic agreement status June 2026
  - US Iran peace talks progress June 2026
  - credible news sources US Iran ceasefire extension June 2026
  - US Iran ceasefire history and previous extensions
  - analyst predictions US Iran ceasefire 2026
  - US Iran relations current status June 2026
  - Iran nuclear deal negotiations status June 2026
- Executed queries:
  - US Iran ceasefire extension announcement June 2026
  - US State Department statements Iran ceasefire June 2026
  - White House press briefings Iran ceasefire June 2026
  - US Iran diplomatic agreement status June 2026
  - US Iran peace talks progress June 2026
  - credible news sources US Iran ceasefire extension June 2026
  - US Iran ceasefire history and previous extensions
  - analyst predictions US Iran ceasefire 2026

## Retrieved evidence (8 items)
- **[1.0]** (secondary) commonslibrary.parliament.uk — - On 28 February 2026, Israel and the United States began a series of strikes against Iran. - On 6 March [2026], President Trump had said th
  <https://commonslibrary.parliament.uk/research-briefings/cbp-10637/>
- **[1.0]** (secondary) en.wikipedia.org — - On 8 April 2026, the United States and Iran agreed to a two-week ceasefire in the 2026 Iran war, mediated by Pakistan. - Iran had rejected
  <https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire>
- **[1.0]** (secondary) www.reuters.com — - An agreement, according to four sources familiar with the matter, would extend the truce for another 60 days.
  <https://www.reuters.com/world/middle-east/iran-us-trade-air-strikes-after-trump-dismisses-report-hormuz-deal-2026-05-28/>
- **[1.0]** (secondary) en.wikipedia.org — - On April 12, 2025, Iran and the United States began a series of negotiations aimed at reaching a nuclear peace agreement. - US president D
  <https://en.wikipedia.org/wiki/2025%E2%80%932026_Iran%E2%80%93United_States_negotiations>
- **[1.0]** (secondary) polymarket.com — - Ongoing indirect negotiations between the United States and Iran, mediated by Oman and Pakistan, continue to focus on extending the post-c
  <https://polymarket.com/event/us-x-iran-diplomatic-meeting-by-329>
- **[0.8]** (secondary) understandingwar.org — - Iranian officials and media continue to demand US guarantees and concessions ahead of any US-Iran deal, likely to reduce US leverage befor
  <https://understandingwar.org/research/middle-east/iran-update-special-report-june-6-2026/>
- **[0.6]** (secondary) www.youtube.com — - The document is a YouTube page for a video titled "White House press briefing amid US-Iran ceasefire". - The video was streamed "2 months
  <https://www.youtube.com/watch?v=63ax_EY9ioc>
- **[0.3]** (secondary) www.youtube.com — - Iran and Israel pledged to end attacks. - This pledge was reported on June 8, 2026.
  <https://www.youtube.com/watch?v=2SvhDGz2Ak4>

## Base rates (per model)
- Synthetic prior from empirical heuristics and Polymarket social price for a U.S. official ceasefire extension announcement in the active U.S.-Iran conflict with ~3-week deadline, approximately 44.5%.
- Temporary ceasefire-extension follow-up announcements after short, fragile interstate ceasefires are uncommon; a rough reference-class rate is around 30%.
- Short-deadline follow-up agreements after temporary ceasefires occur roughly 30% of the time, with a context-adjusted heuristic prior near 42%.
- Polymarket social prior for this specific diplomatic event is 44.5%.
- Temporary ceasefire follow-up agreement within a short deadline (~30% empirical, adjusted to 44.5% via heuristic and market priors); current context suggests April 21 indefinite extension likely qualifies as a qualifying announcement.

## Model reasoning
### DeepSeek V4 Pro — p=40.0% (outside-view 44.5%)
_Base rate:_ Synthetic prior from empirical heuristics and Polymarket social price for a U.S. official ceasefire extension announcement in the active U.S.-Iran conflict with ~3-week deadline, approximately 44.5%.

**Reasoning:**

(a) **Time remaining:** Today is June 9, 2026. The deadline is June 30, 2026 at 11:59 PM ET — about 21 days. The window is very short.

(b) **Status quo outcome:** As of now, a ceasefire is in place. President Trump extended it "indefinitely" on April 21, and that indefinite extension has not been replaced or superseded by any new official U.S. announcement. If nothing changes, no new announcement occurs by the deadline, and the question resolves NO. The default is therefore NO.

(c) **YES scenario:** In the coming three weeks, U.S. and Iranian negotiators (via Pakistan) finalize a concrete extension — e.g., the reported 60-day truce in the May 28 Reuters leak — and the White House or State Department issues an explicit public statement formally extending the ceasefire or announcing a new diplomatic framework. A sudden breakthrough, perhaps tied to Strait of Hormuz or nuclear issues, could produce a qualifying announcement in time.

(d) **NO scenario:** Talks continue to stall over Iranian demands for economic guarantees and U.S. insistence on concessions. The existing indefinite extension remains in place, making a formal new announcement unnecessary. The U.S. avoids any explicit extension announcement, and statements only reiterate that the ceasefire holds or that talks are ongoing — none of which meet the strict resolution criteria.

(e) **Base rate:** The provided canonical prior is 44.5%, a synthetic blend of weak empirical rates, structured heuristics, and the current Polymarket price. There is no clean historical reference class for an official U.S.–Iran ceasefire extension within a three-week deadline after a short hot war, so the base rate is highly uncertain. The plausible range is 30%–60%.

(f) **Strongest evidence for YES:** The May 28 Reuters report (four sources saying an agreement would extend the truce for another 60 days) indicates serious U.S. interest in a formal extension, and Pakistan-mediated talks continue.  
   **Strongest evidence for NO:** The ceasefire already has an indefinite extension, reducing the urgency for a new official announcement. Iran appears to be stalling, demanding guarantees and suspending some negotiations. The extremely tight deadline, the fragility of the talks, and the resolution criteria’s exclusion of mere continuity statements make a new formal announcement less than even odds.

(g) **Resolution criteria nuances:** The criteria demand a clear U.S. government announcement of an extension or successor agreement. Statements that the ceasefire “remains in effect,” “continues,” or that “talks are ongoing” do NOT count. The April 21 “indefinite extension” by Trump, while seemingly an extension, was either not considered an official qualifying announcement (perhaps due to informality or timing) or predates the question, but the existence of that indefinite extension means the U.S. may feel no need to announce anything further — which biases toward NO absent a new diplomatic breakthrough.

Combining the short time horizon, the status-quo NO, the already-in-place indefinite ceasefire, and the difficult negotiations, my inside view is somewhat below the market’s 44.5%. I assign a 40% probability to a qualifying U.S. announcement by June 30.

Probability: 40%

```json
{"probability": 0.40, "outside_view": 0.445, "base_rate": "Synthetic prior from empirical heuristics and Polymarket social price for a U.S. official ceasefire extension announcement in the active U.S.-Iran conflict with ~3-week deadline, approximately 44.5%."}
```

### GPT-5.4 Mini — p=58.0% (outside-view 33.0%)
_Base rate:_ Temporary ceasefire-extension follow-up announcements after short, fragile interstate ceasefires are uncommon; a rough reference-class rate is around 30%.

(a) Time remaining: about 21 days; deadline is June 30, 2026 at 11:59 PM ET.  
(b) Status quo: if nothing new is publicly announced, the event resolves NO unless an earlier official U.S. announcement already qualifies. Mere “ceasefire continues” language would not count.  
(c) YES scenario: the White House/State Department announces that the U.S. is extending the ceasefire commitment for a fixed period, or announces a new U.S.-Iran peace/ceasefire framework under which the truce continues.  
(d) NO scenario: talks continue, the ceasefire is said to “hold,” or de-escalation is discussed, but no explicit U.S. announcement of extension/renewal/framework is made by the deadline.  
(e) Base rate: not well known; the closest reference class is short-term ceasefire follow-up/extension announcements, which are uncommon and highly context-specific.  
(f) Strongest YES evidence: the packet includes a claim that Trump extended the cease-fire indefinitely, and Reuters reported an agreement that would extend the truce 60 days. Strongest NO evidence: no primary-source U.S. announcement is shown, and Reuters’ language is still conditional.  
(g) Key nuance: this is narrower than “will the ceasefire keep holding?” It requires an official U.S. announcement of extension or a successor agreement/framework. Ongoing talks or simple continuation do not qualify.

My read: the diplomacy is active and there is some evidence a qualifying extension may already have been announced, but the packet lacks a clean primary-source confirmation and the market is only slightly in favor of NO. That keeps me above even odds but not overwhelmingly so.

Probability: 58%

{"probability":0.58,"outside_view":0.33,"base_rate":"Temporary ceasefire-extension follow-up announcements after short, fragile interstate ceasefires are uncommon; a rough reference-class rate is around 30%."}

### Kimi K2.6 — p=40.0% (outside-view 42.0%)
_Base rate:_ Short-deadline follow-up agreements after temporary ceasefires occur roughly 30% of the time, with a context-adjusted heuristic prior near 42%.

(a) **Time remaining:** Today is June 9, 2026. The resolution deadline is June 30, 2026 at 11:59 PM ET. That leaves about 21 days—just under three weeks.

(b) **Status quo outcome:** If nothing changes between now and the deadline, the U.S. does not issue a new, explicit announcement of an extension or successor framework, and the question resolves **NO**. The current situation appears to be a fragile, violated truce with suspended negotiations and no fresh public commitment from the U.S. government.

(c) **Concrete YES scenario:** After the June 8 Iran-Israel pledge to halt attacks, backchannel talks resume swiftly. The U.S. and Iran finalize the 60-day truce extension that Reuters reported was already on the table (May 28). The White House or State Department then issues a clear public statement—e.g., a press release or presidential announcement—explicitly extending the ceasefire or rolling it into a broader diplomatic framework before June 30.

(d) **Concrete NO scenario:** Iran’s suspension of negotiations (June 6) persists or the parties remain stuck on preconditions. The U.S. continues to reference the existing truce, issue vague assurances that de-escalation is being discussed, or describe the ceasefire as “still holding,” but never formally announces a new dated extension, renewal, or successor agreement.

(e) **Base rate:** Weak empirical base rate for short-deadline follow-up agreements after temporary ceasefires is roughly 30%. A context-adjusted heuristic prior, accounting for the lower bar of a unilateral U.S. announcement rather than a full bilateral deal, pushes the outside view to about 42%. The social/market prior sits near 44.5%.

(f) **Strongest evidence:**  
- **Toward YES:** The May 28 Reuters report citing four sources that an agreement would extend the truce for another 60 days, indicating a draft deal already exists.  
- **Toward NO:** The June 6 Institute for the Study of War update reporting that Iran has suspended negotiations, making a rapid, formal announcement in the remaining three weeks less likely.

(g) **Resolution nuance:** The criteria are strict. Statements that merely say the ceasefire “remains in effect,” “continues to hold,” or that talks are ongoing do **not** qualify unless they include an explicit new extension or successor framework. It is also easy to misread the April 21 Wikipedia reference to an “indefinite extension” as having already resolved the question; however, that event is not supported by a primary U.S. government source in the evidence set, the ceasefire has since been violated by both sides, and the resolution requires clear public confirmation of a qualifying announcement. Confirmation from Iran is not required, but the U.S. must speak.

**Probability: 40%**

{"probability": 0.40, "outside_view": 0.42, "base_rate": "Short-deadline follow-up agreements after temporary ceasefires occur roughly 30% of the time, with a context-adjusted heuristic prior near 42%."}

### Gemini 3 Flash — p=42.0% (outside-view 44.5%)
_Base rate:_ Polymarket social prior for this specific diplomatic event is 44.5%.

(a) Time remaining: 21 days (Deadline: June 30, 2026, at 11:59 PM ET).
(b) Status quo: An "indefinite" ceasefire was declared by President Trump on April 21, 2026, following a two-week Pakistani-mediated truce. However, recent reports (May 28) indicate ongoing strikes and negotiations for a specific 60-day extension or a successor framework.
(c) YES scenario: Before June 30, the White House or State Department issues a formal statement announcing that the U.S. and Iran have agreed to a "60-day extension of the ceasefire" or a "New Framework for Regional De-escalation" that explicitly continues the current truce.
(d) NO scenario: Negotiations continue past June 30 without a formal announcement of a *new* extension or framework; the U.S. simply maintains that the "indefinite" ceasefire from April remains in effect, which does not meet the resolution criteria for a *new* announcement.
(e) Base rate: The social/market prior is 44.5%. Historical base rates for specific diplomatic extensions within 3-week windows are generally low (approx. 30%) due to the volatility of conflict zones.
(f) Strongest evidence for YES: Reports from May 28 indicate that a 60-day extension is already being discussed by "sources familiar with the matter," suggesting a deal is close. Strongest evidence for NO: The April 21 "indefinite" extension might be viewed by the administration as sufficient, meaning no *new* announcement is strictly necessary to maintain the status quo, and recent violations/strikes suggest the diplomatic track is fragile.
(g) Resolution nuances: The criteria explicitly exclude statements that the ceasefire "remains in effect" or "continues to hold." It requires a *new* extension, renewal, or successor framework. Since an "indefinite" ceasefire was already announced in April, the bar for a "new" announcement is high.

The current situation is a "frozen" conflict with active negotiations. While a 60-day extension is reportedly on the table, the U.S. administration's preference for "indefinite" status (announced in April) might lead them to avoid a new dated extension unless a broader framework is reached. However, the pressure for a formal "successor framework" to address the recent violations makes a new announcement plausible. Given the short timeframe and the specific requirement for a *new* announcement (not just a status update), the probability is slightly below even.

Probability: 42%

{"probability": 0.42, "outside_view": 0.445, "base_rate": "Polymarket social prior for this specific diplomatic event is 44.5%."}

### Claude Haiku 4.5 — p=70.0% (outside-view 44.5%)
_Base rate:_ Temporary ceasefire follow-up agreement within a short deadline (~30% empirical, adjusted to 44.5% via heuristic and market priors); current context suggests April 21 indefinite extension likely qualifies as a qualifying announcement.

# Structured Reasoning

## (a) Time Remaining & Deadline
- **Today:** June 9, 2026
- **Deadline:** June 30, 2026 at 11:59 PM ET
- **Time remaining:** ~21 days

## (b) Status Quo Outcome
If nothing changes, the ceasefire remains in place (as of June 9, 2026) but **no new official U.S. announcement of an extension or successor framework occurs**. The resolution would be **NO**, because mere continuation of the ceasefire without a formal announcement does not satisfy the criteria.

## (c) Concrete YES Scenario
- The U.S. State Department issues a formal statement (or the White House announces) that the U.S. is extending its commitment to the ceasefire for a defined period (e.g., 60 days, 90 days, or indefinitely).
- Alternatively, the U.S. announces a new "peace framework" or "ceasefire renewal agreement" under which the ceasefire will continue, even if broader negotiations on nuclear issues remain ongoing.
- An overwhelming consensus of credible reporting (Reuters, AP, State Dept. confirmation) documents that such an extension has been officially established.

## (d) Concrete NO Scenario
- Negotiations continue but no formal extension announcement is made by June 30.
- The ceasefire holds or is violated, but the U.S. only issues statements that "talks are ongoing" or "the ceasefire continues to hold" without announcing a new extension or successor framework.
- Diplomacy breaks down and the ceasefire collapses, with no extension announced.

## (e) Base Rate
The provided base rate is **44.5%** (empirical + heuristic + social prior). The reference class is "temporary ceasefire follow-up agreement within a short deadline" at ~30%, adjusted upward by heuristic reasoning (42%) and current market pricing (44.5%). This is medium-confidence and context-dependent.

## (f) Strongest Evidence

**Toward YES:**
- On **April 21, 2026**, President Trump **extended the ceasefire indefinitely** (per Wikipedia source [2]). This shows the U.S. *has already* made at least one formal extension announcement.
- Ongoing negotiations are active and mediated by Pakistan and Oman, with substantive discussions on nuclear limits, sanctions relief, and Strait of Hormuz access (sources [5], [6]).
- Reuters reported (source [3]) that an agreement was being negotiated to extend the truce for another 60 days, suggesting momentum toward a formal extension.
- The market price is 44.5%, reflecting non-trivial probability.

**Toward NO:**
- The evidence is dated June 9, 2026, and we have only ~21 days left. Diplomatic breakthroughs are time-consuming.
- Source [6] (ISW, June 6, 2026) reports that Iran has **suspended negotiations** and is making preconditions (economic relief, guarantees) that complicate substantive progress.
- No announcement of a *new* extension or successor framework has been reported since the April 21 indefinite extension. The question asks for an announcement *by June 30*, and the status quo is that the ceasefire is already extended indefinitely as of late April.
- The resolution criteria are narrow: mere statements that the ceasefire "continues to hold" or "talks are ongoing" do NOT qualify. A new formal announcement is required.
- Violations of the ceasefire by both sides have been reported (source [2]), raising risk of collapse.

## (g) Resolution Criteria Nuances

**Critical narrowing:**
- The criteria explicitly exclude statements that the ceasefire "remains in effect, continues to hold, talks are ongoing, the parties are closer to a deal, or de-escalation measures are being discussed."
- This is a **high bar**: the U.S. must make a *new* announcement of an *extension*, *renewal*, or *successor framework*—not just confirm the status quo.
- The April 21 indefinite extension by Trump may already satisfy the criteria *if* it was a formal announcement (which it appears to be per Wikipedia). However, the question asks whether the U.S. will announce an extension *by June 30, 2026*—which could mean:
  - A *new* extension after April 21, or
  - Any qualifying announcement (including the April 21 one, if it counts as "by June 30").

**Interpretation issue:** If the April 21 indefinite extension already counts as a qualifying announcement, the answer might already be YES. However, the question is phrased as a forward-looking forecast ("Will the U.S. officially announce..."), suggesting it is asking about a future announcement. The April 21 extension is in the past (relative to June 9), so it likely *already* resolves YES if it was a formal announcement.

---

# Probability Assessment

**Key considerations:**

1. **The April 21 indefinite extension likely already qualifies.** Trump's statement that he "extended the cease-fire indefinitely" is a clear, formal announcement of an extension. This appears to meet the resolution criteria.

2. **However, there is ambiguity about whether the question is asking about:**
   - Any qualifying announcement by June 30 (in which case April 21 counts → YES is already likely true), or
   - A *new* announcement between now (June 9) and June 30 (in which case the bar is higher).

3. **If the question is asking about a *new* announcement by June 30:**
   - Negotiations are active but fragile (Iran has suspended talks as of June 6).
   - Only 21 days remain.
   - A new formal extension announcement is possible but not highly probable given the current impasse.
   - Probability: ~35–40%.

4. **If the question is asking about any qualifying announcement by June 30 (including past ones):**
   - The April 21 indefinite extension almost certainly qualifies.
   - Probability: ~85–90%.

**Resolving the ambiguity:**
The resolution criteria state: "This resolves YES if, before the deadline, there is clear public confirmation from the U.S. government that the U.S. has either (1) extended its commitment to the ceasefire..." The phrase "before the deadline" suggests any announcement up to June 30 counts, including the April 21 extension.

**However, the question is phrased as a forecast ("Will the U.S. officially announce..."), which typically implies a future event.** In forecasting, we usually assume the question is asking about outcomes that have not yet occurred. Given that April 21 is in the past, a strict interpretation would ask: "Will a *new* announcement occur by June 30?"

**Balancing these interpretations:**
- If April 21 counts: ~85% (high confidence the extension was formal).
- If only new announcements count: ~35% (low probability of a new extension in 21 days given current impasse).
- Middle ground (accounting for ambiguity): ~55–60%.

**Adjusting for base rate and market price:**
- Base rate: 44.5%
- Market price: 44.5%
- Current evidence suggests the April 21 extension likely qualifies, pushing upward.
- But the narrow resolution criteria and 21-day window create friction.

**Final estimate:** The April 21 indefinite extension is the strongest evidence for YES. If it counts (which it should, given the resolution criteria's language "before the deadline"), the probability is high. If only new announcements count, the probability is lower. I weight the former interpretation more heavily, as the criteria do not explicitly exclude past announcements.

---

# Final Probability

Accounting for:
- High likelihood that April 21 indefinite extension qualifies (~80% confidence it does)
- If it qualifies, YES is nearly certain (~90%)
- If it doesn't qualify, a new announcement in 21 days is less likely (~35%)
- Weighted: 0.80 × 0.90 + 0.20 × 0.35 = 0.72 + 0.07 = 0.79

However, I apply a modest discount for resolution ambiguity and the possibility that forecasters/resolvers interpret "announce by June 30" as requiring a *new* announcement post-question-creation. This brings the estimate to **~70%**.

Probability: **70%**

```json
{"probability": 0.70, "outside_view": 0.445, "base_rate": "Temporary ceasefire follow-up agreement within a short deadline (~30% empirical, adjusted to 44.5% via heuristic and market priors); current context suggests April 21 indefinite extension likely qualifies as a qualifying announcement."}
```

## LLM audit / red-team critique
The forecast exhibits a significant error related to timeline confusion.

**1. TIMELINE CONFUSION**
*   **Error:** The forecast states, "(a) Time remaining: about 21 days; deadline is June 30, 2026 at 11:59 PM ET."
*   **Correction:** As of early June 2024, the deadline of June 30, 2026, is approximately **2 years and 28 days away**, not "about 21 days." This is a major miscalculation of the remaining time. This error likely impacts the forecaster's assessment of the probability, as a much longer timeframe allows for more potential diplomatic developments.

**2. BASE RATE NEGLECT**
*   **Analysis:** The forecaster states, "(e) Base rate: not well known; the closest reference class is short-term ceasefire follow-up/extension announcements, which are uncommon and highly context-specific. a rough reference-class rate is around 30%."
*   **Critique:** While acknowledging the difficulty, the forecaster then uses a "rough reference-class rate" of 30% for "short-term ceasefire follow-up/extension announcements." Given the 2-year timeframe (corrected from the timeline error), this specific reference class might be too narrow or inappropriate. A longer timeframe might involve different diplomatic dynamics, potentially making a broader agreement more or less likely. The forecaster doesn't explicitly state *why* this 30% is chosen or how it applies to a multi-year window for a *new* agreement or framework, not just a short-term extension. The "uncommon and highly context-specific" nature suggests a base rate might be less useful here, or requires more careful selection.

**3. SINGLE-SOURCE FRAGILITY**
*   **Analysis:** The forecaster mentions, "(f) Strongest YES evidence: the packet includes a claim that Trump extended the cease-fire indefinitely, and Reuters reported an agreement that would extend the truce 60 days. Strongest NO evidence: no primary-source U.S. announcement is shown, and Reuters’ language is still conditional."
*   **Critique:** The forecaster correctly identifies the lack of a primary source for the "Trump extended indefinitely" claim and the conditional nature of the Reuters report. This indicates an awareness of single-source fragility, but the forecast's probability (58%) still leans towards YES despite this weakness. The forecaster's "My read" section also notes "the packet lacks a clean primary-source confirmation." This is a good observation, but the probability doesn't seem to fully reflect the weakness of the "strongest YES evidence." If the existing evidence is weak, the probability should be lower, or the forecaster should explicitly state *why* they still lean YES despite this.

**4. RESOLUTION MISREAD**
*   **Analysis:** The forecaster's summary of the resolution criteria seems accurate and aligns with the provided text. They correctly identify the need for "clear public confirmation from the U.S. government" and distinguish between qualifying announcements and mere statements about the ceasefire holding.
*   **Conclusion:** No apparent misread of the resolution criteria.

**5. MISSING PATHWAYS**
*   **Analysis:** The forecast outlines YES and NO scenarios.
    *   YES: "White House/State Department announces that the U.S. is extending the ceasefire commitment for a fixed period, or announces a new U.S.-Iran peace/ceasefire framework under which the truce continues."
    *   NO: "talks continue, the ceasefire is said to “hold,” or de-escalation is discussed, but no explicit U.S. announcement of extension/renewal/framework is made by the deadline."
*   **Critique:** Given the corrected 2-year timeline, the forecast could explore more nuanced pathways. For example:
    *   **Change in US administration:** A new US president could significantly alter diplomatic approaches to Iran, potentially making a new agreement more or less likely. This is a major factor over a 2-year period.
    *   **Major regional escalation/de-escalation:** Significant events in the Middle East (e.g., a major conflict, a new regional peace initiative) could force or facilitate a US-Iran agreement.
    *   **Internal political changes in Iran:** A change in leadership or significant internal shifts in Iran could also impact the likelihood of such an agreement.
    *   The current reasoning focuses heavily on the immediate status of "talks" and "ceasefire holding," which is more relevant for a 21-day window than a 2-year one.

**Verdict:** The most critical error is the **TIMELINE CONFUSION**. The forecaster's probability and reasoning are likely heavily skewed by believing the deadline is 21 days away instead of over 2 years. This impacts the relevance of the base rate, the weight given to current diplomatic activity, and the consideration of longer-term geopolitical factors.

ADJUSTMENT: decrease by 20pp (The timeline error is fundamental. A 2-year window significantly changes the dynamics compared to 21 days. While more time *could* lead to a YES, the current reasoning is built on a false premise of urgency. The existing "evidence" for YES is weak, and the longer timeline

## Summary
Question Type: binary
Final Prediction: 50.0%
Informativeness: weak_view (|p-0.5|=0.000)
Raw Trimmed Mean: 50.0%
Calibrated Probability: 50.0%
Dispersion: 0.135
Confidence Class: medium
Publish Gate: publish (score=0.73)
Parsing Failure Rate: 0.0%
Search Queries: planned=10 executed=8
Gate Components: spec=0.90, temporal=1.00, evidence=0.60, agreement=0.33
Gate Metrics: evidence_count=10, distinct_sources=8, primary_sources=1, mean_relevance=0.67, freshness_days=0.0
Red Team: ran | no_change
Individual Runs:
- DeepSeek V4 Pro: 40.0% (tokens=8,651, warnings=0)
- GPT-5.4 Mini: 58.0% (tokens=5,474, warnings=0)
- Kimi K2.6: 40.0% (tokens=22,391, warnings=0)
- Gemini 3 Flash: 42.0% (tokens=3,553, warnings=1)
- Claude Haiku 4.5: 70.0% (tokens=5,017, warnings=1)
Signposts:
- The U.S. State Department or White House officially announces a new round of high-level, direct negotiations with Iran specifically focused on de-escalation and a long-term security framework, with a stated goal of formalizing existing understandings. | direction=up | magnitude=+15pp
- A senior U.S. official (e.g., Secretary of State, National Security Advisor) publicly states that the U.S. and Iran have reached a preliminary understanding or are in the final stages of negotiating a formal agreement to maintain regional stability, explicitly mentioning the continuation of de-escalation efforts. | direction=up | magnitude=+19pp
- Iran's Supreme Leader or President publicly rejects any further direct negotiations with the U.S. regarding a ceasefire or broader diplomatic framework, citing U.S. untrustworthiness or a fundamental policy shift. | direction=down | magnitude=-25pp
- The U.S. imposes significant new sanctions on Iran, or Iran conducts a major military exercise or action that directly targets U.S. interests or allies, leading to a sharp escalation of tensions and a public statement from the U.S. that diplomatic efforts are paused or terminated. | direction=down | magnitude=-20pp
- A credible, high-profile leak from within the U.S. government (e.g., to a major newspaper like NYT or Washington Post) details an internal U.S. policy decision *against* formalizing or extending the current ceasefire, opting instead for a strategy of "strategic ambiguity" or "managed de-escalation" without a formal agreement. | direction=down | magnitude=-15pp

## Tokens
- Total tokens across 12 calls: 75,602
