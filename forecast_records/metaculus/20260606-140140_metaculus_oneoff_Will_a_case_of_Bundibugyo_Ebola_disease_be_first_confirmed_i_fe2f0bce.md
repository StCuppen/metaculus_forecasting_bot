# Will a case of Bundibugyo Ebola disease be first confirmed in the US before 2027?

- **Platform / run type:** metaculus / oneoff
- **Question type:** binary
- **URL:** https://www.metaculus.com/questions/43606
- **Forecast date (UTC):** 2026-06-06T14:01:40.834631+00:00
- **Pipeline:** lean-ensemble/v2-2026.06 · models: deepseek/deepseek-v4-pro, openai/gpt-5.4-mini, moonshotai/kimi-k2.6, google/gemini-3-flash-preview, anthropic/claude-haiku-4.5

## Final forecast
- **Probability: 4.2%**
- Action: **publish** · Confidence: high · Informativeness: strong_view
- Outside-view (base rate) probability: 1.7%

## Outcome / benchmark
- Resolved: no (pending)
- Community prediction: not available (hidden for this question while open)

## Publish gate
- evidence=10 · primary_sources=6 · distinct=7 · mean_relevance=0.63 · freshness_days=0.002331256655092593
- gate_score=0.8341078709457392 · dispersion=0.02588435821108957 · n_runs=5
  - HARD FLOOR: Mean relevance 0.63 < 0.70. Evidence sufficiency capped at 0.6.
  - Gate action: publish.

## Search
- Provider: `serper+linkup`
- Planned queries:
  - Bundibugyo Ebola US CDC confirmed case 2026
  - Ebola virus disease outbreaks 2026 Bundibugyo strain
  - US public health preparedness Bundibugyo Ebola
  - CDC guidelines Bundibugyo Ebola diagnosis US
  - Bundibugyo Ebola transmission risk US
  - history of Ebola cases in US by strain
  - expert predictions Bundibugyo Ebola US 2026
  - Ebola vaccine development Bundibugyo strain 2026
  - travel restrictions Bundibugyo Ebola affected areas 2026
  - US biosafety level 4 labs Bundibugyo Ebola
- Executed queries:
  - Bundibugyo Ebola US CDC confirmed case 2026
  - Ebola virus disease outbreaks 2026 Bundibugyo strain
  - US public health preparedness Bundibugyo Ebola
  - CDC guidelines Bundibugyo Ebola diagnosis US
  - Bundibugyo Ebola transmission risk US
  - history of Ebola cases in US by strain
  - expert predictions Bundibugyo Ebola US 2026
  - Ebola vaccine development Bundibugyo strain 2026

## Retrieved evidence (8 items)
- **[1.0]** (primary) www.who.int — - A medical doctor from the United States of America who was exposed as part of their work caring for patients in the Democratic Republic of
  <https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON605>
- **[0.9]** (secondary) www.naccho.org — - On May 15, 2026, the Ministry of Health of the Democratic Republic of the Congo (DRC) confirmed an outbreak of Ebola disease in Ituri Prov
  <https://www.naccho.org/blog/articles/ebola-outbreak-resources>
- **[0.8]** (primary) www.cdc.gov — - The CDC is issuing a Health Advisory about a new outbreak of Ebola disease in the Democratic Republic of the Congo (DRC) and Uganda caused
  <https://www.cdc.gov/han/php/notices/han00530.html>
- **[0.8]** (primary) www.who.int — - The Director-General of the WHO has determined that the Ebola disease caused by Bundibugyo virus in the Democratic Republic of the Congo a
  <https://www.who.int/news/item/17-05-2026-epidemic-of-ebola-disease-in-the-democratic-republic-of-the-congo-and-uganda-determined-a-public-health-emergency-of-international-concern>
- **[0.8]** (primary) www.cdc.gov — - Bundibugyo virus (species Orthoebolavirus bundibugyoense) causes Bundibugyo virus disease. - Orthoebolaviruses (the group Bundibugyo virus
  <https://www.cdc.gov/ebola/about/index.html>
- **[0.6]** (secondary) www.doctorswithoutborders.org — - The current outbreak discussed in the document is caused by the Bundibugyo virus. - For the Bundibugyo virus, no vaccine or treatment has
  <https://www.doctorswithoutborders.org/latest/bundibugyo-virus-why-ebola-disease-outbreak-different>
- **[0.6]** (secondary) netec.org — - On May 17, the World Health Organization (WHO) declared the Ebola outbreak caused by the Bundibugyo virus in the Democratic Republic of th
  <https://netec.org/2026/05/18/what-healthcare-professionals-should-know-about-the-bundibugyo-ebola-outbreak/>
- **[0.5]** (primary) pmc.ncbi.nlm.nih.gov — - The first known Ebola hemorrhagic fever (EHF) outbreak caused by Bundibugyo Ebola virus occurred in Bundibugyo District, Uganda, in 2007.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3294552/>

## Base rates (per model)
- Only 1 of ~30+ historical Ebola outbreaks (the massive 2014-2016 West African epidemic) produced cases first confirmed in the US, and zero of two prior Bundibugyo outbreaks exported cases outside Africa.
- Bundibugyo Ebola first confirmed in the US is an ultra-rare event class with no known historical instances; imported Ebola cases of other species have occurred, but Bundibugyo-specific U.S. first confirmations have effectively a 0% historical rate.
- Prior Bundibugyo outbreaks (2007, 2012) and other small-to-moderate African Ebola outbreaks produced no laboratory-confirmed cases in the US; the only US-diagnosed Ebola cases arose from the 2014–2016 West Africa Zaire ebolavirus epidemic with >28,000 infections.
- Only one out of dozens of recorded Ebola outbreaks since 1976 has resulted in a case first confirmed on US soil.
- Ebola virus species reaching US: ~4 confirmed cases out of 11,000+ cases globally (0.04%), but BVD-specific history shows 0/2 previous outbreaks escaped Africa; adjusted for entry restrictions and evacuation protocols: 1-2%

## Model reasoning
### DeepSeek V4 Pro — p=n/a

_(no output)_

### GPT-5.4 Mini — p=n/a

_(no output)_

### Kimi K2.6 — p=n/a

_(no output)_

### Gemini 3 Flash — p=n/a

_(no output)_

### Claude Haiku 4.5 — p=n/a

_(no output)_

## Red-team critique
The forecast is well-structured and addresses many key aspects. However, I've identified a potential area for improvement related to "Missing Pathways."

**1. TIMELINE CONFUSION:**
*   The forecast correctly identifies the current date (June 6, 2026) and the deadline (January 1, 2027), and accurately calculates the remaining time. No confusion here.

**2. BASE RATE NEGLECT:**
*   The forecast explicitly discusses the base rate: "There have been only two prior BVD outbreaks (Uganda 2007, DRC 2012), neither of which produced cases outside Africa. For Ebola generally, only the massive 2014–2016 West African Zaire ebolavirus epidemic (with ~28,000 cases) produced cases diagnosed on US soil (4 cases)." It also includes a specific `base_rate` field in the JSON. This is well-addressed.

**3. SINGLE-SOURCE FRAGILITY:**
*   The reasoning summary cites "CDC and NACCHO" for risk assessment, and mentions "PHEIC" (Public Health Emergency of International Concern), implying WHO. It also references "mid-May 2026" for outbreak size, suggesting ongoing monitoring. While specific links aren't provided, the reasoning doesn't appear to rely on a single, easily invalidated source. The information seems to be drawn from general public health reporting.

**4. RESOLUTION MISREAD:**
*   The forecast explicitly highlights and correctly interprets the key narrowing elements of the resolution criteria: "first confirmed in any of the 50 US states or the District of Columbia" and "only Bundibugyo virus counts." It correctly notes that medical evacuations of cases confirmed elsewhere would not count. This is well-understood.

**5. MISSING PATHWAYS:**
*   The forecast's "Scenario leading to YES" focuses on an "asymptomatic or pre-symptomatic traveler from the affected region (DRC/Uganda) enters the US... develops symptoms days later, seeks care... and is laboratory-confirmed." This is a plausible and common pathway for imported infectious diseases.
*   However, it largely overlooks the possibility of **secondary transmission within the US**. While the initial case would still need to be "first confirmed" in the US, the forecast doesn't explicitly consider the possibility that this initial case might infect others *before* diagnosis, and one of *those* secondary cases could be the one that is "first confirmed" in the US. While less likely for Ebola due to transmission dynamics (requires direct contact with bodily fluids of symptomatic individuals), it's not impossible, especially if the initial case has atypical symptoms or is misdiagnosed for a period.
*   More significantly, the forecast emphasizes the "low" risk assessment by the CDC and NACCHO, and the effectiveness of "travel restrictions and exit screening." While these are important, they are not foolproof. The "Strongest evidence for YES" mentions the outbreak spreading to Kampala, a major travel hub, increasing export risk.
*   The forecast also states, "The one known infected American was transported to Germany, not the US." This is used as evidence for NO. However, this scenario (medical evacuation) is distinct from a case *first confirmed* in the US. The fact that an American *was infected* and *could have been brought to the US* (even if not counting for resolution) indicates a potential for US citizens to be exposed and then return home.
*   The forecast's probability of 4.2% seems quite low given the 7-month timeframe and the fact that a PHEIC has been declared. While the outbreak is small *currently*, Ebola outbreaks can escalate rapidly. The "low" risk assessment by the CDC is often a public communication strategy and doesn't necessarily reflect the full spectrum of tail risks. The forecast acknowledges the "tail event" nature but might be underestimating the probability of such a tail event occurring over 7 months, especially with international spread already confirmed. The "low" risk assessment might be overly reassuring.

**Verdict:** The forecast is generally strong, but the probability might be slightly underestimated due to an implicit over-reliance on current containment measures and a slight underestimation of the "tail risk" over a 7-month period, especially considering the international spread and the declaration of a PHEIC. The "Missing Pathways" concern is primarily about the robustness of the "NO" scenario's assumptions (perfect containment, no secondary transmission leading to first US confirmation).

ADJUSTMENT: increase by 2pp
CONFIDENCE IN ADJUSTMENT: medium

## Summary
Question Type: binary
Final Prediction: 4.2%
Informativeness: strong_view (|p-0.5|=0.458)
Raw Trimmed Mean: 4.2%
Calibrated Probability: 4.2%
Dispersion: 0.026
Confidence Class: high
Publish Gate: publish (score=0.83)
Parsing Failure Rate: 0.0%
Search Queries: planned=10 executed=8
Gate Components: spec=0.90, temporal=1.00, evidence=0.60, agreement=0.87
Gate Metrics: evidence_count=10, distinct_sources=7, primary_sources=6, mean_relevance=0.63, freshness_days=0.0
Red Team: ran | no_change
Individual Runs:
- DeepSeek V4 Pro: 4.0% (tokens=3,212, warnings=0)
- GPT-5.4 Mini: 3.0% (tokens=4,861, warnings=0)
- Kimi K2.6: 5.0% (tokens=12,335, warnings=1)
- Gemini 3 Flash: 8.0% (tokens=3,175, warnings=0)
- Claude Haiku 4.5: 1.0% (tokens=3,942, warnings=0)
Signposts:
- The WHO declares the Bundibugyo outbreak to be a Public Health Emergency of International Concern (PHEIC) for a second time, specifically citing widespread international spread or a significant increase in cases in major travel hubs outside the DRC/Uganda. | direction=up | magnitude=+15pp
- The CDC or US Department of State issues a "Do Not Travel" advisory for all of Uganda and/or the DRC, and implements mandatory 21-day quarantine for all travelers arriving in the US from these countries, regardless of symptoms. | direction=down | magnitude=-3pp
- A laboratory-confirmed case of Bundibugyo Ebola is reported in a major international travel hub (e.g., London, Paris, Dubai, Johannesburg) in a patient with no direct travel history to the DRC/Uganda, indicating secondary transmission outside the endemic region. | direction=up | magnitude=+20pp
- The current Bundibugyo outbreak in DRC/Uganda is officially declared over by the WHO and national health authorities, with no new cases reported for at least 42 consecutive days. | direction=down | magnitude=-3pp
- The number of confirmed Bundibugyo cases in the current outbreak exceeds 500, with significant spread to multiple new districts or provinces in DRC/Uganda, including at least one major city with an international airport, and the WHO reports a significant increase in the R0 value. | direction=up | magnitude=+25pp

## Tokens
- Total tokens across 12 calls: 53,004
