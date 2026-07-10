# Graph Report - tavolarotonda-due  (2026-07-02)

## Corpus Check
- 28 files · ~36,298 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 318 nodes · 799 edges · 11 communities
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 82 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `785beb3d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11

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
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → /mnt/backup/PROGETTI/tavolarotonda/tavolarotonda/memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → /mnt/backup/PROGETTI/tavolarotonda/tavolarotonda/memory_palace.py
- `MultiProvider` --uses--> `CircuitBreaker`  [INFERRED]
  gui/app.py → tavolarotonda/providers.py
- `MultiProvider` --uses--> `ProviderResult`  [INFERRED]
  gui/app.py → tavolarotonda/providers.py
- `_build_provider()` --calls--> `MockProvider`  [INFERRED]
  gui/app.py → tavolarotonda/providers.py

## Communities (11 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (61): Agent, Director, int, LLMProvider, str, int, LLMProvider, str (+53 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (30): float, ProviderKind, ProviderResult, bool, float, int, str, CircuitBreaker (+22 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (39): int, LLMProvider, MemoryPalace, str, float, int, str, int (+31 more)

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (14): int, MemoryPalace, str, int, MemoryPalace, str, tavolarotonda — Council multi-agente per decisioni reali e concrete.  Package: 9, audit_report_from_palace() (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (20): int, str, int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search() (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (9): str, str, agent_by_name(), default_council(), polarities_for(), 18 personas fisse con polarity pairs (Council of High Intelligence pattern).  Og, Cerca un agente per key (case-insensitive). Ritorna None se non trovato., Ritorna il set di agenti di default (12, bilanciati per dominio). (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (8): LLMProvider, MemoryPalace, str, LLMProvider, MemoryPalace, str, Aggiorna palace.strategy_summary in place., Genera un summary testuale della strategia per i prompt successivi.

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
Cohesion: 0.40
Nodes (4): Altri file root, .Claude (`.claude/`), tavolarotonda-due — Indice Progetto, Tavolarotonda (`tavolarotonda/`)

## Knowledge Gaps
- **41 isolated node(s):** `Altri file root`, `.Claude (`.claude/`)`, `Tavolarotonda (`tavolarotonda/`)`, `1. Rename + spostamento progetto`, `2. Integrazione Ornith-35B (Qwen3.6 MoE, ctx 256K, Q4_K_M)` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 0` to `Community 8`, `Community 1`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.322) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 2` to `Community 0`, `Community 4`, `Community 7`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `_build_provider()` connect `Community 8` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `LLMProvider` (e.g. with `Director` and `PhaseEvent`) actually correct?**
  _`LLMProvider` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `MemoryPalace` (e.g. with `str` and `int`) actually correct?**
  _`MemoryPalace` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Secretary` (e.g. with `LLMProvider` and `MemoryPalace`) actually correct?**
  _`Secretary` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Director` (e.g. with `LLMProvider` and `PhaseEvent`) actually correct?**
  _`Director` has 10 INFERRED edges - model-reasoned connections that need verification._