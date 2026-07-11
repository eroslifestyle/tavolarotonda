# Project Global TOD — tavolarotonda-due

**Main HEAD**: da1f90b · **Branch**: main · **Updated**: 2026-07-02 00:00

## ✅ Done (evidence-gated)

- [x] **TR-001** — mv repo da `/mnt/backup/PROGETTI/tavolarotonda/` → `Obsidian/Memoria/progetti/tavolarotonda-due/` · git HEAD `da1f90b` preservato (2026-07-02)
- [x] **TR-002** — Integrato `ornith-35b:latest` in `gui/app.py` (MODELS + routing triade/alternating) · test e2e OK latency 0.86s (2026-07-02)
- [x] **TR-003** — Fix `_strip_think` in `providers.py` per pattern `<think>...</think>` (Ornith usa XML, non Qwen3 unicode) (2026-07-02)
- [x] **TR-004** — Creata pagina vault canonica `tavolarotonda-due.md` + redirect vecchia pagina (2026-07-02)
- [x] **TR-000** — Bootstrap progetto: 9 moduli Python, GUI Flask :8912, 18 agenti, wiring `/usr/local/bin/war-room-tavolarotonda` (2026-06-21)

## 🔄 In Progress

- [ ] **TR-040** — Roadmap AQ TavolaRotonda 2.0 (20 domande → piano sviluppo)
      Owner: sessione 2026-07-11
      Done when: piano approvato, implementazione iniziata

## ⬜ Backlog (in ordine di priorità)

- [x] **TR-010** — `git commit + push` modifiche sessione 2026-07-02 (gui/app.py + providers.py) · commit `785beb3` (2026-07-02)
- [x] **TR-011** — Test sessione reale Ornith (3 round, mode topic, council monolitico) · session `625965bc086d`, HTML 6051B (2026-07-02)
- [x] **TR-012** — Aggiunta `ornith-9b` (5.6 GB, 0.86s) come provider "veloce" opzionale · `ornith-9b:latest` state=ok (2026-07-02)
- [x] **TR-013** — Verifica `bin/war-room-tavolarotonda` dopo mv del repo · exit 0 (2026-07-02)

- [ ] **TR-014** — Ornith-35b nella triade: valutare se sostituire anche in routing CLI default
      Nota: ora CLI usa `local_only` → primo Ollama disponibile; ornith-35b è il primo → OK di default

- [ ] **TR-041** — Implementare config.yaml centralizzato (modelli, agenti, preset, prompt)
      Comando: creare `tavolarotonda/config.yaml` + refactoring `gui/app.py`
      Done when: config.yaml funziona, tutti i modelli presenti

- [ ] **TR-042** — Aggiungere Top 5 modelli AQ alla GUI (qwen3.6-opus, coder-32b, gemma-4, qwen2.5:14b, qwen2.5:7b)
      Done when: model-select mostra 5 modelli benchmarkati

- [ ] **TR-043** — Unificare LLMProvider + AnthropicCompatProvider
      Done when: una sola classe provider gestisce tutti gli endpoint

- [ ] **TR-044** — GitHub Actions CI (test + lint + type-check)
      Done when: workflow attivo su push/PR

- [ ] **TR-045** — Integrazione Obsidian (topic da vault, risultati in vault)
      Done when: `/api/obsidian-topic` funziona, output markdown salvato in vault

- [ ] **TR-020** — Implementare MCP server (vs quorum-cli)
      Done when: `tavolarotonda serve --mcp` + client test

- [ ] **TR-021** — Wiring con `opus-m3-confer` per routing decisioni complesse
      Riferimento: `[[tavolarotonda-due]]` sezione Prossimi passi

## 🚫 Deferred / Blocked

- [~] **TR-030** — Claude API SDK (ora solo HTTP raw) — roadmap v0.2
- [~] **TR-031** — SearXNG/Brave search — Mock fallback OK per ora
- [~] **TR-032** — Pubblicazione repo pubblico GitHub — decisione utente

## Cross-ref

- Vault entry: `[[tavolarotonda-due]]`
- Sessioni: `sessioni/`
- Decisioni: `decisioni/`
