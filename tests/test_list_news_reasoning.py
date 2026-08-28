import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from list_news_reasoning import list_news_reasoning, main  # noqa: E402


def test_extracts_reasoning():
    payload = [
        {"reasoning": " Strong source "},
        {"reasoning": ""},
        "skip",
        {"reasoning": "Timely"},
    ]
    assert list_news_reasoning(payload) == ["Strong source", "Timely"]


def test_non_list():
    assert list_news_reasoning({"reasoning": "X"}) == []


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"reasoning": "Market moving"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["reasoning"] == ["Market moving"]


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
