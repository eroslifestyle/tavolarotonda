"""Entry point CLI per tavolarotonda.

Uso:
    python -m tavolarotonda [OPTIONS] [TOPIC]

    # Modalità audit: analizza un file di codice
    python -m tavolarotonda --audit path/to/file.py

    # Modalità Q&A: domande multiple, risposte multi-agente
    python -m tavolarotonda --qa "Q1?" "Q2?" "Q3?"

    # Modalità demo (con mock provider, no LLM reale)
    python -m tavolarotonda --mock "Topico di esempio"

    # Output HTML audit
    python -m tavolarotonda --audit target.py --output report.html

Privacy:
    --privacy local_only  : solo Ollama, niente cloud
    --privacy cloud_ok    : + Claude/OpenAI (default)
    --privacy free_api_ok : + Groq/Cerebras via LiteLLM (NON inviare dati sensibili)
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from .agents import AGENTS, default_council
from .memory_palace import MemoryPalace, transcript_markdown
from .phases import run_full_council
from .providers import LLMProvider, MockProvider, AnthropicCompatProvider
from .reports import audit_report_from_palace, render_audit_report, render_qa_template


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tavolarotonda",
        description="Council multi-agente per decisioni reali, audit e Q&A multi-domanda.",
    )
    parser.add_argument("topic", nargs="?", help="Topico della tavola rotonda")
    parser.add_argument("--audit", metavar="FILE", help="Modalità audit: analizza un file di codice")
    parser.add_argument("--qa", nargs="+", metavar="Q", help="Modalità Q&A: lista di domande")
    parser.add_argument("--rounds", type=int, default=3, help="Numero di round (default: 3)")
    parser.add_argument("--council", nargs="+", metavar="AGENT",
                        help="Lista agenti (default: 12 bilanciati)")
    parser.add_argument("--privacy", choices=["local_only", "cloud_ok", "free_api_ok"],
                        default="cloud_ok", help="Privacy tier (default: cloud_ok)")
    parser.add_argument("--mock", action="store_true", help="Usa MockProvider (no LLM reale)")
    parser.add_argument("--no-research", action="store_true", help="Salta ricerca web")
    parser.add_argument("--no-critique", action="store_true", help="Salta fase critica")
    parser.add_argument("--output", "-o", metavar="PATH", help="File di output (HTML o JSON)")
    parser.add_argument("--format", choices=["text", "html", "json"], default="text",
                        help="Formato output (default: text)")
    parser.add_argument("--save-palace", metavar="PATH", help="Salva Memory Palace JSON")
    parser.add_argument("--provider", choices=["ollama", "openai", "anthropic", "mock"],
                        default="anthropic", help="Provider LLM (default: anthropic)")
    parser.add_argument("--anthropic-url", default="http://127.0.0.1:8787",
                        help="URL base per provider anthropic (default: http://127.0.0.1:8787)")
    return parser.parse_args(argv)


def _build_provider(args: argparse.Namespace) -> LLMProvider:
    if args.mock or os.environ.get("TAVOLAROTONDA_MOCK"):
        return MockProvider(privacy_tier=args.privacy)

    provider_type = getattr(args, "provider", "anthropic")

    if provider_type == "anthropic":
        return AnthropicCompatProvider(
            base_url=getattr(args, "anthropic_url", "http://127.0.0.1:8787"),
            api_key=os.environ.get("ANTHROPIC_API_KEY", "mock"),
            privacy_tier=args.privacy,
        )
    elif provider_type == "ollama":
        return LLMProvider(
            ollama_base_url=os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            privacy_tier=args.privacy,
        )
    elif provider_type == "openai":
        return LLMProvider(
            openai_base_url=os.environ.get("OPENAI_BASE_URL"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            privacy_tier=args.privacy,
        )
    else:
        return MockProvider(privacy_tier=args.privacy)


def _build_council(args: argparse.Namespace) -> list:
    keys = args.council or default_council()
    return [AGENTS[k] for k in keys if k in AGENTS]


def _emit_event(events: list):
    """Callback per stampare eventi durante l'esecuzione."""
    async def _cb(ev) -> None:
        events.append(ev)
        # Stampa sintetica
        prefix = f"[{ev.phase}]"
        if ev.round:
            prefix += f" r{ev.round}"
        print(f"  {prefix} {ev.agent}: {ev.text[:120]}{'…' if len(ev.text) > 120 else ''}")
    return _cb


async def run_topic(args: argparse.Namespace, topic: str) -> MemoryPalace:
    """Esegue una sessione di tavola rotonda su un topic."""
    palace = MemoryPalace(topic=topic)
    provider = _build_provider(args)
    council = _build_council(args)

    provider_name = getattr(args, "provider", "anthropic") if not args.mock else "mock"
    print(f"\n🥽 Tavola Rotonda: {topic}")
    print(f"   Council: {len(council)} agenti | Rounds: {args.rounds} | "
          f"Privacy: {args.privacy} | Provider: {provider_name}")
    print()

    events = []
    await run_full_council(
        palace,
        council,
        provider,
        rounds=args.rounds,
        include_research=not args.no_research,
        include_critique=not args.no_critique,
        include_verdict=True,
        on_event=_emit_event(events),
    )
    return palace


async def run_audit(args: argparse.Namespace, file_path: str) -> str:
    """Modalità audit: analizza un file di codice."""
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File non trovato: {file_path}", file=sys.stderr)
        sys.exit(1)
    code = path.read_text(encoding="utf-8", errors="replace")

    # Topic = descrizione del file
    topic = (
        f"AUDIT DEL CODICE: '{path.name}'.\n"
        f"Devi analizzare il seguente codice e produrre un audit report con:\n"
        f"PRO, CONTRO, PUNTI DI FORZA, CRITICITÀ, CONSIGLI CONCRETI.\n\n"
        f"```\n{code[:8000]}\n```"
    )
    palace = MemoryPalace(topic=topic)
    provider = _build_provider(args)
    council = _build_council(args)

    print(f"\n📋 Audit Report: {path.name}")
    print(f"   Council: {len(council)} agenti | Privacy: {args.privacy}")
    print()

    events = []
    await run_full_council(
        palace, council, provider,
        rounds=args.rounds,
        include_research=False,  # niente web per audit di codice locale
        include_critique=True,
        include_verdict=True,
        on_event=_emit_event(events),
    )

    # Genera HTML
    html = audit_report_from_palace(
        palace,
        target_name=path.name,
        target_description=f"Audit del codice in {path}. Analisi multi-agente con {len(council)} agenti.",
    )
    return html


async def run_qa(args: argparse.Namespace, questions: list[str]) -> str:
    """Modalità Q&A: risposte multi-agente in parallelo."""
    # Per semplicità: facciamo UNA domanda "composta" con tutte le sotto-domande
    topic = (
        f"Q&A MULTI-DOMANDA. Rispondi a CIASCUNA delle seguenti domande in modo "
        f"indipendente, etichettando chiaramente la risposta (es. 'Q1:', 'Q2:', ...).\n\n"
        + "\n".join(f"Q{i+1}: {q}" for i, q in enumerate(questions))
    )
    palace = MemoryPalace(topic=topic)
    provider = _build_provider(args)
    council = _build_council(args)

    print(f"\n❓ Q&A Multi-Domanda ({len(questions)} domande)")
    print(f"   Council: {len(council)} agenti")
    print()

    events = []
    await run_full_council(
        palace, council, provider,
        rounds=min(args.rounds, 2),  # Q&A più rapido
        include_research=False,
        include_critique=True,
        include_verdict=False,
        on_event=_emit_event(events),
    )

    # Pre-fill answers per il template Q&A
    prefill = {}
    for i in range(len(questions)):
        # Prendi l'ultimo contributo per ogni agente
        agent_answers = {}
        for b in palace.brainstorm:
            if b["agent"] not in agent_answers:
                agent_answers[b["agent"]] = b["text"]
        prefill[i] = agent_answers

    return render_qa_template(
        title=f"Q&A — {len(questions)} domande, {len(council)} agenti",
        questions=questions,
        prefill_answers=prefill,
    )


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    try:
        if args.audit:
            output = asyncio.run(run_audit(args, args.audit))
            ext = "html"
        elif args.qa:
            output = asyncio.run(run_qa(args, args.qa))
            ext = "html"
        elif args.topic:
            palace = asyncio.run(run_topic(args, args.topic))
            # Stampa transcript
            print("\n" + "=" * 60)
            print(transcript_markdown(palace))

            if args.format == "json" or args.save_palace:
                import json as _json
                palace_json = _json.dumps(palace.to_dict(), indent=2, ensure_ascii=False)
                if args.save_palace:
                    Path(args.save_palace).write_text(palace_json, encoding="utf-8")
                    print(f"\n💾 Memory Palace salvato: {args.save_palace}")
                if args.format == "json":
                    print(palace_json)
            return 0
        else:
            print("❌ Specifica un topic, --audit FILE, o --qa 'Q1' 'Q2' ...", file=sys.stderr)
            _parse_args(["--help"])
            return 1

        # Salva output HTML
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"\n💾 Report salvato: {args.output}")
        else:
            # Stampa anteprima
            print("\n" + output[:2000] + ("\n...[truncated, usa --output per salvare]" if len(output) > 2000 else ""))
        return 0

    except KeyboardInterrupt:
        print("\n⚠️ Interrotto.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
