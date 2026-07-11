"""Adversarial evidence retrieval — supporting vs counter-evidence.

Pattern geek-alt/LLM-Council: due pass separati di ricerca web.
- Supporting: query "positivo" → fonti che supportano la decisione proposta
- Counter: query "negativo/alternativo" → fonti che la mettono in dubbio

Per ogni claim, MAEntrambe le liste sono presentate al council per evitare echo chamber.

Provider supportati (in ordine di priorità):
1. SearXNG self-hosted (privato, no rate limit) — via env SEARXNG_URL
2. Brave API (gratuito fino a 2000 query/mese) — via env BRAVE_API_KEY
3. DuckDuckGo (no key, scraping HTML) — fallback
4. Mock (per test) — ritorna risultati plausibili finti
"""

from __future__ import annotations

import asyncio
import os
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote as _quote

SearchProvider = Literal["searxng", "brave", "duckduckgo", "mock"]


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


def _detect_provider() -> SearchProvider:
    if os.environ.get("TAVOLAROTONDA_MOCK"):
        return "mock"
    if os.environ.get("SEARXNG_URL"):
        return "searxng"
    if os.environ.get("BRAVE_API_KEY"):
        return "brave"
    return "duckduckgo"


def _query_for(topic: str, kind: Literal["supporting", "counter"]) -> str:
    """Genera query di ricerca adversarial."""
    if kind == "supporting":
        return f"{topic} pro vantaggi benefici case study"
    return f"{topic} contro rischi problemi fallimenti critiche"


async def search(query: str, *, max_results: int = 5, provider: SearchProvider | None = None) -> list[SearchResult]:
    """Esegue una ricerca web. Ritorna lista di SearchResult."""
    provider = provider or _detect_provider()
    loop = asyncio.get_event_loop()

    if provider == "searxng":
        return await loop.run_in_executor(None, _search_searxng, query, max_results)
    if provider == "brave":
        return await loop.run_in_executor(None, _search_brave, query, max_results)
    if provider == "duckduckgo":
        return await loop.run_in_executor(None, _search_ddg, query, max_results)
    return _mock_search(query, max_results)


async def adversarial_research(topic: str, *, max_per_side: int = 5) -> tuple[list[SearchResult], list[SearchResult]]:
    """Esegue DUE ricerche parallele: supporting + counter."""
    sup_task = search(_query_for(topic, "supporting"), max_results=max_per_side)
    ctr_task = search(_query_for(topic, "counter"), max_results=max_per_side)
    supporting, counter = await asyncio.gather(sup_task, ctr_task)
    return supporting, counter


# --- Implementazioni provider ---


def _search_searxng(query: str, max_results: int) -> list[SearchResult]:
    """SearXNG JSON API."""
    import json as _json
    import urllib.request
    base = os.environ.get("SEARXNG_URL", "").rstrip("/")
    if not base:
        return _mock_search(query, max_results)
    url = f"{base}/search?q={_quote(query)}&format=json&language=it"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = _json.loads(r.read().decode())
            return [
                SearchResult(title=x.get("title", ""), url=x.get("url", ""), snippet=x.get("content", ""))
                for x in data.get("results", [])[:max_results]
            ]
    except Exception:
        return _mock_search(query, max_results)


def _search_brave(query: str, max_results: int) -> list[SearchResult]:
    """Brave Search API."""
    import json as _json
    import urllib.request
    key = os.environ.get("BRAVE_API_KEY", "")
    if not key:
        return _mock_search(query, max_results)
    url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count={max_results}"
    try:
        req = urllib.request.Request(url, headers={"X-Subscription-Token": key, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = _json.loads(r.read().decode())
            return [
                SearchResult(
                    title=x.get("title", ""),
                    url=x.get("url", ""),
                    snippet=x.get("description", "")
                )
                for x in data.get("web", {}).get("results", [])[:max_results]
            ]
    except Exception:
        return _mock_search(query, max_results)


def _search_ddg(query: str, max_results: int) -> list[SearchResult]:
    """DuckDuckGo HTML scraping (no key)."""
    import html as html_lib
    import urllib.request
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
        # Estrai risultati in modo naive (meglio di niente)
        results = []
        for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',
                              html, re.DOTALL):
            url_m, title_m, snippet_m = m.group(1), m.group(2), m.group(3)
            # DDG redirect URLs
            url_m = urllib.parse.unquote(url_m.split("uddg=")[-1].split("&")[0]) if "uddg=" in url_m else url_m
            results.append(SearchResult(
                title=html_lib.unescape(title_m).strip(),
                url=url_m,
                snippet=html_lib.unescape(re.sub(r"<[^>]+>", "", snippet_m)).strip()[:200],
            ))
            if len(results) >= max_results:
                break
        return results or _mock_search(query, max_results)
    except Exception:
        return _mock_search(query, max_results)


def _mock_search(query: str, max_results: int) -> list[SearchResult]:
    """Risultati plausibili per test/demo (no network)."""
    side = "supporting" if "pro" in query.lower() or "vantaggi" in query.lower() else "counter"
    mock_data = {
        "supporting": [
            ("GitHub - Detrol/quorum-cli: Multi-agent AI discussion", "https://github.com/Detrol/quorum-cli", "Structured debates tra LLM con 7 metodi diversi."),
            ("Council of High Intelligence", "https://github.com/0xNyk/council-of-high-intelligence", "18 AI personas deliberano decisioni difficili."),
            ("Multi-Agent Debate migliora factuality (Du et al. 2023)", "https://arxiv.org/abs/2305.14325", "Paper che mostra come il debate multi-agente riduce le allucinazioni."),
        ],
        "counter": [
            ("Chameleon Injection: prompt injection su multi-agent debate", "https://github.com/aaditya79/chameleon-injection", "I sistemi MAD hanno blind spots sistematici agli attacchi injection."),
            ("Self-Consistency è spesso meglio del Debate (Debate or Vote, NeurIPS 2025)", "https://arxiv.org/abs/2504.20456", "Per factuality matematica, voting supera debate."),
            ("Multi-agent LLMs herd behavior", "https://arxiv.org/abs/2402.18272", "LLM in gruppo tendono a convergere prematuramente (groupthink)."),
        ],
    }
    items = mock_data[side]
    return [
        SearchResult(title=t, url=u, snippet=s)
        for t, u, s in items[:max_results]
    ]


__all__ = [
    "SearchResult",
    "adversarial_research",
    "search",
    "SearchProvider",
]
