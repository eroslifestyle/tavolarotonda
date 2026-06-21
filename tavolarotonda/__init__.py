"""tavolarotonda — Council multi-agente per decisioni reali e concrete.

Package: 9 moduli indipendenti, zero duplicazione, single-source-of-truth.

Moduli:
- agents:     18 personas con polarity pairs
- providers:  LLM abstraction (Ollama / OpenAI-compat / Claude / mock)
- evidence:   Adversarial retrieval (SearXNG / Brave / DDG / mock)
- memory_palace: Stato persistente condiviso
- prompts:    Template prompt centralizzati (anti-duplicazione)
- director:   Regista (focus + assignments per round)
- secretary:  Segretario (strategy live)
- phases:     Pipeline (Research → Restate → Brainstorm → Critique → Synthesis → Vote)
- reports:    HTML audit + Q&A generator

Uso CLI:
    python -m tavolarotonda.tavolarotonda "Dovrei aprire-sorgere il mio agent framework?"
    python -m tavolarotonda.tavolarotonda --audit examples/audit_target.py
    python -m tavolarotonda.tavolarotonda --qa "Domanda 1" "Domanda 2"
"""

__version__ = "0.1.0"

from .agents import AGENTS, Agent, POLARITY_PAIRS, default_council
from .memory_palace import MemoryPalace, transcript_markdown
from .phases import run_full_council
from .providers import LLMProvider, MockProvider
from .reports import audit_report_from_palace, render_audit_report, render_qa_template

__all__ = [
    "AGENTS",
    "Agent",
    "POLARITY_PAIRS",
    "default_council",
    "MemoryPalace",
    "transcript_markdown",
    "run_full_council",
    "LLMProvider",
    "MockProvider",
    "render_audit_report",
    "render_qa_template",
    "audit_report_from_palace",
]
