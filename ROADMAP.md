# ROADMAP — TavolaRotonda 2.0
# Synthesized from: AQ sessione 2026-07-11 (20 domande, 20 risposte)
# Commit base: da59563

---

## 📊 Risposte AQ sintetizzate

| Q | Area | Risposta | Implicazione roadmap |
|---|---|---|---|
| Q1 | Priorità | E (tutti distribuito) | Sprint distribuiti, non un task alla volta |
| Q2 | Use case | E (tutti) | Council già generico — mantenere |
| Q3 | Utenti | A (solo io) | Zero auth, single-user, privacy-first |
| Q4 | Budget | B (2-4 sett) | Scope realistico per ogni sprint |
| Q5 | Provider | A (solo ai-router) | Endpoint unico :8787 — niente multi-provider diretto |
| Q6 | Modello routing | C (fisso benchmark) | qwen3.6-opus-abliterated:35b come riferimento |
| Q7 | Fallback | A (silent) | Fallback automatico se un modello è giù |
| Q8 | Routing modelli | B (top 5 AQ) | GUI mostra i 5 modelli migliori dal benchmark |
| Q9 | UX priority | A (responsive) | Mobile-friendly, non PWA completo |
| Q10 | UI arch | A (SPA attuale) | NON riscrivere GUI — solo estendere |
| Q11 | Output viz | C (streaming UX) | Colori per ruolo, highlight agente attivo |
| Q12 | Export | D (tutti+API) | HTML+JSON+PDF+Markdown+CSV+API |
| Q13 | Config | A (config.yaml) | File unico centralizzato e versionato |
| Q14 | Test | B (solo provider) | Test sugli adapter LLM, non coverage completo |
| Q15 | Storage | A (filesystem) | Reports in `output/`, sessioni in `sessioni/` |
| Q16 | Refactor | A (unifica providers) | Una classe LLMProvider, niente AnthropicCompatProvider separato |
| Q17 | Test strategy | C (benchmark AQ continuo) | Test = benchmark AQ periodico, non smoke/unit |
| Q18 | CI/CD | A (GH Actions) | Lint + type-check + benchmark AQ su push |
| Q19 | Auth | A (nessuna) | Nessun login, nessun RBAC |
| Q20 | Future | ABCD (tutti) | Multi-turn, voice, memory palace export, plugin system |

---

## 🎯 Sprint plan

### Sprint 1 — Foundation (1-2 settimane)
**TR-041** · config.yaml centralizzato *(Q13=A)*
- `tavolarotonda/config.yaml`: modelli, provider, preset routing, agent mapping, timeout, retry
- `tavolarotonda/config.py`: loader che valida lo schema e ritorna config dict
- GUI carica da `config.yaml` (non più valori hardcoded in `app.py`)
- Benchmark AQ scores dentro config.yaml
- Schema JSON Schema incluso per validazione

**TR-046** · Unificare LLMProvider + AnthropicCompatProvider *(Q16=A)*
- Merge `AnthropicCompatProvider` in `LLMProvider`
- Unico costruttore con `provider_kind: ollama | openai_compat | anthropic_compat | mock`
- Retrocompatibilità con ai-router :8787

**TR-042** · Top 5 modelli AQ in GUI *(Q8=B, Q6=C)*
- Legge scores da `config.yaml`
- Model selector mostra 5 modelli con rank AQ
- Routing basato su benchmark score, non fixed

### Sprint 2 — UX & Streaming (2-3 settimane)
**TR-047** · Streaming UX a colori *(Q11=C, Q9=A)*
- SSE stream con metadata ruolo (agent name, phase, polarity)
- CSS per-agent con colori da `config.yaml`
- Highlight agente attivo nel flusso
- Responsive mobile-friendly

**TR-048** · Export completo + API *(Q12=D)*
- Export HTML + JSON + PDF + Markdown + CSV
- API REST endpoint per scaricare report
- `/api/report/<id>` → ritorna formati multipli via `?format=`

**TR-049** · Silent fallback *(Q7=A)*
- Se un modello/provider fallisce → silent retry sul prossimo
- Log dettagliato ma UI pulita
- Circuit breaker configurabile da `config.yaml`

### Sprint 3 — CI/CD & Polish (1-2 settimane)
**TR-044** · GitHub Actions CI *(Q18=A, Q17=C)*
- `.github/workflows/ci.yml`: lint + type-check + benchmark AQ
- Benchmark AQ runna su ogni push (10 domande veloci, non tutte e 20)
- Badge AQ score nel README

**TR-050** · Obsidian integration *(Q15=A)*
- `/api/obsidian-topic` → cerca nel vault
- Salva risultati council nel vault come nota

**TR-051** · Preset marketplace (import/export) *(Q20=C)*
- Export preset council come YAML
- Import preset da file
- `~/.config/tavolarotonda/presets/`

### Sprint 4 — Future (opzionale)
**TR-052** · Multi-turn debate *(Q20=A)*
- Stato conversazionale tra round
- Agent ricorda argomenti precedenti

**TR-053** · Voice input/output *(Q20=B)*
- STT per domanda iniziale
- TTS per streaming risposte

**TR-054** · Plugin system *(Q20=D)*
- Plugin discovery in `plugins/`
- Hook pre/post round
- API pubblica per estendere fasi

---

## 📁 File struttura finale

```
tavolarotonda-due/
├── tavolarotonda/
│   ├── config.yaml          ← NUOVO: config centralizzato
│   ├── config.py             ← NUOVO: loader + validatore
│   ├── agents.py
│   ├── providers.py
│   ├── phases.py
│   └── ...
├── gui/
│   ├── app.py               ← usa config.yaml (non più hardcoded)
│   └── ...
├── output/                   ← export reports (esistente)
├── sessioni/                 ← sessioni (esistente)
└── .claude/
    └── benchmarks/
        └── models.db        ← AQ scores (esistente)
```

---

## 🚫 Out of scope (risposte AQ)

- Multi-user / auth / RBAC (Q3=A, Q19=A)
- Multi-page app / riscrittura GUI (Q10=A)
- Test E2E / property-based (Q14=B, Q17=C≠B)
- PostgreSQL / S3 storage (Q15=A)
- PWA completo (Q9=A≠D)
- Marketplace online (Q14=B≠D)

---

## 🏆 AQ Top 5 modelli (da benchmark 2026-07-11)

| Rank | Modello | Score | Provider |
|---|---|---|---|
| 1 | qwen3.6-opus-abliterated:35b | 4.69 | Ollama locale |
| 2 | qwen2.5-coder-uncensored:32b | 2.23 | Ollama locale |
| 3 | huihui_ai/gemma-4-abliterated:26b | 2.00 | Ollama locale |
| 4 | qwen2.5:14b | 2.00 | Ollama locale |
| 5 | qwen2.5:7b | 2.00 | Ollama locale |

*Benchmark: 40 risposte/modello · qwen3.6-opus-abliterated:35b è il riferimento di default.*
