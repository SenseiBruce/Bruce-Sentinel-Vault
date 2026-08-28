import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from list_news_sources import list_news_sources, main  # noqa: E402


def test_extracts_sources():
    payload = [
        {"source": " Reuters "},
        {"source": ""},
        "skip",
        {"source": "PTI"},
    ]
    assert list_news_sources(payload) == ["Reuters", "PTI"]


def test_non_list():
    assert list_news_sources({"source": "X"}) == []


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"source": "Bloomberg"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["sources"] == ["Bloomberg"]


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
