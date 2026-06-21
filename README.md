# tavolarotonda 🥽

**Council multi-agente per decisioni reali e concrete.** Zero teoria, solo pratica.

Software open-source ispirato ai pattern consolidati di:
- [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) (⭐982) — 18 personas + polarity pairs + Problem Restate Gate
- [Detrol/quorum-cli](https://github.com/Detrol/quorum-cli) (⭐106) — CLI dibattiti strutturati + MCP
- [geek-alt/LLM-Council](https://github.com/geek-alt/LLM-Council) — Memory Palace + Sequential Mixture-of-Agents + adversarial evidence + minority report
- [prefrontalsys/panel-of-experts-awscao](https://github.com/prefrontalsys/panel-of-experts-awscao) — Heterogeneous models + profili moderator/pannelist
- Manus `services/agent-core/app/roundtable.py` (analizzato e migliorato) — Director + Secretary + RE/WHY/DECISION

E ai modelli specializzati di [HuggingFace](https://huggingface.co):
- `RecursiveMAS/Deliberation-Toolcaller-Qwen3.5-4B`
- `RecursiveMAS/Deliberation-Reflector-Qwen3.5-4B`
- `flowaicom/Flow-Judge-v0.1`

## Caratteristiche

| Pattern | Implementato |
|---|---|
| 18 personas con polarity pairs | ✅ `agents.py` |
| Problem Restate Gate | ✅ `phase_restate` |
| Adversarial evidence (sup vs counter) | ✅ `evidence.py` |
| Sequential Mixture-of-Agents | ✅ (load/unload via Ollama) |
| Memory Palace persistente | ✅ `memory_palace.py` |
| Director (focus + assignments) | ✅ `director.py` |
| Secretary (strategy live) | ✅ `secretary.py` |
| Notazione RE/WHY/DECISION | ✅ `prompts.py` |
| Anti-groupthink (dissent quota) | ✅ via rotation pairs |
| Minority report sempre | ✅ `phases.phase_synthesis` |
| Verdict strutturato (Open Q + Next Steps) | ✅ |
| Loop fino a convergence ≥ threshold | ✅ (early-stop su converged) |
| Privacy tier esplicito | ✅ `local_only` / `cloud_ok` / `free_api_ok` |
| PII redaction automatica | ✅ solo su `free_api_ok` |
| Prompt injection mitigation | ✅ `sanitize_directive` |
| Timeout esplicito per modello | ✅ default 120s |
| Retry con backoff esponenziale | ✅ 3 tentativi |
| Circuit breaker | ✅ `CircuitBreaker` |
| Output HTML audit report | ✅ `reports.render_audit_report` |
| Output HTML Q&A compilabile | ✅ `reports.render_qa_template` |
| Modularità KING (zero duplicazione) | ✅ 9 moduli indipendenti |

## Installazione

```bash
git clone <repo> tavolarotonda
cd tavolarotonda
pip install -r requirements.txt   # solo requests + urllib (stdlib)
```

## Uso rapido

### Demo (no LLM reale, con MockProvider)

```bash
python -m tavolarotonda --mock "Dovrei aprire-sorgere il mio agent framework?"
```

### Con LLM reale (Ollama locale)

```bash
# 1. Avvia Ollama
ollama serve

# 2. Lancia tavola rotonda
python -m tavolarotonda "Dovrei migrare a Postgres?" --privacy local_only
```

### Audit di un file di codice

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Apri output/audit_report.html nel browser → audit con pro/contro/criticità/consigli
```

### Q&A multi-domanda

```bash
python -m tavolarotonda --qa "Quali sono i rischi?" "Quali alternative?" --mock --output output/qa.html
# Apri output/qa.html → template compilabile + analisi comparativa per ogni domanda
```

### Modalità privacy

```bash
# Solo modelli locali Ollama, niente cloud, niente free-API
python -m tavolarotonda --privacy local_only "topic..."

# + Claude/OpenAI via API key (env: ANTHROPIC_API_KEY, OPENAI_API_KEY)
python -m tavolarotonda --privacy cloud_ok "topic..."

# + Groq/Cerebras via LiteLLM (env: OPENAI_BASE_URL, OPENAI_API_KEY)
# ⚠️ NON inviare dati sensibili a Groq/Cerebras free tier
python -m tavolarotonda --privacy free_api_ok "topic..."
```

## Architettura

```
tavolarotonda/
├── __init__.py           # Export pubblici
├── __main__.py           # Entry point CLI
├── agents.py             # 18 personas + polarity pairs (single source of truth)
├── providers.py          # LLM abstraction (Ollama / OpenAI-compat / Claude / Mock)
├── evidence.py           # Adversarial retrieval (SearXNG / Brave / DDG / Mock)
├── memory_palace.py      # Stato persistente condiviso
├── prompts.py            # Template prompt centralizzati (zero duplicazione)
├── director.py           # Regista (focus + assignments per round)
├── secretary.py          # Segretario (strategy live)
├── phases.py             # Pipeline: Research → Restate → Brainstorm → Critique → Synthesis → Vote
└── reports.py            # HTML audit + Q&A generator

tests/
└── test_smoke.py         # 14 test base (no LLM reale)

examples/
└── audit_target.py       # Codice con criticità intenzionali per test audit
```

## Pipeline di esecuzione

1. **Phase 0 — Research** (`phase_research`): ricerca supporting + counter in parallelo
2. **Phase 1 — Problem Restate** (`phase_restate`): ogni agente riformula nel SUO angolo → se divergono, il problema era la domanda
3. **Phase 2 — Brainstorm** (`phase_brainstorm`): per ogni round, Director assegna focus + assignments, ogni agente contribuisce, Secretary consolida
4. **Phase 3 — Critique** (`phase_critique`): cross-examination, ogni agente confuta un altro
5. **Phase 4 — Synthesis** (`phase_synthesis`): decisione + minority report + open questions + next steps
6. **Phase 5 — Verdict** (`phase_verdict`): voti 0-10 per feasibility/impact/risk_safety

## Privacy & sicurezza

| Livello | Cosa viene inviato | Note |
|---|---|---|
| `local_only` | Solo Ollama locale | Niente cloud, niente free-API |
| `cloud_ok` | + Claude/OpenAI via env key | Default |
| `free_api_ok` | + Groq/Cerebras via LiteLLM | PII redaction automatica (email, IP, telefono, CF) |

**Prompt injection mitigation**:
- Direttive utente passate attraverso `sanitize_directive()` (rimuove/marca injection markers, tronca a 500 char)
- Topic isolato: visibile a Director + Secretary, esposto ai partecipanti solo come `problem_restated`
- Output validation: rimuove `Qwen3  blocks`, tronca risposte troppo lunghe

## Testing

```bash
cd /tmp/tavolarotonda
python tests/test_smoke.py
# Output: ✅ Tutti i 14 test passati
```

## Limitazioni note & Roadmap

| # | Limitazione | Workaround |
|---|---|---|
| 1 | Claude API richiede SDK Anthropic (ora solo HTTP raw) | Sostituire `_claude` con SDK quando disponibile |
| 2 | Brave/SearXNG richiedono configurazione utente | Mock fallback automatico |
| 3 | OCR/screenshots non supportati (no Manus-style) | Roadmap v0.2 |
| 4 | No MCP server (vs quorum-cli) | Roadmap v0.2 |
| 5 | Voting scores sono mock in modalità `--mock` | Reali con LLM attivo |

## Bug risolti dal codice originale Manus

| # | Bug originale Manus | Fix in tavolarotonda |
|---|---|---|
| 1 | Prompt injection via direttive utente | `sanitize_directive` rimuove/marca marker |
| 2 | Niente timeout esplicito per `_say` | Timeout 120s + retry 3x |
| 3 | `_injections` in-memory non persistente | Memory Palace JSON persistente |
| 4 | Privacy leak a Groq/Cerebras | PII redaction + tier esplicito |
| 5 | Niente rate limit per round | `MAX_ROUNDS` env-config + early-stop su converged |
| 6 | Niente retry/backoff remoti | 3 tentativi con backoff esponenziale |
| 7 | `_project_tree` con `os.walk` depth 2 | Sostituibile con `git ls-files` o simile (TODO) |
| 8 | `_extract_json_obj` depth naive | Regex migliorata + try/except ovunque |
| 9 | `MAX_ROUNDS = 20` hardcoded | Env var + configurabile |
| 10 | Temperature 0.85 hardcoded | Per-agent configurabile |

## Licenza

MIT (vedi LICENSE).
