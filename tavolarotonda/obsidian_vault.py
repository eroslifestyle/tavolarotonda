"""Integrazione Obsidian vault — lettura topic e salvataggio sessioni."""

from __future__ import annotations

from datetime import date
from pathlib import Path


def read_topic(vault: Path, topic_name: str) -> str:
    """Legge un file .md dal vault Obsidian per nome topic.

    Cerca in vault/istanze/, poi vault/sessioni/, poi vault/.
    Ritorna il contenuto markdown. Solleva FileNotFoundError se non trovato.
    """
    search_paths = [
        vault / "istanze" / f"{topic_name}.md",
        vault / "sessioni" / f"{topic_name}.md",
        vault / "progetti" / "tavolarotonda" / "sessioni" / f"{topic_name}.md",
        vault / f"{topic_name}.md",
    ]
    for path in search_paths:
        if path.exists():
            return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Topic '{topic_name}' non trovato nel vault")


def save_session(
    markdown: str,
    vault: Path,
    session_id: str,
    folder: str = "progetti/tavolarotonda/sessioni/",
) -> Path:
    """Salva il transcript di una sessione nel vault Obsidian.

    Crea la cartella se non esiste. Nome file: sessioni/YYYY-MM-DD-{session_id}.md
    """
    dest_dir = vault / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{date.today().isoformat()}-{session_id}.md"
    dest_path = dest_dir / filename
    dest_path.write_text(markdown, encoding="utf-8")
    return dest_path
