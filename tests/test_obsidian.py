"""Test per obsidian_vault.py."""

from pathlib import Path

import pytest

from tavolarotonda.obsidian_vault import read_topic, save_session


def test_read_topic_found(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "sessioni").mkdir()
    topic_file = vault / "sessioni" / "test-topic.md"
    topic_file.write_text("# Test Topic\n\nContenuto di test.", encoding="utf-8")
    content = read_topic(vault, "test-topic")
    assert "Test Topic" in content


def test_read_topic_not_found(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    with pytest.raises(FileNotFoundError):
        read_topic(vault, "nonexistent")


def test_save_session(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    markdown = "# Sessione Test\n\nContenuto."
    path = save_session(markdown, vault, "test-123")
    assert path.exists()
    assert "# Sessione Test" in path.read_text(encoding="utf-8")


def test_save_session_creates_folder(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    save_session("# Test", vault, "abc", folder="progetti/tavolarotonda/sessioni/")
    assert (vault / "progetti" / "tavolarotonda" / "sessioni").exists()
