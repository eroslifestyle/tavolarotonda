"""Test per mcp_server.py."""

import pytest
from tavolarotonda.mcp_server import handle_mcp_request


@pytest.mark.asyncio
async def test_initialize():
    result = await handle_mcp_request({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {},
    })
    assert result["id"] == 1
    assert "serverInfo" in result["result"]


@pytest.mark.asyncio
async def test_tools_list():
    result = await handle_mcp_request({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {},
    })
    assert result["id"] == 2
    tools = result["result"]["tools"]
    names = [t["name"] for t in tools]
    assert "discuss" in names
    assert "status" in names
    assert "history" in names


@pytest.mark.asyncio
async def test_tools_call_status_unknown_session():
    result = await handle_mcp_request({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "status", "arguments": {"session_id": "nonexistent"}},
    })
    assert result["id"] == 3
    assert "not found" in result["result"]["content"][0]["text"].lower()


@pytest.mark.asyncio
async def test_tools_call_history_unknown_session():
    result = await handle_mcp_request({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {"name": "history", "arguments": {"session_id": "nonexistent"}},
    })
    assert result["id"] == 4
    assert "not found" in result["result"]["content"][0]["text"].lower()


@pytest.mark.asyncio
async def test_unknown_method():
    result = await handle_mcp_request({
        "jsonrpc": "2.0",
        "id": 5,
        "method": "foobar",
        "params": {},
    })
    assert result["id"] == 5
    assert result["error"] is not None
    assert result["error"]["code"] == -32601


@pytest.mark.asyncio
async def test_notification_no_response():
    """Notifications non devono tornare una response object."""
    result = await handle_mcp_request({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    })
    assert result["id"] is None
