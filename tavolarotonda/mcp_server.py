"""MCP server per tavolarotonda — Model Context Protocol."""

from __future__ import annotations

import asyncio
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from .memory_palace import MemoryPalace, transcript_markdown


# MCP protocol types
@dataclass
class MCPRequest:
    jsonrpc: str
    id: int | str | None
    method: str
    params: dict[str, Any] = field(default_factory=dict)

@dataclass
class MCPResponse:
    jsonrpc: str = "2.0"
    id: int | str | None = None
    result: Any = None
    error: dict[str, Any] | None = None

# Session management
@dataclass
class Session:
    id: str
    palace: Any  # MemoryPalace
    created_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)

_sessions: dict[str, Session] = {}
_cleanup_task: asyncio.Task | None = None

def _get_or_create_session(session_id: str) -> Session:
    now = time.time()
    if session_id in _sessions:
        s = _sessions[session_id]
        s.last_seen = now
        return s
    s = Session(id=session_id, palace=MemoryPalace(topic="(new session)"))
    _sessions[session_id] = s
    return s

async def _cleanup_loop():
    while True:
        await asyncio.sleep(300)
        now = time.time()
        expired = [sid for sid, s in _sessions.items() if now - s.last_seen > 1800]
        for sid in expired:
            _sessions.pop(sid, None)

def _start_cleanup():
    global _cleanup_task
    if _cleanup_task is None:
        _cleanup_task = asyncio.create_task(_cleanup_loop())

async def handle_initialize(params: dict) -> dict:
    """MCP initialize — handshake iniziale."""
    return {
        "protocolVersion": "2024-11-05",
        "serverInfo": {"name": "tavolarotonda", "version": "0.1.0"},
        "capabilities": {"tools": {}, "resources": {}},
    }

async def handle_tools_list(params: dict) -> dict:
    """MCP tools/list."""
    return {
        "tools": [
            {
                "name": "discuss",
                "description": "Avvia una discussione multi-agente su un topic",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Topic della discussione"},
                        "session_id": {"type": "string", "description": "ID sessione (opzionale, genera nuovo se assente)"},
                        "rounds": {"type": "integer", "description": "Numero di round", "default": 3},
                        "agents": {"type": "array", "items": {"type": "string"}, "description": "Agenti da usare"},
                    },
                    "required": ["topic"],
                },
            },
            {
                "name": "status",
                "description": "Stato di una sessione",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                    },
                    "required": ["session_id"],
                },
            },
            {
                "name": "history",
                "description": "Storico di una sessione come markdown",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                    },
                    "required": ["session_id"],
                },
            },
        ]
    }

async def handle_tools_call(name: str, params: dict) -> dict:
    """Esegui un tool MCP."""
    if name == "discuss":
        topic = params["topic"]
        session_id = params.get("session_id", f"mcp-{int(time.time())}")
        rounds = params.get("rounds", 3)
        agents = params.get("agents")

        session = _get_or_create_session(session_id)
        if topic != session.palace.topic:
            session.palace = MemoryPalace(topic=topic)
        else:
            session.palace.topic = topic

        # Build provider and council
        from .agents import AGENTS, agent_by_name, default_council
        from .phases import run_full_council
        from .providers import AnthropicCompatProvider
        provider = AnthropicCompatProvider()
        if agents:
            council_list = [agent_by_name(a) or agent_by_name("aristotle") for a in agents[:12]]
            council: list[Any] = [c for c in council_list if c]
        else:
            keys = default_council()
            council = [AGENTS[k] for k in keys]

        # Run council
        await run_full_council(session.palace, council, provider, rounds=rounds)  # type: ignore[arg-type]

        return {
            "content": [{"type": "text", "text": transcript_markdown(session.palace)}],
            "session_id": session_id,
        }

    elif name == "status":
        s = _sessions.get(params["session_id"])
        if not s:
            return {"content": [{"type": "text", "text": f"Session '{params['session_id']}' not found"}]}
        return {
            "content": [{
                "type": "text",
                "text": f"Session: {s.id}\nTopic: {s.palace.topic}\n"
                        f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.created_at))}\n"
                        f"Last seen: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.last_seen))}",
            }]
        }

    elif name == "history":
        s = _sessions.get(params["session_id"])
        if not s:
            return {"content": [{"type": "text", "text": f"Session '{params['session_id']}' not found"}]}
        return {
            "content": [{"type": "text", "text": transcript_markdown(s.palace)}],
        }

    return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

async def handle_mcp_request(data: dict) -> dict:
    """Processa una richiesta MCP JSON-RPC 2.0."""
    req = MCPRequest(
        jsonrpc=data.get("jsonrpc", "2.0"),
        id=data.get("id"),
        method=data.get("method", ""),
        params=data.get("params", {}),
    )

    if req.method == "initialize":
        result = await handle_initialize(req.params)
        return asdict(MCPResponse(id=req.id, result=result))
    elif req.method == "tools/list":
        result = await handle_tools_list(req.params)
        return asdict(MCPResponse(id=req.id, result=result))
    elif req.method == "tools/call":
        name = req.params.get("name", "")
        params = req.params.get("arguments", {})
        result = await handle_tools_call(name, params)
        return asdict(MCPResponse(id=req.id, result=result))
    elif req.method == "notifications/initialized":
        return asdict(MCPResponse(id=None))
    else:
        return asdict(MCPResponse(
            id=req.id,
            error={"code": -32601, "message": f"Method not found: {req.method}"},
        ))
