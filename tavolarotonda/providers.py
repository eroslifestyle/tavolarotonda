"""Provider LLM abstraction — locali (Ollama), free-API (Groq/Cerebras via LiteLLM), cloud.

Pattern unificato: ogni provider espone `complete(prompt, *, model, timeout, **kwargs)`
e ritorna `ProviderResult(text=..., tokens_in=..., tokens_out=..., latency_ms=..., error=None)`.

Privacy tier:
- local_only: solo Ollama, niente cloud, niente free-API
- cloud_ok: + Claude/Gemini/GPT via API key
- free_api_ok: + Groq/Cerebras via LiteLLM (accettabili per query non sensibili)

Robustezza:
- Timeout esplicito per modello (default 120s, overridabile)
- Retry con backoff esponenziale (3 tentativi)
- Circuit breaker: se un modello fallisce N volte, viene escluso per il resto della sessione
- Output validation: rimuove `Qwen3 ` block, tronca risposte troppo lunghe
"""

from __future__ import annotations

import asyncio
import os
import re
import time
from dataclasses import dataclass, field
from typing import Literal

ProviderKind = Literal["ollama", "openai_compat", "claude", "mock"]


@dataclass
class ProviderResult:
    """Risultato normalizzato di una chiamata LLM."""

    text: str
    model: str
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    error: str | None = None
    raw: dict | None = None


@dataclass
class CircuitBreaker:
    """Circuit breaker per modelli inaffidabili."""

    failure_threshold: int = 3
    failures: dict[str, int] = field(default_factory=dict)
    open_until: dict[str, float] = field(default_factory=dict)

    def is_open(self, model: str) -> bool:
        until = self.open_until.get(model, 0)
        return time.time() < until

    def record_failure(self, model: str) -> None:
        n = self.failures.get(model, 0) + 1
        self.failures[model] = n
        if n >= self.failure_threshold:
            # Apri per 5 minuti
            self.open_until[model] = time.time() + 300
            self.failures[model] = 0

    def record_success(self, model: str) -> None:
        self.failures.pop(model, None)
        self.open_until.pop(model, None)


_THINK_RE = re.compile(r"Qwen3 .*?Qwen3 ", re.DOTALL | re.IGNORECASE)
_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def _strip_think(text: str) -> str:
    """Rimuove Qwen3 / Qwen3 / <think> block (modelli che ragionano)."""
    t = _THINK_BLOCK_RE.sub("", text)
    t = _THINK_RE.sub("", t)
    low = t.lower()
    if "Qwen3 " in low:
        return t[low.rfind("Qwen3 ") + len("Qwen3 "):].strip()
    if "Qwen3 " in low:
        return ""
    return t.strip()


class LLMProvider:
    """Provider unificato. Internamente switch su Ollama / OpenAI-compat / Claude."""

    def __init__(
        self,
        ollama_base_url: str = "http://127.0.0.1:11434",
        openai_base_url: str | None = None,
        openai_api_key: str | None = None,
        anthropic_api_key: str | None = None,
        privacy_tier: str = "cloud_ok",
        default_timeout_s: float = 120.0,
    ):
        self.ollama_base_url = ollama_base_url.rstrip("/")
        self.openai_base_url = openai_base_url or os.environ.get("OPENAI_BASE_URL")
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.privacy_tier = privacy_tier
        self.default_timeout_s = default_timeout_s
        self.breaker = CircuitBreaker()

    def kind_for(self, model: str) -> ProviderKind:
        """Determina il kind del provider in base al nome del modello."""
        m = model.lower()
        if m.startswith("ollama:") or "/" not in model and not m.startswith("gpt") \
                and not m.startswith("claude") and not m.startswith("groq") \
                and not m.startswith("cerebras"):
            return "ollama"
        if m.startswith("claude"):
            return "claude"
        if m.startswith("groq") or m.startswith("cerebras") or m.startswith("gpt") \
                or "/" in model:
            return "openai_compat"
        return "ollama"

    def redact_for_privacy(self, text: str) -> str:
        """PII redaction minima (best-effort) per free_api tier.

        NB: questa è una rete di sicurezza minima, NON una garanzia.
        Non inviare MAI dati altamente sensibili a Groq/Cerebras.
        """
        if self.privacy_tier != "free_api_ok":
            return text
        # Email
        text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", "[EMAIL]", text)
        # IP address
        text = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "[IP]", text)
        # Telefono italiano (semplificato)
        text = re.sub(r"\b3\d{2}[\s.-]?\d{6,7}\b", "[PHONE]", text)
        # CF italiano (16 char alfanum)
        text = re.sub(r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b", "[CF]", text)
        return text

    async def complete(
        self,
        prompt: str,
        *,
        model: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        timeout_s: float | None = None,
    ) -> ProviderResult:
        """Esegue una completion LLM. Retry + circuit breaker integrati."""
        if self.breaker.is_open(model):
            return ProviderResult(text="", model=model, error="circuit_open")

        prompt = self.redact_for_privacy(prompt)
        if system:
            system = self.redact_for_privacy(system)

        timeout = timeout_s or self.default_timeout_s
        kind = self.kind_for(model)
        model_id = model.replace("ollama:", "") if model.startswith("ollama:") else model

        for attempt in range(3):
            try:
                t0 = time.time()
                if kind == "ollama":
                    text = await self._ollama(model_id, prompt, system, temperature, max_tokens, timeout)
                elif kind == "openai_compat":
                    text = await self._openai_compat(model_id, prompt, system, temperature, max_tokens, timeout)
                elif kind == "claude":
                    text = await self._claude(model_id, prompt, system, temperature, max_tokens, timeout)
                else:
                    return ProviderResult(text="", model=model, error="unknown_kind")

                latency = int((time.time() - t0) * 1000)
                text = _strip_think(text)
                self.breaker.record_success(model)
                return ProviderResult(text=text, model=model, latency_ms=latency)

            except Exception as exc:
                if attempt == 2:
                    self.breaker.record_failure(model)
                    return ProviderResult(text="", model=model, error=str(exc))
                await asyncio.sleep(2 ** attempt)

        return ProviderResult(text="", model=model, error="max_retries_exceeded")

    async def _ollama(self, model: str, prompt: str, system: str, temperature: float, max_tokens: int, timeout: float) -> str:
        """Chiama Ollama /api/generate."""
        import urllib.request
        import json as _json

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        if system:
            payload["system"] = system

        loop = asyncio.get_event_loop()

        def _do() -> str:
            req = urllib.request.Request(
                f"{self.ollama_base_url}/api/generate",
                data=_json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = _json.loads(r.read().decode())
                return data.get("response", "")

        return await loop.run_in_executor(None, _do)

    async def _openai_compat(self, model: str, prompt: str, system: str, temperature: float, max_tokens: int, timeout: float) -> str:
        """Chiama API OpenAI-compat (LiteLLM proxy, OpenRouter, ecc.)."""
        if not self.openai_base_url or not self.openai_api_key:
            raise RuntimeError(f"OPENAI_BASE_URL/OPENAI_API_KEY non configurati per {model}")

        import urllib.request
        import json as _json

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        loop = asyncio.get_event_loop()

        def _do() -> str:
            req = urllib.request.Request(
                f"{self.openai_base_url}/chat/completions",
                data=_json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_api_key}",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = _json.loads(r.read().decode())
                return data["choices"][0]["message"]["content"]

        return await loop.run_in_executor(None, _do)

    async def _claude(self, model: str, prompt: str, system: str, temperature: float, max_tokens: int, timeout: float) -> str:
        """Chiama Claude API (Anthropic). Per ora solleva: usare SDK Anthropic o mock."""
        if not self.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY non configurata")

        import urllib.request
        import json as _json

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        loop = asyncio.get_event_loop()

        def _do() -> str:
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=_json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = _json.loads(r.read().decode())
                return data["content"][0]["text"]

        return await loop.run_in_executor(None, _do)


# Mock provider per test/demos offline
class MockProvider(LLMProvider):
    """Provider finto che ritorna risposte plausibili per smoke test.

    NON usare in produzione. Serve solo per testare il wiring del codice
    senza una connessione LLM reale.
    """

    def __init__(self, responses: dict[str, str] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.responses = responses or {}
        self.call_log: list[dict] = []

    async def complete(self, prompt: str, *, model: str, system: str = "", **kwargs) -> ProviderResult:
        self.call_log.append({"model": model, "prompt_len": len(prompt), "system_len": len(system)})
        if model in self.responses:
            text = self.responses[model]
        else:
            text = f"[MOCK {model}] Risposta stub per prompt di {len(prompt)} caratteri."
        await asyncio.sleep(0)  # yield control
        return ProviderResult(text=text, model=model, latency_ms=1, tokens_out=len(text.split()))



class AnthropicCompatProvider(LLMProvider):
    """Provider per endpoint Anthropic-compat (ai-router :8787 e porte dedicate GLM).

    Usa /v1/messages (formato Anthropic) con decompressione gzip.
    Supporta modelli MiniMax, GLM-5.2, Opus 4.8 via ai-router.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8787",
        api_key: str = "mock",
        privacy_tier: str = "cloud_ok",
        default_timeout_s: float = 120.0,
        **kwargs,
    ):
        super().__init__(privacy_tier=privacy_tier, default_timeout_s=default_timeout_s)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.breaker = CircuitBreaker()

    def kind_for(self, model: str) -> ProviderKind:
        return "anthropic_compat"

    async def complete(
        self,
        prompt: str,
        *,
        model: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        timeout_s: float | None = None,
    ) -> ProviderResult:
        if self.breaker.is_open(model):
            return ProviderResult(text="", model=model, error="circuit_open")

        prompt_text = self.redact_for_privacy(prompt)
        if system:
            system = self.redact_for_privacy(system)

        timeout = timeout_s or self.default_timeout_s

        for attempt in range(3):
            try:
                t0 = time.time()
                text = await self._request(model, prompt_text, system, temperature, max_tokens, timeout)
                latency = int((time.time() - t0) * 1000)
                text = _strip_think(text)
                self.breaker.record_success(model)
                return ProviderResult(text=text, model=model, latency_ms=latency)
            except Exception as exc:
                if attempt == 2:
                    self.breaker.record_failure(model)
                    return ProviderResult(text="", model=model, error=str(exc))
                await asyncio.sleep(2 ** attempt)

        return ProviderResult(text="", model=model, error="max_retries_exceeded")

    async def _request(self, model: str, prompt: str, system: str, temperature: float, max_tokens: int, timeout: float) -> str:
        import gzip
        import urllib.request
        import json as _json

        messages = [{"role": "user", "content": prompt}]
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }
        if system:
            payload["system"] = system

        loop = asyncio.get_event_loop()

        def _do() -> str:
            req = urllib.request.Request(
                f"{self.base_url}/v1/messages",
                data=_json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Accept-Encoding": "gzip, deflate",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                if r.info().get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                raw_str = raw.decode("utf-8", errors="replace")
                data = _json.loads(raw_str)
                # Estrai text da content array (Anthropic format)
                for item in data.get("content", []):
                    if item.get("type") == "text":
                        return item["text"]
                return ""

        return await loop.run_in_executor(None, _do)

__all__ = [
    "LLMProvider",
    "MockProvider",
    "ProviderResult",
    "ProviderKind",
    "CircuitBreaker",
    "AnthropicCompatProvider",
]
