import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from list_news_succeeded import list_news_succeeded, main  # noqa: E402


def test_extracts_passed_titles():
    payload = [
        {"title": "  RBI pause  ", "verdict": "passed"},
        {"title": "Fake tax", "verdict": "FAILED"},
        {"verdict": "PASSED"},
        "skip",
        {"title": "Cut", "verdict": "  PASSED  "},
    ]
    assert list_news_succeeded(payload) == ["RBI pause", "Cut"]


def test_non_list():
    assert list_news_succeeded({"title": "x", "verdict": "PASSED"}) == []


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "Ok", "verdict": "PASSED"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["succeeded"] == ["Ok"]


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
