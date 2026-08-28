import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from list_news_urls import list_news_urls, main  # noqa: E402


def test_extracts_urls():
    payload = [
        {"url": " https://example.com/a "},
        {"url": ""},
        "skip",
        {"url": "https://example.com/b"},
    ]
    assert list_news_urls(payload) == [
        "https://example.com/a",
        "https://example.com/b",
    ]


def test_non_list():
    assert list_news_urls({"url": "https://example.com"}) == []


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"url": "https://example.com/demo"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["urls"] == ["https://example.com/demo"]


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
