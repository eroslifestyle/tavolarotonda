---
title: tavolarotonda-due — Rename + Integrazione Ornith-35B
type: sessione
project: tavolarotonda-due
date: 2026-07-02
updated: 2026-07-02
tags: [tavolarotonda-due, ornith, llm-integration, rename, routing]
---

# Sessione 2026-07-02 — Rename + Integrazione Ornith-35B

## Cosa è stato fatto

### 1. Rename + spostamento progetto
- Trovato repo Python a `/mnt/backup/PROGETTI/tavolarotonda/` (era fuori scope Dropbox/Obsidian)
- Spostato via `mv` a `/home/mrxxx/Obsidian/Memoria/progetti/tavolarotonda-due/`
- Git HEAD `da1f90b` preservato, symlink `graphify-out` relativo → funziona ancora
- Creata pagina vault canonica `tavolarotonda-due.md`
- Vecchia `progetti/tavolarotonda/tavolarotonda.md` convertita a redirect

### 2. Integrazione Ornith-35B (Qwen3.6 MoE, ctx 256K, Q4_K_M)
- **Modello Ollama**: `ornith-35b:latest` (21 GB, context 262144, famiglia qwen35moe)
- **Registrato in `gui/app.py`**:
  - Aggiunto in `MODELS` dict con icon 🐦, label "Ornith 35B (qwen3.6 MoE, ctx 256k)", `provider_kind=ollama`
  - Aggiunto in `_MODEL_FOR_PROVIDER`
  - Sostituito `ollama-auto` con `ornith-35b` in **triade bilanciata** Gruppo C (torvalds/musashi/meadows/munger/taleb/rams)
  - Sostituito `ollama-auto` con `ornith-35b` nel **round-robin alternato**
- **Fix `providers.py`**: `_strip_think` esteso con `_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)` — Ornith usa `<think>` invece del pattern Qwen3

### 3. Test end-to-end verificati
- `2+2=4` → latency 4.6s, error=None ✅
- `capitale Francia = Parigi` → latency 0.86s, niente `<think>` residuo ✅
- `/api/models` → `ornith-35b` state=ok, model=`ornith-35b:latest` ✅
- `/api/council-presets` → triade + alternating: 6 agenti → ornith-35b ✅

## Stato post-sessione

- **GUI**: `http://localhost:8912/` (Flask, 6 modelli, 18 agenti, task bg `b4i7pvl7m`)
- **Modelli attivi nel routing multi-provider**:
  - Gruppo A (6 agenti razionali) → `opus-4.8` (richiede ANTHROPIC_API_KEY)
  - Gruppo B (6 agenti creativi) → `MiniMax-M3` (richiede MiniMax_API_KEY)
  - Gruppo C (6 agenti pratici) → `ornith-35b` ✅ locale, nessuna key

## File modificati

| File | Modifica |
|---|---|
| `gui/app.py` | +ornith-35b in MODELS, _MODEL_FOR_PROVIDER, routing triade+alternating, descrizione triade |
| `tavolarotonda/providers.py` | +`_THINK_BLOCK_RE` per strip `<think>` |
| `tavolarotonda-due.md` | Nuova pagina vault canonica (entry del progetto) |
| `_INDEX.md` | Auto-aggiornato da hook obsidian_auto_update |

## Prossimi passi

1. `git commit + push` con le modifiche di questa sessione
2. Test sessione reale con Ornith (mode topic, 3 round, `ornith-35b`)
3. Aggiunta ornith-9b (9B, 862ms) per agenti "veloci" opzionali
4. Aggiornare il wiring `/usr/local/bin/war-room-tavolarotonda` se si usa ornith come default CLI

## Wikilink

- [[tavolarotonda-due]] — pagina principale del progetto
- [[2026-06-21-bootstrap-progetto-vault]] — sessione bootstrap iniziale
