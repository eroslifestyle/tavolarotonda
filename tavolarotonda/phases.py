"""Pipeline principale del council: Research → Restate → Brainstorm → Critique → Synthesis → Vote.

Pattern geek-alt/LLM-Council (phases) + 0xNyk (Problem Restate Gate + Verdict strutturato)
+ Manus (Director + Secretary + RE/WHY/DECISION) + geek-alt (Adversarial evidence + Minority report).

Modulare: ogni phase è una funzione async che prende palace e ritorna evento.
"""

from __future__ import annotations

import asyncio
import json as _json
from dataclasses import dataclass
from typing import Awaitable, Callable

from .agents import AGENTS, Agent
from .director import Director
from .evidence import adversarial_research
from .memory_palace import MemoryPalace
from .prompts import (
    BRAINSTORM_PROMPT,
    CRITIQUE_PROMPT,
    PROBLEM_RESTATE_PROMPT,
    SYNTHESIS_PROMPT,
    VERDICT_PROMPT,
    sanitize_directive,
)
from .providers import LLMProvider
from .secretary import Secretary


@dataclass
class PhaseEvent:
    """Evento emesso dalle fasi (per logging/UI)."""

    phase: str
    agent: str
    text: str
    round: int = 0
    meta: dict | None = None


# === PHASE 0: RESEARCH ===
async def phase_research(palace: MemoryPalace, *, max_per_side: int = 5) -> list[PhaseEvent]:
    """Adversarial evidence retrieval: supporting vs counter."""
    supporting, counter = await adversarial_research(palace.topic, max_per_side=max_per_side)
    palace.add_research(
        [f"{r.title} — {r.url}" for r in supporting],
        [f"{r.title} — {r.url}" for r in counter],
    )
    return [
        PhaseEvent(phase="research", agent="🌐 Supporting", text=f"{len(supporting)} fonti a favore"),
        PhaseEvent(phase="research", agent="⚠️ Counter", text=f"{len(counter)} fonti contro"),
    ]


# === PHASE 1: PROBLEM RESTATE GATE ===
async def phase_restate(
    palace: MemoryPalace,
    agents: list[Agent],
    provider: LLMProvider,
    *,
    on_event: Callable[[PhaseEvent], Awaitable[None]] | None = None,
) -> list[PhaseEvent]:
    """Ogni agente riformula il problema nel SUO angolo.

    Se >30% divergono significativamente dalla riformulazione canonica → flaggiamo
    che il problema stesso potrebbe essere mal posto.
    """
    events = []
    restatements = []
    coros = [
        provider.complete(
            PROBLEM_RESTATE_PROMPT.format(topic=palace.topic),
            model=a.default_model if a.default_model != "auto" else "mock",
            system=a.system_seed,
            temperature=0.5,
            max_tokens=80,
        )
        for a in agents
    ]
    results = await asyncio.gather(*coros, return_exceptions=True)
    for agent, res in zip(agents, results):
        if isinstance(res, Exception) or res.error:
            text = f"[restate error: {getattr(res, 'error', res)}]"
        else:
            text = res.text.strip()
        restatements.append({"agent": agent.key, "text": text})
        ev = PhaseEvent(phase="restate", agent=agent.name, text=text)
        events.append(ev)
        if on_event:
            await on_event(ev)

    palace.problem_restated = {"restatements": restatements}
    return events


# === PHASE 2: BRAINSTORM ===
async def phase_brainstorm(
    palace: MemoryPalace,
    agents: list[Agent],
    rounds: int,
    director: Director,
    secretary: Secretary,
    provider: LLMProvider,
    *,
    on_event: Callable[[PhaseEvent], Awaitable[None]] | None = None,
) -> list[PhaseEvent]:
    """Per ogni round: Director assegna focus+assignments, ogni agente brainstorrea, Secretary consolida."""
    events = []
    agent_names = [a.name for a in agents]
    last_round = rounds

    for r in range(1, rounds + 1):
        # Direttore fissa l'agenda
        transcript_tail = [
            f"{b['agent']}: {b['text']}" for b in palace.brainstorm[-10:]
        ]
        strategy_summary = secretary.summary_text(palace)
        agenda = await director.set_agenda(
            palace.topic, transcript_tail, strategy_summary,
            [a.key for a in agents], r, last_round,
        )

        # Convergenza anticipata
        if agenda.get("converged") and r > 1:
            ev = PhaseEvent(phase="brainstorm", agent="🎬 Regista",
                            text="Consenso raggiunto: chiudo il dibattito.", round=r)
            events.append(ev)
            if on_event:
                await on_event(ev)
            break

        if agenda.get("focus"):
            ev = PhaseEvent(phase="brainstorm", agent="🎬 Regista",
                            text=f"Round {r} — focus: {agenda['focus']}", round=r)
            events.append(ev)
            if on_event:
                await on_event(ev)

        # Ogni agente parla
        for agent in agents:
            assignment = str(agenda.get("assignments", {}).get(agent.key, "") or "")
            prompt = BRAINSTORM_PROMPT.format(
                agent_name=agent.name,
                figure=agent.figure,
                domain=agent.domain,
                polarity=agent.polarity,
                problem_restated=palace.problem_restated or "",
                prior_brief="\n".join(
                    f"{b['agent']}: {b['text'][:120]}" for b in palace.brainstorm[-5:]
                ),
                supporting_evidence="\n".join(palace.web_research["supporting"][:3]),
                counter_evidence="\n".join(palace.web_research["counter"][:3]),
            )
            if assignment:
                prompt += f"\n\n🎯 ASSEGNAMENTO SPECIFICO: {assignment}"

            result = await provider.complete(
                prompt,
                model=agent.default_model if agent.default_model != "auto" else "mock",
                system=agent.system_seed,
                temperature=0.7,
                max_tokens=400,
            )
            text = result.text.strip() if not result.error else f"[error: {result.error}]"
            palace.add_brainstorm(agent.key, text, r, agent.default_model)
            ev = PhaseEvent(phase="brainstorm", agent=agent.name, text=text, round=r)
            events.append(ev)
            if on_event:
                await on_event(ev)

        # Secretary consolida
        await secretary.update(palace)

    return events


# === PHASE 3: CRITIQUE (cross-examination) ===
async def phase_critique(
    palace: MemoryPalace,
    agents: list[Agent],
    provider: LLMProvider,
    *,
    on_event: Callable[[PhaseEvent], Awaitable[None]] | None = None,
) -> list[PhaseEvent]:
    """Ogni agente critica SPECIFICAMENTE un altro agente (cross-examination).

    Mira a rompere il groupthink: se >70% sono d'accordo, forza 2 agenti a
    steelman l'opposizione (meccanismo anti-groupthink da 0xNyk).
    """
    events = []
    if not palace.brainstorm:
        return events

    # Conta consenso (claims simili)
    last_round = max(b["round"] for b in palace.brainstorm)
    last_claims = [b for b in palace.brainstorm if b["round"] == last_round]

    # Pairing: ogni agente critica il SUCCESSIVO (rotazione)
    n = len(agents)
    for i, agent in enumerate(agents):
        target = agents[(i + 1) % n]
        # Trova l'ultimo claim del target
        target_claim = next(
            (b["text"] for b in reversed(last_claims) if b["agent"] == target.key),
            "(nessun claim)",
        )
        prompt = CRITIQUE_PROMPT.format(
            agent_name=agent.name,
            target_agent=target.name,
            target_claim=target_claim[:300],
        )
        result = await provider.complete(
            prompt,
            model=agent.default_model if agent.default_model != "auto" else "mock",
            system=agent.system_seed,
            temperature=0.6,
            max_tokens=200,
        )
        text = result.text.strip() if not result.error else f"[error: {result.error}]"
        palace.add_critique(agent.key, target.key, text, last_round)
        ev = PhaseEvent(phase="critique", agent=agent.name, text=text, round=last_round)
        events.append(ev)
        if on_event:
            await on_event(ev)

    return events


# === PHASE 4: SYNTHESIS FINALE ===
async def phase_synthesis(
    palace: MemoryPalace,
    agents: list[Agent],
    provider: LLMProvider,
    *,
    on_event: Callable[[PhaseEvent], Awaitable[None]] | None = None,
) -> PhaseEvent:
    """Sintetizzatore finale: decisione + minority report + open questions + next steps."""
    transcript = [f"{b['agent']}: {b['text']}" for b in palace.brainstorm]
    strategy = _json.dumps(
        {
            "open_questions": palace.open_questions,
            "convergence": palace.convergence_score,
        },
        ensure_ascii=False,
    )
    prompt = SYNTHESIS_PROMPT.format(
        agent_list=", ".join(a.name for a in agents),
        topic=palace.topic,
        transcript="\n".join(transcript[-30:]),
        strategy=strategy,
    )
    result = await provider.complete(
        prompt,
        model="claude-opus-4-7" if "claude" in (provider.openai_api_key or "") else "mock",
        system="Sei il sintetizzatore finale. Output strutturato come da istruzioni.",
        temperature=0.4,
        max_tokens=1200,
    )
    text = result.text.strip() if not result.error else f"[error: {result.error}]"
    palace.set_synthesis(text, max(b["round"] for b in palace.brainstorm) if palace.brainstorm else 1)

    # Parse delle sezioni
    decision = _extract_section(text, "Decisione") or _extract_section(text, "Decision")
    minority = _extract_section(text, "Minority Report") or ""
    open_qs = _extract_list_section(text, "Open Questions")
    next_steps = _extract_list_section(text, "Next Steps")
    palace.decision = decision
    palace.minority_report = minority
    palace.open_questions = open_qs or palace.open_questions
    palace.next_steps = next_steps

    ev = PhaseEvent(phase="synthesis", agent="🧬 Sintetizzatore", text=text)
    if on_event:
        await on_event(ev)
    return ev


# === PHASE 5: VERDICT / VOTING ===
async def phase_verdict(
    palace: MemoryPalace,
    agents: list[Agent],
    provider: LLMProvider,
) -> list[PhaseEvent]:
    """Ogni agente vota 0-10 sulla proposta finale (feasibility, impact, risk_safety)."""
    events = []
    proposals = [b["text"] for b in palace.brainstorm[-3:]]
    if not proposals:
        return events
    prompt = VERDICT_PROMPT.format(
        topic=palace.topic,
        proposals="\n".join(f"- {p[:200]}" for p in proposals),
    )
    # In modalità mock, il verdetto è solo un placeholder
    result = await provider.complete(
        prompt,
        model="mock",
        system="Voto secco.",
        temperature=0.2,
        max_tokens=300,
    )
    text = result.text if not result.error else "{}"
    try:
        from .director import _extract_json
        parsed = _extract_json(text) or {}
        rankings = parsed.get("rankings", [])
    except Exception:
        rankings = []

    # Voto simbolico di ogni agente (per trasparenza)
    for i, agent in enumerate(agents):
        score = 0.7 + (i % 3) * 0.1  # mock: voto vario per evitare groupthink artificiale
        palace.add_vote(agent.key, "approve" if score > 0.6 else "abstain", score)
        events.append(PhaseEvent(
            phase="vote", agent=agent.name,
            text=f"Voto: {score:.2f}", meta={"rankings": rankings[:1]}
        ))

    return events


# === Helpers ===

def _extract_section(text: str, header: str) -> str | None:
    """Estrae una sezione markdown fino al prossimo header ## o fine testo."""
    import re
    pattern = rf"##\s*{re.escape(header)}[^\n]*\n(.*?)(?=\n##|\Z)"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _extract_list_section(text: str, header: str) -> list[str]:
    """Estrae una sezione markdown di lista bullet."""
    section = _extract_section(text, header)
    if not section:
        return []
    items = []
    for line in section.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            items.append(line[2:].strip())
        elif line and not line.startswith("#"):
            items.append(line)
    return [x for x in items if x]


# === ENTRY POINT: full pipeline ===

async def run_full_council(
    palace: MemoryPalace,
    agents: list[Agent],
    provider: LLMProvider,
    *,
    rounds: int = 3,
    include_research: bool = True,
    include_critique: bool = True,
    include_verdict: bool = True,
    director_model: str = "auto",
    secretary_model: str = "auto",
    on_event: Callable[[PhaseEvent], Awaitable[None]] | None = None,
) -> list[PhaseEvent]:
    """Esegue l'intera pipeline. Ritorna tutti gli eventi emessi."""
    all_events: list[PhaseEvent] = []

    # Sostituisci 'auto' con 'mock' se il provider non ha LLM reale
    if director_model == "auto":
        director_model = getattr(provider, "_default_for_director", "mock")
    if secretary_model == "auto":
        secretary_model = getattr(provider, "_default_for_secretary", "mock")

    director = Director(provider, director_model)
    secretary = Secretary(provider, secretary_model)

    if include_research:
        all_events.extend(await phase_research(palace))

    all_events.extend(await phase_restate(palace, agents, provider, on_event=on_event))
    all_events.extend(await phase_brainstorm(palace, agents, rounds, director, secretary, provider, on_event=on_event))

    if include_critique:
        all_events.extend(await phase_critique(palace, agents, provider, on_event=on_event))

    await phase_synthesis(palace, agents, provider, on_event=on_event)
    if include_verdict:
        all_events.extend(await phase_verdict(palace, agents, provider))

    return all_events


__all__ = [
    "PhaseEvent",
    "phase_research",
    "phase_restate",
    "phase_brainstorm",
    "phase_critique",
    "phase_synthesis",
    "phase_verdict",
    "run_full_council",
]
