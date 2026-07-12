"""Multi-model debate phase — AQ Session 3/10.

3 modelli (Opus, GLM, MiniMax) rispondono a turno allo stesso topic,
reagendo alle risposte precedenti.
"""
from __future__ import annotations

import os
from tavolarotonda.providers import AnthropicCompatProvider, LLMProvider, MockProvider
from tavolarotonda.memory_palace import MemoryPalace
from tavolarotonda.phases import PhaseEvent


def _make_provider(key: str) -> LLMProvider | MockProvider:
    """Crea un provider per un provider_key dal config."""
    import yaml
    path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(path) as f:
        cfg = yaml.safe_load(f)
    models = cfg.get("models", {})
    m = models.get(key, {})
    kind = m.get("provider_kind", "mock")
    env_req = m.get("env_required", [])
    missing = [e for e in env_req if not os.environ.get(e)]
    if missing:
        return MockProvider(privacy_tier="cloud_ok")
    base_url = m.get("default_base_url", "http://127.0.0.1:8787")
    api_key = os.environ.get(env_req[0], "mock") if env_req else "mock"
    if kind == "anthropic_compat":
        return AnthropicCompatProvider(base_url=base_url, api_key=api_key,
                                      privacy_tier="cloud_ok", default_timeout_s=120)
    return MockProvider(privacy_tier="cloud_ok")


# I 3 modelli del debate
_DEBATE_MODELS = [
    ("Opus", "opus-4.8", "🧠"),
    ("GLM", "glm-5.2", "🔮"),
    ("MiniMax", "MiniMax-M3", "🌊"),
]


async def phase_debate(
    palace: MemoryPalace,
    topic: str,
    rounds: int = 3,
    on_event=None,
) -> list[PhaseEvent]:
    """Esegue un debate tra 3 modelli cloud.

    Ogni round: ogni modello risponde al topic + risposte precedenti.
    """
    events: list[PhaseEvent] = []
    history: list[str] = []

    # Crea i 3 provider
    providers: dict[str, LLMProvider] = {}
    for name, key, icon in _DEBATE_MODELS:
        prov = _make_provider(key)
        providers[name] = prov
        # testa che non sia mock
        if isinstance(prov, MockProvider):
            print(f"  ⚠️  {name}: mock (env mancanti)")

    for round_num in range(1, rounds + 1):
        for model_name, _, icon in _DEBATE_MODELS:
            # Costruisci il prompt con history
            prompt = topic
            if history:
                prompt += "\n\n--- Risposte precedenti ---\n"
                prompt += "\n".join(history[-6:])  # max 6 entries in context

            provider = providers.get(model_name, MockProvider(privacy_tier="cloud_ok"))
            model_key = next((k for n, k, i in _DEBATE_MODELS if n == model_name), "mock")

            system = (
                f"Sei {model_name} nel debate della Tavola Rotonda AI. "
                f"Rispondi in modo conciso, argomentato, nel tuo stile tipico. "
                f"Massimo 200 parole. Rispondi in italiano."
            )

            try:
                result = await provider.complete(prompt, model=model_key, system=system)
                response = result.text.strip()
            except Exception as e:
                response = f"[Errore: {e}]"

            # Salva in history
            history.append(f"{icon} {model_name} (round {round_num}): {response}")

            # Salva in palace come brainstorm speciale
            palace.add_brainstorm(
                agent=f"debate-{model_name}",
                text=response,
                round=round_num,
                model=model_name,
            )

            ev = PhaseEvent(
                phase="debate",
                agent=f"debate-{model_name}",
                text=response,
                round=round_num,
            )
            events.append(ev)
            if on_event:
                await on_event(ev)
            print(f"  [debate r{round_num}] {model_name}: {response[:80]}...")

    # Aggiungi synthesis del debate
    synthesis = f"## Debate tra 3 modelli ({rounds} round)\n\n" + "\n\n".join(history)
    palace.set_synthesis("debate", synthesis)

    return events
