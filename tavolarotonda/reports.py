"""Report generator — HTML audit + HTML Q&A compilabile.

Output atteso per l'utente:
1. AUDIT REPORT HTML: pro/contro, criticità, punti di forza, consigli
   - Generato automaticamente alla fine di una sessione di audit
   - Include: riassunto, voti per agente, pro estratti, contro estratti, consigli
2. Q&A HTML: domande multiple → risposte multiple simultanee → analisi comparative
   - L'utente compila il template e il sistema genera risposte in parallelo
   - Output comparativo: per ogni domanda, risposta di ogni agente + sintesi

NO dipendenze esterne (no Jinja2): template f-string puri.
"""

from __future__ import annotations

import html
from datetime import datetime

from .i18n import get_lang, t
from .memory_palace import MemoryPalace

# ponytail: no lang param on template funcs → uses active i18n lang
# callers pass lang= explicitly if they need control over the HTML lang attr


# === TEMPLATE HTML — STILI ===

_HTML_BASE_EN = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --bg: #0e1117; --fg: #e6edf3; --muted: #8b949e;
  --accent: #58a6ff; --success: #3fb950; --danger: #f85149; --warn: #d29922;
  --card: #161b22; --border: #30363d;
}}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
       background: var(--bg); color: var(--fg); margin: 0; padding: 24px; line-height: 1.6; }}
.container {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ font-size: 2.2em; border-bottom: 1px solid var(--border); padding-bottom: 12px; }}
h2 {{ color: var(--accent); margin-top: 32px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
h3 {{ color: var(--fg); margin-top: 20px; }}
.meta {{ color: var(--muted); font-size: 0.9em; margin-bottom: 24px; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px;
         padding: 18px; margin: 14px 0; }}
.pro {{ border-left: 4px solid var(--success); }}
.contro {{ border-left: 4px solid var(--danger); }}
.neutral {{ border-left: 4px solid var(--muted); }}
.crit {{ border-left: 4px solid var(--warn); }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75em;
        background: var(--border); color: var(--muted); margin-right: 6px; }}
.tag.success {{ background: rgba(63,185,80,.15); color: var(--success); }}
.tag.danger {{ background: rgba(248,81,73,.15); color: var(--danger); }}
.tag.warn {{ background: rgba(210,153,34,.15); color: var(--warn); }}
table {{ width: 100%; border-collapse: collapse; margin: 14px 0; }}
th, td {{ padding: 10px; border: 1px solid var(--border); text-align: left; }}
th {{ background: var(--card); }}
.qa-question {{ background: rgba(88,166,255,.05); border: 1px solid var(--accent);
                border-radius: 8px; padding: 14px; margin: 18px 0; }}
.qa-answers {{ display: grid; gap: 10px; grid-template-columns: 1fr 1fr; margin-top: 10px; }}
.qa-answer {{ background: var(--card); border: 1px solid var(--border); border-radius: 6px;
              padding: 12px; font-size: 0.92em; }}
.qa-answer h4 {{ margin: 0 0 6px 0; font-size: 1em; color: var(--accent); }}
.q-form {{ display: flex; flex-direction: column; gap: 8px; margin: 16px 0; }}
.q-form input, .q-form textarea {{
  background: var(--bg); color: var(--fg); border: 1px solid var(--border);
  border-radius: 4px; padding: 8px; font-family: inherit; font-size: 0.95em;
}}
.q-form button {{ background: var(--accent); color: var(--bg); border: none;
                 padding: 10px; border-radius: 4px; cursor: pointer; font-weight: 600; }}
.q-form button:hover {{ opacity: 0.85; }}
.q-item {{ padding: 8px; border: 1px solid var(--border); border-radius: 4px;
           margin: 6px 0; background: var(--bg); display: flex; gap: 8px; align-items: center; }}
.q-item input[type="checkbox"] {{ transform: scale(1.2); }}
hr {{ border: none; border-top: 1px dashed var(--border); margin: 24px 0; }}
small {{ color: var(--muted); }}
footer {{ margin-top: 40px; color: var(--muted); text-size: 0.85em; text-align: center; }}
</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>
"""


_HTML_BASE_IT = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --bg: #0e1117; --fg: #e6edf3; --muted: #8b949e;
  --accent: #58a6ff; --success: #3fb950; --danger: #f85149; --warn: #d29922;
  --card: #161b22; --border: #30363d;
}}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
       background: var(--bg); color: var(--fg); margin: 0; padding: 24px; line-height: 1.6; }}
.container {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ font-size: 2.2em; border-bottom: 1px solid var(--border); padding-bottom: 12px; }}
h2 {{ color: var(--accent); margin-top: 32px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
h3 {{ color: var(--fg); margin-top: 20px; }}
.meta {{ color: var(--muted); font-size: 0.9em; margin-bottom: 24px; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px;
         padding: 18px; margin: 14px 0; }}
.pro {{ border-left: 4px solid var(--success); }}
.contro {{ border-left: 4px solid var(--danger); }}
.neutral {{ border-left: 4px solid var(--muted); }}
.crit {{ border-left: 4px solid var(--warn); }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75em;
        background: var(--border); color: var(--muted); margin-right: 6px; }}
.tag.success {{ background: rgba(63,185,80,.15); color: var(--success); }}
.tag.danger {{ background: rgba(248,81,73,.15); color: var(--danger); }}
.tag.warn {{ background: rgba(210,153,34,.15); color: var(--warn); }}
table {{ width: 100%; border-collapse: collapse; margin: 14px 0; }}
th, td {{ padding: 10px; border: 1px solid var(--border); text-align: left; }}
th {{ background: var(--card); }}
.qa-question {{ background: rgba(88,166,255,.05); border: 1px solid var(--accent);
                border-radius: 8px; padding: 14px; margin: 18px 0; }}
.qa-answers {{ display: grid; gap: 10px; grid-template-columns: 1fr 1fr; margin-top: 10px; }}
.qa-answer {{ background: var(--card); border: 1px solid var(--border); border-radius: 6px;
              padding: 12px; font-size: 0.92em; }}
.qa-answer h4 {{ margin: 0 0 6px 0; font-size: 1em; color: var(--accent); }}
.q-form {{ display: flex; flex-direction: column; gap: 8px; margin: 16px 0; }}
.q-form input, .q-form textarea {{
  background: var(--bg); color: var(--fg); border: 1px solid var(--border);
  border-radius: 4px; padding: 8px; font-family: inherit; font-size: 0.95em;
}}
.q-form button {{ background: var(--accent); color: var(--bg); border: none;
                 padding: 10px; border-radius: 4px; cursor: pointer; font-weight: 600; }}
.q-form button:hover {{ opacity: 0.85; }}
.q-item {{ padding: 8px; border: 1px solid var(--border); border-radius: 4px;
           margin: 6px 0; background: var(--bg); display: flex; gap: 8px; align-items: center; }}
.q-item input[type="checkbox"] {{ transform: scale(1.2); }}
hr {{ border: none; border-top: 1px dashed var(--border); margin: 24px 0; }}
small {{ color: var(--muted); }}
footer {{ margin-top: 40px; color: var(--muted); text-size: 0.85em; text-align: center; }}
</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>
"""

_HTML_BASE = _HTML_BASE_EN  # kept for backward compat, callers use _get_html_base(lang)


def _get_html_base(lang: str) -> str:
    """Return the HTML base template for the given language."""
    return _HTML_BASE_IT if lang == "it" else _HTML_BASE_EN


def _section(lang: str, key: str, **kwargs) -> str:
    """Translate with lang override (bypasses global set_lang)."""
    strings = __import__("tavolarotonda.i18n", fromlist=["STRINGS"]).STRINGS.get(key, {})
    text = strings.get(lang, strings.get("en", key))
    return text.format(**kwargs) if kwargs else text


# === AUDIT REPORT — pro/contro/criticità/punti di forza/consigli ===

def render_audit_report(
    target_name: str,
    target_description: str,
    analysis: dict,
    *,
    title: str | None = None,
    lang: str | None = None,
) -> str:
    """Genera HTML per un audit report.

    `analysis` deve avere:
        - pros: list[str]
        - cons: list[str]
        - crit_points: list[str]  # criticità
        - strong_points: list[str]  # punti di forza
        - suggestions: list[str]
        - agent_opinions: dict[agent_name, str] (opzionale)
        - verdict: str (decisione finale)
        - confidence: float 0-1
        - minority_report: str (opzionale)
        - open_questions: list[str]
    """
    lang = lang or get_lang()
    title = title or f"Audit Report — {target_name}"

    # Estrai elementi con default
    pros = analysis.get("pros", [])
    cons = analysis.get("cons", [])
    crit_points = analysis.get("crit_points", analysis.get("criticisms", []))
    strong_points = analysis.get("strong_points", analysis.get("strengths", []))
    suggestions = analysis.get("suggestions", [])
    agent_opinions = analysis.get("agent_opinions", {})
    verdict = analysis.get("verdict", "(verdict not specified)")
    confidence = float(analysis.get("confidence", 0.0))
    minority = analysis.get("minority_report", "")
    open_qs = analysis.get("open_questions", [])

    # HTML escape
    def e(s: str) -> str:
        return html.escape(str(s)).replace("\n", "<br>")

    # Header
    body_parts = [
        f"<h1>📋 {e(title)}</h1>",
        f'<div class="meta">Target: <b>{e(target_name)}</b> &middot; ',
        f'{_section(lang, "generated", date=datetime.now().strftime("%Y-%m-%d %H:%M"))} &middot; ',
        f'{_section(lang, "confidence")}: <b>{confidence*100:.0f}%</b></div>',
        f'<div class="card">{e(target_description)}</div>',
    ]

    # Verdetto
    body_parts.append(f"""
    <h2>🎯 {_section(lang, "verdict_council")}</h2>
    <div class="card"><b>{e(verdict)}</b></div>
    """)

    # Pro
    if pros:
        body_parts.append(f"<h2>✅ {_section(lang, 'pro_arguments')}</h2>")
        for p in pros:
            body_parts.append(f'<div class="card pro">{e(p)}</div>')

    # Contro
    if cons:
        body_parts.append(f"<h2>❌ {_section(lang, 'contra_arguments')}</h2>")
        for c in cons:
            body_parts.append(f'<div class="card contro">{e(c)}</div>')

    # Punti di forza
    if strong_points:
        body_parts.append(f"<h2>💪 {_section(lang, 'strong_points')}</h2>")
        for s in strong_points:
            body_parts.append(f'<div class="card pro"><span class="tag success">FORZA</span> {e(s)}</div>')

    # Criticità
    if crit_points:
        body_parts.append(f"<h2>⚠️ {_section(lang, 'critical_issues')}</h2>")
        for c in crit_points:
            body_parts.append(f'<div class="card crit"><span class="tag warn">CRITICITÀ</span> {e(c)}</div>')

    # Consigli
    if suggestions:
        body_parts.append(f"<h2>💡 {_section(lang, 'recommendations')}</h2>")
        for s in suggestions:
            body_parts.append(f'<div class="card neutral"><span class="tag">CONSIGLIO</span> {e(s)}</div>')

    # Minority report
    if minority:
        body_parts.append(f"""
        <h2>⚠️ {_section(lang, 'minority_report')}</h2>
        <div class="card crit">{e(minority)}</div>
        """)

    # Open Questions
    if open_qs:
        body_parts.append(f"<h2>❓ {_section(lang, 'open_questions')}</h2><ul>")
        for q in open_qs:
            body_parts.append(f"<li>{e(q)}</li>")
        body_parts.append("</ul>")

    # Opinioni per agente
    if agent_opinions:
        body_parts.append(f"<h2>👥 {_section(lang, 'per_agente')}</h2>")
        for agent_name, opinion in agent_opinions.items():
            body_parts.append(f"""
            <div class="card">
              <h3>{e(agent_name)}</h3>
              <div>{e(opinion)}</div>
            </div>
            """)

    # Footer
    body_parts.append(f"<footer>{_section(lang, 'footer_generated')}</footer>")

    return _get_html_base(lang).format(title=e(title), body="\n".join(body_parts))


# === Q&A HTML — domande multiple → risposte multiple simultanee ===

def render_qa_template(
    title: str,
    questions: list[str] | None = None,
    *,
    prefill_answers: dict[int, dict[str, str]] | None = None,
    lang: str | None = None,
) -> str:
    """Genera un template Q&A compilabile.

    `prefill_answers`: {question_index: {agent_name: answer_text}} — se passato,
    mostra le risposte in formato comparativo (analisi affiancate).
    """
    lang = lang or get_lang()
    questions = questions or [
        "Quali sono i 3 vantaggi principali di adottare questa soluzione?",
        "Quali sono i 3 rischi o svantaggi principali?",
        "Quali alternative dovremmo considerare?",
        "Quali passi concreti consigli nei prossimi 30 giorni?",
        "Esiste un caso d'uso killer che dimostra il valore?",
    ]

    def e(s: str) -> str:
        return html.escape(str(s)).replace("\n", "<br>")

    body = [f"<h1>📝 {e(title)}</h1>"]
    body.append(f'<div class="meta">{_section(lang, "qa_meta")}</div>')

    # Form per aggiungere/modificare domande
    body.append(f'<h2>✏️ {_section(lang, "questions_label")}</h2>')
    body.append('<div id="q-list">')
    for i, q in enumerate(questions):
        body.append(f"""
        <div class="q-item" data-idx="{i}">
          <input type="checkbox" checked>
          <input type="text" value="{e(q)}" style="flex:1">
          <button onclick="this.parentNode.remove()">×</button>
        </div>
        """)
    body.append('</div>')
    body.append(f"""
    <button onclick="addQuestion()" style="margin-top:8px;padding:8px;background:var(--border);
                                            color:var(--fg);border:none;border-radius:4px;cursor:pointer;">
      {_section(lang, "add_question")}
    </button>
    <button onclick="runAnalysis()" style="margin-top:8px;padding:10px 16px;background:var(--accent);
                                              color:var(--bg);border:none;border-radius:4px;cursor:pointer;
                                              font-weight:600;display:block;width:100%;">
      ▶️ {_section(lang, "run_analysis")}
    </button>
    """)

    # Area risultati
    body.append(f'<h2>📊 {_section(lang, "results")}</h2>')
    body.append('<div id="results">'
                f'<p style="color:var(--muted)">{_section(lang, "results_placeholder")}</p>'
                '</div>')

    # Se abbiamo risposte precompilate, mostriamo l'analisi comparativa
    if prefill_answers:
        body.append(f"<hr><h2>🔍 {_section(lang, 'comparative_analysis')}</h2>")
        for i, q in enumerate(questions):
            answers = prefill_answers.get(i, {})
            if not answers:
                continue
            body.append(f'<div class="qa-question"><h3>Q{i+1}: {e(q)}</h3>')
            body.append('<div class="qa-answers">')
            for agent_name, ans in answers.items():
                body.append(f'<div class="qa-answer"><h4>{e(agent_name)}</h4><div>{e(ans)}</div></div>')
            body.append('</div></div>')

    # JS
    body.append("""
    <script>
    function addQuestion() {
      const list = document.getElementById('q-list');
      const idx = list.children.length;
      const item = document.createElement('div');
      item.className = 'q-item';
      item.dataset.idx = idx;
      item.innerHTML = '<input type="checkbox" checked><input type="text" placeholder="Nuova domanda..." style="flex:1"><button onclick="this.parentNode.remove()">×</button>';
      list.appendChild(item);
    }

    function gatherQuestions() {
      const items = document.querySelectorAll('.q-item');
      const qs = [];
      items.forEach(it => {
        const cb = it.querySelector('input[type=checkbox]');
        const txt = it.querySelector('input[type=text]');
        if (cb && cb.checked && txt && txt.value.trim()) qs.push(txt.value.trim());
      });
      return qs;
    }

    async function runAnalysis() {
      const qs = gatherQuestions();
      if (!qs.length) { alert('Inserisci almeno una domanda'); return; }

      const res = document.getElementById('results');
      res.innerHTML = '<p style="color:var(--accent)">⏳ Lancio il council multi-agente...</p>';

      // Demo: qui si chiama l'endpoint backend. Per static demo, simula risposte.
      // In produzione: fetch('/api/qa', {method:'POST', body: JSON.stringify({questions: qs})})
      try {
        const r = await fetch('/api/qa', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({questions: qs})
        });
        if (!r.ok) throw new Error('Backend non raggiungibile');
        const data = await r.json();
        renderResults(data);
      } catch (err) {
        res.innerHTML = '<p style="color:var(--danger)">⚠️ ' + err.message + '. Per vedere una demo funzionante, lancia tavolarotonda localmente.</p>';
      }
    }

    function renderResults(data) {
      const res = document.getElementById('results');
      let html = '';
      (data.answers || []).forEach((qa, i) => {
        html += '<div class="qa-question"><h3>Q' + (i+1) + ': ' + qa.question + '</h3><div class="qa-answers">';
        Object.entries(qa.answers || {}).forEach(([agent, text]) => {
          html += '<div class="qa-answer"><h4>' + agent + '</h4><div>' + text + '</div></div>';
        });
        html += '</div></div>';
      });
      res.innerHTML = html || '<p>Nessuna risposta.</p>';
    }
    </script>
    """)

    body.append(f"<footer>{_section(lang, 'footer_qa')}</footer>")
    return _get_html_base(lang).format(title=e(title), body="\n".join(body))


# === AUDIT REPORT DAL PALACE (auto-generato) ===

def audit_report_from_palace(
    palace: MemoryPalace,
    target_name: str,
    target_description: str,
    *,
    lang: str | None = None,
) -> str:
    """Genera un audit report HTML a partire da un MemoryPalace (post-sessione)."""
    lang = lang or get_lang()
    # Estrai pro/contro/crit dalle brainstorm/critique
    pros, cons = [], []
    for b in palace.brainstorm:
        text = b.get("text", "")
        if any(k in text.lower() for k in ["pro:", "vantaggio", "punto di forza", "approvo"]):
            pros.append(f"**{b['agent']}** (round {b['round']}): {text}")
        if any(k in text.lower() for k in ["contro:", "rischio", "debolezza", "contro"]):
            cons.append(f"**{b['agent']}** (round {b['round']}): {text}")

    crit_points = [
        f"**{c['agent']} → {c['target_agent']}**: {c['text']}"
        for c in palace.critique
    ]

    # Consigli = action items + next steps
    suggestions = list(palace.next_steps or [])
    if not suggestions and palace.synthesis:
        # Estrai "Next Steps" dalla sintesi
        from .phases import _extract_list_section
        if palace.synthesis.get("text"):
            suggestions = _extract_list_section(palace.synthesis["text"], "Next Steps")

    agent_opinions = {
        b["agent"]: b["text"] for b in palace.brainstorm[-6:]  # ultimi 6 contributi
    }

    analysis = {
        "pros": pros[:10],
        "cons": cons[:10],
        "crit_points": crit_points[:10],
        "strong_points": pros[:5],  # alias
        "suggestions": suggestions[:8],
        "agent_opinions": agent_opinions,
        "verdict": palace.decision or "(verdict not yet produced)",
        "confidence": palace.convergence_score,
        "minority_report": palace.minority_report or "",
        "open_questions": palace.open_questions,
    }
    return render_audit_report(target_name, target_description, analysis, lang=lang)


__all__ = [
    "render_audit_report",
    "render_qa_template",
    "audit_report_from_palace",
]
