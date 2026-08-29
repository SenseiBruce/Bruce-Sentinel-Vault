import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_news_failed import count_news_failed, main  # noqa: E402


def test_counts_failed():
    payload = [
        {"title": "Fake tax", "verdict": "failed"},
        {"title": "RBI pause", "verdict": "PASSED"},
        {"verdict": "FAILED"},
        "skip",
        {"title": "Rumor", "verdict": "  FAILED  "},
    ]
    assert count_news_failed(payload) == 3


def test_non_list():
    assert count_news_failed({"verdict": "FAILED"}) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "Nope", "verdict": "FAILED"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["failed_count"] == 1


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
