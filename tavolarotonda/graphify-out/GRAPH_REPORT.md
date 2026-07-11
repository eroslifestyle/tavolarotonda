# Graph Report - tavolarotonda  (2026-07-11)

## Corpus Check
- 15 files · ~11,135 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 913 nodes · 1883 edges · 42 communities (39 shown, 3 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 184 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b3f7c23`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]

## God Nodes (most connected - your core abstractions)
1. `MemoryPalace` - 81 edges
2. `LLMProvider` - 72 edges
3. `run_full_council()` - 48 edges
4. `AnthropicCompatProvider` - 38 edges
5. `MockProvider` - 28 edges
6. `Secretary` - 28 edges
7. `PhaseEvent` - 28 edges
8. `Director` - 26 edges
9. `phase_brainstorm()` - 25 edges
10. `Agent` - 25 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `audit_report_from_palace()` --calls--> `Any`  [INFERRED]
  reports.py → phases.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `str` --uses--> `ProviderResult`  [INFERRED]
  gui/app.py → providers.py
- `bool` --uses--> `ProviderResult`  [INFERRED]
  gui/app.py → providers.py

## Communities (42 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (35): Agent, Any, Director, bool, int, bool, int, LLMProvider (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (47): float, ProviderKind, ProviderResult, bool, float, int, str, CircuitBreaker (+39 more)

### Community 2 - "Community 2"
Cohesion: 0.21
Nodes (11): float, int, str, float, int, str, float, int (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (44): str, int, str, Starlette, handle_mcp_request(), Processa una richiesta MCP JSON-RPC 2.0., Path, str (+36 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (43): int, LLMProvider, MemoryPalace, str, int, LLMProvider, MemoryPalace, str (+35 more)

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (31): int, str, int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search() (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (5): Commit, Sessione 2026-07-02 — TR-011/012/013, TR-011 ✅ — Test sessione reale Ornith, TR-012 ✅ — ornith-9b come provider veloce, TR-013 ✅ — war-room path dopo mv

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (20): appendEvent(), clearStream(), connectStream(), escapeHtml(), formatResearch(), formatText(), handleEvent(), loadCouncilPresets() (+12 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (72): float, str, api_agents(), api_council_presets(), api_models(), api_palace(), api_report(), api_run() (+64 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (18): Architettura / componenti, code:bash (# Demo no-LLM), code:bash (cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due), code:bash (cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due), Collegamenti, Come avviare la GUI (2026-07-01), Decisioni chiave, Discussion di esempio (output HTML) (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (9): 1. Rename + spostamento progetto, 2. Integrazione Ornith-35B (Qwen3.6 MoE, ctx 256K, Q4_K_M), 3. Test end-to-end verificati, Cosa è stato fatto, File modificati, Prossimi passi, Sessione 2026-07-02 — Rename + Integrazione Ornith-35B, Stato post-sessione (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (6): Altri file root, .Claude (`.claude/`), .Pytest_Cache (`.pytest_cache/`), Sessioni (`sessioni/`), tavolarotonda-due — Indice Progetto, Tavolarotonda (`tavolarotonda/`)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (13): 🏆 AQ Top 5 modelli (da benchmark 2026-07-11), code:block1 (tavolarotonda-due/), Commit base: da59563, 📁 File struttura finale, 🚫 Out of scope (risposte AQ), 📊 Risposte AQ sintetizzate, ROADMAP — TavolaRotonda 2.0, Sprint 1 — Foundation (1-2 settimane) (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 14 - "Community 14"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 19 - "Community 19"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 20 - "Community 20"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 21 - "Community 21"
Cohesion: 0.08
Nodes (24): brainstorm, convergence_score, created_at, critique, decision, metrics, models_used, tokens_in (+16 more)

### Community 22 - "Community 22"
Cohesion: 0.08
Nodes (24): Architettura, Audit di un file di codice, Bug risolti dal codice originale Manus, Caratteristiche, code:bash (git clone <repo> tavolarotonda), code:bash (python -m tavolarotonda --mock "Dovrei aprire-sorgere il mio), code:bash (# 1. Avvia Ollama), code:bash (python -m tavolarotonda --audit examples/audit_target.py --m) (+16 more)

### Community 23 - "Community 23"
Cohesion: 0.11
Nodes (13): calculate_discount(), get_db_connection(), get_user(), parse_config(), float, str, Esempio di codice da audire — contiene pattern realistici con criticità intenzio, Get user by username — INSECURE! (+5 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (29): int, MemoryPalace, str, int, MemoryPalace, str, tavolarotonda — Council multi-agente per decisioni reali e concrete.  Package: 1, from_dict() (+21 more)

### Community 26 - "Community 26"
Cohesion: 0.15
Nodes (18): int, LLMProvider, str, int, LLMProvider, str, _extract_json(), int (+10 more)

### Community 27 - "Community 27"
Cohesion: 0.09
Nodes (24): int, str, int, str, int, str, Rimuove marker di prompt injection, tronca a max_length.      NON è una garanzia, sanitize_directive() (+16 more)

### Community 28 - "Community 28"
Cohesion: 0.18
Nodes (10): AQ Top 5 modelli, Commit, Contesto, Deliverables, Link, Prossimi passi, Risposte AQ chiave, ROADMAP.md (+2 more)

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (7): code:python (# ancora funziona (deprecato):), Decisione, Nuovo uso preferito, Problema, Provider Unification (TR-046), Retrocompatibilità, Riferimenti

### Community 30 - "Community 30"
Cohesion: 0.22
Nodes (8): Contesto, Fix applicate in sessione, Inventario Ollama (29 modelli), Link, Modelli testati, Risultati AQ Benchmark (40 risposte/modello, 2 sessioni), Roadmap proposta (consigli basati su AQ), Sessione 2026-07-11 — AQ Benchmark 20 Domande TavolaRotonda 2.0

### Community 31 - "Community 31"
Cohesion: 0.29
Nodes (6): Chiusure, Commit, TR-042 — Top 5 modelli AQ in GUI, TR-046/042/047 — Provider unificato + AQ scores + Color stream, TR-046 — Unificazione LLMProvider + AnthropicCompatProvider, TR-047 — Streaming UX a colori

### Community 32 - "Community 32"
Cohesion: 0.19
Nodes (11): LLMProvider, MemoryPalace, str, LLMProvider, MemoryPalace, str, LLMProvider, MemoryPalace (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.20
Nodes (12): LLMProvider, MemoryPalace, phase_restate(), phase_verdict(), PhaseEvent, Ogni agente vota 0-10 sulla proposta finale (feasibility, impact, risk_safety)., Ogni agente vota 0-10 sulla proposta finale (feasibility, impact, risk_safety)., Ogni agente vota 0-10 sulla proposta finale (feasibility, impact, risk_safety). (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.30
Nodes (4): Director / Regista — per ogni round fissa il focus e assegna chi confuta chi.  P, Pipeline principale del council: Research → Restate → Brainstorm → Critique → Sy, Template di prompt centralizzati — anti-duplicazione (regola modularità KING)., Secretary / Segretario — consolida la strategia live dopo ogni turn.  Output JSO

### Community 36 - "Community 36"
Cohesion: 0.23
Nodes (17): str, _cleanup_loop(), _get_or_create_session(), handle_initialize(), handle_tools_call(), handle_tools_list(), MCPRequest, MCPResponse (+9 more)

### Community 37 - "Community 37"
Cohesion: 0.20
Nodes (9): Commit, Config progetto (`pyproject.toml`), Cosa fatto, GitHub Actions CI (`.github/workflows/ci.yml`), Goal, Next, Ruff auto-fix (14 file), Test result (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.25
Nodes (12): str, str, agent_by_name(), default_council(), polarities_for(), str, 18 personas fisse con polarity pairs (Council of High Intelligence pattern).  Og, Cerca un agente per key (case-insensitive). Ritorna None se non trovato. (+4 more)

### Community 39 - "Community 39"
Cohesion: 0.33
Nodes (7): phase_critique(), str, Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Resolve model + optional tier for an agent.      When agent.default_model == "au, _resolve_agent_model()

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (13): str, _extract_list_section(), _extract_section(), phase_synthesis(), Sintetizzatore finale: decisione + minority report + open questions + next steps, Sintetizzatore finale: decisione + minority report + open questions + next steps, Sintetizzatore finale: decisione + minority report + open questions + next steps, Estrae una sezione markdown fino al prossimo header ## o fine testo. (+5 more)

## Knowledge Gaps
- **289 isolated node(s):** `str`, `int`, `bool`, `int`, `float` (+284 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 26` to `Community 0`, `Community 1`, `Community 32`, `Community 35`, `Community 4`, `Community 36`, `Community 34`, `Community 39`, `Community 8`, `Community 24`, `Community 27`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 24` to `Community 0`, `Community 32`, `Community 2`, `Community 35`, `Community 4`, `Community 36`, `Community 34`, `Community 39`, `Community 8`, `Community 26`, `Community 27`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `run_full_council()` connect `Community 0` to `Community 34`, `Community 35`, `Community 4`, `Community 36`, `Community 39`, `Community 40`, `Community 8`, `Community 24`, `Community 26`, `Community 27`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `MemoryPalace` (e.g. with `str` and `int`) actually correct?**
  _`MemoryPalace` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `LLMProvider` (e.g. with `Secretary` and `LLMProvider`) actually correct?**
  _`LLMProvider` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `AnthropicCompatProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`AnthropicCompatProvider` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MockProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`MockProvider` has 11 INFERRED edges - model-reasoned connections that need verification._