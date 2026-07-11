"""Director — sets focus and assigns cross-examination for each round.

Output JSON: {focus, assignments{agent: instruction}, converged}.
"""

from __future__ import annotations

import json as _json
import re

from .prompts import DIRECTOR_AGENDA_PROMPT
from .providers import LLMProvider

_JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(text: str) -> dict:
    """Best-effort JSON extraction (gestisce code fences e testo intorno)."""
    text = text.strip()
    # Rimuovi code fences
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    # Trova il primo { bilanciato
    start = text.find("{")
    if start == -1:
        return {}
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return _json.loads(text[start:i + 1])
                except _json.JSONDecodeError:
                    return {}
    return {}


class Director:
    """Il regista della tavola rotonda: fissa focus + assignments per round."""

    def __init__(self, provider: LLMProvider, model: str):
        self.provider = provider
        self.model = model

    async def set_agenda(
        self,
        topic: str,
        transcript_tail: list[str],
        strategy_summary: str,
        agent_list: list[str],
        round_no: int,
        last_round: int,
    ) -> dict:
        """Restituisce {focus, assignments{agent: instruction}, converged}."""
        prompt = DIRECTOR_AGENDA_PROMPT.format(
            agent_list=", ".join(agent_list),
            topic=topic,
            strategy_summary=strategy_summary or "(nessuna strategia consolidata ancora)",
            transcript_tail="\n".join(transcript_tail[-10:]) if transcript_tail else "(dibattito non iniziato)",
            round_no=round_no,
            last_round=last_round,
            final_marker=" ROUND FINALE: forza decisioni concrete, no 'it depends'." if (round_no >= last_round) else "",
        )
        result = await self.provider.complete(
            prompt,
            model=self.model,
            system="Sei il regista. Rispondi SOLO con JSON valido.",
            temperature=0.3,  # bassa temperatura per output deterministico
            max_tokens=800,
        )
        if result.error:
            return {"focus": "", "assignments": {}, "converged": False}
        parsed = _extract_json(result.text) or {}
        return {
            "focus": str(parsed.get("focus", "")).strip(),
            "assignments": parsed.get("assignments", {}) if isinstance(parsed.get("assignments"), dict) else {},
            "converged": bool(parsed.get("converged", False)),
        }


__all__ = ["Director"]
