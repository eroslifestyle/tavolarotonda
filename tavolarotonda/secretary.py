"""Secretary / Segretario — consolida la strategia live dopo ogni turn.

Output JSON: {hypotheses, decisions, action_items, open_questions, convergence_score}.
"""

from __future__ import annotations

import json as _json

from .memory_palace import MemoryPalace
from .prompts import SECRETARY_PROMPT
from .providers import LLMProvider
from .director import _extract_json


class Secretary:
    """Consolida la strategia live ad ogni turn."""

    def __init__(self, provider: LLMProvider, model: str):
        self.provider = provider
        self.model = model

    async def update(self, palace: MemoryPalace) -> dict:
        """Aggiorna palace.strategy_summary in place."""
        transcript = [
            f"{b['agent']}: {b['text']}" for b in palace.brainstorm
        ] + [
            f"{c['agent']}→{c['target_agent']}: {c['text']}" for c in palace.critique
        ]

        prompt = SECRETARY_PROMPT.format(
            topic=palace.topic,
            transcript="\n".join(transcript) or "(vuoto)",
            prev_strategy=_json.dumps(
                {
                    "hypotheses": palace.open_questions[:5],
                    "decisions": [],
                    "action_items": [],
                    "open_questions": palace.open_questions,
                },
                ensure_ascii=False,
            ),
        )
        result = await self.provider.complete(
            prompt,
            model=self.model,
            system="Sei il segretario. Rispondi SOLO con JSON valido.",
            temperature=0.2,
            max_tokens=600,
        )
        if result.error:
            return {}
        parsed = _extract_json(result.text) or {}

        # Scrivi nel palace
        palace.open_questions = list(parsed.get("open_questions", []) or [])[:5]
        palace.convergence_score = float(parsed.get("convergence_score", 0.0) or 0.0)
        palace.metrics["tokens_out"] = palace.metrics.get("tokens_out", 0) + result.tokens_out
        palace.metrics["tokens_in"] = palace.metrics.get("tokens_in", 0) + result.tokens_in
        return parsed

    def summary_text(self, palace: MemoryPalace) -> str:
        """Genera un summary testuale della strategia per i prompt successivi."""
        parts = []
        if palace.open_questions:
            parts.append("Open: " + "; ".join(palace.open_questions[:3]))
        parts.append(f"Convergence: {palace.convergence_score:.2f}")
        return "\n".join(parts)


__all__ = ["Secretary"]
