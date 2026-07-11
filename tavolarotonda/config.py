"""Configuration loader for Tavola Rotonda."""

import json
import warnings
from pathlib import Path

import yaml  # pip install pyyaml

_CONFIG: dict | None = None


def _load_config() -> dict:
    """Load and cache config.yaml."""
    global _CONFIG
    if _CONFIG is None:
        path = Path(__file__).parent / "config.yaml"
        try:
            with open(path, encoding="utf-8") as f:
                _CONFIG = yaml.safe_load(f)
        except FileNotFoundError:
            warnings.warn(f"config.yaml not found at {path}, using empty config")
            _CONFIG = {}
        except yaml.YAMLError as e:
            warnings.warn(f"Failed to parse config.yaml: {e}, using empty config")
            _CONFIG = {}
    return _CONFIG


def load() -> dict:
    """Return the full configuration dict."""
    return _load_config()


def get_model(key: str) -> dict | None:
    """Return model config by key, or None if not found."""
    cfg = _load_config()
    return cfg.get("models", {}).get(key)


def get_preset(key: str) -> dict | None:
    """Return council preset by key, or None if not found."""
    cfg = _load_config()
    return cfg.get("council_presets", {}).get(key)


def get_agent_color(key: str) -> str:
    """Return hex color for agent, or default blue."""
    cfg = _load_config()
    return cfg.get("agent_colors", {}).get(key, "#58a6ff")


def get_timeout() -> float:
    """Return default timeout in seconds."""
    cfg = _load_config()
    return float(cfg.get("timeout", {}).get("default_timeout_s", 180))


if __name__ == "__main__":
    print(json.dumps(load(), indent=2))
