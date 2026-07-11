"""Memory Palace — stato condiviso persistente per la sessione di tavola rotonda.

Pattern ispirato a `geek-alt/LLM-Council`. Tutti gli agenti leggono/scrivono
qui. Persiste su disco come JSON per resume/replay.

Schema:
{
  "session_id": str,
  "created_at": iso,
  "updated_at": iso,
  "topic": str,
  "problem_restated": dict | None,        # Problem Restate Gate
  "web_research": {"supporting": [...], "counter": [...]},  # Adversarial evidence
  "brainstorm": [{"agent": str, "text": str, "round": int}],
  "critique": [{"agent": str, "target_agent": str, "text": str, "round": int}],
  "synthesis": {"text": str, "round": int} | None,
  "votes": [{"agent": str, "verdict": str, "score": float}],
  "minority_report": str | None,           # sempre presente se converged
  "convergence_score": float,              # 0..1, loop fino a >= threshold
  "decision": str | None,                  # decisione finale se converged
  "open_questions": [str],                 # sempre presenti
  "next_steps": [str],                     # sempre presenti
  "metrics": {"tokens_in": int, "tokens_out": int, "models_used": [...]}
}
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field


@dataclass
class MemoryPalace:
    """Stato persistente condiviso della sessione di dibattito."""

    session_id: str = field(default_factory=lambda: f"tr-{uuid.uuid4().hex[:8]}")
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))
    updated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))
    topic: str = ""
    problem_restated: dict | None = None
    web_research: dict = field(default_factory=lambda: {"supporting": [], "counter": []})
    brainstorm: list[dict] = field(default_factory=list)
    critique: list[dict] = field(default_factory=list)
    synthesis: dict | None = None
    votes: list[dict] = field(default_factory=list)
    minority_report: str | None = None
    convergence_score: float = 0.0
    decision: str | None = None
    open_questions: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=lambda: {"tokens_in": 0, "tokens_out": 0, "models_used": []})

    def touch(self) -> None:
        self.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    def add_brainstorm(self, agent: str, text: str, round: int, model: str = "") -> None:
        self.brainstorm.append({"agent": agent, "text": text, "round": round, "model": model})
        self.touch()

    def add_critique(self, agent: str, target_agent: str, text: str, round: int) -> None:
        self.critique.append({
            "agent": agent, "target_agent": target_agent, "text": text, "round": round
        })
        self.touch()

    def set_synthesis(self, text: str, round: int) -> None:
        self.synthesis = {"text": text, "round": round}
        self.touch()

    def add_vote(self, agent: str, verdict: str, score: float) -> None:
        self.votes.append({"agent": agent, "verdict": verdict, "score": score})
        self.touch()

    def add_research(self, supporting: list, counter: list) -> None:
        self.web_research["supporting"].extend(supporting)
        self.web_research["counter"].extend(counter)
        self.touch()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> MemoryPalace:
        # Filtra solo i campi noti (per forward-compat)
        valid = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**valid)

    def save(self, path: str) -> None:
        """Salva su disco come JSON pretty-printed."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.touch()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> MemoryPalace:
        with open(path, encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


def transcript_markdown(palace: MemoryPalace) -> str:
    """Esporta la sessione come transcript markdown leggibile."""
    lines = [f"# Tavola Rotonda — {palace.topic}", ""]
    lines.append(f"**Sessione**: `{palace.session_id}`  ")
    lines.append(f"**Creato**: {palace.created_at}  ")
    lines.append(f"**Aggiornato**: {palace.updated_at}  ")
    if palace.decision:
        lines.append(f"\n## 🎯 Decisione\n\n{palace.decision}\n")
    lines.append("\n## 🌐 Ricerca web\n")
    lines.append(f"**Supporting ({len(palace.web_research['supporting'])}):**")
    for r in palace.web_research["supporting"][:5]:
        lines.append(f"- {r}")
    lines.append(f"\n**Counter ({len(palace.web_research['counter'])}):**")
    for r in palace.web_research["counter"][:5]:
        lines.append(f"- {r}")
    lines.append("\n## 💡 Brainstorm\n")
    for b in palace.brainstorm:
        lines.append(f"### {b['agent']} (round {b['round']})\n\n{b['text']}\n")
    if palace.critique:
        lines.append("\n## ⚔️ Critica\n")
        for c in palace.critique:
            lines.append(f"**{c['agent']} → {c['target_agent']}** (round {c['round']}): {c['text']}\n")
    if palace.synthesis:
        lines.append(f"\n## 🧬 Sintesi\n\n{palace.synthesis['text']}\n")
    if palace.votes:
        lines.append("\n## 🗳️ Voti\n")
        for v in palace.votes:
            lines.append(f"- **{v['agent']}**: {v['verdict']} (score {v['score']:.2f})")
    if palace.minority_report:
        lines.append(f"\n## ⚠️ Minority Report (caso CONTRO)\n\n{palace.minority_report}\n")
    lines.append("\n## ❓ Open Questions\n")
    for q in palace.open_questions:
        lines.append(f"- {q}")
    lines.append("\n## ➡️ Next Steps\n")
    for s in palace.next_steps:
        lines.append(f"- {s}")
    return "\n".join(lines)


__all__ = ["MemoryPalace", "transcript_markdown"]
