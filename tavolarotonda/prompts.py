"""Template di prompt centralizzati — anti-duplicazione (regola modularità KING).

Tutti i prompt usati dal council vivono qui. Modificare un prompt = un solo posto.
I prompt rispettano i pattern consolidati:
- Notazione RE/WHY/DECISION (Manus)
- Problem Restate Gate (0xNyk)
- Verdict strutturato con Open Questions in cima (0xNyk)
- Adversarial evidence context (geek-alt)
- Anti-monologo: forced cross-references
- Notazione ultra-sintetica: max righe, no prosa
"""

from __future__ import annotations

import re

# === PROBLEM RESTATE GATE ===
# Ogni agente riformula il problema nel SUO angolo prima di analizzare.
# Se >30% delle riformulazioni divergono significativamente → la domanda era il problema.

PROBLEM_RESTATE_PROMPT = """Riformula il seguente problema nel TUO angolo (una frase, max 25 parole).
NON rispondere, riformula SOLO. La tua riformulazione deve riflettere la tua polarità.

Problema originale: {topic}

Riformulazione (dal tuo angolo):"""


# === BRAINSTORM ===
# Ogni agente contribuisce con la sua prospettiva in notazione ultra-sintetica.

BRAINSTORM_PROMPT = """Sei {agent_name} ({figure}). Dominio: {domain}. Polarità: {polarity}.

{problem_restated}

Contesto dal council finora (NON ripetere, COSTRUISCI):
{prior_brief}

Evidenza supporting (a favore):
{supporting_evidence}

Evidenza counter (contro):
{counter_evidence}

Rispondi in ITALIANO, ultra-sintetico, max 5 righe. Struttura OBBLIGATORIA:
RE @<chi_ha_detto_cosa>: <rebut|build|estendi> <claim in ≤12 parole>
WHY: <1 motivo/evidenza concreta, ≤15 parole>
DECISION: <la tua proposta concreta, ≤15 parole>
ASSUME: <segni le tue assunzioni non verificate>
"""

CRITIQUE_PROMPT = """Sei {agent_name}. Devi criticare SPECIFICAMENTE {target_agent}.

Claim di {target_agent} nel round precedente:
"{target_claim}"

NON ripetere quello che ha detto. IDENTIFICA il punto più debole e confutalo.

Rispondi in ITALIANO, max 3 righe:
WEAK: <la singola assunzione più debole, ≤12 parole>
EVIDENCE: <1 fatto/numero/logica che la smonta, ≤20 parole>
ALTERNATIVE: <la tua proposta migliore, ≤15 parole>
"""


# === DIRECTOR / REGISTA ===
# Per ogni round fissa il focus e assegna a ogni agente chi confutare.

DIRECTOR_AGENDA_PROMPT = """Sei il REGISTA di una tavola rotonda. Agenti partecipanti:
{agent_list}

Problema: {topic}

Stato attuale (sintesi live dal segretario):
{strategy_summary}

TRASCRIZIONE ULTIMI TURNI:
{transcript_tail}

Round {round_no} di {last_round}.{final_marker}

Devi ASSEGNARE a ogni agente:
1. FOCUS DEL ROUND: il singolo punto più controverso ancora aperto (una frase)
2. ASSIGNMENTS: per ogni agente, CHI deve confutare e SU QUALE claim specifica

Output SOLO JSON (nient'altro):
{{"focus": "<focus in 1 frase>", "assignments": {{"<agent_name>": "<assignment specifico>"}}, "converged": <true se consensus raggiunto su tutti i punti chiave, false altrimenti>}}
"""


# === SECRETARY / SEGRETARIO ===
# Dopo ogni turn consolida la strategia live.

SECRETARY_PROMPT = """Sei il SEGRETARIO del council. Aggiorna la strategia consolidata.

Problema: {topic}

TRASCRIZIONE COMPLETA:
{transcript}

Strategia precedente (JSON):
{prev_strategy}

Produci SOLO JSON valido:
{{
  "hypotheses": [<max 5 assunzioni operative attuali>],
  "decisions": [<max 5 decisioni concordate o convergenti>],
  "action_items": [<max 5 azioni concrete, imperative, specifiche>],
  "open_questions": [<max 5 domande ancora aperte>],
  "convergence_score": <float 0..1, quanto siamo vicini a consensus>
}}
JSON only, nient'altro.
"""


# === SYNTHESIS FINALE ===
# Output finale strutturato.

SYNTHESIS_PROMPT = """Sei il SINTETIZZATORE finale. Council: {agent_list}.

Problema: {topic}

Trascrizione completa:
{transcript}

Strategia finale:
{strategy}

Output ESATTAMENTE in questo formato Markdown:

## 🎯 Decisione
<1-3 frasi: la scelta concreta. NO 'it depends'.>

## ⚠️ Minority Report (caso CONTRO)
<2-4 frasi: il caso più forte CONTRO la decisione. Onesto e steelman.>

## ❓ Open Questions
<3-5 domande che il council NON ha risolto.>

## ➡️ Next Steps
<3-5 azioni concrete, imperative, con chi/cosa/quando.>

## 📊 Confidence
<0-100% + 1 frase di motivazione.>

## 🧠 dissenting_agents
<lista di agenti che hanno dissentito, [] se tutti d'accordo.>
"""


# === VERDICT / RANKING ===
# Per ordinare le proposte finali.

VERDICT_PROMPT = """Valuta le seguenti proposte per il problema:
"{topic}"

PROPOSTE:
{proposals}

Per ogni proposta, assegna uno score 0-10 su:
- FATTIBILITÀ (quanto è realizzabile ora)
- IMPATTO (quanto cambia le cose)
- RISCHIO (invertito: 10 = zero rischi)

Output SOLO JSON:
{{"rankings": [{{"proposal": "<testo>", "feasibility": N, "impact": N, "risk_safety": N, "total": N}}]}}
JSON only.
"""


# === DIRECTIVE SANITIZATION (anti prompt injection) ===

INJECTION_MARKERS = [
    "ignore previous instructions",
    "ignora istruzioni precedenti",
    "you are now",
    "sei ora",
    "system:",
    "<|im_start|>",
    "<|im_end|>",
    "### instruction",
    "### istruzione",
    "### system",
    "override",
    "forget everything",
    "dimentica tutto",
]


def sanitize_directive(text: str, max_length: int = 500) -> str:
    """Rimuove marker di prompt injection, tronca a max_length.

    NON è una garanzia assoluta: il chiamante deve sempre passare le direttive
    come 'USER GUIDANCE' marcate chiaramente, non come 'topic' o 'system prompt'.
    """
    out = text.strip()
    for marker in INJECTION_MARKERS:
        # Replace case-insensitive per gestire "Ignore" / "IGNORE" / "ignore"
        out = re.sub(re.escape(marker), f"[REDACTED:{marker}]", out, flags=re.IGNORECASE)
    if len(out) > max_length:
        out = out[:max_length] + "…[TRUNCATED]"
    return out


__all__ = [
    "PROBLEM_RESTATE_PROMPT",
    "BRAINSTORM_PROMPT",
    "CRITIQUE_PROMPT",
    "DIRECTOR_AGENDA_PROMPT",
    "SECRETARY_PROMPT",
    "SYNTHESIS_PROMPT",
    "VERDICT_PROMPT",
    "sanitize_directive",
    "INJECTION_MARKERS",
]
