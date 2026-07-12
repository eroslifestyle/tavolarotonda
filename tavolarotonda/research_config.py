"""Research gating config — AQ Session 8/10.

Controlla quali agenti fanno web research prima di rispondere.
Config persistente in JSON.
"""
from __future__ import annotations

import json
from pathlib import Path

_STORE = Path(__file__).parent.parent / "data" / "research_config.json"

# Default: research abilitata globalmente ma disabilitata per-agente
_DEFAULT = {
    "global_enabled": False,
    "per_agent": {},  # agent_key → bool
    "max_per_side": 5,
    "provider": "auto",  # searxng | brave | duckduckgo | mock | auto
}


def _load() -> dict:
    if not _STORE.exists():
        return dict(_DEFAULT)
    try:
        data = json.loads(_STORE.read_text(encoding="utf-8"))
        return {**_DEFAULT, **data}
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT)


def _save(cfg: dict) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def get_config() -> dict:
    """Ritorna la config research corrente."""
    return _load()


def set_global(enabled: bool) -> dict:
    """Abilita/disabilita research globalmente."""
    cfg = _load()
    cfg["global_enabled"] = enabled
    _save(cfg)
    return cfg


def set_agent(agent_key: str, enabled: bool) -> dict:
    """Abilita/disabilita research per uno specifico agente."""
    cfg = _load()
    cfg["per_agent"][agent_key] = enabled
    _save(cfg)
    return cfg


def is_research_enabled(agent_key: str) -> bool:
    """Verifica se un agente deve fare research.

    Priorità: override per-agente > globale.
    """
    cfg = _load()
    if agent_key in cfg["per_agent"]:
        return cfg["per_agent"][agent_key]
    return cfg["global_enabled"]


def set_provider(provider: str) -> dict:
    """Imposta il provider di ricerca."""
    cfg = _load()
    cfg["provider"] = provider
    _save(cfg)
    return cfg
