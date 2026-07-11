"""HTTP server minimale per tavolarotonda — API Obsidian + health."""

from __future__ import annotations

import argparse
from pathlib import Path

from .i18n import t
from .mcp_server import handle_mcp_request
from .obsidian_vault import read_topic, save_session

# ponytail: global lock, swap to async worker pool if throughput matters
HAS_STARLETTE = False
HAS_UVICORN = False

try:
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    from starlette.responses import JSONResponse, PlainTextResponse
    from starlette.routing import Route

    HAS_STARLETTE = True
except ImportError:
    pass

try:
    import uvicorn  # type: ignore

    HAS_UVICORN = True
except ImportError:
    pass


async def mcp_endpoint(request):  # type: ignore[no-untyped-def]
    """POST /mcp — JSON-RPC 2.0 MCP requests."""
    body = await request.json()
    response = await handle_mcp_request(body)
    return JSONResponse(response)


async def health(request):  # type: ignore[no-untyped-def]
    return JSONResponse({"status": "ok", "service": "tavolarotonda-serve"})


async def obsidian_topic(request):  # type: ignore[no-untyped-def]
    topic = request.query_params.get("topic", "")
    if not topic:
        return JSONResponse({"error": "missing ?topic= parameter"}, status_code=400)
    vault = Path(request.app.state.vault)
    try:
        content = read_topic(vault, topic)
        return PlainTextResponse(content, media_type="text/markdown")
    except FileNotFoundError:
        return JSONResponse({"error": f"Topic '{topic}' not found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def obsidian_save(request):  # type: ignore[no-untyped-def]
    """POST /api/obsidian/save — salva markdown nel vault."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    session_id = body.get("session_id", "unknown")
    markdown = body.get("markdown", "")
    if not markdown:
        return JSONResponse({"error": "missing markdown body"}, status_code=400)
    vault = Path(request.app.state.vault)
    path = save_session(markdown, vault, session_id)
    return JSONResponse({"saved": str(path)})


def build_app(vault_path: str):  # type: ignore[no-untyped-def]
    if not HAS_STARLETTE:
        raise RuntimeError(t("error_starlette_missing"))
    app = Starlette(
        routes=[
            Route("/health", health),
            Route("/mcp", mcp_endpoint, methods=["POST"]),
            Route("/api/obsidian/topic", obsidian_topic),
            Route("/api/obsidian/save", obsidian_save, methods=["POST"]),
        ],
        middleware=[
            Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"]),
        ],
    )
    app.state.vault = vault_path
    return app


def run(vault_path: str, port: int = 8765) -> None:  # type: ignore[no-untyped-def]
    if not HAS_STARLETTE:
        print(t("error_starlette_missing"))
        return
    if not HAS_UVICORN:
        print(t("error_uvicorn_missing"))
        return
    app = build_app(vault_path)
    print(t("server_started", port=port))
    print(t("route_health"))
    print(t("route_mcp"))
    print(t("route_obsidian_read"))
    print(t("route_obsidian_save"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--vault", default=None)
    args = parser.parse_args()
    vault = args.vault or str(Path.home() / "Obsidian" / "Memoria")
    run(vault, args.port)
