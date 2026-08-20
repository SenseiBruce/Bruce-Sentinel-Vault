"""Unit tests for pydantic entry-point schemas."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "grader-agent" / "src"))

from schemas import (  # noqa: E402
    SchemaError,
    parse_news_items,
    parse_script_entries,
)


def test_parse_news_items_valid():
    items = parse_news_items(
        [{"title": "RBI rate hold", "source": "Mint"}, {"title": "Tax update"}]
    )
    assert items[0].title == "RBI rate hold"
    assert items[1].source == ""


def test_parse_news_items_invalid_blank_title():
    with pytest.raises(SchemaError):
        parse_news_items([{"title": "   ", "source": "x"}])


def test_parse_news_items_rejects_non_list():
    with pytest.raises(SchemaError, match="list"):
        parse_news_items({"title": "nope"})


def test_parse_script_entries_valid():
    entries = parse_script_entries(
        [
            {
                "project_name": "Demo",
                "scenes": [{"narration": "hi", "image_prompt": "city"}],
            }
        ]
    )
    assert entries[0].project_name == "Demo"
    assert entries[0].scenes[0].image_prompt == "city"


def test_parse_script_entries_invalid_project_name():
    with pytest.raises(SchemaError):
        parse_script_entries([{"project_name": "", "scenes": []}])
