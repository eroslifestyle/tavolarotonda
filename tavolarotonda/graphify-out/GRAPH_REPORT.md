# Graph Report - tavolarotonda-due  (2026-07-11)

## Corpus Check
- 43 files · ~47,920 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 874 nodes · 1778 edges · 32 communities (30 shown, 2 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 174 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db5b90cc`
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
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]

## God Nodes (most connected - your core abstractions)
1. `MemoryPalace` - 79 edges
2. `LLMProvider` - 71 edges
3. `run_full_council()` - 46 edges
4. `AnthropicCompatProvider` - 35 edges
5. `MockProvider` - 27 edges
6. `Secretary` - 27 edges
7. `Director` - 25 edges
8. `Agent` - 24 edges
9. `PhaseEvent` - 23 edges
10. `phase_brainstorm()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → tavolarotonda/memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → tavolarotonda/memory_palace.py
- `LLMProvider` --uses--> `LLMProvider`  [INFERRED]
  director.py → tavolarotonda/providers.py
- `int` --uses--> `LLMProvider`  [INFERRED]
  director.py → tavolarotonda/providers.py
- `run_audit()` --calls--> `Path`  [INFERRED]
  tavolarotonda/__main__.py → gui/app.py

## Communities (32 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (78): Agent, Director, bool, int, LLMProvider, MemoryPalace, str, int (+70 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (34): ProviderKind, bool, float, int, str, bool, float, int (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (48): Any, float, int, str, float, int, str, _cleanup_loop() (+40 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (28): Starlette, Path, str, Integrazione Obsidian vault — lettura topic e salvataggio sessioni., Legge un file .md dal vault Obsidian per nome topic.      Cerca in vault/istanze, Salva il transcript di una sessione nel vault Obsidian.      Crea la cartella se, read_topic(), save_session() (+20 more)

### Community 4 - "Community 4"
Cohesion: 0.20
Nodes (19): float, str, get_agent_color(), get_aq_score(), get_model(), get_preset(), get_timeout(), load() (+11 more)

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
Nodes (78): api_agents(), api_council_presets(), api_models(), api_palace(), api_report(), api_run(), api_sessions(), api_stream() (+70 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (18): Architettura / componenti, code:bash (# Demo no-LLM), code:bash (cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due), code:bash (cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due), Collegamenti, Come avviare la GUI (2026-07-01), Decisioni chiave, Discussion di esempio (output HTML) (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (9): 1. Rename + spostamento progetto, 2. Integrazione Ornith-35B (Qwen3.6 MoE, ctx 256K, Q4_K_M), 3. Test end-to-end verificati, Cosa è stato fatto, File modificati, Prossimi passi, Sessione 2026-07-02 — Rename + Integrazione Ornith-35B, Stato post-sessione (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (6): Altri file root, .Claude (`.claude/`), Decisioni (`decisioni/`), Sessioni (`sessioni/`), tavolarotonda-due — Indice Progetto, Tavolarotonda (`tavolarotonda/`)

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
Cohesion: 0.06
Nodes (65): str, MemoryPalace, str, str, int, LLMProvider, MemoryPalace, str (+57 more)

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
Cohesion: 0.10
Nodes (23): int, LLMProvider, str, int, LLMProvider, str, LLMProvider, MemoryPalace (+15 more)

## Knowledge Gaps
- **281 isolated node(s):** `float`, `bool`, `int`, `str`, `int` (+276 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 8` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 32`, `Community 24`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 2` to `Community 0`, `Community 32`, `Community 3`, `Community 8`, `Community 24`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `run_full_council()` connect `Community 0` to `Community 24`, `Community 8`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 41 inferred relationships involving `MemoryPalace` (e.g. with `str` and `Namespace`) actually correct?**
  _`MemoryPalace` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `LLMProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`LLMProvider` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `AnthropicCompatProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`AnthropicCompatProvider` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MockProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`MockProvider` has 11 INFERRED edges - model-reasoned connections that need verification._