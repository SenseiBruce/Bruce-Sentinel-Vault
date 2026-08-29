import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_news_items import count_news_items, main  # noqa: E402


def test_counts_dict_items():
    payload = [
        {"title": "Fake tax"},
        {"title": "RBI pause"},
        "skip",
        {"title": "Rumor"},
    ]
    assert count_news_items(payload) == 3


def test_non_list():
    assert count_news_items({"title": "Nope"}) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "A"}, {"title": "B"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["item_count"] == 2


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
