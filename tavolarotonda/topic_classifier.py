"""Topic classifier — Tavola Rotonda AQ Session 2/10.

Classifica il topic e consiglia il preset migliore.
"""
from __future__ import annotations

# Keyword per tipo di topic (in ordine di priorità: primo match)
_TYPE_PATTERNS: list[tuple[str, list[str]]] = [
    ("codice", [
        "codice", "funzione", "algoritmo", "bug", "refactor", "python", "javascript",
        "react", "api", "database", "sql", "debug", "programmazione", "software",
        "classe", "loop", "errore", "compil", "test", "deploy", "git",
    ]),
    ("pratica", [
        "come fare", "come risolvo", "miglior", "ottimizz", "efficient", "veloc",
        "configur", "install", "setup", "fare una scelta", "decisione pratica",
        "runway", "budget", "tempo", "deadline", "piano", "organizz",
    ]),
    ("etica", [
        "giusto", "sbagliato", "etica", "morale", "bias", "discriminaz",
        "responsabil", "privacy", "trasparen", "onest", "bugia", "tradiment",
        "correttezza", " fairness",
    ]),
    ("filosofia", [
        "significato", "esistenza", "coscienza", "libero arbitrio", "scopo",
        "senso della vita", "immortalità", "trascendenza", " metafisic",
        "epistemolog", "ontolog",
    ]),
    ("strategia", [
        "strategia", "business", "startup", "investimento", "mercato",
        "competitor", "prodotto", "uten", "crescita", "pivot", "modello di business",
        "roi", "concorrenza", "vantaggio", "posizionament",
    ]),
    ("creativo", [
        "crea", "idea", "brainstorm", "innov", "design", "fantasi",
        "immagina", "progetta", "concept", "storytelling", "brand",
        "reinvent", "trasform",
    ]),
]

# Mappatura tipo → preset consigliato + motivazione
_TYPE_TO_PRESET: dict[str, tuple[str, str]] = {
    "codice": (
        "alternating",
        "Coding + pratica → alternating cloud: MiniMax veloce + GLM per soluzioni creative + Opus per architettura"
    ),
    "pratica": (
        "alternating",
        "Questione operativa → alternating cloud: risposte concrete da MiniMax + validazione Opus + creatività GLM"
    ),
    "etica": (
        "triade",
        "Argomento etico → triade cloud: Opus per profondità argomentativa + GLM per prospettive filosofiche"
    ),
    "filosofia": (
        "triade",
        "Domanda filosofica → triade cloud: Opus per ragionamento astratto + GLM per pensiero strategico"
    ),
    "strategia": (
        "trilogy",
        "Decisione strategica → trilogy: tutti e 3 i modelli premium per visione completa"
    ),
    "creativo": (
        "trilogy",
        "Richiesta creativa → trilogy: GLM per originalità + Opus per profondità + MiniMax per fattibilità"
    ),
}

_TYPE_LABELS: dict[str, str] = {
    "codice": "Codice / Tecnico",
    "pratica": "Pratica / Operativa",
    "etica": "Etica / Morale",
    "filosofia": "Filosofia / Astratta",
    "strategia": "Strategia / Business",
    "creativo": "Creatività / Idee",
}


def classify_topic(topic: str) -> tuple[str, str, str]:
    """Classifica un topic e ritorna (tipo, preset, motivazione).

    Returns:
        tipo: categoria del topic
        preset: nome del preset consigliato
        motivazione: spiegazione della scelta (per UI)
    """
    if not topic:
        return "pratica", "alternating", "Topic vuoto → alternating cloud come default"

    topic_lower = topic.lower()

    for tipo, keywords in _TYPE_PATTERNS:
        for kw in keywords:
            if kw in topic_lower:
                preset, motivazione = _TYPE_TO_PRESET[tipo]
                return tipo, preset, motivazione

    # Default: alternating
    return "pratica", "alternating", "Topic generico → alternating cloud: bilanciato e versatile"


def get_routing_preview(topic: str) -> dict:
    """Ritorna un dict completo per la UI con spiegazione."""
    tipo, preset, motivazione = classify_topic(topic)
    label = _TYPE_LABELS.get(tipo, tipo)
    return {
        "tipo": tipo,
        "tipo_label": label,
        "preset": preset,
        "preset_label": preset.title(),
        "motivazione": motivazione,
        "topic_preview": topic[:100] + ("…" if len(topic) > 100 else ""),
    }

