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
- [x] **TR-045** — Integrazione Obsidian: obsidian_vault.py (read_topic/save_session) + serve.py HTTP API (/api/obsidian/topic, /api/obsidian/save, /health) · commit `db5b90c` (2026-07-11)
- [x] **TR-020** — MCP server: mcp_server.py (discuss/status/history tools) + POST /mcp JSON-RPC + MCP handshake OK · commit `db5b90c` (2026-07-11)
- [x] **TR-021** — opus-m3-confer wiring: MODEL_TIER_MAP + confer_phase() + --intensity CLI flag (fast|standard|reasoning|critical) · commit `db5b90c` (2026-07-11)
- [x] **mypy fix** — 12 type errors fixed (providers.py, evidence.py, phases.py, __main__.py) → mypy 0 issues · commit `db5b90c` (2026-07-11)

## 🔄 In Progress

nessuna

## ⬜ Backlog (in ordine di priorità)


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
