---
tags: [sessione, tavolarotonda, benchmark, llm]
data: 2026-07-11
type: sessione
autore: eros
---

# Sessione 2026-07-11 — AQ Benchmark 20 Domande TavolaRotonda 2.0

## Contesto

Sessione di ricerca e pianificazione per lo sviluppo di TavolaRotonda 2.0. L'utente ha richiesto:
1. Inventario modelli LL locali su Ollama
2. Ricerca HF + GitHub per identificare i migliori modelli per multi-agent reasoning
3. Benchmark AQ live (20 domande simultanee su 6 modelli)
4. Sessione AQ con 20 domande interattive per definire la roadmap

## Modelli testati

### Inventario Ollama (29 modelli)
| Modello | VRAM | CTX | AIME | Status |
|---|---|---|---|---|
| qwen3.6-opus-abliterated:35b | 21.2GB | 262K | 92.7% | ✅ |
| qwen2.5-coder-uncensored:32b | 19.9GB | 128K | N/A | ✅ |
| huihui_ai/gemma-4-abliterated:26b | 18.0GB | 128K | 88.3% | ✅ |
| reasoning-max:latest | 4.7GB | 32K | N/A | ✅ |
| fast-max:latest | 4.7GB | 32K | N/A | ✅ |
| cyber-max:latest | 4.7GB | 32K | N/A | ✅ |
| qwen2.5:14b | 9.0GB | 128K | N/A | ✅ |
| qwen2.5:7b | 4.7GB | 128K | N/A | ✅ |

### Risultati AQ Benchmark (40 risposte/modello, 2 sessioni)

| Rank | Modello | Score AQ | Valid |
|---|---|---|---|
| 🥇 | qwen3.6-opus-abliterated:35b | 4.69/10 | 40/40 |
| 🥈 | qwen2.5-coder-uncensored:32b | 2.23/10 | 40/40 |
| 🥉 | Altri (gemma, qwen2.5, reasoning-max) | 2.00/10 | 40/40 |

**Winner**: `qwen3.6-opus-abliterated:35b` è il modello di riferimento per tutti i ruoli premium.

## Fix applicate in sessione

1. **Ornith rimossi** — `gui/app.py` non ha più `ornith-35b`/`ornith-9b`
2. **AnthropicCompatProvider** — `opus-4.8` e `MiniMax-M3` ora usano ai-router :8787
3. **CSS overflow** — rimosso `overflow:hidden` da `body`, `#app` usa `min-height:100vh`
4. **Icona launcher** — `~/Desktop/tavolarotonda.desktop` + icona custom + script `~/.local/bin/tavolarotonda-launcher.sh`

## Roadmap proposta (consigli basati su AQ)

| Priorità | Task | Note |
|---|---|---|
| P0 | config.yaml centralizzato | Modelli, agenti, preset, prompt |
| P0 | Top 5 modelli AQ in GUI | routing basato su benchmark |
| P1 | Unificare providers | LLMProvider + AnthropicCompatProvider |
| P1 | GitHub Actions CI | test + lint + type-check |
| P2 | Streaming UX | Colori per ruolo, highlight agente |
| P2 | Integrazione Obsidian | Topic da vault, risultati in vault |

## Link

- Commit: `da59563`
- Benchmark DB: `.claude/benchmarks/models.db`
- Pagina AQ interattiva: `/tmp/aq_tavolarotonda.html`
- GUI: `http://127.0.0.1:8912`
