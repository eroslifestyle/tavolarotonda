"""Custom personas CRUD — AQ Session 5/10.

Permette all'utente di creare/modificare/eliminare personas custom
con LLM assegnato, salvate in JSON.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

_STORE_PATH = Path(__file__).parent.parent / "data" / "custom_personas.json"


@dataclass
class CustomPersona:
    """Una persona creata dall'utente."""
    key: str
    name: str
    figure: str
    domain: str
    provider_key: str
    polarity: str
    system_seed: str
    role_tag: str = ""


def _ensure_store() -> None:
    _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not _STORE_PATH.exists():
        _STORE_PATH.write_text("{}", encoding="utf-8")


def load_personas() -> dict:
    _ensure_store()
    try:
        data = json.loads(_STORE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    return {k: CustomPersona(**v) for k, v in data.items()}


def _save_all(personas: dict) -> None:
    _ensure_store()
    data = {k: asdict(v) for k, v in personas.items()}
    _STORE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def create_persona(persona: CustomPersona) -> CustomPersona:
    personas = load_personas()
    personas[persona.key] = persona
    _save_all(personas)
    return persona


def get_persona(key: str):
    return load_personas().get(key)


def delete_persona(key: str) -> bool:
    personas = load_personas()
    if key in personas:
        del personas[key]
        _save_all(personas)
        return True
    return False


def list_personas() -> list:
    return [asdict(p) for p in load_personas().values()]


def export_personas() -> str:
    _ensure_store()
    return _STORE_PATH.read_text(encoding="utf-8")


def import_personas(json_str: str, merge: bool = True) -> int:
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return 0
    existing = load_personas() if merge else {}
    count = 0
    for k, v in data.items():
        try:
            existing[k] = CustomPersona(**v)
            count += 1
        except TypeError:
            continue
    _save_all(existing)
    return count
