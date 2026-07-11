# Project Global TOD — tavolarotonda-due

**Main HEAD**: 2adbdde · **Branch**: main · **Updated**: 2026-07-11 21:15

## ✅ Done (evidence-gated)

- [x] **TR-001** — mv repo da `/mnt/backup/PROGETTI/tavolarotonda/` → `Obsidian/Memoria/progetti/tavolarotonda-due/` · git HEAD `da1f90b` preservato (2026-07-02)
- [x] **TR-002** — Integrato `ornith-35b:latest` in `gui/app.py` (MODELS + routing triade/alternating) · test e2e OK latency 0.86s (2026-07-02)
- [x] **TR-003** — Fix `_strip_think` in `providers.py` per pattern `<think>...</think>` (Ornith usa XML, non Qwen3 unicode) (2026-07-02)
- [x] **TR-004** — Creata pagina vault canonica `tavolarotonda-due.md` + redirect vecchia pagina (2026-07-02)
- [x] **TR-041** — config.yaml centralizzato: models/presets/colors in tavolarotonda/config.yaml + config.py, gui/app.py li carica · commit `2adbdde` (2026-07-11)
- [x] **TR-040** — Roadmap AQ: 20 risposte → ROADMAP.md sprint plan, AQ top5, out-of-scope · `2adbdde` (2026-07-11)
- [x] **TR-000** — Bootstrap progetto: 9 moduli Python, GUI Flask :8912, 18 agenti, wiring `/usr/local/bin/war-room-tavolarotonda` (2026-06-21)
- [x] **TR-046** — Unificato LLMProvider + AnthropicCompatProvider (deprecated → thin wrapper) · commit `49e5619` (2026-07-11)
- [x] **TR-042** — aq_score in api_models + top_5_by_aq ranking · commit `49e5619` (2026-07-11)
- [x] **TR-047** — Streaming SSE con agent_key + agent_color · commit `49e5619` (2026-07-11)
- [x] **TR-044** — GitHub Actions CI: test (pytest 3.11/3.12 + coverage) + lint (ruff) + type-check (mypy) · commit `fa2db97` (2026-07-11)
      Note: mypy 8 errors tracked separately (providers/phases/__main__ type annotations)

## 🔄 In Progress

nessuna

## ⬜ Backlog (in ordine di priorità)

- [ ] **TR-045** — Integrazione Obsidian (topic da vault, risultati in vault)
      Comando: `cd /mnt/backup/Dropbox/1\ Programmazione/Progetti/tavolarotonda-due && python -m tavolarotonda serve`
      Done when: endpoint `/api/obsidian-topic` risponde, output markdown salvato in vault

- [ ] **TR-020** — Implementare MCP server (tavolarotonda serve --mcp)
      Comando: `cd /mnt/backup/Dropbox/1\ Programmazione/Progetti/tavolarotonda-due && python -m tavolarotonda serve --mcp`
      Done when: client test OK, risposta HTTP 200 da MCP handshake

- [ ] **TR-021** — Wiring con `opus-m3-confer` per routing decisioni complesse
      Riferimento: `[[tavolarotonda-due]]` sezione Prossimi passi

- [ ] **TR-014** — Ornith-35b nella triade: valutare se sostituire anche in routing CLI default
      Nota: ora CLI usa `local_only` → primo Ollama disponibile; ornith-35b è il primo → OK di default


## 🚫 Deferred / Blocked

- [~] **TR-030** — Claude API SDK (ora solo HTTP raw) — roadmap v0.2
- [~] **TR-031** — SearXNG/Brave search — Mock fallback OK per ora
- [~] **TR-032** — Pubblicazione repo pubblico GitHub — decisione utente

## Cross-ref

- Vault entry: `[[tavolarotonda-due]]`
- Sessioni: `sessioni/`
- Decisioni: `decisioni/`
