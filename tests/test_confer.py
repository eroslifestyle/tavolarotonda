"""Test per opus-m3-confer pattern."""
import pytest
from tavolarotonda.providers import MODEL_TIER_MAP


def test_model_tier_map_exists():
    assert "critical" in MODEL_TIER_MAP
    assert "reasoning" in MODEL_TIER_MAP
    assert "standard" in MODEL_TIER_MAP
    assert "fast" in MODEL_TIER_MAP


def test_model_tier_map_values():
    assert MODEL_TIER_MAP["critical"] == "opus-4-7"
    assert MODEL_TIER_MAP["reasoning"] == "minimax-sonar-pro"
    assert MODEL_TIER_MAP["standard"] == "claude-sonnet-5"
    assert MODEL_TIER_MAP["fast"] == "claude-haiku-4"
