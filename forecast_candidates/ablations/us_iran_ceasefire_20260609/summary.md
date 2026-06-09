# US-Iran Ceasefire Prior Ablation - 2026-06-09

Question: Will the U.S. officially announce an extension of the ceasefire agreement between the U.S. and Iran, or announce a new peace agreement, ceasefire framework, or diplomatic agreement under which the ceasefire will continue, by June 30, 2026 at 11:59 PM ET?

Polymarket snapshot at spec creation:

- Yes: 44.5%
- No: 55.5%
- Captured: 2026-06-09T17:22:57Z
- URL: https://polymarket.com/event/us-announces-new-iran-agreementceasefire-extension-by

## Arms

| Arm | Final YES | Notes |
| --- | ---: | --- |
| baseline_no_prior_packet | 86.8% | Very high; several models treated reported progress or the April 21 indefinite extension as close to or already qualifying. |
| empirical_history_prior_packet | 60.0% | Weak empirical prior pulled the aggregate down, but dispersion was very high. |
| structured_heuristic_prior_packet | 57.6% | Similar to empirical arm; explicit threshold logic reduced overconfidence but one model still output 99%. |
| empirical_heuristic_market_social_prior_packet | 50.0% | Closest to the 44.5% market snapshot; market/social prior damped the high-YES interpretation. |

## Interpretation

This is a much more sensitive ablation than the Fed/ECB test. The explicit prior packets moved the aggregate substantially:

- Baseline to empirical: -26.8pp
- Baseline to structured heuristic: -29.2pp
- Baseline to market/social: -36.8pp

The run also exposed a resolution-interpretation hazard. Several baseline models leaned heavily on claims that President Trump had already extended the ceasefire indefinitely on April 21, or that a deal was "largely negotiated" and imminent. That may be resolution-relevant, but it is not obviously the same as the market's narrow June 30 announcement criterion, especially if the market expects a new or successor announcement. The red-team audit flagged vague base-rate and interpretation issues but did not adjust the forecast.

Operational takeaway: for geopolitical markets with legally narrow resolution wording, the base-rate packet is doing useful work partly by forcing threshold decomposition, not just by adding historical frequency information. The market/social prior arm also helps prevent models from over-updating on optimistic diplomatic language.
