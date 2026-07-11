# HELP — tavolarotonda / AI Round Table

**Council multi-agente for real, concrete decisions.** Zero theory, only practice.

**Consiglio multi-agente per decisioni reali e concrete.** Zero teoria, solo pratica.

---

## Table of Contents / Indice

1. [Quick Start / Avvio rapido](#quick-start--avvio-rapido)
2. [CLI Flags / Opzioni CLI](#cli-flags--opzioni-cli)
3. [Privacy Modes / Modalità di privacy](#privacy-modes--modalità-di-privacy)
4. [Output Formats / Formati di output](#output-formats--formati-di-output)
5. [Troubleshooting / Risoluzione problemi](#troubleshooting--risoluzione-problemi)
6. [Architecture / Architettura](#architecture--architettura)
7. [Contributing / Contribuire](#contributing--contribuire)
8. [License / Licenza](#license--licenza)

---

## Quick Start / Avvio rapido

### Demo — no real LLM / senza LLM reale

```bash
python -m tavolarotonda --mock "Should I open-source my agent framework?"
```

### With Ollama (local model) / Con Ollama (modello locale)

```bash
ollama serve
python -m tavolarotonda "Should I migrate to Postgres?" --privacy local_only
```

### With Claude API / Con API Claude

```bash
export ANTHROPIC_API_KEY=your-key-here
python -m tavolarotonda "What are the risks of microservices?" --model claude-sonnet-5
```

### Audit a code file / Audit di un file di codice

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Open output/audit_report.html → audit with pros/cons/criticisms/advice
# Apri output/audit_report.html → audit con pro/contro/criticità/consigli
```

### Multi-question Q&A / Q&A multi-domanda

```bash
python -m tavolarotonda --qa "Quali sono i rischi?" "Quali alternative?" --mock --output output/qa.html
# Open output/qa.html → compilable template + comparative analysis
# Apri output/qa.html → template compilabile + analisi comparativa
```

---

## CLI Flags / Opzioni CLI

| Flag | Description / Descrizione | Default |
|---|---|---|
| `--mock` | Use MockProvider — no API calls / Usa MockProvider — senza chiamate API | — |
| `--privacy local_only\|cloud_ok\|free_api_ok` | Privacy tier (see Privacy Modes below) | `cloud_ok` |
| `--model <name>` | LLM model name / Nome modello LLM | from MODEL_TIER_MAP |
| `--intensity <tier>` | Intensity tier: `critical\|reasoning\|standard\|fast\|ornith` | `standard` |
| `--rounds <N>` | Number of brainstorming rounds / Numero di round brainstorming | `3` |
| `--audit <file>` | Audit a code file / Audit di un file di codice | — |
| `--qa "Q1" "Q2"` | Multi-question Q&A mode / Modalità Q&A multi-domanda | — |
| `--output <path>` | Output HTML path / Percorso output HTML | `output/report.html` |
| `--provider ollama\|openai\|anthropic\|mock` | LLM provider to use / Provider LLM da usare | auto-detect |
| `--port <N>` | Server port (if using server mode) / Porta server | `8765` |
| `--help` | Show this help / Mostra questa guida | — |

---

## Privacy Modes / Modalità di privacy

**Critical: choose the right tier before sending any data. / Critico: scegli il tier giusto prima di inviare qualsiasi dato.**

| Mode / Modalità | What sends / Cosa invia | Notes / Note |
|---|---|---|
| `local_only` | Only local Ollama | No cloud, no free API / Nessun cloud, nessuna free API |
| `cloud_ok` | + Claude / OpenAI via env key | Default / Predefinito |
| `free_api_ok` | + Groq / Cerebras via LiteLLM | PII redaction active / PII redaction attiva |

> **Warning / Avviso:** `free_api_ok` sends data to third-party free tiers. Do NOT send sensitive data (PII, credentials, proprietary code) in this mode.
> **Attenzione:** `free_api_ok` invia dati a tier free di terze parti. NON inviare dati sensibili (PII, credenziali, codice proprietario) in questa modalità.

---

## Output Formats / Formati di output

### Console — Terminale colorato / Coloured terminal

```bash
python -m tavolarotonda "Should I refactor this service?"
# Rich coloured text output with agent opinions and final verdict
# Output testuale colorato con opinioni degli agenti e verdetto finale
```

### HTML — Audit report / Report di audit

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Open in browser → full audit with pros/cons/criticisms/minority report
# Apri nel browser → audit completo con pro/contro/criticità/minority report
```

### HTML — Q&A template / Template Q&A

```bash
python -m tavolarotonda --qa "Quali rischi?" "Quali alternative?" --mock --output output/qa.html
# Open in browser → compilable Q&A template with comparative analysis per question
# Apri nel browser → template Q&A compilabile con analisi comparativa per domanda
```

---

## Troubleshooting / Risoluzione problemi

### Ollama not running / Ollama non avviato

```bash
ollama serve
```

### API key missing / Chiave API mancante

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...
export OPENAI_API_KEY=sk-...
```

### Model not found / Modello non trovato

```bash
ollama pull llama3.2
# or / oppure
ollama list
```

### Port already in use / Porta già in uso

```bash
python -m tavolarotonda --port 8081
```

### Mock mode always works / La modalità mock funziona sempre

```bash
# If anything fails, fall back to mock:
# Se qualsiasi cosa fallisce, ricadi su mock:
python -m tavolarotonda --mock "Your question here"
```

### Import errors / Errori di import

```bash
pip install requests
# No other dependencies required / Nessun'altra dipendenza richiesta
```

---

## Architecture / Architettura

```
tavolarotonda/
├── __main__.py       # CLI entry point / Entry point CLI
├── agents.py         # 18 personas + polarity pairs
├── providers.py      # LLM abstraction (Ollama / OpenAI / Claude / Mock)
├── evidence.py       # Adversarial retrieval (SearXNG / Brave / DuckDuckGo / Mock)
├── memory_palace.py  # Persistent shared state / Stato persistente condiviso
├── phases.py         # 6-phase pipeline (Research → Restate → Brainstorm → Critique → Synthesis → Vote)
├── director.py       # Director (focus + round assignments / focus + assegnazioni per round)
├── secretary.py      # Secretary (live strategy consolidation / consolidamento strategia live)
├── prompts.py        # Centralised prompt templates (zero duplication / zero duplicazione)
└── reports.py        # HTML audit + Q&A generator
```

### Execution pipeline / Pipeline di esecuzione

| Phase / Fase | Function / Funzione | What it does / Cosa fa |
|---|---|---|
| 0 | Research | Supporting + counter evidence in parallel / Evidenza a favore e contro in parallelo |
| 1 | Problem Restate | Each agent reformulates from their angle / Ogni agente riformula dal proprio angolo |
| 2 | Brainstorm | Director assigns focus + assignments, agents contribute, Secretary consolidates / Director assegna focus + assegnazioni, agenti contribuiscono, Secretary consolida |
| 3 | Critique | Cross-examination, each agent rebuts another / Cross-examination, ogni agente confuta un altro |
| 4 | Synthesis | Decision + minority report + open questions + next steps |
| 5 | Verdict | Votes 0–10 on feasibility / impact / risk_safety |

### Security built-ins / Sicurezza integrata

- **Prompt injection mitigation** via `sanitize_directive()` — removes/marks injection markers, truncates to 500 chars
- **PII redaction** — active only on `free_api_ok` tier; masks email, IP, phone, tax code (Italian CF)
- **Circuit breaker** — `CircuitBreaker` class prevents cascade failures
- **Timeout** — 120s default per LLM call, 3 retries with exponential backoff

---

## Contributing / Contribuire

1. **Fork** the repository / Fai un fork del repository
2. **Create a feature branch** / Crea un branch per la feature

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Run tests** / Esegui i test

   ```bash
   python -m pytest tests/ -q
   # All 14 tests should pass / Tutti i 14 test dovrebbero passare
   ```

4. **Submit a pull request** / Invia una pull request

### Adding a new agent persona / Aggiungere una nuova persona-agente

Edit `agents.py` — personas follow the pattern:

```python
Persona(
    name="Your Persona",
    role="description",
    polarity_pair=(pro_position, con_position),
    archetype="archetype"
)
```

### Adding a new LLM provider / Aggiungere un nuovo provider LLM

Edit `providers.py` — implement `LLMProvider` interface:

```python
class YourProvider(LLMProvider):
    def complete(self, model, prompt, **kwargs) -> str:
        ...
```

---

## License / Licenza

**MIT License** — see `LICENSE` file for full terms.

**Licenza MIT** — vedi il file `LICENSE` per i termini completi.

---

_Generated for tavolarotonda-due / Generato per tavolarotonda-due — 2026-07-11_
