"""Exporters — CSV, Markdown, JSON, PDF."""
from __future__ import annotations

import csv
import io
import json
import re
from fpdf import FPDF
from tavolarotonda.memory_palace import MemoryPalace, transcript_markdown


def to_csv(palace: MemoryPalace) -> str:
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["phase", "agent", "round", "model", "text"])
    for b in palace.brainstorm:
        w.writerow(["brainstorm", b.get("agent",""), b.get("round",""), b.get("model",""), (b.get("text","") or "").replace("\n"," ")[:500]])
    for c in palace.critique:
        w.writerow(["critique", c.get("agent",""), c.get("round",""), c.get("model",""), (c.get("text","") or "").replace("\n"," ")[:500]])
    return output.getvalue()


def to_markdown(palace: MemoryPalace) -> str:
    return transcript_markdown(palace)


def to_json(palace: MemoryPalace) -> str:
    return json.dumps(palace.to_dict(), indent=2, ensure_ascii=False)


def to_pdf(palace: MemoryPalace) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Tavola Rotonda - Council Report", ln=True)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, f"Topic: {palace.topic or 'N/A'}", ln=True)
    pdf.cell(0, 6, f"Session: {palace.session_id}", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Brainstorm", ln=True)
    pdf.set_font("Helvetica", "", 9)
    for b in palace.brainstorm[:30]:
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 5, f"[{b.get('agent','?')}]", ln=True)
        pdf.set_font("Helvetica", "", 8)
        for line in (b.get("text","") or "").split("\n")[:3]:
            for chunk in re.findall(r".{1,120}(?:\s|$)", line):
                pdf.multi_cell(0, 4, f"  {chunk}")
    pdf.ln(3)
    if palace.votes:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Votes", ln=True)
        pdf.set_font("Helvetica", "", 9)
        for v in palace.votes:
            pdf.cell(0, 5, f"  {v.get('agent','?')}: {v.get('verdict','?')} ({v.get('score',0):.2f})", ln=True)
    return bytes(pdf.output())


_EXPORTERS = {
    "csv": (to_csv, "text/csv", False),
    "markdown": (to_markdown, "text/markdown", False),
    "md": (to_markdown, "text/markdown", False),
    "json": (to_json, "application/json", False),
    "pdf": (to_pdf, "application/pdf", True),
}


def export(palace: MemoryPalace, fmt: str) -> tuple:
    """Ritorna (contenuto, mimetype, is_binary)."""
    exp = _EXPORTERS.get(fmt, (to_json, "application/json", False))
    result = exp[0](palace)
    return result, exp[1], exp[2]
