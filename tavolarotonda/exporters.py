"""Exporters — AQ Session 7/10.

Esporta un MemoryPalace in vari formati: CSV, Markdown, JSON.
"""
from __future__ import annotations

import csv
import io
import json

from tavolarotonda.memory_palace import MemoryPalace, transcript_markdown


def to_csv(palace: MemoryPalace) -> str:
    """Esporta gli eventi del palace in CSV per analisi."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["phase", "agent", "round", "model", "text"])

    for b in palace.brainstorm:
        writer.writerow([
            "brainstorm",
            b.get("agent", ""),
            b.get("round", ""),
            b.get("model", ""),
            (b.get("text", "") or "").replace("\n", " ")[:500],
        ])
    for c in palace.critique:
        writer.writerow([
            "critique",
            c.get("agent", ""),
            c.get("round", ""),
            c.get("model", ""),
            (c.get("text", "") or "").replace("\n", " ")[:500],
        ])
    return output.getvalue()


def to_markdown(palace: MemoryPalace) -> str:
    """Esporta il transcript completo in Markdown."""
    return transcript_markdown(palace)


def to_json(palace: MemoryPalace) -> str:
    """Esporta il palace completo in JSON."""
    return json.dumps(palace.to_dict(), indent=2, ensure_ascii=False)


_EXPORTERS = {
    "csv": (to_csv, "text/csv"),
    "markdown": (to_markdown, "text/markdown"),
    "md": (to_markdown, "text/markdown"),
    "json": (to_json, "application/json"),
}


def export(palace: MemoryPalace, fmt: str) -> tuple[str, str]:
    """Esporta nel formato richiesto. Ritorna (contenuto, mimetype)."""
    exporter, mimetype = _EXPORTERS.get(fmt, (to_json, "application/json"))
    return exporter(palace), mimetype
