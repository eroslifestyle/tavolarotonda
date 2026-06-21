# Graph Report - tavolarotonda  (2026-06-21)

## Corpus Check
- 11 files · ~8,420 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 177 nodes · 464 edges · 9 communities
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

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
1. `MemoryPalace` - 40 edges
2. `LLMProvider` - 38 edges
3. `run_full_council()` - 24 edges
4. `Secretary` - 18 edges
5. `Director` - 16 edges
6. `PhaseEvent` - 14 edges
7. `Agent` - 14 edges
8. `str` - 13 edges
9. `MockProvider` - 13 edges
10. `MemoryPalace` - 12 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `str` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `Secretary` --uses--> `LLMProvider`  [INFERRED]
  secretary.py → providers.py
- `LLMProvider` --uses--> `LLMProvider`  [INFERRED]
  secretary.py → providers.py

## Communities (9 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (35): Agent, Director, bool, int, LLMProvider, MemoryPalace, str, Secretary (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (17): ProviderKind, bool, float, int, str, CircuitBreaker, ProviderResult, Determina il kind del provider in base al nome del modello. (+9 more)

### Community 2 - "Community 2"
Cohesion: 0.16
Nodes (26): MemoryPalace, str, Namespace, int, MemoryPalace, str, _build_council(), _build_provider() (+18 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (17): int, LLMProvider, str, int, LLMProvider, _extract_json(), Director / Regista — per ogni round fissa il focus e assegna chi confuta chi.  P, Best-effort JSON extraction (gestisce code fences e testo intorno). (+9 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (11): float, int, str, from_dict(), load(), MemoryPalace, Memory Palace — stato condiviso persistente per la sessione di tavola rotonda., Esporta la sessione come transcript markdown leggibile. (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (18): int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search(), _query_for(), Adversarial evidence retrieval — supporting vs counter-evidence.  Pattern geek-a (+10 more)

### Community 6 - "Community 6"
Cohesion: 0.28
Nodes (8): str, agent_by_name(), default_council(), polarities_for(), 18 personas fisse con polarity pairs (Council of High Intelligence pattern).  Og, Cerca un agente per key (case-insensitive). Ritorna None se non trovato., Ritorna il set di agenti di default (12, bilanciati per dominio)., Ritorna le keys degli agenti in polarità con l'agent dato.

### Community 7 - "Community 7"
Cohesion: 0.25
Nodes (5): LLMProvider, MemoryPalace, str, Aggiorna palace.strategy_summary in place., Genera un summary testuale della strategia per i prompt successivi.

### Community 8 - "Community 8"
Cohesion: 0.50
Nodes (4): int, str, Rimuove marker di prompt injection, tronca a max_length.      NON è una garanzia, sanitize_directive()

## Knowledge Gaps
- **5 isolated node(s):** `str`, `int`, `bool`, `ProviderKind`, `float`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.289) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 4` to `Community 0`, `Community 2`, `Community 3`, `Community 7`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `adversarial_research()` connect `Community 5` to `Community 0`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `MemoryPalace` (e.g. with `str` and `int`) actually correct?**
  _`MemoryPalace` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `LLMProvider` (e.g. with `Secretary` and `LLMProvider`) actually correct?**
  _`LLMProvider` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Secretary` (e.g. with `MemoryPalace` and `LLMProvider`) actually correct?**
  _`Secretary` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Director` (e.g. with `PhaseEvent` and `MemoryPalace`) actually correct?**
  _`Director` has 10 INFERRED edges - model-reasoned connections that need verification._