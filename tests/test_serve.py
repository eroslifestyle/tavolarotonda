"""Test per serve.py (mock senza network)."""

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette

from tavolarotonda.serve import build_app


@pytest.fixture
def app(tmp_path: "pytest.fixture") -> Starlette:
    vault = tmp_path / "vault"
    vault.mkdir()
    return build_app(str(vault))  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_health(app: Starlette) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_obsidian_topic_found(tmp_path: "pytest.fixture") -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "sessioni").mkdir()
    topic_file = vault / "sessioni" / "my-topic.md"
    topic_file.write_text("# My Topic\n\nContent here.", encoding="utf-8")
    app2 = build_app(str(vault))
    transport = ASGITransport(app=app2)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/obsidian/topic?topic=my-topic")
        assert r.status_code == 200
        assert "My Topic" in r.text


@pytest.mark.asyncio
async def test_obsidian_topic_missing_param(app: Starlette) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/obsidian/topic")
        assert r.status_code == 400


@pytest.mark.asyncio
async def test_obsidian_save(app: Starlette) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/obsidian/save", json={"session_id": "test", "markdown": "# Test"})
        assert r.status_code == 200
        assert "saved" in r.json()
