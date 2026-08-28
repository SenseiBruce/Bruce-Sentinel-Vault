import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_news_urls import count_news_urls, main  # noqa: E402


def test_counts_urls():
    payload = [
        {"title": "RBI hold", "url": "https://example.com/a"},
        {"title": "Skip", "url": "  "},
        "skip",
        {"title": "Tax update", "url": "http://example.com/b"},
    ]
    assert count_news_urls(payload) == 2


def test_non_list():
    assert count_news_urls({"url": "https://x"}) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "Demo", "url": "https://n.example"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["url_count"] == 1


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
