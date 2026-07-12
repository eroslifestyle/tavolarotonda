"""Voting analysis — AQ Session 9/10.

Analizza i voti degli agenti: scorecard, consenso, heatmap di conflitto.
"""
from __future__ import annotations

from tavolarotonda.memory_palace import MemoryPalace


def build_scorecard(palace: MemoryPalace) -> dict:
    """Costruisce una scorecard dai voti degli agenti."""
    votes = palace.votes
    if not votes:
        return {"votes": [], "consensus": 0.0, "avg_score": 0.0, "verdict_counts": {}}

    scores = [v.get("score", 0.0) for v in votes]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    # Conta i verdetti
    verdict_counts: dict[str, int] = {}
    for v in votes:
        verdict = v.get("verdict", "unknown")
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

    # Consenso = quota del verdetto più votato
    total = len(votes)
    max_count = max(verdict_counts.values()) if verdict_counts else 0
    consensus = max_count / total if total else 0.0

    return {
        "votes": votes,
        "consensus": round(consensus, 3),
        "avg_score": round(avg_score, 2),
        "verdict_counts": verdict_counts,
        "total_voters": total,
    }


def build_heatmap(palace: MemoryPalace) -> dict:
    """Costruisce una heatmap di consenso/conflitto tra agenti.

    Ritorna una matrice: per ogni coppia di agenti, quanto sono d'accordo
    (differenza di score normalizzata).
    """
    votes = palace.votes
    agents = [v.get("agent", "") for v in votes]
    scores = {v.get("agent", ""): v.get("score", 0.0) for v in votes}

    matrix = []
    for a1 in agents:
        row = []
        for a2 in agents:
            # Agreement = 1 - |diff score normalizzato|
            diff = abs(scores.get(a1, 0) - scores.get(a2, 0))
            agreement = round(1.0 - min(diff, 1.0), 2)
            row.append(agreement)
        matrix.append(row)

    return {
        "agents": agents,
        "matrix": matrix,
        "size": len(agents),
    }


def find_outliers(palace: MemoryPalace, threshold: float = 0.3) -> list[dict]:
    """Trova gli agenti il cui voto diverge molto dalla media (minority report)."""
    votes = palace.votes
    if not votes:
        return []
    scores = [v.get("score", 0.0) for v in votes]
    avg = sum(scores) / len(scores)
    outliers = []
    for v in votes:
        deviation = abs(v.get("score", 0.0) - avg)
        if deviation > threshold:
            outliers.append({
                "agent": v.get("agent", ""),
                "score": v.get("score", 0.0),
                "deviation": round(deviation, 2),
                "verdict": v.get("verdict", ""),
            })
    return sorted(outliers, key=lambda x: x["deviation"], reverse=True)
