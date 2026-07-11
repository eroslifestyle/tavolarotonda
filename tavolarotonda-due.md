---
title: tavolarotonda-due
type: progetto
created: 2026-07-01
updated: 2026-07-01
aliases: [Tavola Rotonda 2, tavola-rotonda-due, council, war-room, tavolarotonda]
tags: [auto-registered, multi-agent, council, llm, python, open-source]
sources: 1
status: attivo
repo: /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due
---

# tavolarotonda-due 🥽

**Council multi-agente per decisioni reali e concrete.** Zero teoria, solo pratica.

> **2026-07-01 — RENAME + SPOSTAMENTO**: ex `tavolarotonda`, ora vive in `Memoria/progetti/tavolarotonda-due/` (era in `/mnt/backup/PROGETTI/tavolarotonda/`, fuori scope `Dropbox/1 Programmazione/Progetti/`). Git history intatto (HEAD `da1f90b2`). Vecchia pagina `progetti/tavolarotonda/tavolarotonda.md` aggiornata come redirect.

Software Python ispirato a 5 reference consolidati:
- [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) (⭐982) — 18 personas + polarity pairs + Problem Restate Gate
- [Detrol/quorum-cli](https://github.com/Detrol/quorum-cli) (⭐106) — CLI dibattiti strutturati + MCP
- [geek-alt/LLM-Council](https://github.com/geek-alt/LLM-Council) — Memory Palace + Sequential MoA + adversarial evidence + minority report
- [prefrontalsys/panel-of-experts-awscao](https://github.com/prefrontalsys/panel-of-experts-awscao) — Heterogeneous models + profili moderator/pannelist
- Original implementation: Director + Secretary + RE/WHY/DECISION notation

## Obiettivo

Decisioni multi-prospettiva con modelli LLM eterogenei, persistenti, anti-groupthink, con audit/Q&A HTML, privacy tier esplicita e prompt-injection mitigation. Single source of truth: `repo/README.md`.

## Stato attuale

- Repo: `/home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due/` (~564 KB, 9 moduli Python + GUI Flask + 14 test + 5 discussion HTML)
- **RENAME 2026-07-01**: directory spostata da `/mnt/backup/PROGETTI/tavolarotonda/` → `Obsidian/Memoria/progetti/tavolarotonda-due/` (mv, NON git mv perché git repo era locale e head aveva unmodified change)
- **GIT HEAD**: `da1f90b2dde813b00068fb8acad9de0e66f51609` (preservato, branch main)
- Moduli: `agents.py` (18 personas) · `phases.py` (pipeline 6 fasi) · `director.py` · `secretary.py` · `providers.py` (Ollama/OpenAI/Claude/Mock) · `evidence.py` · `memory_palace.py` · `prompts.py` · `reports.py` (HTML audit+Q&A)
- Privacy tier: `local_only` (default Ollama) / `cloud_ok` (Claude+OpenAI) / `free_api_ok` (Groq+Cerebras con PII redaction)
- Hardening: 10 improvements (prompt injection, timeout, persistence, privacy, rate limit, retry/backoff, project tree depth, json extract, MAX_ROUNDS configurable, temperature configurable)

## Architettura / componenti

| File | Ruolo | LOC stima |
|---|---|---|
| `tavolarotonda/agents.py` | 18 personas + polarity pairs (single source of truth) | ~250 |
| `tavolarotonda/providers.py` | LLM abstraction (Ollama / OpenAI-compat / Claude / Mock) | ~180 |
| `tavolarotonda/evidence.py` | Adversarial retrieval (SearXNG / Brave / DDG / Mock) | ~120 |
| `tavolarotonda/memory_palace.py` | Stato persistente condiviso (JSON) | ~100 |
| `tavolarotonda/prompts.py` | Template prompt centralizzati (zero duplicazione) | ~150 |
| `tavolarotonda/director.py` | Regista (focus + assignments per round) | ~80 |
| `tavolarotonda/secretary.py` | Segretario (strategy live) | ~80 |
| `tavolarotonda/phases.py` | Pipeline: Research → Restate → Brainstorm → Critique → Synthesis → Vote | ~300 |
| `tavolarotonda/reports.py` | HTML audit + Q&A generator | ~200 |
| `gui/app.py` | Frontend Flask (visualizzazione discussion) | ~150 |

Pipeline: **Phase 0 Research** → **Phase 1 Restate** → **Phase 2 Brainstorm** → **Phase 3 Critique** → **Phase 4 Synthesis** (minority report) → **Phase 5 Verdict** (voti 0-10).

## Modalità d'uso

```bash
# Demo no-LLM
python -m tavolarotonda --mock "Dovrei migrare a Postgres?"

# Con Ollama locale (privacy default)
python -m tavolarotonda --privacy local_only "Argomento complesso"

# Audit di un file
python -m tavolarotonda --audit examples/audit_target.py --output output/audit_report.html

# Q&A multi-domanda
python -m tavolarotonda --qa "Rischio X?" "Alternative Y?" --output output/qa.html

# GUI Flask
python gui/app.py  # http://localhost:5000
```

## Decisioni chiave

- [2026-06-21] **Spostato in `/mnt/backup/PROGETTI/tavolarotonda`** (fuori da `/tmp`) + registrato nel vault come progetto canonico
- [2026-06-21] Architettura a 9 moduli indipendenti (modularità KING — zero duplicazione)
- [2026-06-21] Privacy tier esplicito + PII redaction automatica per free tier
- [2026-06-21] Prompt injection mitigation via `sanitize_directive()` + topic isolation
- [2026-06-21] 10 hardening improvements identified and implemented
- [2026-06-21] **Repo GitHub privato** → `github.com/eroslifestyle/tavolarotonda` (commit `c882083`, branch `main`)
- [2026-06-21] **LICENSE MIT** aggiunto (Copyright 2026 Eros De Grande)
- [2026-06-21] **Wiring operativo skill Pi** → adapter `bin/war-room-tavolarotonda` + symlink `/usr/local/bin/` (test E2E con 12 personas OK)
- [2026-06-21] **GUI anti-troncamento** → commit `fc0c7b0`: info panel modello + radio cards council mode + classe utility `.text-wrap-anywhere` (5 problemi risolti)
- **[2026-07-01]** **RENAME a `tavolarotonda-due/` + spostato dentro `Obsidian/Memoria/progetti/`** (era in `/mnt/backup/PROGETTI/` fuori scope). Git history intatto (HEAD `da1f90b2`). Vecchia pagina vault mantenuta come redirect.

## Wiring con skill Pi (2026-06-21)

Decisione utente: **wiring SI** → adapter invocabile da qualsiasi contesto, **NON** modifica le skill Pi esistenti (war-room SKILL.md usato da più progetti, rischio basso = niente edit).

**Come funziona:**
- `bin/war-room-tavolarotonda` → wrapper bash che risolve il repo root via `readlink -f` (gestisce symlink) e lancia `python -m tavolarotonda`
- Symlink globale: `/usr/local/bin/war-room-tavolarotonda` → disponibile in `$PATH` ovunque
- Default `--privacy local_only` se non specificato (override via env `PRIVACY` o flag)

**Skill Pi che possono ora delegare a tavolarotonda:**
| Skill | Uso consigliato |
|---|---|
| `/skill:war-room` | Spawn multi-agente tradizionale → ora delega a `tavolarotonda` via shell exec per discussioni persistenti + HTML audit |
| `/skill:opus-m3-confer` | Dialogo strutturato → tavolarotonda aggiunge persistent Memory Palace + adversarial evidence |
| `/skill:swarm` | Bruteforce parallelo → backend council opzionale per cross-validazione decisioni |

## Come avviare la GUI (2026-07-01)

```bash
cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due
# Senza dipendenze extra → mock mode (no LLM richiesto):
python gui/app.py
# poi aprire http://localhost:5000 in Chrome
```

Backend Flask usa import dei moduli in `tavolarotonda/` — funziona out-of-the-box se Python 3.10+ è disponibile (le 11 dipendenze sono stdlib oggi; se mancanti il mock fallback è OK).

## Problemi noti / aperti

| # | Issue | Stato |
|---|---|---|
| 1 | Claude API solo HTTP raw (no SDK Anthropic) | Roadmap v0.2 |
| 2 | Brave/SearXNG richiede config utente | Mock fallback OK |
| 3 | OCR/screenshots non supportati | Roadmap v0.2 |
| 4 | No MCP server (vs quorum-cli) | Roadmap v0.2 |
| 5 | Voting scores mock in `--mock` mode | Reali con LLM attivo |
| 6 | Repo remoto GitHub privato a `eroslifestyle/tavolarotonda` — locale e remoto disallineati (remote va re-pushato) | 2026-07-01 |

## Prossimi passi

1. ~~`git init` + remote GitHub~~ ✅ FATTO 2026-06-21 → `eroslifestyle/tavolarotonda` (privato) — **richiede git push dopo rename locale**
2. ~~Aggiungere LICENSE MIT~~ ✅ FATTO
3. ~~Wiring con skill Pi~~ ✅ FATTO
4. **Re-impostare remote** dopo rename: `git remote add origin git@github.com:eroslifestyle/tavolarotonda.git && git push`
5. Test integrazione Ollama locale con modelli pinned (`chat-max`, `cyber-max`)
6. Aggiungere MCP server (vs `quorum-cli`)
7. Wiring con `opus-m3-confer` per routing decisioni complesse
8. Pubblicare release v0.1

## Test status

```bash
cd /home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due
python tests/test_smoke.py
# ✅ 14 test base passati (ultima esecuzione 2026-06-21)
```

## Discussion di esempio (output HTML)

- `output/discussion_3e0385f2e4fd.html` — sessione reale con LLM
- `output/audit_report.html` — audit di codice con criticità
- `output/qa_template.html` — Q&A multi-domanda compilabile

## Single source of truth

- **Documentazione canonica**: `README.md` (repo)
- **Indice vault**: [[_INDEX]]
- **Hot cache globale**: [[Wiki - Hot Cache|Hot Cache]]
- **Log globale**: [[Wiki - Log Globale|Log Globale]]

## Collegamenti

- Skill correlata: `/skill:war-room` (orchestrazione multi-agente in Pi)
- Skill correlata: `/skill:swarm` (bruteforce parallelo)
- Skill correlata: `/skill:opus-m3-confer` (dialogo strutturato Opus↔M3)
- Pagina vault precedente (redirect): `progetti/tavolarotonda/tavolarotonda.md`

## Fonti

- Repo locale: `README.md` (in repo)
- Pagina vault precedente: `progetti/tavolarotonda/tavolarotonda.md`
