# Graph Report - tavolarotonda-due  (2026-07-10)

## Corpus Check
- 29 files · ~36,459 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 325 nodes · 805 edges · 12 communities
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 82 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `699e831b`
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

## God Nodes (most connected - your core abstractions)
1. `LLMProvider` - 43 edges
2. `MemoryPalace` - 41 edges
3. `run_full_council()` - 30 edges
4. `Secretary` - 19 edges
5. `Director` - 17 edges
6. `MockProvider` - 16 edges
7. `phase_brainstorm()` - 16 edges
8. `str` - 15 edges
9. `tavolarotonda-due 🥽` - 15 edges
10. `PhaseEvent` - 15 edges

## Surprising Connections (you probably didn't know these)
- `LLMProvider` --uses--> `LLMProvider`  [INFERRED]
  director.py → tavolarotonda/providers.py
- `int` --uses--> `LLMProvider`  [INFERRED]
  director.py → tavolarotonda/providers.py
- `MultiProvider` --uses--> `CircuitBreaker`  [INFERRED]
  gui/app.py → tavolarotonda/providers.py
- `MultiProvider` --uses--> `ProviderResult`  [INFERRED]
  gui/app.py → tavolarotonda/providers.py
- `_build_provider()` --calls--> `MockProvider`  [INFERRED]
  gui/app.py → tavolarotonda/providers.py

## Communities (12 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (52): Agent, str, Director, str, bool, int, LLMProvider, MemoryPalace (+44 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (30): float, ProviderKind, ProviderResult, bool, float, int, str, CircuitBreaker (+22 more)

### Community 2 - "Community 2"
Cohesion: 0.20
Nodes (25): int, LLMProvider, MemoryPalace, str, int, LLMProvider, MemoryPalace, str (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (9): int, str, int, str, Director / Regista — per ogni round fissa il focus e assegna chi confuta chi.  P, Template di prompt centralizzati — anti-duplicazione (regola modularità KING)., Rimuove marker di prompt injection, tronca a max_length.      NON è una garanzia, sanitize_directive() (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (28): float, int, str, float, int, str, int, MemoryPalace (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (20): int, str, int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search() (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (5): Commit, Sessione 2026-07-02 — TR-011/012/013, TR-011 ✅ — Test sessione reale Ornith, TR-012 ✅ — ornith-9b come provider veloce, TR-013 ✅ — war-room path dopo mv

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (17): int, LLMProvider, str, int, LLMProvider, str, LLMProvider, MemoryPalace (+9 more)

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (53): bool, api_agents(), api_council_presets(), api_models(), api_palace(), api_report(), api_run(), api_sessions() (+45 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (18): Architettura / componenti, code:bash (# Demo no-LLM), code:bash (cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due), code:bash (cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due), Collegamenti, Come avviare la GUI (2026-07-01), Decisioni chiave, Discussion di esempio (output HTML) (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.20
Nodes (9): 1. Rename + spostamento progetto, 2. Integrazione Ornith-35B (Qwen3.6 MoE, ctx 256K, Q4_K_M), 3. Test end-to-end verificati, Cosa è stato fatto, File modificati, Prossimi passi, Sessione 2026-07-02 — Rename + Integrazione Ornith-35B, Stato post-sessione (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.33
Nodes (5): Altri file root, .Claude (`.claude/`), Sessioni (`sessioni/`), tavolarotonda-due — Indice Progetto, Tavolarotonda (`tavolarotonda/`)

## Knowledge Gaps
- **46 isolated node(s):** `Sessioni (`sessioni/`)`, `Altri file root`, `.Claude (`.claude/`)`, `Tavolarotonda (`tavolarotonda/`)`, `TR-011 ✅ — Test sessione reale Ornith` (+41 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 0` to `Community 8`, `Community 1`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.308) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 4` to `Community 0`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `_build_provider()` connect `Community 8` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `LLMProvider` (e.g. with `Director` and `PhaseEvent`) actually correct?**
  _`LLMProvider` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `MemoryPalace` (e.g. with `str` and `int`) actually correct?**
  _`MemoryPalace` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Secretary` (e.g. with `LLMProvider` and `MemoryPalace`) actually correct?**
  _`Secretary` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Director` (e.g. with `LLMProvider` and `PhaseEvent`) actually correct?**
  _`Director` has 10 INFERRED edges - model-reasoned connections that need verification._