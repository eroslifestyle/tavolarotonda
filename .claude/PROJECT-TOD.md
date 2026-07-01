# Project Global TOD — tavolarotonda-due

**Main HEAD**: da1f90b · **Branch**: main · **Updated**: 2026-07-02 00:00

## ✅ Done (evidence-gated)

- [x] **TR-001** — mv repo da `/mnt/backup/PROGETTI/tavolarotonda/` → `Obsidian/Memoria/progetti/tavolarotonda-due/` · git HEAD `da1f90b` preservato (2026-07-02)
- [x] **TR-002** — Integrato `ornith-35b:latest` in `gui/app.py` (MODELS + routing triade/alternating) · test e2e OK latency 0.86s (2026-07-02)
- [x] **TR-003** — Fix `_strip_think` in `providers.py` per pattern `<think>...</think>` (Ornith usa XML, non Qwen3 unicode) (2026-07-02)
- [x] **TR-004** — Creata pagina vault canonica `tavolarotonda-due.md` + redirect vecchia pagina (2026-07-02)
- [x] **TR-000** — Bootstrap progetto: 9 moduli Python, GUI Flask :8912, 18 agenti, wiring `/usr/local/bin/war-room-tavolarotonda` (2026-06-21)

## 🔄 In Progress

(nessuno)

## ⬜ Backlog (in ordine di priorità)

- [ ] **TR-010** — `git commit + push` modifiche sessione 2026-07-02 (gui/app.py + providers.py)
      Comando: `cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due && git add gui/app.py tavolarotonda/providers.py && git commit -m "feat: integrate ornith-35b as llm provider + fix think-strip" && git push`
      Done when: `git push` exit 0, `git status` → "up to date"

- [ ] **TR-011** — Test sessione reale Ornith (3 round, mode topic, council monolitico)
      Comando: avvia GUI `python gui/app.py` → POST `/api/run` con `model=ornith-35b, rounds=3`
      Done when: `/api/report/<sid>` HTML generato, nessun errore nel log

- [ ] **TR-012** — Aggiunta `ornith-9b` (5.6 GB, 0.86s) come provider "veloce" opzionale
      Comando: edit `gui/app.py` MODELS + `_MODEL_FOR_PROVIDER`, test smoke analogos TR-002
      Done when: `/api/models` mostra `ornith-9b` state=ok

- [ ] **TR-013** — Aggiornare `bin/war-room-tavolarotonda` con nuovo path dopo mv
      Comando: `cat /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due/bin/war-room-tavolarotonda` e verifica path; aggiorna symlink `/usr/local/bin/` se rotto
      Done when: `war-room-tavolarotonda --mock --rounds 1 "test"` exit 0

- [ ] **TR-014** — Ornith-35b nella triade: valutare se sostituire anche in routing CLI default
      Nota: ora CLI usa `local_only` → primo Ollama disponibile; ornith-35b è il primo → OK di default

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
