import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_news_verdicts import count_news_verdicts, main  # noqa: E402


def test_counts_verdicts():
    payload = [
        {"verdict": "  PASSED  "},
        {"verdict": ""},
        "skip",
        {"verdict": "FAILED"},
        {"title": "no verdict"},
    ]
    assert count_news_verdicts(payload) == 2


def test_non_list():
    assert count_news_verdicts({"verdict": "PASSED"}) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"verdict": "PASSED"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["verdict_count"] == 1


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
