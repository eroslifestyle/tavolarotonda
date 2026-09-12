# Graph Report - tavolarotonda-due  (2026-07-12)

## Corpus Check
- 55 files · ~54,810 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1125 nodes · 2190 edges · 59 communities (57 shown, 2 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 169 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e3804cd7`
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
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]

## God Nodes (most connected - your core abstractions)
1. `MemoryPalace` - 77 edges
2. `LLMProvider` - 69 edges
3. `run_full_council()` - 49 edges
4. `PhaseEvent` - 35 edges
5. `AnthropicCompatProvider` - 34 edges
6. `MockProvider` - 27 edges
7. `phase_brainstorm()` - 26 edges
8. `Director` - 26 edges
9. `Secretary` - 26 edges
10. `run_audit()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `int` --uses--> `MemoryPalace`  [INFERRED]
  tavolarotonda/reports.py → memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  tavolarotonda/reports.py → memory_palace.py
- `int` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `MemoryPalace` --uses--> `MemoryPalace`  [INFERRED]
  reports.py → memory_palace.py
- `MultiProvider` --uses--> `CustomPersona`  [INFERRED]
  gui/app.py → tavolarotonda/custom_personas.py

## Communities (59 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (35): Agent, Any, Director, MemoryPalace, bool, int, bool, int (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.28
Nodes (8): str, Exporters — AQ Session 7/10.  Esporta un MemoryPalace in vari formati: CSV, Mark, Esporta gli eventi del palace in CSV per analisi., Esporta il transcript completo in Markdown., Esporta il palace completo in JSON., to_csv(), to_json(), to_markdown()

### Community 2 - "Community 2"
Cohesion: 0.20
Nodes (10): Smoke test base — verifica che il wiring del codice funzioni senza LLM reale.  U, Esegue tutti i test in sequenza., Alcune polarity pairs chiave devono esistere., Rimuove/ marca injection markers., PII redaction per free_api tier., run_all(), _run_async_tests(), test_polarity_pairs() (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.26
Nodes (12): detect_lang(), get_lang(), str, i18n — English/Italian localization for CLI and HTML output.  Usage:     from .i, Auto-detect from LANG/LANGUAGE env vars., Return active language (default: detect)., Set active language ('en' or 'it')., Reset to auto-detection (clears cached language). (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (37): MemoryPalace, str, int, LLMProvider, MemoryPalace, str, Namespace, _build_council() (+29 more)

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (31): int, str, int, str, SearchProvider, adversarial_research(), _detect_provider(), _mock_search() (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (5): Commit, Sessione 2026-07-02 — TR-011/012/013, TR-011 ✅ — Test sessione reale Ornith, TR-012 ✅ — ornith-9b come provider veloce, TR-013 ✅ — war-room path dopo mv

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (20): appendEvent(), clearStream(), connectStream(), escapeHtml(), formatResearch(), formatText(), handleEvent(), loadCouncilPresets() (+12 more)

### Community 8 - "Community 8"
Cohesion: 0.20
Nodes (19): float, str, get_agent_color(), get_aq_score(), get_model(), get_preset(), get_timeout(), load() (+11 more)

### Community 9 - "Community 9"
Cohesion: 0.11
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
Cohesion: 0.09
Nodes (24): Architecture, Code audit, code:bash (git clone <repo> tavolarotonda), code:bash (python -m tavolarotonda --mock "Should I open-source my agen), code:bash (# 1. Start Ollama), code:bash (python -m tavolarotonda --audit examples/audit_target.py --m), code:bash (python -m tavolarotonda --qa "What are the risks?" "What alt), code:bash (# Only local Ollama models, no cloud, no free-API) (+16 more)

### Community 23 - "Community 23"
Cohesion: 0.11
Nodes (13): calculate_discount(), get_db_connection(), get_user(), parse_config(), float, str, Esempio di codice da audire — contiene pattern realistici con criticità intenzio, Get user by username — INSECURE! (+5 more)

### Community 24 - "Community 24"
Cohesion: 0.10
Nodes (27): int, MemoryPalace, str, int, MemoryPalace, str, audit_report_from_palace(), _get_html_base() (+19 more)

### Community 26 - "Community 26"
Cohesion: 0.04
Nodes (46): Adding a new agent persona / Aggiungere una nuova persona-agente, Adding a new LLM provider / Aggiungere un nuovo provider LLM, API key missing / Chiave API mancante, Architecture / Architettura, Audit a code file / Audit di un file di codice, CLI Flags / Opzioni CLI, code:bash (python -m tavolarotonda --mock "Should I open-source my agen), code:bash (export ANTHROPIC_API_KEY=sk-ant-api03-...) (+38 more)

### Community 27 - "Community 27"
Cohesion: 0.15
Nodes (17): int, LLMProvider, str, int, LLMProvider, str, int, LLMProvider (+9 more)

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
Cohesion: 0.16
Nodes (11): ProviderKind, Determina il kind del provider in base al nome del modello., Determina il kind del provider in base al nome del modello., Determina il kind del provider in base al nome del modello., Determina il kind del provider in base al nome del modello., Determina il kind del provider in base al nome del modello., Esegue una completion LLM. Retry + circuit breaker integrati., Esegue una completion LLM. Retry + circuit breaker integrati. (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.09
Nodes (37): str, str, str, agent_by_name(), default_council(), polarities_for(), str, 18 personas fisse con polarity pairs (Council of High Intelligence pattern).  Og (+29 more)

### Community 35 - "Community 35"
Cohesion: 0.15
Nodes (16): LLMProvider, MemoryPalace, phase_research(), phase_restate(), phase_verdict(), MemoryPalace, Ogni agente vota 0-10 sulla proposta finale (feasibility, impact, risk_safety)., Ogni agente vota 0-10 sulla proposta finale (feasibility, impact, risk_safety). (+8 more)

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (13): tavolarotonda — Council multi-agente per decisioni reali e concrete.  Package: 1, from_dict(), load(), MemoryPalace, Memory Palace — stato condiviso persistente per la sessione di tavola rotonda., Esporta la sessione come transcript markdown leggibile., Esporta la sessione come transcript markdown leggibile., Stato persistente condiviso della sessione di dibattito. (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.20
Nodes (9): Commit, Config progetto (`pyproject.toml`), Cosa fatto, GitHub Actions CI (`.github/workflows/ci.yml`), Goal, Next, Ruff auto-fix (14 file), Test result (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.21
Nodes (17): api_set_research_config(), Aggiorna la config research (globale, per-agente, provider)., get_config(), is_research_enabled(), _load(), bool, str, Research gating config — AQ Session 8/10.  Controlla quali agenti fanno web rese (+9 more)

### Community 39 - "Community 39"
Cohesion: 0.14
Nodes (16): str, _extract_list_section(), _extract_section(), phase_synthesis(), Sintetizzatore finale: decisione + minority report + open questions + next steps, Sintetizzatore finale: decisione + minority report + open questions + next steps, Sintetizzatore finale: decisione + minority report + open questions + next steps, Sintetizzatore finale: decisione + minority report + open questions + next steps (+8 more)

### Community 40 - "Community 40"
Cohesion: 0.09
Nodes (36): str, int, str, Starlette, Path, str, Integrazione Obsidian vault — lettura topic e salvataggio sessioni., Legge un file .md dal vault Obsidian per nome topic.      Cerca in vault/istanze (+28 more)

### Community 41 - "Community 41"
Cohesion: 0.25
Nodes (11): float, int, str, float, int, str, float, int (+3 more)

### Community 42 - "Community 42"
Cohesion: 0.18
Nodes (10): CLI --model + --intensity ornith (__main__.py), code:python (MODEL_TIER_MAP = {), Commit, Cosa è stato fatto, Goal, MODEL_TIER_MAP (providers.py), phases.py wiring, Risultati verificati (+2 more)

### Community 43 - "Community 43"
Cohesion: 0.17
Nodes (21): api_create_persona(), api_delete_persona(), api_list_personas(), Lista tutte le personas custom., Crea una nuova persona custom., Elimina una persona custom., create_persona(), CustomPersona (+13 more)

### Community 44 - "Community 44"
Cohesion: 0.08
Nodes (29): api_agents(), api_council_presets(), api_export(), api_export_personas(), api_history(), api_history_delete(), api_history_detail(), api_import_personas() (+21 more)

### Community 45 - "Community 45"
Cohesion: 0.10
Nodes (28): bool, api_diff(), api_palace(), api_report(), api_run(), api_sessions(), audit_collect_targets(), audit_project_stats() (+20 more)

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (11): ProviderResult, bool, str, CircuitBreaker, ProviderResult, Risultato normalizzato di una chiamata LLM., Risultato normalizzato di una chiamata LLM., Circuit breaker per modelli inaffidabili. (+3 more)

### Community 47 - "Community 47"
Cohesion: 0.15
Nodes (20): _build_multi_provider(), _build_provider(), _check_env(), _check_ollama(), _extract_agent_key(), MultiProvider, Estrae l'agent_key dal system_seed (es. 'Sei Aristotele. ...' → 'aristotele')., Provider che instrada ogni chiamata al sub-provider giusto in base all'agent_key (+12 more)

### Community 48 - "Community 48"
Cohesion: 0.21
Nodes (15): MockProvider, PhaseEvent, _make_provider(), phase_debate(), int, LLMProvider, MemoryPalace, str (+7 more)

### Community 49 - "Community 49"
Cohesion: 0.13
Nodes (16): float, float, int, Chiama Ollama /api/generate., Chiama Ollama /api/generate., Chiama Ollama /api/generate., Chiama Ollama /api/generate., Chiama Ollama /api/generate. (+8 more)

### Community 50 - "Community 50"
Cohesion: 0.19
Nodes (11): LLMProvider, MemoryPalace, str, LLMProvider, MemoryPalace, str, LLMProvider, MemoryPalace (+3 more)

### Community 51 - "Community 51"
Cohesion: 0.13
Nodes (17): int, LLMProvider, int, AnthropicCompatProvider, MockProvider, Provider LLM abstraction — locali (Ollama), free-API (Groq/Cerebras via LiteLLM), Provider finto che ritorna risposte plausibili per smoke test.      NON usare in, Provider finto che ritorna risposte plausibili per smoke test.      NON usare in (+9 more)

### Community 53 - "Community 53"
Cohesion: 0.28
Nodes (8): api_classify_topic(), Classifica un topic e consiglia il preset migliore., classify_topic(), get_routing_preview(), str, Topic classifier — Tavola Rotonda AQ Session 2/10.  Classifica il topic e consig, Ritorna un dict completo per la UI con spiegazione., Classifica un topic e ritorna (tipo, preset, motivazione).      Returns:

### Community 56 - "Community 56"
Cohesion: 0.15
Nodes (15): int, str, int, str, _extract_json(), Director — sets focus and assigns cross-examination for each round.  Output JSON, Best-effort JSON extraction (gestisce code fences e testo intorno)., Best-effort JSON extraction (gestisce code fences e testo intorno). (+7 more)

### Community 57 - "Community 57"
Cohesion: 0.24
Nodes (9): api_voting(), Ritorna scorecard + heatmap + outliers per una sessione., build_heatmap(), build_scorecard(), find_outliers(), Voting analysis — AQ Session 9/10.  Analizza i voti degli agenti: scorecard, con, Costruisce una scorecard dai voti degli agenti., Costruisce una heatmap di consenso/conflitto tra agenti.      Ritorna una matric (+1 more)

### Community 58 - "Community 58"
Cohesion: 0.33
Nodes (5): Chiama Claude API (Anthropic). Per ora solleva: usare SDK Anthropic o mock., Chiama Claude API (Anthropic). Per ora solleva: usare SDK Anthropic o mock., Chiama Claude API (Anthropic). Per ora solleva: usare SDK Anthropic o mock., Chiama Claude API (Anthropic). Per ora solleva: usare SDK Anthropic o mock., Chiama Claude API (Anthropic). Per ora solleva: usare SDK Anthropic o mock.

### Community 59 - "Community 59"
Cohesion: 0.33
Nodes (5): PII redaction minima (best-effort) per free_api tier.          NB: questa è una, PII redaction minima (best-effort) per free_api tier.          NB: questa è una, PII redaction minima (best-effort) per free_api tier.          NB: questa è una, PII redaction minima (best-effort) per free_api tier.          NB: questa è una, PII redaction minima (best-effort) per free_api tier.          NB: questa è una

### Community 60 - "Community 60"
Cohesion: 0.33
Nodes (6): Rimuove Qwen3  block (se delimitato correttamente)., Rimuove Qwen3 / Qwen3 / <think> block (modelli che ragionano)., Rimuove Qwen3 / Qwen3 / <think> block (modelli che ragionano)., _strip_think(), Rimuove Qwen3  blocks., test_strip_think()

### Community 61 - "Community 61"
Cohesion: 0.25
Nodes (8): phase_critique(), Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).      Mir, Resolve model + optional tier for an agent.      When agent.default_model == "au, Resolve model + optional tier for an agent.      When agent.default_model == "au, _resolve_agent_model()

## Knowledge Gaps
- **317 isolated node(s):** `int`, `state`, `Sessioni (`sessioni/`)`, `Altri file root`, `.Claude (`.claude/`)` (+312 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MemoryPalace` connect `Community 36` to `Community 0`, `Community 34`, `Community 3`, `Community 4`, `Community 2`, `Community 41`, `Community 44`, `Community 45`, `Community 48`, `Community 50`, `Community 51`, `Community 56`, `Community 24`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `LLMProvider` connect `Community 27` to `Community 0`, `Community 32`, `Community 2`, `Community 3`, `Community 4`, `Community 36`, `Community 44`, `Community 47`, `Community 48`, `Community 49`, `Community 50`, `Community 51`, `Community 56`, `Community 58`, `Community 59`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `run_full_council()` connect `Community 0` to `Community 34`, `Community 35`, `Community 4`, `Community 3`, `Community 36`, `Community 39`, `Community 2`, `Community 44`, `Community 45`, `Community 48`, `Community 51`, `Community 56`, `Community 61`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `MemoryPalace` (e.g. with `PhaseEvent` and `int`) actually correct?**
  _`MemoryPalace` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `LLMProvider` (e.g. with `LLMProvider` and `PhaseEvent`) actually correct?**
  _`LLMProvider` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `PhaseEvent` (e.g. with `str` and `LLMProvider`) actually correct?**
  _`PhaseEvent` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `AnthropicCompatProvider` (e.g. with `MultiProvider` and `LLMProvider`) actually correct?**
  _`AnthropicCompatProvider` has 16 INFERRED edges - model-reasoned connections that need verification._