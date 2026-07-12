---
name: sessione-2026-07-11-tr-014
description: TR-014 Ornith-35b CLI flag — MODEL_TIER_MAP + --model + --intensity ornith
metadata:
  type: session
  project: tavolarotonda-due
  date: 2026-07-11
---

# TR-014 — Sessione 2026-07-11 Ornith-35b CLI

## Goal
Aggiungere Ornith-35b come tier nel routing CLI di tavolarotonda.

## Cosa è stato fatto

### MODEL_TIER_MAP (providers.py)
Aggiunto tier `"ornith"` → `"ornith-35b"`:
```python
MODEL_TIER_MAP = {
    "critical": "opus-4-7",
    "reasoning": "minimax-sonar-pro",
    "standard": "claude-sonnet-5",
    "fast": "claude-haiku-4",
    "ornith": "ornith-35b",  # nuovo
}
```

### CLI --model + --intensity ornith (__main__.py)
- `--model MODEL` — model override per il council (es. `--model ornith-35b`)
- `--intensity` choices: aggiunto `"ornith"`
- `council_model=getattr(args, "model", None)` passato a `run_full_council` in `run_topic`, `run_audit`, `run_qa`

### phases.py wiring
- `_resolve_agent_model()` helper: risolve `default_model="auto"` → `council_model` con tier mapping
- `run_full_council()`: param `council_model: str | None`, passato a `phase_brainstorm` e `phase_critique`
- `phase_brainstorm` e `phase_critique`: usano `_resolve_agent_model` → `model=` + `model_tier=` in `provider.complete`

## Risultati verificati
| Check | Esito |
|---|---|
| `MODEL_TIER_MAP["ornith"]` | `ornith-35b` ✅ |
| `python -m tavolarotonda --help` | `--model MODEL` + `--intensity {fast,standard,reasoning,critical,ornith}` ✅ |
| mypy | 0 errori (15 file) ✅ |
| test suite | 30/30 PASS ✅ |
| git commit | `4b3f7c2` ✅ |
| git push | OK ✅ |

## Commit
`4b3f7c2` — feat(TR-014): Ornith-35b in MODEL_TIER_MAP + --model CLI flag

## Todo rimasti
- TR-030 — Claude API SDK (HTTP raw → SDK)
- TR-031 — SearXNG/Brave search (mock OK per ora)
- TR-032 — Pubblicazione repo pubblico GitHub
