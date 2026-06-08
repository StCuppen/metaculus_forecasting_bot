from __future__ import annotations

import json
from typing import Any


def format_prior_packet_for_prompt(packet: dict[str, Any] | None) -> str:
    """Render a prior/base-rate packet for forecaster prompts.

    The packet may contain empirical base rates, heuristic priors, and social priors.
    Keep the labels explicit so a market/crowd prior is not mistaken for a historical
    base rate.
    """
    if not isinstance(packet, dict) or not packet:
        return ""

    status = str(packet.get("status") or packet.get("canonical_prior_status") or "unknown")
    canonical = packet.get("canonical_prior")
    canonical_type = packet.get("canonical_prior_type") or packet.get("prior_type")
    confidence = packet.get("confidence") or packet.get("prior_confidence")
    should_anchor = packet.get("should_anchor_strongly")
    lines = [
        "BASE-RATE / PRIOR PACKET",
        f"- Status: {status}",
    ]
    if canonical is not None:
        lines.append(f"- Canonical prior: {float(canonical):.1%}")
    if canonical_type:
        lines.append(f"- Canonical prior type: {canonical_type}")
    if confidence:
        lines.append(f"- Confidence: {confidence}")
    if should_anchor is not None:
        lines.append(f"- Should anchor strongly: {bool(should_anchor)}")
    if packet.get("plausible_range"):
        try:
            lo, hi = packet["plausible_range"]
            lines.append(f"- Plausible range: {float(lo):.1%} to {float(hi):.1%}")
        except Exception:
            lines.append(f"- Plausible range: {packet.get('plausible_range')}")

    def _append_candidates(title: str, rows: Any) -> None:
        if not isinstance(rows, list) or not rows:
            return
        lines.append(f"\n{title}:")
        for idx, row in enumerate(rows[:6], start=1):
            if not isinstance(row, dict):
                continue
            name = row.get("name") or row.get("reference_class") or f"candidate {idx}"
            p = row.get("horizon_adjusted_probability")
            if p is None:
                p = row.get("probability") or row.get("prior")
            width = row.get("width") or row.get("class_width")
            reliability = row.get("reliability")
            prefix = f"{idx}. {name}"
            if p is not None:
                try:
                    prefix += f" ({float(p):.1%})"
                except Exception:
                    prefix += f" ({p})"
            meta = ", ".join(str(x) for x in (width, reliability) if x)
            if meta:
                prefix += f" [{meta}]"
            lines.append(prefix)
            rationale = row.get("rationale") or row.get("synthesis_rationale")
            if rationale:
                lines.append(f"   rationale: {str(rationale)[:500]}")
            mismatch = row.get("mismatch_notes") or row.get("mismatch") or row.get("caveats")
            if isinstance(mismatch, list) and mismatch:
                lines.append(f"   caveats: {'; '.join(str(x) for x in mismatch[:3])}")

    _append_candidates("Empirical base-rate candidates", packet.get("empirical_base_rates") or packet.get("reference_classes"))
    _append_candidates("Heuristic priors", packet.get("heuristic_priors"))

    social = packet.get("market_social_prior") or packet.get("social_prior")
    if isinstance(social, dict):
        lines.append("\nSocial prior (not a historical base rate):")
        lines.append(json.dumps(social, ensure_ascii=False, sort_keys=True)[:1200])

    if packet.get("synthesis_rationale"):
        lines.append(f"\nSynthesis rationale: {str(packet.get('synthesis_rationale'))[:1000]}")
    uncertainties = packet.get("main_uncertainties")
    if isinstance(uncertainties, list) and uncertainties:
        lines.append("Main uncertainties:")
        for item in uncertainties[:5]:
            lines.append(f"- {item}")

    lines.append(
        "\nUse this as outside-view context, not as the final answer. "
        "If the packet is weak, heuristic, or mismatched, say so and explain your adjustment."
    )
    return "\n".join(lines)
