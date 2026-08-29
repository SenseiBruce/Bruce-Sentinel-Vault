import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_news_dates import count_news_dates, main  # noqa: E402


def test_counts_dates():
    payload = [
        {"date": " 2026-08-01 "},
        {"published_at": ""},
        "skip",
        {"published": "2026-08-02T10:00:00Z"},
        {"publishedAt": "2026-08-03"},
    ]
    assert count_news_dates(payload) == 3


def test_non_list():
    assert count_news_dates({"date": "2026-01-01"}) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"date": "2026-02-01"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["date_count"] == 1


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
