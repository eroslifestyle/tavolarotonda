# HELP — tavolarotonda

**Multi-agent council for real, concrete decisions.** Zero theory, only practice.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [CLI Flags](#cli-flags)
3. [Privacy Modes](#privacy-modes)
4. [Output Formats](#output-formats)
5. [Troubleshooting](#troubleshooting)
6. [Architecture](#architecture)
7. [Contributing](#contributing)
8. [License](#license)

---

## Quick Start

### Demo — mock provider (no real LLM)

```bash
python -m tavolarotonda --mock "Should I open-source my agent framework?"
```

### With Ollama (local model)

```bash
ollama serve
python -m tavolarotonda "Should I migrate to Postgres?" --privacy local_only
```

### With Claude API

```bash
export ANTHROPIC_API_KEY=your-key-here
python -m tavolarotonda "What are the risks of microservices?" --model claude-sonnet-5
```

### Code audit

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Open output/audit_report.html in browser for audit with pros/cons/criticisms/advice
```

### Multi-question Q&A

```bash
python -m tavolarotonda --qa "What are the risks?" "What alternatives?" --mock --output output/qa.html
# Open output/qa.html for fillable template + comparative analysis per question
```

---

## CLI Flags

| Flag | Description | Default |
|---|---|---|
| `--mock` | Use MockProvider — no API calls | — |
| `--privacy local_only\|cloud_ok\|free_api_ok` | Privacy tier (see Privacy Modes) | `cloud_ok` |
| `--model <name>` | LLM model name | from MODEL_TIER_MAP |
| `--intensity <tier>` | Intensity tier: `critical\|reasoning\|standard\|fast\|ornith` | `standard` |
| `--rounds <N>` | Number of brainstorming rounds | `3` |
| `--audit <file>` | Audit a code file | — |
| `--qa "Q1" "Q2"` | Multi-question Q&A mode | — |
| `--output <path>` | Output HTML path | `output/report.html` |
| `--provider ollama\|openai\|anthropic\|mock` | LLM provider to use | auto-detect |
| `--port <N>` | Server port (if using server mode) | `8765` |
| `--help` | Show this help | — |

---

## Privacy Modes

**Critical: choose the right tier before sending any data.**

| Mode | What sends | Notes |
|---|---|---|
| `local_only` | Only local Ollama | No cloud, no free API |
| `cloud_ok` | + Claude / OpenAI via env key | Default |
| `free_api_ok` | + Groq / Cerebras via LiteLLM | PII redaction active |

> **Warning:** `free_api_ok` sends data to third-party free tiers. Do NOT send sensitive data (PII, credentials, proprietary code) in this mode.

---

## Output Formats

### Console — colored terminal

```bash
python -m tavolarotonda "Should I refactor this service?"
# Colored text output with agent opinions and final verdict
```

### HTML — Audit report

```bash
python -m tavolarotonda --audit examples/audit_target.py --mock --output output/audit_report.html
# Open in browser for full audit with pros/cons/criticisms/minority report
```

### HTML — Q&A template

```bash
python -m tavolarotonda --qa "What risks?" "What alternatives?" --mock --output output/qa.html
# Open in browser for fillable Q&A template with comparative analysis per question
```

---

## Troubleshooting

### Ollama not running

```bash
ollama serve
```

### API key missing

```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...
export OPENAI_API_KEY=sk-...
```

### Model not found

```bash
ollama pull llama3.2
# or
ollama list
```

### Port already in use

```bash
python -m tavolarotonda --port 8081
```

### Mock mode always works

```bash
# If anything fails, fall back to mock:
python -m tavolarotonda --mock "Your question here"
```

### Import errors

```bash
pip install requests
# No other dependencies required
```

---

## Architecture

```
tavolarotonda/
├── __main__.py       # CLI entry point
├── agents.py         # 18 personas + polarity pairs
├── providers.py      # LLM abstraction (Ollama / OpenAI / Claude / Mock)
├── evidence.py       # Adversarial retrieval (SearXNG / Brave / DuckDuckGo / Mock)
├── memory_palace.py  # Persistent shared state
├── phases.py         # 6-phase pipeline (Research → Restate → Brainstorm → Critique → Synthesis → Vote)
├── director.py       # Director (focus + round assignments)
├── secretary.py      # Secretary (live strategy consolidation)
├── prompts.py        # Centralized prompt templates (zero duplication)
└── reports.py        # HTML audit + Q&A generator
```

### Execution pipeline

| Phase | Function | What it does |
|---|---|---|
| 0 | Research | Supporting + counter evidence in parallel |
| 1 | Problem Restate | Each agent reformulates from their angle |
| 2 | Brainstorm | Director assigns focus + assignments, agents contribute, Secretary consolidates |
| 3 | Critique | Cross-examination, each agent rebuts another |
| 4 | Synthesis | Decision + minority report + open questions + next steps |
| 5 | Verdict | Votes 0-10 on feasibility / impact / risk_safety |

### Security built-ins

- **Prompt injection mitigation** via `sanitize_directive()` — removes/marks injection markers, truncates to 500 chars
- **PII redaction** — active only on `free_api_ok` tier; masks email, IP, phone, tax code
- **Circuit breaker** — `CircuitBreaker` class prevents cascade failures
- **Timeout** — 120s default per LLM call, 3 retries with exponential backoff

---

## Contributing

1. **Fork** the repository
2. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Run tests**

   ```bash
   python -m pytest tests/ -q
   # All 14 tests should pass
   ```

4. **Submit a pull request**

### Adding a new agent persona

Edit `agents.py` — personas follow the pattern:

```python
Persona(
    name="Your Persona",
    role="description",
    polarity_pair=(pro_position, con_position),
    archetype="archetype"
)
```

### Adding a new LLM provider

Edit `providers.py` — implement `LLMProvider` interface:

```python
class YourProvider(LLMProvider):
    def complete(self, model, prompt, **kwargs) -> str:
        ...
```

---

## License

**MIT License** — see `LICENSE` file for full terms.

---

_Generated for tavolarotonda — 2026-07-11_
