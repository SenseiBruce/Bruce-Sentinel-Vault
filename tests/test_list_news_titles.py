import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from list_news_titles import list_news_titles, main  # noqa: E402


def test_extracts_titles():
    payload = [
        {"title": " RBI hold "},
        {"title": ""},
        "skip",
        {"title": "Tax update"},
    ]
    assert list_news_titles(payload) == ["RBI hold", "Tax update"]


def test_non_list():
    assert list_news_titles({"title": "X"}) == []


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "Demo"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["titles"] == ["Demo"]


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
