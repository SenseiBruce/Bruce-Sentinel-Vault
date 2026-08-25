import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from total_narration_words import main, summarize  # noqa: E402


def test_counts_example():
    payload = json.loads((ROOT / "scripts.example.json").read_text(encoding="utf-8"))
    result = summarize(payload)
    assert result["scripts"] == 1
    assert result["scenes"] == 2
    assert result["words"] > 10


def test_empty():
    assert summarize([])["words"] == 0
    assert summarize({})["scripts"] == 0


def test_cli():
    assert main([]) == 0


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
