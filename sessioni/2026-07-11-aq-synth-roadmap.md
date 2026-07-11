---
tags: [sessione, tavolarotonda, aq, config, roadmap]
data: 2026-07-11
type: sessione
autore: eros
---

# Sessione 2026-07-11 — AQ Synth + Roadmap + TR-041

## Contesto

Follow-up della sessione AQ benchmark. L'utente ha completato le 20 domande AQ nella pagina `/tmp/aq_tavolarotonda.html`. Sintetizzo risposte → genero roadmap → implemento TR-041 (config.yaml centralizzato).

## Risposte AQ chiave

- Q1=E (tutti distribuito), Q3=A (solo io), Q4=B (2-4 sett)
- Q5=A (solo ai-router), Q6=C (fisso benchmark), Q7=A (silent fallback)
- Q8=B (top 5 AQ), Q10=A (SPA attuale), Q11=C (streaming UX)
- Q12=D (tutti+API), Q13=A (config.yaml), Q14=B (solo provider)
- Q15=A (filesystem), Q16=A (unifica providers), Q17=C (benchmark AQ continuo)
- Q18=A (GH Actions), Q19=A (nessuna auth), Q20=ABCD (tutti future)

## Deliverables

### ROADMAP.md
Generata con sprint plan 4 fasi:
- Sprint 1 (1-2 sett): TR-041 config.yaml + TR-046 unifica providers + TR-042 top5 AQ
- Sprint 2 (2-3 sett): TR-047 streaming UX + TR-048 export+API + TR-049 silent fallback
- Sprint 3 (1-2 sett): TR-044 GH Actions CI + TR-050 Obsidian + TR-051 preset import/export
- Sprint 4 (opzionale): TR-052 multi-turn + TR-053 voice + TR-054 plugin system

### TR-041 — config.yaml centralizzato

**File creati:**
- `tavolarotonda/config.yaml` — 170 righe: models (5), council_presets (3), model_for_provider, agent_colors (18), timeout, export_formats
- `tavolarotonda/config.py` — loader con `load()`, `get_model()`, `get_preset()`, `get_agent_color()`, `get_timeout()`

**gui/app.py refactoring:**
- `MODELS` → caricato da `config.yaml` via `load_config()`
- `COUNCIL_PRESETS` → caricato da `config.yaml`
- `MODEL_FOR_PROVIDER` → caricato da `config.yaml`
- Tutti i `180.0` hardcoded → `get_timeout()`
- Fix: `monolithic` preset con `routing: null` non crashava più `/api/council-presets`

**Verifiche:**
- YAML valido (5 models, 3 presets, 18 agent_colors)
- `config.py` loader funziona: `get_model("opus-local")["aq_score"]=4.69`
- Flask smoke test: `/api/health`, `/api/models`, `/api/council-presets` → tutti 200
- Commit: `2adbdde` (527 righe aggiunte, 112 rimosse)

## AQ Top 5 modelli

| Rank | Modello | Score | Provider |
|---|---|---|---|
| 1 | qwen3.6-opus-abliterated:35b | 4.69 | Ollama locale |
| 2 | qwen2.5-coder-uncensored:32b | 2.23 | Ollama locale |
| 3 | huihui_ai/gemma-4-abliterated:26b | 2.00 | Ollama locale |
| 4 | qwen2.5:14b | 2.00 | Ollama locale |
| 5 | qwen2.5:7b | 2.00 | Ollama locale |

## Commit

- `2adbdde` — feat(aq): synthesize 20 answers → roadmap + config.yaml centralizzato (TR-041)

## Prossimi passi

- TR-046: unificare LLMProvider + AnthropicCompatProvider
- TR-042: top 5 modelli AQ in GUI
- TR-047: streaming UX a colori

## Link

- Commit: `2adbdde`
- ROADMAP.md: `progetti/tavolarotonda-due/ROADMAP.md`
- Config: `progetti/tavolarotonda-due/tavolarotonda/config.{yaml,py}`
- GUI: `progetti/tavolarotonda-due/gui/app.py`
- Checkpoint: `.claude/checkpoints/CP_20260711_2115.md`
