# Graph Report - tavolarotonda  (2026-07-02)

## Corpus Check
- 11 files · ~8,434 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 222 nodes · 619 edges · 9 communities
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `da1f90b2`
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

## God Nodes (most connected - your core abstractions)
1. `MemoryPalace` - 41 edges
2. `LLMProvider` - 39 edges
3. `run_full_council()` - 30 edges
4. `Secretary` - 19 edges
5. `Director` - 17 edges
6. `phase_brainstorm()` - 16 edges
7. `PhaseEvent` - 15 edges
8. `Agent` - 15 edges
9. `run_audit()` - 15 edges
10. `run_qa()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → /mnt/backup/PROGETTI/tavolarotonda/tavolarotonda/memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → /mnt/backup/PROGETTI/tavolarotonda/tavolarotonda/memory_palace.py
- `LLMProvider` --uses--> `LLMProvider`  [INFERRED]
  director.py → providers.py
- `int` --uses--> `LLMProvider`  [INFERRED]
  director.py → providers.py
- `str` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → /mnt/backup/PROGETTI/tavolarotonda/tavolarotonda/memory_palace.py

## Communities (9 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (42): Agent, Director, bool, int, LLMProvider, MemoryPalace, str, bool (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (25): ProviderKind, bool, float, int, str, CircuitBreaker, ProviderResult, Provider LLM abstraction — locali (Ollama), free-API (Groq/Cerebras via LiteLLM) (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.19
Nodes (25): int, LLMProvider, MemoryPalace, str, int, LLMProvider, MemoryPalace, str (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (19): int, LLMProvider, str, int, LLMProvider, str, int, str (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (14): float, int, str, float, int, str, from_dict(), load() (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (20): int, str, int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search() (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.31
Nodes (9): str, str, agent_by_name(), default_council(), polarities_for(), 18 personas fisse con polarity pairs (Council of High Intelligence pattern).  Og, Cerca un agente per key (case-insensitive). Ritorna None se non trovato., Ritorna il set di agenti di default (12, bilanciati per dominio). (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (8): LLMProvider, MemoryPalace, str, LLMProvider, MemoryPalace, str, Aggiorna palace.strategy_summary in place., Genera un summary testuale della strategia per i prompt successivi.

### Community 8 - "Community 8"
Cohesion: 0.19
Nodes (14): int, MemoryPalace, str, int, MemoryPalace, str, tavolarotonda — Council multi-agente per decisioni reali e concrete.  Package: 9, audit_report_from_palace() (+6 more)

## Knowledge Gaps
- **16 isolated node(s):** `LLMProvider`, `int`, `str`, `int`, `int` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.290) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 4` to `Community 0`, `Community 2`, `Community 3`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Why does `run_full_council()` connect `Community 0` to `Community 8`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `MemoryPalace` (e.g. with `str` and `int`) actually correct?**
  _`MemoryPalace` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `LLMProvider` (e.g. with `Secretary` and `LLMProvider`) actually correct?**
  _`LLMProvider` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Secretary` (e.g. with `LLMProvider` and `MemoryPalace`) actually correct?**
  _`Secretary` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Director` (e.g. with `LLMProvider` and `PhaseEvent`) actually correct?**
  _`Director` has 10 INFERRED edges - model-reasoned connections that need verification._