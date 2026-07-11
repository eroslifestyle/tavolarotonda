# tavolarotonda 🥽 / AI Round Table

**Multi-agent council for real, concrete decisions.** Zero theory, only practice.
**Consiglio multi-agente per decisioni reali e concrete.** Zero teoria, solo pratica.

---

## Concept

An open-source council of specialized AI agents that debates your questions through structured phases before delivering actionable verdicts. Each agent represents a distinct persona with a specific angle (advocate, skeptic, analyst, creative) and polarity pairs to prevent groupthink. The system runs locally via Ollama by default, with optional cloud models for increased reasoning power.

Inspired by proven patterns from [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) (⭐982), [Detrol/quorum-cli](https://github.com/Detrol/quorum-cli) (⭐106), and specialized models from [HuggingFace](https://huggingface.co): `RecursiveMAS/Deliberation-Toolcaller-Qwen3.5-4B`, `RecursiveMAS/Deliberation-Reflector-Qwen3.5-4B`, `flowaicom/Flow-Judge-v0.1`. Based on Manus `services/agent-core/app/roundtable.py` (analyzed and improved).

---

## Concept / Concetto

Un council open-source di agenti AI specializzati che dibattono le tue domande attraverso fasi strutturate prima di fornire verdetti actionable. Ogni agente rappresenta una persona distinta con un angolo specifico (avvocato, scettico, analista, creativo) e coppie di polarità per prevenire il groupthink. Il sistema gira localmente via Ollama di default, con modelli cloud opzionali per maggiore potenza di ragionamento.

Ispirato a pattern consolidati da [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) (⭐982), [Detrol/quorum-cli](https://github.com/Detrol/quorum-cli) (⭐106), e modelli specializzati da [HuggingFace](https://huggingface.co). Basato su Manus `services/agent-core/app/roundtable.py` (analizzato e migliorato).

---

## Features / Funzionalità

| Pattern | Implemented |
|---|---|
| 18 personas with polarity pairs | ✅ `agents.py` |
| Problem Restate Gate | ✅ `phase_restate` |
| Adversarial evidence (sup vs counter) | ✅ `evidence.py` |
| Sequential Mixture-of-Agents | ✅ (load/unload via Ollama) |
| Persistent Memory Palace | ✅ `memory_palace.py` |
| Director (focus + assignments) | ✅ `director.py` |
| Secretary (live strategy) | ✅ `secretary.py` |
| RE/WHY/DECISION notation | ✅ `prompts.py` |
| Anti-groupthink (dissent quota) | ✅ via rotation pairs |
| Always minority report | ✅ `phases.phase_synthesis` |
| Structured verdict (Open Q + Next Steps) | ✅ |
| Loop until convergence ≥ threshold | ✅ (early-stop on converged) |
| Explicit privacy tier | ✅ `local_only` / `cloud_ok` / `free_api_ok` |
| Automatic PII redaction | ✅ only on `free_api_ok` |
| Prompt injection mitigation | ✅ `sanitize_directive` |
| Explicit timeout per model | ✅ default 120s |
| Retry with exponential backoff | ✅ 3 attempts |
| Circuit breaker | ✅ `CircuitBreaker` |
| HTML audit report output | ✅ `reports.render_audit_report` |
| HTML Q&A template output | ✅ `reports.render_qa_template` |
| KING modularity (zero duplication) | ✅ 9 independent modules |

---

## Installation / Installazione

```bash
git clone <repo> tavolarotonda
cd tavolarotonda
pip install -r requirements.txt   # only requests + urllib (stdlib)
```

---

## Quick Usage / Uso rapido

### Demo (no real LLM, with MockProvider)

```bash
python -m tavolarotonda --mock "Should I open-source my agent framework?"
```

### Demo (no LLM reale, con MockProvider)

```bash
python -m tavolarotonda --mock "Dovrei aprire-sorgere il mio agent framework?"
```

### With real LLM (local Ollama)

```bash
# 1. Start Ollama
ollama serve

# 2. Launch round table
python -m tavolarotonda "Should I migrate to Postgres?" --privacy local_only
```

### Con LLM reale (Ollama locale)

```bash
# 1. Avvia Ollama
ollama serve

# 2. Lancia tavola rotonda
python -m tavolarotonda "Dovrei migrare a Postgres?" --privacy local_only
```

### Code audit

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Open output/audit_report.html in browser → audit with pros/cons/critiques/advice
```

### Audit di un file di codice

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Apri output/audit_report.html nel browser → audit con pro/contro/criticità/consigli
```

### Multi-question Q&A

```bash
python -m tavolarotonda --qa "What are the risks?" "What alternatives?" --mock --output output/qa.html
# Open output/qa.html → fillable template + comparative analysis per question
```

### Q&A multi-domanda

```bash
python -m tavolarotonda --qa "Quali sono i rischi?" "Quali alternative?" --mock --output output/qa.html
# Apri output/qa.html → template compilabile + analisi comparativa per ogni domanda
```

### Privacy modes / Modalità privacy

```bash
# Only local Ollama models, no cloud, no free-API
python -m tavolarotonda --privacy local_only "topic..."

# + Claude/OpenAI via API key (env: ANTHROPIC_API_KEY, OPENAI_API_KEY)
python -m tavolarotonda --privacy cloud_ok "topic..."

# + Groq/Cerebras via LiteLLM (env: OPENAI_BASE_URL, OPENAI_API_KEY)
# ⚠️ DO NOT send sensitive data to Groq/Cerebras free tier
python -m tavolarotonda --privacy free_api_ok "topic..."
```

---

## Architecture / Architettura

```
tavolarotonda/
├── __init__.py           # Public exports
├── __main__.py           # CLI entry point
├── agents.py             # 18 personas + polarity pairs (single source of truth)
├── providers.py          # LLM abstraction (Ollama / OpenAI-compat / Claude / Mock)
├── evidence.py           # Adversarial retrieval (SearXNG / Brave / DDG / Mock)
├── memory_palace.py      # Shared persistent state
├── prompts.py            # Centralized prompt templates (zero duplication)
├── director.py           # Director (focus + per-round assignments)
├── secretary.py          # Secretary (live strategy)
├── phases.py             # Pipeline: Research → Restate → Brainstorm → Critique → Synthesis → Vote
└── reports.py            # HTML audit + Q&A generator

tests/
└── test_smoke.py         # 14 base tests (no real LLM)

examples/
└── audit_target.py       # Code with intentional issues for audit testing
```

---

## Pipeline (6 phases / 6 fasi)

| Phase | EN | IT |
|---|---|---|
| 0 | **Research**: parallel supporting + counter evidence retrieval | Ricerca in parallelo di evidenze a supporto e contro |
| 1 | **Problem Restate**: each agent reformulates from their angle → if they diverge, the question was wrong | Ogni agente riformula dal proprio angolo → se divergono, la domanda era sbagliata |
| 2 | **Brainstorm**: Director assigns focus + assignments per round, Secretary consolidates | Director assegna focus + compiti per round, Secretary consolida |
| 3 | **Critique**: cross-examination, each agent refutes another | Cross-examination, ogni agente confuta un altro |
| 4 | **Synthesis**: decision + minority report + open questions + next steps | Decisione + minority report + domande aperte + prossimi passi |
| 5 | **Verdict**: votes 0-10 on feasibility/impact/risk_safety | Voti 0-10 su fattibilità/impatto/sicurezza_rischi |

---

## Privacy & Security / Privacy & Sicurezza

| Tier | What is sent | Notes |
|---|---|---|
| `local_only` | Only local Ollama | No cloud, no free-API |
| `cloud_ok` | + Claude/OpenAI via env key | Default |
| `free_api_ok` | + Groq/Cerebras via LiteLLM | Automatic PII redaction (email, IP, phone, tax ID) |

**Prompt injection mitigation**:
- User directives passed through `sanitize_directive()` (removes/marks injection markers, truncates to 500 chars)
- Topic isolated: visible to Director + Secretary, exposed to participants only as `problem_restated`
- Output validation: removes `Qwen3 blocks`, truncates overly long responses

---

## Testing / Test

```bash
cd /tmp/tavolarotonda
python tests/test_smoke.py
# Output: ✅ All 14 tests passed
```

---

## Limitations & Roadmap / Limitazioni & Roadmap

| # | Limitation | Workaround |
|---|---|---|
| 1 | Claude API requires Anthropic SDK (currently only raw HTTP) | Replace `_claude` with SDK when available |
| 2 | Brave/SearXNG require user configuration | Automatic Mock fallback |
| 3 | OCR/screenshots not supported (no Manus-style) | Roadmap v0.2 |
| 4 | No MCP server (vs quorum-cli) | Roadmap v0.2 |
| 5 | Voting scores are mock in `--mock` mode | Real with active LLM |

---

## Bugs Fixed from Original Manus Code / Bug Risolti dal Codice Originale Manus

| # | Original Manus Bug | Fix in tavolarotonda |
|---|---|---|
| 1 | Prompt injection via user directives | `sanitize_directive` removes/marks markers |
| 2 | No explicit timeout for `_say` | Timeout 120s + retry 3x |
| 3 | `_injections` in-memory not persistent | Persistent Memory Palace JSON |
| 4 | Privacy leak to Groq/Cerebras | PII redaction + explicit tier |
| 5 | No rate limit per round | `MAX_ROUNDS` env-config + early-stop on converged |
| 6 | No remote retry/backoff | 3 attempts with exponential backoff |
| 7 | `_project_tree` with `os.walk` depth 2 | Replaceable with `git ls-files` (TODO) |
| 8 | `_extract_json_obj` naive depth | Improved regex + try/except everywhere |
| 9 | `MAX_ROUNDS = 20` hardcoded | Env var + configurable |
| 10 | Temperature 0.85 hardcoded | Per-agent configurable |

---

## License / Licenza

MIT (see LICENSE).
