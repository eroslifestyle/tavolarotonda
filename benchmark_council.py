#!/usr/bin/env python3
"""Benchmark council presets — Tavola Rotonda AQ Session 1/10."""
import argparse, asyncio, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from tavolarotonda.config import load as load_config, get_preset
from tavolarotonda.providers import AnthropicCompatProvider, MockProvider, LLMProvider
from gui.app import MultiProvider
from tavolarotonda.agents import AGENTS
from tavolarotonda.memory_palace import MemoryPalace
from tavolarotonda.phases import run_full_council

def _check_env(names):
    return [n for n in names if not os.environ.get(n)]

def _build_provider_for(key, timeout_s=120):
    cfg = load_config()["models"].get(key, {})
    kind = cfg.get("provider_kind", "mock")
    missing = _check_env(cfg.get("env_required", []))
    if missing:
        return None, key
    if kind == "mock":
        return MockProvider(privacy_tier="cloud_ok"), key
    elif kind == "ollama":
        base = cfg.get("default_base_url") or "http://127.0.0.1:11434"
        return LLMProvider(ollama_base_url=base, privacy_tier="cloud_ok", default_timeout_s=timeout_s), key
    elif kind == "anthropic_compat":
        return AnthropicCompatProvider(
            base_url=cfg.get("default_base_url", "http://127.0.0.1:8787"),
            api_key=os.environ.get(cfg["env_required"][0], "mock"),
            privacy_tier="cloud_ok", default_timeout_s=timeout_s,
        ), key
    return None, key

def load_preset(preset_key):
    cfg = get_preset(preset_key)
    if not cfg or not cfg.get("routing"):
        return None, None
    routing = cfg["routing"]
    providers = {}
    for pk in set(routing.values()):
        prov, _ = _build_provider_for(pk)
        if prov:
            providers[pk] = prov
    agents = [AGENTS[k] for k in routing if k in AGENTS]
    if not providers or not agents:
        return None, None
    return agents, MultiProvider(providers, routing)

async def run_benchmark(topic, preset_key, rounds=2):
    result = load_preset(preset_key)
    if not result or not result[0]:
        print(f"ERR: preset '{preset_key}' not available")
        return None
    agents, provider = result
    print(f"BENCHMARK | preset={preset_key} | agents={len(agents)} | rounds={rounds}")
    print(f"Topic: {topic}")
    palace = MemoryPalace(topic=topic)
    t0 = time.time()
    await run_full_council(palace, agents, provider, rounds=rounds,
                          intensity="standard", include_critique=True, include_verdict=True)
    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s | brainstorm={len(palace.brainstorm)} | critique={len(palace.critique)}")
    return palace, elapsed

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--preset", default="triade", choices=["triade", "trilogy", "alternating"])
    p.add_argument("--topic", "-t", default="È giusto usare AI per scrivere codice che poi vendi come tuo lavoro?")
    p.add_argument("--rounds", type=int, default=2)
    args = p.parse_args()
    asyncio.run(run_benchmark(args.topic, args.preset, args.rounds))

if __name__ == "__main__":
    main()
