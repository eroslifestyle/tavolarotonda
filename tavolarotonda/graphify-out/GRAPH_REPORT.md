# Graph Report - tavolarotonda  (2026-07-11)

## Corpus Check
- 15 files · ~11,083 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 926 nodes · 1896 edges · 36 communities (34 shown, 2 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 184 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `412bf62b`
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
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 41|Community 41]]

## God Nodes (most connected - your core abstractions)
1. `MemoryPalace` - 81 edges
2. `LLMProvider` - 73 edges
3. `run_full_council()` - 48 edges
4. `AnthropicCompatProvider` - 39 edges
5. `MockProvider` - 29 edges
6. `Secretary` - 28 edges
7. `PhaseEvent` - 28 edges
8. `Director` - 26 edges
9. `phase_brainstorm()` - 25 edges
10. `Agent` - 25 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `int` --uses--> `MemoryPalace`  [INFERRED]
  tavolarotonda/reports.py → memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  tavolarotonda/reports.py → memory_palace.py
- `str` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py

## Communities (36 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (89): Agent, Any, Director, int, LLMProvider, str, int, LLMProvider (+81 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (53): bool, float, int, ProviderKind, ProviderResult, bool, float, int (+45 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (56): str, float, int, str, float, int, str, LLMProvider (+48 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (35): str, int, str, Starlette, tavolarotonda — Council multi-agente per decisioni reali e concrete.  Package: 1, Path, str, Integrazione Obsidian vault — lettura topic e salvataggio sessioni. (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (63): str, MultiProvider, Provider che instrada ogni chiamata al sub-provider giusto in base all'agent_key, LLMProvider, int, LLMProvider, MemoryPalace, str (+55 more)

### Community 5 - "Community 5"
Cohesion: 0.19
Nodes (29): int, str, int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search() (+21 more)

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (5): Commit, Sessione 2026-07-02 — TR-011/012/013, TR-011 ✅ — Test sessione reale Ornith, TR-012 ✅ — ornith-9b come provider veloce, TR-013 ✅ — war-room path dopo mv

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (20): appendEvent(), clearStream(), connectStream(), escapeHtml(), formatResearch(), formatText(), handleEvent(), loadCouncilPresets() (+12 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (69): float, str, api_agents(), api_council_presets(), api_models(), api_palace(), api_report(), api_run() (+61 more)

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
Cohesion: 0.21
Nodes (12): MemoryPalace, str, MemoryPalace, str, audit_report_from_palace(), MemoryPalace, str, Genera un audit report HTML a partire da un MemoryPalace (post-sessione). (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.40
Nodes (5): Pipeline completa end-to-end con MockProvider., Esegue tutti i test in sequenza., run_all(), _run_async_tests(), test_full_pipeline_mock()

### Community 27 - "Community 27"
Cohesion: 0.20
Nodes (10): int, str, int, str, int, str, Rimuove marker di prompt injection, tronca a max_length.      NON è una garanzia, sanitize_directive() (+2 more)

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

### Community 37 - "Community 37"
Cohesion: 0.20
Nodes (9): Commit, Config progetto (`pyproject.toml`), Cosa fatto, GitHub Actions CI (`.github/workflows/ci.yml`), Goal, Next, Ruff auto-fix (14 file), Test result (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.12
Nodes (16): Smoke test base — verifica che il wiring del codice funzioni senza LLM reale.  U, Query adversarial genera stringhe diverse per supporting vs counter., 18 personas devono essere presenti., Alcune polarity pairs chiave devono esistere., Lookup case-insensitive., Rimuove Qwen3  blocks., Si apre dopo N fallimenti., PII redaction per free_api tier. (+8 more)

### Community 41 - "Community 41"
Cohesion: 0.20
Nodes (8): int, int, int, Report generator — HTML audit + HTML Q&A compilabile.  Output atteso per l'utent, Genera un template Q&A compilabile.      `prefill_answers`: {question_index: {ag, render_qa_template(), Genera HTML Q&A compilabile., test_html_qa_template()

## Knowledge Gaps
- **289 isolated node(s):** `str`, `int`, `bool`, `int`, `float` (+284 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMProvider` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 38`, `Community 8`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `MemoryPalace` connect `Community 2` to `Community 0`, `Community 3`, `Community 4`, `Community 38`, `Community 8`, `Community 41`, `Community 24`, `Community 26`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `run_full_council()` connect `Community 0` to `Community 2`, `Community 3`, `Community 4`, `Community 38`, `Community 8`, `Community 26`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `MemoryPalace` (e.g. with `str` and `int`) actually correct?**
  _`MemoryPalace` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `LLMProvider` (e.g. with `Secretary` and `LLMProvider`) actually correct?**
  _`LLMProvider` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `AnthropicCompatProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`AnthropicCompatProvider` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `MockProvider` (e.g. with `str` and `Namespace`) actually correct?**
  _`MockProvider` has 11 INFERRED edges - model-reasoned connections that need verification._