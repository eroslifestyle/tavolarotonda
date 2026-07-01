"""
TavolaRotonda GUI — Web App interattiva
=======================================
Flask + Server-Sent Events per streaming live del council.

Endpoints:
  GET  /              → SPA index.html
  GET  /api/models    → lista modelli LLM disponibili con stato (env / ollama)
  GET  /api/agents    → lista agenti disponibili
  POST /api/run       → avvia un dibattito (ritorna session_id)
  GET  /api/stream/<id> → SSE stream degli eventi live (PhaseEvent)
  GET  /api/report/<id> → scarica HTML audit/qa
  GET  /api/palace/<id> → scarica Memory Palace JSON
  GET  /api/health    → health check
"""
from __future__ import annotations
import sys
import json
import asyncio
import threading
import queue
import time
import uuid
import logging
import os
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# Path setup per importare il pacchetto
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from flask import Flask, Response, request, jsonify, send_from_directory, abort, stream_with_context

from tavolarotonda import (
    AGENTS,
    Agent,
    MemoryPalace,
    MockProvider,
    LLMProvider,
    run_full_council,
    audit_report_from_palace,
    render_qa_template,
)
from tavolarotonda.evidence import adversarial_research
from tavolarotonda.providers import CircuitBreaker, ProviderResult

import re
from tavolarotonda.providers import CircuitBreaker, ProviderResult

import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("tavolarotonda-gui")

# Lista di Agent da passare a run_full_council (AGENTS è un dict)
COUNCIL: list[Agent] = list(AGENTS.values())

# Event loop globale per SSE
_LOOP = asyncio.new_event_loop()
_THREAD = threading.Thread(target=_LOOP.run_forever, daemon=True)
_THREAD.start()

# Session storage: {session_id: {...}}
SESSIONS: dict[str, dict] = {}

# === MODEL CONFIGURATION ===
# Mappa dei modelli LLM selezionabili dalla GUI.
# Ogni modello: provider_kind, env_required, default_model, default_base_url, label, icon
MODELS: dict[str, dict] = {
    "mock": {
        "label": "Mock (no LLM reale)",
        "description": "Risposte stub per testare il wiring del council. Nessuna chiamata di rete.",
        "provider_kind": "mock",
        "env_required": [],
        "default_model": None,
        "default_base_url": None,
        "icon": "🧪",
    },
    "ollama-auto": {
        "label": "Ollama locale (auto)",
        "description": "Usa il primo modello Ollama disponibile. Richiede Ollama in esecuzione su :11434.",
        "provider_kind": "ollama",
        "env_required": [],
        "default_model": "auto",
        "default_base_url": None,
        "icon": "🏠",
    },
    "opus-local": {
        "label": "Opus locale (Qwen3.6 35B abliterated)",
        "description": "qwen3.6-opus-abliterated:35b via Ollama. Nessuna chiave richiesta.",
        "provider_kind": "ollama",
        "env_required": [],
        "default_model": "qwen3.6-opus-abliterated:35b",
        "default_base_url": None,
        "icon": "🏛️",
    },
    "ornith-35b": {
        "label": "Ornith 35B (qwen3.6 MoE, ctx 256k)",
        "description": "ornith-35b:latest via Ollama. MoE 34.7B Q4_K_M, context 262k. Nessuna chiave richiesta.",
        "provider_kind": "ollama",
        "env_required": [],
        "default_model": "ornith-35b:latest",
        "default_base_url": None,
        "icon": "🐦",
    },
    "opus-4.8": {
        "label": "Opus 4.8 (Anthropic)",
        "description": "Claude Opus 4.8 via Anthropic Messages API. Richiede ANTHROPIC_API_KEY.",
        "provider_kind": "claude",
        "env_required": ["ANTHROPIC_API_KEY"],
        "default_model": "claude-opus-4-8",
        "default_base_url": None,
        "icon": "🧠",
    },
    "MiniMax-M3": {
        "label": "MiniMax M3",
        "description": "MiniMax-M3 via OpenAI-compat API. Richiede MiniMax_API_KEY (+ opzionale MiniMax_BASE_URL).",
        "provider_kind": "openai_compat",
        "env_required": ["MiniMax_API_KEY"],
        "default_model": "MiniMax/MiniMax-M3",
        "default_base_url": os.environ.get("MiniMax_BASE_URL", "https://api.MiniMax.chat/v1"),
        "icon": "🌊",
    },
}


def _check_env(env_required: list[str]) -> list[str]:
    """Ritorna lista env var mancanti (vuota se tutte presenti)."""
    return [k for k in env_required if not os.environ.get(k)]


def _check_ollama(base_url: str = "http://127.0.0.1:11434") -> tuple[bool, list[str]]:
    """Verifica se Ollama è raggiungibile e ritorna lista modelli disponibili."""
    try:
        with urllib.request.urlopen(f"{base_url}/api/tags", timeout=2) as r:
            data = json.loads(r.read())
            models = [m["name"] for m in data.get("models", [])]
            return True, models
    except Exception:
        return False, []


# === COUNCIL MODES (multi-provider routing) ===
# Permette di fare una tavola rotonda TRA PIÙ PROVIDER (es. Opus + MiniMax + Ollama).
# Ogni preset definisce un routing dict[agent_key → provider_key].
COUNCIL_PRESETS: dict[str, dict] = {
    "monolithic": {
        "label": "Monolitico (1 LLM per tutti)",
        "description": "Tutti i 18 agenti usano il modello selezionato sopra. Nessun routing.",
        "icon": "🧊",
    },
    "triade": {
        "label": "Triade bilanciata (3 LLM)",
        "description": "Razionali/analitici → Opus · Creativi/dialogo → MiniMax · Pratici/tecnici → Ornith 35B",
        "icon": "🔱",
        "routing": {
            # Gruppo A → Opus 4.8 (ragionamento forte)
            "aristotle": "opus-4.8",
            "socrates": "opus-4.8",
            "feynman": "opus-4.8",
            "karpathy": "opus-4.8",
            "kahneman": "opus-4.8",
            "sutskever": "opus-4.8",
            # Gruppo B → MiniMax-M3 (creatività + dialogo)
            "sun_tzu": "MiniMax-M3",
            "ada": "MiniMax-M3",
            "aurelius": "MiniMax-M3",
            "machiavelli": "MiniMax-M3",
            "lao_tzu": "MiniMax-M3",
            "watts": "MiniMax-M3",
            # Gruppo C → Ornith 35B (pratico + veloce, ctx 256k)
            "torvalds": "ornith-35b",
            "musashi": "ornith-35b",
            "meadows": "ornith-35b",
            "munger": "ornith-35b",
            "taleb": "ornith-35b",
            "rams": "ornith-35b",
        },
    },
}
# Round-robin alternato: cicla A,B,C,A,B,C,...
_keys_all = list(AGENTS.keys())
_choices_alt = ["opus-4.8", "MiniMax-M3", "ornith-35b"]
COUNCIL_PRESETS["alternating"] = {
    "label": "Round-robin alternato",
    "description": "Cicla Opus → MiniMax → Ollama → Opus → ... sugli agenti in ordine",
    "icon": "🔄",
    "routing": {k: _choices_alt[i % 3] for i, k in enumerate(_keys_all)},
}


# Modello concreto da passare a `complete(model=...)` per ogni provider_key
_MODEL_FOR_PROVIDER = {
    "mock": "mock",
    "opus-4.8": "claude-opus-4-8",
    "MiniMax-M3": "MiniMax/MiniMax-M3",
    "ollama-auto": "auto",
    "opus-local": "qwen3.6-opus-abliterated:35b",
    "ornith-35b": "ornith-35b:latest",
}


def _extract_agent_key(system: str) -> str | None:
    """Estrae l'agent_key dal system_seed (es. 'Sei Aristotele. ...' → 'aristotele')."""
    if not system:
        return None
    m = re.match(r"Sei\s+([A-ZÀÈÌÒÙ][A-Za-zàèìòù\s]+?)\.", system)
    if not m:
        return None
    name = m.group(1).strip().lower()
    for key, agent in AGENTS.items():
        if agent.name.lower() == name:
            return key
    for key in AGENTS:
        if key.replace("_", " ").lower() == name:
            return key
    return None


class MultiProvider(LLMProvider):
    """Provider che instrada ogni chiamata al sub-provider giusto in base all'agent_key."""

    def __init__(self, providers: dict[str, LLMProvider], agent_routing: dict[str, str]):
        # Non chiamiamo super().__init__ per evitare di richiedere tutti i parametri
        # ma ereditiamo comunque da LLMProvider per compatibilità type-check.
        self.providers = providers
        self.agent_routing = agent_routing
        self.default_provider_name = next(iter(providers.keys()))
        self.default_provider = providers[self.default_provider_name]
        self.privacy_tier = "cloud_ok"
        self.breaker = CircuitBreaker()
        self.default_timeout_s = 180.0
        self.kind = "multi"
        self.call_log: list[dict] = []
        self.ollama_base_url = "http://127.0.0.1:11434"
        self.openai_base_url = None
        self.openai_api_key = None
        self.anthropic_api_key = None

    async def complete(self, prompt: str, *, model: str, system: str = "", **kwargs) -> ProviderResult:
        agent_key = _extract_agent_key(system)
        provider_name = self.default_provider_name
        if agent_key and agent_key in self.agent_routing:
            provider_name = self.agent_routing[agent_key]
        provider = self.providers.get(provider_name, self.default_provider)
        target_model = _MODEL_FOR_PROVIDER.get(provider_name, model)
        self.call_log.append({"agent": agent_key, "provider": provider_name, "model": target_model})
        return await provider.complete(prompt, model=target_model, system=system, **kwargs)


def _build_multi_provider(council_mode: str, fallback_model_key: str, privacy_tier: str = "cloud_ok") -> tuple:
    """Istanzia il provider giusto (singolo o MultiProvider) per il council mode scelto."""
    if council_mode == "monolithic":
        return _build_provider(fallback_model_key, privacy_tier)

    preset = COUNCIL_PRESETS.get(council_mode)
    if not preset or "routing" not in preset:
        return _build_provider(fallback_model_key, privacy_tier)

    routing = preset["routing"]
    needed = sorted(set(routing.values()))
    providers = {}
    statuses = {}
    for name in needed:
        prov, st = _build_provider(name, privacy_tier)
        providers[name] = prov
        statuses[name] = st

    multi = MultiProvider(providers, routing)
    counts = {}
    for ak, pn in routing.items():
        counts[pn] = counts.get(pn, 0) + 1
    fallback_count = sum(1 for st in statuses.values() if st["state"] == "fallback_mock")

    return multi, {
        "state": "ok" if fallback_count == 0 else "partial",
        "reason": (f"MultiProvider: {len(providers)} sub-provider, "
                   f"{len(routing)} agenti instradati · "
                   f"{', '.join(f'{k}={v}' for k,v in counts.items())}"),
        "model": f"multi[{','.join(needed)}]",
        "providers": statuses,
        "routing": routing,
        "counts": counts,
        "fallback_count": fallback_count,
    }


def _build_provider(choice: str, privacy_tier: str = "cloud_ok") -> tuple:
    """Istanzia il provider giusto per la scelta utente, con fallback automatico.

    Ritorna (provider, status_dict):
      - state: "ok" | "fallback_mock"
      - reason: descrizione leggibile del perchè
      - model: nome modello effettivamente usato (o "mock")
    """
    cfg = MODELS.get(choice, MODELS["mock"])
    kind = cfg["provider_kind"]

    if kind == "mock":
        return MockProvider(privacy_tier=privacy_tier), {
            "state": "ok",
            "reason": "mock attivo (nessuna chiamata di rete)",
            "model": "mock",
        }

    if kind == "ollama":
        base_url = cfg.get("default_base_url") or "http://127.0.0.1:11434"
        ok, models = _check_ollama(base_url)
        if not ok:
            return MockProvider(privacy_tier=privacy_tier), {
                "state": "fallback_mock",
                "reason": f"Ollama non raggiungibile su {base_url}",
                "model": "mock",
            }
        # Scegli il modello: "auto" = primo disponibile, altrimenti quello richiesto
        chosen = cfg["default_model"]
        if chosen == "auto":
            chosen = models[0] if models else None
        if chosen and chosen not in models:
            return MockProvider(privacy_tier=privacy_tier), {
                "state": "fallback_mock",
                "reason": f"'{chosen}' non in Ollama (disponibili: {', '.join(models[:3])}...)",
                "model": "mock",
            }
        provider = LLMProvider(
            ollama_base_url=base_url,
            privacy_tier=privacy_tier,
            default_timeout_s=180.0,
        )
        return provider, {"state": "ok", "reason": f"Ollama attivo ({len(models)} modelli)", "model": chosen}

    if kind == "claude":
        missing = _check_env(cfg["env_required"])
        if missing:
            return MockProvider(privacy_tier=privacy_tier), {
                "state": "fallback_mock",
                "reason": f"env mancanti: {', '.join(missing)}. Settare: export {missing[0]}=...",
                "model": "mock",
            }
        provider = LLMProvider(
            anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
            privacy_tier=privacy_tier,
            default_timeout_s=180.0,
        )
        return provider, {
            "state": "ok",
            "reason": f"Anthropic API key OK ({cfg['default_model']})",
            "model": cfg["default_model"],
        }

    if kind == "openai_compat":
        missing = _check_env(cfg["env_required"])
        if missing:
            return MockProvider(privacy_tier=privacy_tier), {
                "state": "fallback_mock",
                "reason": f"env mancanti: {', '.join(missing)}. Settare: export {missing[0]}=...",
                "model": "mock",
            }
        provider = LLMProvider(
            openai_base_url=cfg["default_base_url"],
            openai_api_key=os.environ[cfg["env_required"][0]],
            privacy_tier=privacy_tier,
            default_timeout_s=180.0,
        )
        return provider, {
            "state": "ok",
            "reason": f"{cfg['env_required'][0]} OK, endpoint={cfg['default_base_url']}",
            "model": cfg["default_model"],
        }

    return MockProvider(privacy_tier=privacy_tier), {"state": "fallback_mock", "reason": "kind sconosciuto", "model": "mock"}


# === FLASK APP ===
app = Flask(__name__, static_folder="static", template_folder="templates")


# === HTML SERVING ===

@app.route("/")
def index():
    # Cache-busting: passa il commit SHA breve come build_id al template
    build_id = _get_build_id()
    html = (ROOT / "gui" / "templates" / "index.html").read_text()
    html = html.replace("{{ build_id }}", build_id)
    return Response(html, mimetype="text/html",
                    headers={"Cache-Control": "no-store, must-revalidate"})


@app.route("/static/<path:p>")
def static_files(p):
    # Cache breve (1h) per static assets ma con ETag forte = build_id
    # → Chrome ri-valida ad ogni reload ma non re-downloada se non cambiato
    resp = send_from_directory(str(ROOT / "gui" / "static"), p)
    resp.headers["Cache-Control"] = "public, max-age=3600, must-revalidate"
    resp.headers["ETag"] = _get_build_id()
    return resp


def _get_build_id() -> str:
    """Ritorna git SHA breve (8 char) o fallback timestamp se non git repo."""
    try:
        out = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL, timeout=2,
        ).decode().strip()
        if out and len(out) >= 7:
            return out
    except Exception:
        pass
    # Fallback: mtime del file index.html (cambia ad ogni commit)
    try:
        idx = ROOT / "gui" / "templates" / "index.html"
        return f"m{int(idx.stat().st_mtime)}"
    except Exception:
        return "dev"


# === AUDIT HELPERS (raccolta ricorsiva progetto) ===

# Estensioni ammesse per audit di progetto (codice + documentazione + config)
AUDIT_INCLUDE_EXTS = {
    # Codice
    ".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs",
    ".go", ".rs", ".rb", ".php", ".java", ".kt", ".swift", ".c", ".cpp", ".h", ".hpp",
    ".sh", ".bash", ".zsh", ".fish", ".ps1",
    ".sql", ".r", ".scala", ".lua", ".pl", ".pm",
    # Documentazione
    ".md", ".markdown", ".rst", ".txt", ".adoc",
    # Config / dati
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".env", ".properties", ".xml",
    # Web / template
    ".html", ".htm", ".css", ".scss", ".less",
    ".vue", ".svelte", ".astro",
}

# Pattern di esclusione (directory + file) — case-insensitive
AUDIT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", "venv", ".venv", "env", ".env",
    "dist", "build", "out", "output", "target", ".next", ".nuxt", ".cache",
    "vendor", "third_party", "node_modules", "bower_components",
    "graphify-out", ".graphify-out",
    ".idea", ".vscode", ".claude", ".playwright-mcp",
    "coverage", ".coverage", "htmlcov", ".mypy_cache",
    "*.egg-info", ".eggs",
}

# Limiti default audit di progetto
AUDIT_MAX_FILES = 50
AUDIT_MAX_CHARS_PER_FILE = 4000
AUDIT_MAX_TOTAL_CHARS = 200_000  # ~200KB prima di troncare


def _is_auditable(path: Path) -> bool:
    """True se path è un file leggibile e la sua estensione è ammessa."""
    if not path.is_file() or not path.name:
        return False
    # Escludi dotfile (eccetto README, LICENSE, etc.)
    if path.name.startswith("."):
        if path.name.lower() in {".env", ".gitignore", ".dockerignore", ".editorconfig"}:
            return True
        return False
    return path.suffix.lower() in AUDIT_INCLUDE_EXTS


def _should_skip_dir(dirname: str) -> bool:
    """True se la directory deve essere saltata completamente."""
    return dirname.lower() in AUDIT_EXCLUDE_DIRS or dirname.startswith(".") and dirname not in {".github"}


def audit_collect_targets(
    root: Path,
    max_files: int = AUDIT_MAX_FILES,
    max_chars_per_file: int = AUDIT_MAX_CHARS_PER_FILE,
    max_total_chars: int = AUDIT_MAX_TOTAL_CHARS,
) -> list[tuple[str, str, int]]:
    """Raccoglie file da un progetto per audit.

    Ritorna lista di tuple (relpath, content_truncated, size_bytes).
    Applica filtri per estensione, esclude directory comuni (node_modules, .git, ecc.),
    rispetta limiti di sicurezza (max N file, max K chars/file, max M totali).
    """
    results = []
    total_chars = 0

    # Ordine deterministico: prima directory, poi file alfabeticamente
    try:
        all_paths = sorted(root.rglob("*"), key=lambda p: (str(p.parent), p.name))
    except (PermissionError, OSError) as e:
        print(f"[audit] rglob failed: {e}")
        return results

    for p in all_paths:
        if len(results) >= max_files:
            break
        # Salta parti di path che sono directory escluse
        if any(part.lower() in AUDIT_EXCLUDE_DIRS for part in p.relative_to(root).parts[:-1]):
            continue
        if not _is_auditable(p):
            continue
        try:
            content = p.read_text(errors="replace")
        except (UnicodeDecodeError, PermissionError, OSError):
            continue
        # Tronca per file se troppo lungo
        truncated = False
        if len(content) > max_chars_per_file:
            content = content[:max_chars_per_file] + f"\n\n... [truncated at {max_chars_per_file} chars, file totale più lungo]"
            truncated = True
        # Tronca totale se sforato
        if total_chars + len(content) > max_total_chars:
            remaining = max_total_chars - total_chars
            if remaining < 200:
                break
            content = content[:remaining] + f"\n\n... [truncated, audit budget esaurito]"
        total_chars += len(content)
        rel = str(p.relative_to(root))
        size = p.stat().st_size
        results.append((rel, content, size))

    return results


def audit_project_stats(files: list[tuple[str, str, int]]) -> dict:
    """Calcola statistiche di sintesi del progetto raccolto."""
    from collections import Counter
    exts = Counter()
    total_lines = 0
    total_chars = 0
    for rel, content, _size in files:
        ext = Path(rel).suffix.lower() or "(no ext)"
        exts[ext] += 1
        total_lines += content.count("\n") + 1
        total_chars += len(content)
    return {
        "n_files": len(files),
        "total_lines": total_lines,
        "total_chars": total_chars,
        "top_exts": exts.most_common(8),
    }


def audit_render_tree(root: Path, files: list[tuple[str, str, int]]) -> str:
    """Genera albero ASCII della struttura del progetto (solo file inclusi)."""
    paths = sorted(rel for rel, _, _ in files)
    # Costruisci dict nidificato
    tree = {}
    for rel in paths:
        parts = rel.split("/")
        cur = tree
        for part in parts[:-1]:
            cur = cur.setdefault(part, {})
        cur[parts[-1]] = None  # None = file foglia
    # Render ASCII
    lines = [f"{root.name}/"]

    def render(node, prefix=""):
        items = sorted(node.items(), key=lambda x: (x[1] is None, x[0]))  # dir prima, file dopo
        for i, (name, sub) in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            if sub is None:
                lines.append(f"{prefix}{connector}{name}")
            else:
                lines.append(f"{prefix}{connector}{name}/")
                extension = "    " if is_last else "│   "
                render(sub, prefix + extension)

    render(tree)
    return "\n".join(lines[:80])  # cap a 80 righe


def _ext_hint(rel: str) -> str:
    """Hint di linguaggio per code fence (per syntax highlight in output)."""
    ext = Path(rel).suffix.lower()
    return {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".md": "markdown", ".json": "json", ".yaml": "yaml", ".yml": "yaml",
        ".html": "html", ".css": "css", ".sh": "bash", ".sql": "sql",
        ".go": "go", ".rs": "rust", ".rb": "ruby",
    }.get(ext, "")


# === API ===

@app.route("/api/agents", methods=["GET"])
def api_agents():
    """Lista i 18 agenti disponibili con metadati."""
    agents = []
    for a in AGENTS.values():
        agents.append({
            "key": a.key,
            "name": a.name,
            "figure": getattr(a, "figure", ""),
            "domain": a.domain,
            "polarity": getattr(a, "polarity", ""),
            "role_tag": getattr(a, "role_tag", ""),
            "model_tier": getattr(a, "model_tier", ""),
        })
    return jsonify({"agents": agents, "count": len(agents)})


@app.route("/api/council-presets", methods=["GET"])
def api_council_presets():
    """Lista i preset di modalità council (monolitico / triade / alternating)."""
    out = []
    for key, cfg in COUNCIL_PRESETS.items():
        info = {
            "key": key,
            "label": cfg["label"],
            "description": cfg["description"],
            "icon": cfg.get("icon", "🎭"),
        }
        if "routing" in cfg:
            info["routing"] = cfg["routing"]
            counts = {}
            for ak, pn in cfg["routing"].items():
                counts[pn] = counts.get(pn, 0) + 1
            info["counts"] = counts
        out.append(info)
    return jsonify({"presets": out, "count": len(out)})


@app.route("/api/models", methods=["GET"])
def api_models():
    """Lista i modelli LLM disponibili con stato corrente (env / ollama)."""
    out = []
    for key, cfg in MODELS.items():
        status = {"state": "unknown", "reason": "?", "model": cfg.get("default_model")}
        if cfg["provider_kind"] == "mock":
            status = {"state": "ok", "reason": "sempre disponibile", "model": "mock"}
        elif cfg["provider_kind"] == "ollama":
            ok, models = _check_ollama()
            if not ok:
                status = {"state": "unreachable",
                          "reason": "Ollama non raggiungibile su :11434",
                          "model": "mock"}
            else:
                chosen = cfg["default_model"]
                if chosen == "auto":
                    chosen = models[0] if models else None
                if chosen and chosen not in models:
                    status = {"state": "unavailable",
                              "reason": f"'{chosen}' non installato",
                              "model": "mock"}
                else:
                    status = {"state": "ok",
                              "reason": f"Ollama attivo ({len(models)} modelli)",
                              "model": chosen}
        elif cfg["provider_kind"] == "claude":
            missing = _check_env(cfg["env_required"])
            if missing:
                status = {"state": "missing_env",
                          "reason": f"export {missing[0]}=...",
                          "model": "mock"}
            else:
                status = {"state": "ok",
                          "reason": "Anthropic API key OK",
                          "model": cfg["default_model"]}
        elif cfg["provider_kind"] == "openai_compat":
            missing = _check_env(cfg["env_required"])
            if missing:
                status = {"state": "missing_env",
                          "reason": f"export {missing[0]}=...",
                          "model": "mock"}
            else:
                status = {"state": "ok",
                          "reason": f"endpoint {cfg['default_base_url']}",
                          "model": cfg["default_model"]}
        out.append({
            "key": key,
            "label": cfg["label"],
            "description": cfg["description"],
            "icon": cfg.get("icon", "🤖"),
            "provider_kind": cfg["provider_kind"],
            "env_required": cfg["env_required"],
            **status,
        })
    return jsonify({"models": out, "count": len(out)})


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "sessions": len(SESSIONS),
        "uptime": int(time.time()),
        "models_available": len(MODELS),
        "ollama_reachable": _check_ollama()[0],
    })


@app.route("/api/run", methods=["POST"])
def api_run():
    """Avvia un dibattito. Ritorna session_id per lo stream SSE."""
    body = request.get_json(force=True) or {}
    mode = body.get("mode", "topic")
    topic = body.get("topic", "").strip()
    audit_target = body.get("audit_target", "").strip()
    qa_questions = body.get("qa_questions", [])
    rounds = max(1, min(10, int(body.get("rounds", 3))))
    model_choice = body.get("model", "mock")
    council_mode = body.get("council_mode", "monolithic")
    privacy = body.get("privacy", "cloud_ok")
    research = bool(body.get("research", False))

    if mode == "topic" and not topic:
        return jsonify({"error": "topic richiesto"}), 400
    if mode == "audit" and not audit_target:
        return jsonify({"error": "audit_target richiesto"}), 400
    if mode == "qa" and not qa_questions:
        return jsonify({"error": "qa_questions richieste"}), 400
    if council_mode not in COUNCIL_PRESETS:
        return jsonify({"error": f"council_mode '{council_mode}' non valido"}), 400

    sid = uuid.uuid4().hex[:12]
    SESSIONS[sid] = {
        "events_queue": queue.Queue(maxsize=2000),
        "status": "queued",
        "started_at": time.time(),
        "config": body,
        "result": None,
        "html_path": None,
        "palace_path": None,
    }

    def _worker():
        try:
            SESSIONS[sid]["status"] = "running"
            coro = _run_session(sid, mode, topic, audit_target, qa_questions,
                                rounds, model_choice, council_mode, privacy, research)
            future = asyncio.run_coroutine_threadsafe(coro, _LOOP)
            future.result(timeout=1800)  # 30 min max
            SESSIONS[sid]["status"] = "done"
        except Exception as e:
            log.exception("session %s failed", sid)
            SESSIONS[sid]["status"] = "error"
            SESSIONS[sid]["result"] = {"error": str(e)}
            try:
                SESSIONS[sid]["events_queue"].put_nowait({
                    "type": "error", "msg": str(e), "ts": time.time(),
                })
            except queue.Full:
                pass

    threading.Thread(target=_worker, daemon=True).start()
    return jsonify({"session_id": sid, "status": "queued"})


async def _emit_event(q):
    """Factory per callback on_event che mette eventi in queue."""
    async def _cb(ev):
        try:
            q.put_nowait({
                "type": ev.phase,
                "phase": ev.phase,
                "agent": ev.agent,
                "text": ev.text,
                "round": ev.round,
                "meta": ev.meta or {},
                "ts": time.time(),
            })
        except queue.Full:
            log.warning("queue full, dropping event")
    return _cb


async def _run_session(sid, mode, topic, audit_target, qa_questions,
                       rounds, model_choice, council_mode, privacy, research):
    """Coroutine principale: esegue il council e salva gli output."""
    sess = SESSIONS[sid]
    q = sess["events_queue"]

    def push(d):
        d.setdefault("ts", time.time())
        try:
            q.put_nowait(d)
        except queue.Full:
            pass

    # Provider (singolo o MultiProvider in base a council_mode)
    provider, pstatus = _build_multi_provider(council_mode, model_choice, privacy)
    push({"type": "info",
          "msg": f"🚀 Avvio council (mode={mode}, council_mode={council_mode}, "
                 f"rounds={rounds}, model={model_choice}, privacy={privacy}, research={research})"})
    push({"type": "info",
          "msg": f"🧠 Provider: {pstatus['state']} | model={pstatus['model']} | {pstatus['reason']}"})
    if pstatus["state"] == "fallback_mock":
        push({"type": "warn",
              "msg": f"⚠️ Fallback a Mock: {pstatus['reason']}"})
    # Se MultiProvider, logga il routing e stato dei sub-provider
    if council_mode != "monolithic" and "providers" in pstatus:
        push({"type": "info",
              "msg": f"🎭 Council mode: {council_mode} → routing {len(pstatus['routing'])} agenti su {len(pstatus['providers'])} sub-provider"})
        for pname, pst in pstatus["providers"].items():
            icon = "✅" if pst["state"] == "ok" else "⚠️ "
            push({"type": "info",
                  "msg": f"   {icon} {pname}: {pst['state']} | model={pst['model']} | {pst['reason'][:80]}"})

    # Topic effettivo per audit/qa
    if mode == "audit":
        target_path = Path(audit_target)
        if not target_path.exists():
            alt = ROOT / audit_target
            if alt.exists():
                target_path = alt
            else:
                raise FileNotFoundError(f"path non trovato: {audit_target}")

        # Modalità progetto: path è una directory → raccolta ricorsiva
        if target_path.is_dir():
            project_files = audit_collect_targets(target_path, max_files=50, max_chars_per_file=4000)
            if not project_files:
                raise ValueError(f"nessun file leggibile trovato in {target_path}")
            stats = audit_project_stats(project_files)
            tree = audit_render_tree(target_path, project_files)
            file_blocks = "\n\n".join(
                f"### {rel}\n```{_ext_hint(rel)}\n{content}\n```"
                for rel, content, _size in project_files
            )
            topic_actual = (
                f"AUDIT del PROGETTO {target_path.name} "
                f"({len(project_files)} file, {stats['total_lines']} righe totali, "
                f"{stats['total_chars']:,} chars).\n\n"
                f"Estensioni top: {', '.join(f'{e}({n})' for e, n in stats['top_exts'])}.\n\n"
                f"## Struttura ad albero\n```\n{tree}\n```\n\n"
                f"## File inclusi nel contesto\n{file_blocks}\n\n"
                f"Devi produrre un audit dettagliato con sezioni: Pro/Contro, Criticità, "
                f"Punti di forza, Consigli, Open Questions, Minority Report. "
                f"Considera l'architettura, le dipendenze, la qualità del codice, "
                f"la sicurezza, le performance, la manutenibilità."
            )
            target_name = f"📁 {target_path.name} ({len(project_files)} file)"
            target_description = f"Audit progetto {target_path} ({stats['total_lines']} righe, {len(project_files)} file)"
        else:
            # Singolo file (legacy)
            code = target_path.read_text(errors="replace")[:8000]
            topic_actual = (
                f"AUDIT del file {target_path.name}.\n\n"
                f"Devi produrre un audit dettagliato con sezioni: Pro/Contro, Criticità, "
                f"Punti di forza, Consigli, Open Questions, Minority Report.\n\n"
                f"```\n{code}\n```"
            )
            target_name = target_path.name
            target_description = f"Audit del file {target_path} ({len(code)} chars)"
    elif mode == "qa":
        topic_actual = "Q&A multi-domanda:\n" + "\n".join(f"- {qq}" for qq in qa_questions)
        target_name = f"Q&A {len(qa_questions)} domande"
        target_description = "; ".join(qa_questions[:3])
    else:
        topic_actual = topic
        target_name = topic[:80]
        target_description = topic

    # Crea Memory Palace
    palace = MemoryPalace(topic=topic_actual)

    # Esegui council (Director + Secretary creati internamente)
    on_event = await _emit_event(q)

    # Web research opzionale (solo se non mock)
    if research and not isinstance(provider, MockProvider):
        push({"type": "info", "msg": "🔍 Ricerca web avversariale in corso..."})
        try:
            supporting, counter = await adversarial_research(topic_actual, max_per_side=3)
            push({"type": "research",
                  "supporting": [{"title": r.title, "url": r.url, "snippet": r.snippet}
                                 for r in supporting],
                  "counter": [{"title": r.title, "url": r.url, "snippet": r.snippet}
                              for r in counter]})
        except Exception as e:
            push({"type": "warn", "msg": f"ricerca fallita: {e}"})

    events = await run_full_council(
        palace=palace,
        agents=COUNCIL,
        provider=provider,
        rounds=rounds,
        include_research=research and not isinstance(provider, MockProvider),
        include_critique=True,
        include_verdict=True,
        on_event=on_event,
    )

    push({"type": "info", "msg": f"✅ Council completato: {len(events)} eventi emessi"})

    # Salva Memory Palace
    palace_path = ROOT / "output" / f"palace_{sid}.json"
    palace_path.parent.mkdir(exist_ok=True, parents=True)
    palace.save(str(palace_path))
    sess["palace_path"] = palace_path
    push({"type": "info",
          "msg": f"💾 Palace salvato: {palace_path.name} ({palace_path.stat().st_size} bytes)"})

    # Genera HTML finale
    if mode == "audit":
        html = audit_report_from_palace(
            palace=palace,
            target_name=target_name,
            target_description=target_description,
        )
        html_path = ROOT / "output" / f"audit_{sid}.html"
    elif mode == "qa":
        html = render_qa_template(
            title=f"Q&A — {len(qa_questions)} domande, {len(COUNCIL)} agenti",
            questions=qa_questions,
        )
        html_path = ROOT / "output" / f"qa_{sid}.html"
    else:
        html = audit_report_from_palace(
            palace=palace,
            target_name=f"Discussione: {topic[:60]}",
            target_description=topic_actual,
        )
        html_path = ROOT / "output" / f"discussion_{sid}.html"

    html_path.write_text(html)
    sess["html_path"] = html_path
    sess["result"] = {"palace_path": str(palace_path), "html_path": str(html_path)}
    push({"type": "info",
          "msg": f"📄 Report HTML salvato: {html_path.name} ({len(html)} chars)"})
    push({"type": "done",
          "html_url": f"/api/report/{sid}",
          "palace_url": f"/api/palace/{sid}",
          "model_used": pstatus["model"]})

    return palace_path, html_path


@app.route("/api/stream/<sid>")
def api_stream(sid):
    """Server-Sent Events stream per la sessione."""
    if sid not in SESSIONS:
        abort(404)
    sess = SESSIONS[sid]

    @stream_with_context
    def gen():
        yield f"data: {json.dumps({'type': 'connected', 'sid': sid})}\n\n"
        last_keepalive = time.time()
        closed = False
        while not closed:
            status = sess["status"]
            if status in ("done", "error"):
                # Drena queue residua
                drained = 0
                while True:
                    try:
                        ev = sess["events_queue"].get(timeout=0.2)
                        yield f"data: {json.dumps(ev, default=str)}\n\n"
                        drained += 1
                        if drained > 200:
                            break
                    except queue.Empty:
                        break
                yield f"data: {json.dumps({'type': 'closed', 'status': status})}\n\n"
                closed = True
                break
            try:
                ev = sess["events_queue"].get(timeout=1.0)
                yield f"data: {json.dumps(ev, default=str)}\n\n"
            except queue.Empty:
                if time.time() - last_keepalive > 15:
                    yield ": keepalive\n\n"
                    last_keepalive = time.time()

    return Response(gen(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache",
                             "X-Accel-Buffering": "no",
                             "Connection": "keep-alive"})


@app.route("/api/report/<sid>")
def api_report(sid):
    if sid not in SESSIONS or not SESSIONS[sid]["html_path"]:
        abort(404)
    path = Path(SESSIONS[sid]["html_path"])
    return send_from_directory(path.parent, path.name)


@app.route("/api/palace/<sid>")
def api_palace(sid):
    if sid not in SESSIONS or not SESSIONS[sid]["palace_path"]:
        abort(404)
    path = Path(SESSIONS[sid]["palace_path"])
    return send_from_directory(path.parent, path.name)


@app.route("/api/sessions")
def api_sessions():
    """Debug: lista sessioni attive."""
    return jsonify({
        sid: {
            "status": s["status"],
            "started_at": s["started_at"],
            "duration": int(time.time() - s["started_at"]),
            "has_html": bool(s["html_path"]),
            "has_palace": bool(s["palace_path"]),
            "config": s["config"],
        }
        for sid, s in SESSIONS.items()
    })


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8912)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    print(f"🥽 TavolaRotonda GUI → http://{args.host}:{args.port}/")
    print(f"   Agenti: {len(COUNCIL)}")
    print(f"   Modelli LLM: {len(MODELS)}")
    print(f"   Output: {ROOT}/output/")
    print()
    print("📋 Modelli configurati:")
    for k, v in MODELS.items():
        env_ok = "✓" if not _check_env(v["env_required"]) else f"richiede {v['env_required']}"
        print(f"   {v.get('icon','🤖')} {k:15s} {v['label']:42s} [{env_ok}]")
    app.run(host=args.host, port=args.port, debug=False, threaded=True, use_reloader=False)
