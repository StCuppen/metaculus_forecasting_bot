# Will the U.S. officially announce an extension of the ceasefire agreement between the U.S. and Iran, or announce a new peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue, by June 30, 2026 at 11:59 PM ET?

Resolution criteria: This resolves YES if, before the deadline, there is clear public confirmation from the U.S. government that the U.S. has either (1) extended its commitment to the ceasefire, either as a dated/time-based extension or through an explicit statement that the ceasefire has been extended, or (2) renewed the existing ceasefire as part of a broader peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue. A qualifying announcement resolves YES regardless of whether the extension later takes effect. Statements that merely say the ceasefire remains in effect, continues to hold, talks are ongoing, the parties are closer to a deal, or de-escalation measures are being discussed do not qualify unless they announce a new extension, renewal, or successor framework. An overwhelming consensus of credible reporting that a qualifying extension or successor agreement has been definitively established also suffices. Confirmation from Iran is not required. Otherwise resolves NO.

- **Platform / run type:** other / prior_ablation_baseline_
- **Question type:** binary
- **Forecast date (UTC):** 2026-06-09T17:40:34.628734+00:00
- **Pipeline:** lean-ensemble/v2-2026.06 · models: deepseek/deepseek-v4-pro, openai/gpt-5.4-mini, moonshotai/kimi-k2.6, google/gemini-3-flash-preview, anthropic/claude-haiku-4.5

## Question details
### Canonical spec

- One-line: Will the U.S. officially announce an extension of the ceasefire agreement between the U.S. and Iran, or announce a new peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue, by June 30, 2026 at 11:59 PM ET?
- YES: Clear public confirmation from the U.S. government that the U.S. has either (1) extended its commitment to the ceasefire (dated/time-based or explicit statement) or (2) renewed the existing ceasefire as part of a broader peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue. An overwhelming consensus of credible reporting that a qualifying extension or successor agreement has been definitively established also suffices.
- NO: No such announcement or confirmation by the deadline, or only statements that the ceasefire remains in effect, continues to hold, talks are ongoing, parties are closer to a deal, or de-escalation measures are being discussed without announcing a new extension, renewal, or successor framework.
- Window: by June 30, 2026 at 11:59 PM ET
- Threshold: None
- Metric: None

## Final forecast
- **Probability: 86.8%**
- Action: **publish** · Confidence: medium · Informativeness: strong_view
- Outside-view (base rate) probability: 42.0%

## Model forecasts

| Model | Forecast | Outside view | Tokens | Base rate / short rationale |
|---|---:|---:|---:|---|
| DeepSeek V4 Pro | 90.0% | 75.0% | 5739 | When a U.S. President says a major international deal is 'largely negotiated' and details are coming 'soon', the historical rate of an official announcement materializing within ~3 weeks is roughly 70-80% across comparab |
| GPT-5.4 Mini | 98.0% | 15.0% | 3471 | Rare U.S.-Iran ceasefire-extension announcements; historical rate is effectively very low, but no precise reference class found. |
| Kimi K2.6 | 99.0% | 55.0% | 11835 | Reference class: ceasefires in modern interstate wars extended or superseded by a formal agreement within three months; estimated historical rate is roughly 50-60%. |
| Gemini 3 Flash | 75.0% | 40.0% | 3212 | Diplomatic negotiations involving major conflict de-escalation frameworks typically have a moderate success rate within a 30-day window once 'largely negotiated' status is claimed. |
| Claude Haiku 4.5 | 72.0% | 25.0% | 4070 | No clear historical precedent for U.S.-Iran ceasefire extension announcements; base rate unknown |

## Outcome / benchmark
- Resolved: no (pending)

## Publish gate
- evidence=10 · primary_sources=2 · distinct=8 · mean_relevance=0.67 · freshness_days=0.0029631269791666665
- gate_score=0.7332226192440694 · dispersion=0.1267675037223657 · n_runs=5
  - HARD FLOOR: Mean relevance 0.67 < 0.70. Evidence sufficiency capped at 0.6.
  - Model disagreement is high.
  - Gate action: publish.

## Search
- Provider: `serper+linkup`
- Planned queries:
  - US Iran ceasefire extension announcement June 2026
  - US Iran peace agreement negotiations status June 2026
  - Biden administration Iran policy updates ceasefire
  - US State Department statements Iran ceasefire
  - White House press briefings Iran diplomatic efforts
  - Iran nuclear deal JCPOA revival status 2026
  - Congressional statements US Iran relations ceasefire
  - UN Security Council resolutions Iran sanctions ceasefire
  - Think tank analysis US Iran diplomacy 2026
  - Expert predictions US Iran agreement 2026
- Executed queries:
  - US Iran ceasefire extension announcement June 2026
  - US Iran peace agreement negotiations status June 2026
  - Biden administration Iran policy updates ceasefire
  - US State Department statements Iran ceasefire
  - White House press briefings Iran diplomatic efforts
  - Iran nuclear deal JCPOA revival status 2026
  - Congressional statements US Iran relations ceasefire
  - UN Security Council resolutions Iran sanctions ceasefire

## Retrieved evidence (8 items)
- **[1.0]** (secondary) en.wikipedia.org — - On 8 April 2026, the United States and Iran agreed to a two-week ceasefire in the 2026 Iran war, mediated by Pakistan. - Iran had rejected
  <https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire>
- **[1.0]** (secondary) www.reuters.com — - An agreement, according to four sources familiar with the matter, would extend the truce for another 60 days. - The agreement would allow
  <https://www.reuters.com/world/middle-east/iran-us-trade-air-strikes-after-trump-dismisses-report-hormuz-deal-2026-05-28/>
- **[1.0]** (secondary) en.wikipedia.org — - On April 12, 2025, Iran and the United States began a series of negotiations aimed at reaching a nuclear peace agreement. - US president D
  <https://en.wikipedia.org/wiki/2025%E2%80%932026_Iran%E2%80%93United_States_negotiations>
- **[1.0]** (secondary) www.bbc.com — - US President Donald Trump says an agreement with Iran has been "largely negotiated" and details will be announced soon. - The deal would i
  <https://www.bbc.com/news/articles/crmp121z3z8o>
- **[0.8]** (secondary) www.youtube.com — - A deal to extend the ceasefire between the US and Iran is pending. - This pending deal would reopen the Strait of Hormuz.
  <https://www.youtube.com/watch?v=ISenjuD5vcY>
- **[0.8]** (secondary) www.pbs.org — - Barbara Leaf and Michael Doran are former U.S. officials with experience in Near Eastern Affairs and the Middle East on the National Secur
  <https://www.pbs.org/newshour/show/former-u-s-officials-analyze-chances-fragile-iran-ceasefire-can-hold>
- **[0.8]** (secondary) x.com — - President Trump is committed to making the FIFA World Cup 2026™ the greatest sporting event in world history. - President Donald J. Trump
  <https://x.com/StateDept?lang=en>
- **[0.3]** (secondary) www.youtube.com — - The video is titled "US-Iran peace talks: Is a deal realistic or a diplomatic illusion?". - The video was uploaded by "Al Jazeera English"
  <https://www.youtube.com/watch?v=oWWmeXiS1n8>

## Base rates (per model)
- When a U.S. President says a major international deal is 'largely negotiated' and details are coming 'soon', the historical rate of an official announcement materializing within ~3 weeks is roughly 70-80% across comparable diplomatic engagements.
- Rare U.S.-Iran ceasefire-extension announcements; historical rate is effectively very low, but no precise reference class found.
- Reference class: ceasefires in modern interstate wars extended or superseded by a formal agreement within three months; estimated historical rate is roughly 50-60%.
- Diplomatic negotiations involving major conflict de-escalation frameworks typically have a moderate success rate within a 30-day window once 'largely negotiated' status is claimed.
- No clear historical precedent for U.S.-Iran ceasefire extension announcements; base rate unknown

## Model reasoning
### DeepSeek V4 Pro — p=90.0% (outside-view 75.0%)
_Base rate:_ When a U.S. President says a major international deal is 'largely negotiated' and details are coming 'soon', the historical rate of an official announcement materializing within ~3 weeks is roughly 70-80% across comparable diplomatic engagements.

Based on the evidence as of June 9, 2026, a ceasefire between the U.S. and Iran has been in place since April 8 and was already extended "indefinitely" by President Trump on April 21. The question asks about a further official U.S. announcement by June 30, 2026, either extending the ceasefire or announcing a new peace agreement/framework under which the ceasefire continues. Trump stated on June 9 that an agreement has been "largely negotiated" and details will be announced soon, with Reuters (May 28) reporting a pending 60-day truce extension and the reopening of the Strait of Hormuz. Multiple other sources confirm a deal is imminent.

The resolution window is only 21 days. Trump's public statements create strong pressure for a quick official announcement, consistent with his typical style. While the ceasefire is fragile and could still collapse, the overall trajectory heavily favors an official announcement before the deadline. An announcement of a peace deal or a formal extension would satisfy the criteria; mere "talks ongoing" or "ceasefire holds" statements would not. The imminent nature of the reported agreement makes the YES outcome very likely.

Probability: 90%
{"probability": 0.90, "outside_view": 0.75, "base_rate": "When a U.S. President says a major international deal is 'largely negotiated' and details are coming 'soon', the historical rate of an official announcement materializing within ~3 weeks is roughly 70-80% across comparable diplomatic engagements."}

### GPT-5.4 Mini — p=98.0% (outside-view 15.0%)
_Base rate:_ Rare U.S.-Iran ceasefire-extension announcements; historical rate is effectively very low, but no precise reference class found.

(a) Time remaining: about 21 days. Exact deadline is June 30, 2026 at 11:59 PM ET.

(b) Status quo: if nothing changes, the event is already leaning to YES, because the supplied evidence says the U.S. already officially extended the ceasefire on April 21, 2026 (“extended the cease-fire indefinitely”). If that is correct, the criterion has already been met before the deadline.

(c) Concrete YES scenario: the U.S. State Department, White House, or President formally announces that the U.S.-Iran ceasefire is extended again, or that a broader peace/ceasefire framework has been adopted that keeps the ceasefire in force.

(d) Concrete NO scenario: no qualifying U.S. announcement ever occurs; officials only say the ceasefire is holding, talks are ongoing, or de-escalation continues, without any explicit extension/renewal/framework announcement.

(e) Base rate: I don’t know a clean historical base rate for “U.S. officially announces extension of a ceasefire with Iran,” because this is a very rare and context-specific event. In general, formal ceasefire-extension announcements in U.S.-Iran crises are uncommon.

(f) Strongest evidence toward YES: the provided research note stating that on April 21, President Trump “extended the cease-fire indefinitely.” If accurate, that is already a qualifying public announcement. Strongest evidence toward NO: the lack of a primary-source U.S. government citation in the evidence set, plus Reuters language on May 28 describing an agreement that “would extend” the truce, which sounds reported-but-not-yet-official.

(g) Easy-to-misread issue: the question is not asking whether the ceasefire continues in practice, nor whether talks are promising. It specifically requires an official U.S. announcement of an extension/renewal or a successor agreement/framework. Also, the announcement can count even if it happened before today, as long as it occurred by the deadline.

Probability: 98%

{"probability":0.98,"outside_view":0.15,"base_rate":"Rare U.S.-Iran ceasefire-extension announcements; historical rate is effectively very low, but no precise reference class found."}

### Kimi K2.6 — p=99.0% (outside-view 55.0%)
_Base rate:_ Reference class: ceasefires in modern interstate wars extended or superseded by a formal agreement within three months; estimated historical rate is roughly 50-60%.

(a) **Time remaining:** Today is June 9, 2026. The exact deadline is June 30, 2026 at 11:59 PM ET, so roughly 21 days remain.

(b) **Status quo outcome:** The U.S. already announced an indefinite extension of the ceasefire with Iran on April 21, 2026. Because the resolution criteria count any clear public U.S. confirmation of an extension announced *before* the deadline—and do not require Iranian concurrence—the status quo already satisfies the YES condition.

(c) **Concrete YES scenario:** The scenario has already occurred: on April 21, 2026, President Trump publicly stated that the U.S. was extending the ceasefire indefinitely, which qualifies under criterion (1).

(d) **Concrete NO scenario:** The U.S. government would have to retroactively disavow the April 21 extension as non-official, and then fail to issue any new extension, renewal, or successor framework by June 30. This is highly implausible given the record.

(e) **Base rate:** Reference class: ceasefires in modern interstate wars that are extended or replaced by a formal diplomatic framework within three months; precise historical rates are uncertain but estimated in the 50–60% range. Here, however, the specific evidence overrides the base rate because the event has already taken place.

(f) **Strongest evidence:**
- **Toward YES:** Evidence [1] explicitly states that on April 21, 2026, President Trump extended the U.S.-Iran ceasefire indefinitely.
- **Toward NO:** Evidence [1] and [6] note repeated violations and describe the truce as “fragile,” which could raise doubts about durability, though the criteria explicitly ignore subsequent violations for resolution purposes.

(g) **Easy misreading:** The criteria broaden the question by accepting a unilateral U.S. announcement and do not require Iranian confirmation. One might naively assume a new mutual agreement is needed, or that only statements made *after* the present date count, but the resolution window includes any qualifying announcement prior to the deadline.

Probability: 99%

{"probability": 0.99, "outside_view": 0.55, "base_rate": "Reference class: ceasefires in modern interstate wars extended or superseded by a formal agreement within three months; estimated historical rate is roughly 50-60%."}

### Gemini 3 Flash — p=75.0% (outside-view 40.0%)
_Base rate:_ Diplomatic negotiations involving major conflict de-escalation frameworks typically have a moderate success rate within a 30-day window once 'largely negotiated' status is claimed.

As a professional forecaster, I have analyzed the current geopolitical situation between the United States and Iran based on the provided evidence.

(a) **Time remaining:** 21 days remain until the deadline of June 30, 2026, at 11:59 PM ET.
(b) **Status quo:** There is currently a fragile, indefinite ceasefire in place (extended by President Trump on April 21, 2026). Negotiations for a "Memorandum of Understanding pertaining to PEACE" or a formal successor framework are actively ongoing but have not been finalized or officially announced as a new agreement.
(c) **YES scenario:** Before June 30, the U.S. and Iran finalize the "largely negotiated" deal mentioned by President Trump. The White House releases a statement announcing a "New Peace Framework" or a "60-day extension of the truce" to facilitate the reopening of the Strait of Hormuz.
(d) **NO scenario:** Negotiations continue past the deadline without a formal announcement of a *new* extension or framework. The parties simply continue under the existing "indefinite" ceasefire, or the ceasefire collapses into renewed hostilities before a new agreement is signed.
(e) **Base rate:** Diplomatic negotiations of this magnitude often take longer than expected; however, when a "largely negotiated" deal is publicly touted by a U.S. President, the probability of a formal announcement within a month is relatively high.
(f) **Strongest Evidence:** For YES: President Trump's social media posts and public statements that a deal is "largely negotiated" and "details will be announced soon," combined with reports of a pending 60-day extension. For NO: Historical volatility in U.S.-Iran relations and reports of ongoing ceasefire violations and "fragility" that could derail a final announcement.
(g) **Resolution Nuance:** The criteria specifically exclude statements that the ceasefire "remains in effect" or "talks are ongoing." It requires a *new* extension, renewal, or successor framework. Since the current ceasefire is already "indefinite," a simple continuation doesn't count; there must be a new formal step or a broader peace agreement announced.

The evidence suggests that a deal is imminent and being actively messaged by the U.S. executive branch. With 21 days left and the "largely negotiated" status, there is a high likelihood of a formal announcement to capitalize on the diplomatic momentum before the end of June.

Probability: 75%

{"probability": 0.75, "outside_view": 0.4, "base_rate": "Diplomatic negotiations involving major conflict de-escalation frameworks typically have a moderate success rate within a 30-day window once 'largely negotiated' status is claimed."}

### Claude Haiku 4.5 — p=72.0% (outside-view 25.0%)
_Base rate:_ No clear historical precedent for U.S.-Iran ceasefire extension announcements; base rate unknown

# Forecasting Analysis

## (a) Time Remaining and Deadline
- **Today's date:** June 9, 2026
- **Deadline:** June 30, 2026 at 11:59 PM ET
- **Time remaining:** 21 days

## (b) Status Quo Outcome
If nothing changes, the resolution would be **NO**. The ceasefire remains in effect but no formal extension or new agreement framework has been officially announced by the U.S. government as of the research date (June 9, 2026).

## (c) Concrete YES Scenario
The U.S. State Department issues an official statement or press release within the next 21 days formally announcing:
- An extension of the ceasefire agreement with Iran (with or without a specific duration), OR
- A new peace agreement/ceasefire framework that explicitly renews the ceasefire commitment

This could occur as part of ongoing negotiations that appear to be "largely negotiated" according to Trump's recent statements.

## (d) Concrete NO Scenario
The ceasefire continues to hold informally, but no formal U.S. government announcement of an extension or new framework is made by June 30, 2026. Negotiations continue without reaching a formal announcement threshold, or the ceasefire collapses without a successor agreement being announced.

## (e) Base Rate
**Explicitly unknown.** There is no clear historical precedent for U.S.-Iran ceasefire extensions in this specific context. The 2015 JCPOA was a nuclear agreement, not a ceasefire framework. This appears to be a novel situation (2026 Iran war ceasefire).

## (f) Strongest Evidence

**Toward YES:**
- **Evidence [1]:** President Trump extended the ceasefire "indefinitely" on April 21, 2026—this is a formal extension already announced, though the question asks about extensions *by* June 30, 2026. The fact that an indefinite extension was already announced suggests the U.S. is willing to make formal announcements about ceasefire status.
- **Evidence [4]:** Trump states an agreement has been "largely negotiated" with details to be announced "soon" (as of the BBC report date). This suggests an announcement may be imminent within the 21-day window.
- **Evidence [2]:** Reuters reports an agreement to extend the truce for another 60 days, citing four sources familiar with the matter.

**Toward NO:**
- **Evidence [6]:** Former U.S. officials express serious concerns about the ceasefire's fragility, suggesting it may not hold long enough for a formal extension to be negotiated and announced.
- **Time constraint:** Only 21 days remain. While negotiations appear active, formal announcements require bureaucratic processes and may not materialize this quickly.
- **Violation history:** Evidence [1] notes the ceasefire "has been violated by both sides since its declaration," raising questions about whether formal extensions are even feasible.

## (g) Resolution Criteria Nuances

**Key narrowing elements:**
- The criteria explicitly exclude statements that merely say the ceasefire "remains in effect" or "continues to hold"—it must be a formal **extension** or **new framework**
- An "overwhelming consensus of credible reporting" can also trigger YES, not just official U.S. government statements
- The extension must be announced by the deadline; it doesn't need to take effect by then

**Potential ambiguity:**
- Trump's April 21 indefinite extension (Evidence [1]) may already satisfy the criteria if it counts as a formal extension announcement. However, the question asks about announcements "by June 30, 2026," which could mean additional announcements beyond April 21, or it could mean the April 21 announcement already resolves this YES. The phrasing suggests we're looking for announcements within the specified window, but April 21 is before June 9 (today), so it's unclear if this counts as a qualifying event.

---

## Probability Assessment

**Factors supporting YES (21 days remaining):**
1. Trump has already made one formal extension announcement (April 21), demonstrating willingness to make such announcements
2. Trump's recent statement that a deal is "largely negotiated" suggests an announcement may come soon
3. Reuters reports (Evidence [2]) cite sources saying a 60-day extension agreement exists
4. The resolution criteria allow for "overwhelming consensus of credible reporting," not just official statements
5. Active negotiations are ongoing with apparent progress

**Factors supporting NO:**
1. Only 21 days remain—a short window for formal diplomatic announcements
2. The ceasefire has been violated by both sides, creating uncertainty about whether extensions will be pursued
3. The April 21 indefinite extension may already be the qualifying announcement, meaning no *new* extension is needed
4. "Largely negotiated" doesn't mean announced; Trump's timeline for announcements is vague
5. Status quo bias: most diplomatic processes move slowly

**Critical ambiguity:**
The April 21 indefinite extension is crucial. If this already counts as a qualifying announcement under the resolution criteria, the answer is already YES. If the question is asking for *additional* announcements beyond April 21, the probability is lower.

Given the evidence that Trump has already announced an indefinite extension on April 21, and the resolution criteria state "A qualifying announcement resolves YES regardless of whether the extension later takes effect," I interpret this as the April 21 announcement likely already satisfying the criteria. However, if that announcement doesn't count (e.g., if "indefinite" isn't considered a proper extension), then the 21-day window becomes critical, and the probability drops significantly.

**Weighted assessment:**
- If April 21 counts: ~95% (already resolved YES)
- If April 21 doesn't count: ~35% (21 days, active negotiations but no guarantee)
- Blended probability accounting for ambiguity: ~70%

Probability: **72%**

{"probability": 0.72, "outside_view": 0.25, "base_rate": "No clear historical precedent for U.S.-Iran ceasefire extension announcements; base rate unknown"}

## LLM audit / red-team critique
Here's an adversarial review of the forecast:

**1. TIMELINE CONFUSION:**
*   **Analysis:** The forecast correctly identifies the current date (June 9, 2026) and the deadline (June 30, 2026), noting the 21-day window. It also correctly references past events (April 8 ceasefire, April 21 "indefinite" extension) within the context of the question's future deadline. There is no apparent timeline confusion.
*   **Verdict:** No error.

**2. BASE RATE NEGLECT:**
*   **Analysis:** The forecast provides a specific base rate: "When a U.S. President says a major international deal is 'largely negotiated' and details are coming 'soon', the historical rate of an official announcement materializing within ~3 weeks is roughly 70-80% across comparable diplomatic engagements."
*   **Critique:** While a base rate is provided, its applicability and robustness are questionable.
    *   **Specificity:** "Comparable diplomatic engagements" is vague. What specific historical instances are being referenced? Are they truly comparable in terms of geopolitical context (US-Iran relations), the nature of the deal (ceasefire extension vs. broader peace agreement), and the specific President (Trump's unique communication style and follow-through)?
    *   **"Largely negotiated" vs. "soon":** These are subjective terms. A President's definition of "largely negotiated" might differ significantly from the reality of ongoing complex diplomatic talks. "Soon" can mean anything from days to months.
    *   **Trump's history:** While Trump often announces things "soon," his track record also includes deals that were "imminent" but never materialized or took much longer than anticipated (e.g., North Korea denuclearization, various trade deals). This specific base rate might be overly optimistic given the source and the inherent difficulty of US-Iran diplomacy.
    *   **"Indefinite" extension:** The forecast notes a prior "indefinite" extension. If an extension is already "indefinite," what does a *further* extension or "renewal" mean in practical terms, and how does that affect the base rate for *new* announcements? The base rate doesn't account for this specific nuance.
*   **Verdict:** Potential error. The base rate provided is too generic and doesn't adequately account for the specific context of US-Iran relations, President Trump's communication patterns, or the nature of an "indefinite" ceasefire. It might be an optimistic interpretation of "comparable diplomatic engagements."

**3. SINGLE-SOURCE FRAGILITY:**
*   **Analysis:** The forecast heavily relies on President Trump's statement from June 9 ("largely negotiated," "details will be announced soon") as the primary driver for the high probability. It also cites Reuters (May 28) reporting a "pending 60-day truce extension and the reopening of the Strait of Hormuz" and "Multiple other sources confirm a deal is imminent."
*   **Critique:**
    *   **Trump's statements:** While Trump's statements are significant, they are not always reliable indicators of immediate, concrete action. He has a history of making grand pronouncements that either don't materialize as quickly as suggested or are subject to significant changes. Relying on his statement as the *primary* driver for a 90% probability within 21 days introduces fragility.
    *   **"Multiple other sources":** This is vague. Are these independent, highly credible sources with direct knowledge, or are they echoing Trump's statements or general diplomatic optimism? Without specific examples or an assessment of their credibility, this claim doesn't sufficiently diversify the evidence base.
    *   **Reuters report:** The Reuters report is from May 28, nearly two weeks before Trump's June 9 statement. While it suggests a *pending* deal, the details (60-day truce, Strait of Hormuz) might not align perfectly with what Trump is now calling "largely negotiated" or what the final agreement might entail. The forecast treats these as reinforcing, but they could be distinct or evolving.
    *   **Lack of Iranian confirmation/perspective:** While the resolution criteria state "Confirmation from Iran is not required," the *likelihood* of a US announcement is significantly influenced by the state of negotiations with Iran. If Iran is not on board or has different expectations, the US announcement might be delayed or not happen at all, regardless of Trump's optimism. The forecast doesn't consider this external factor that could derail the US announcement.
*   **Verdict:** Significant error. The forecast exhibits single-source fragility by over-relying on President Trump's statement and insufficiently diversifying or critically evaluating other sources, especially given the short timeframe and the complexity of the parties involved.

**4. RESOLUTION MISREAD:**
*   **Analysis:**
    *   **Question:** "Will the U.S. officially announce an extension... or announce a new peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue..."
    *   **YES criteria:** "Clear public confirmation from the U.S. government that the U.S. has either (1) extended its commitment to the ceasefire... or (2) renewed the existing ceasefire as part of a broader peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue." Also, "An

## Summary
Question Type: binary
Final Prediction: 86.8%
Informativeness: strong_view (|p-0.5|=0.368)
Raw Trimmed Mean: 86.8%
Calibrated Probability: 86.8%
Dispersion: 0.127
Confidence Class: medium
Publish Gate: publish (score=0.73)
Parsing Failure Rate: 0.0%
Search Queries: planned=10 executed=8
Gate Components: spec=0.90, temporal=1.00, evidence=0.60, agreement=0.37
Gate Metrics: evidence_count=10, distinct_sources=8, primary_sources=2, mean_relevance=0.67, freshness_days=0.0
Red Team: ran | no_change
Individual Runs:
- DeepSeek V4 Pro: 90.0% (tokens=5,739, warnings=0)
- GPT-5.4 Mini: 98.0% (tokens=3,471, warnings=0)
- Kimi K2.6: 99.0% (tokens=11,835, warnings=0)
- Gemini 3 Flash: 75.0% (tokens=3,212, warnings=1)
- Claude Haiku 4.5: 72.0% (tokens=4,070, warnings=1)
Signposts:
- President Trump or a senior U.S. official explicitly states that negotiations have stalled or broken down, or that the "largely negotiated" agreement is no longer expected to be announced. | direction=down | magnitude=-30pp
- Iran's Supreme Leader or President issues a strong public statement rejecting the terms of the reported agreement or withdrawing from ongoing negotiations. | direction=down | magnitude=-25pp
- A major military incident occurs between U.S. and Iranian forces or proxies, leading to significant casualties or a direct confrontation. | direction=down | magnitude=-19pp
- The U.S. State Department or White House officially announces a specific date and time for a press conference or joint statement regarding the U.S.-Iran ceasefire or a new diplomatic agreement. | direction=up | magnitude=+12pp
- A highly credible, top-tier news organization (e.g., AP, Reuters, NYT, WSJ) reports with high confidence, citing multiple senior U.S. government sources, that a qualifying announcement is confirmed for a specific date within the resolution window. | direction=up | magnitude=+12pp

## Tokens
- Total tokens across 12 calls: 58,297
