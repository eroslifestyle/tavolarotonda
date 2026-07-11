"""tavolarotonda — Council multi-agente per decisioni reali e concrete.

Package: 11 moduli indipendenti, zero duplicazione, single-source-of-truth.

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
- obsidian_vault: Lettura topic e salvataggio sessioni nel vault Obsidian
- serve:      HTTP server API Obsidian (starlette + uvicorn)

Uso CLI:
    python -m tavolarotonda "Dovrei aprire-sorgere il mio agent framework?"
    python -m tavolarotonda --audit examples/audit_target.py
    python -m tavolarotonda --qa "Domanda 1" "Domanda 2"
    python -m tavolarotonda serve --port 8765
"""

__version__ = "0.1.0"

from .agents import AGENTS, POLARITY_PAIRS, Agent, default_council
from .i18n import detect_lang, get_lang, reset_lang, set_lang, t
from .memory_palace import MemoryPalace, transcript_markdown
from .obsidian_vault import read_topic, save_session
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
    "read_topic",
    "save_session",
    "t",
    "set_lang",
    "get_lang",
    "detect_lang",
    "reset_lang",
]
