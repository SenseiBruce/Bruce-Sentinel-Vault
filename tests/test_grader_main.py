"""CLI wiring tests for grader-agent main."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "grader-agent" / "src"))
sys.path.insert(0, str(ROOT))

from main import load_news_items  # noqa: E402


def test_load_news_items_from_file(tmp_path: Path):
    path = tmp_path / "news.json"
    path.write_text(
        json.dumps([{"title": "RBI rate pause", "source": "Mint"}]),
        encoding="utf-8",
    )
    items = load_news_items(str(path))
    assert items[0]["title"] == "RBI rate pause"


def test_main_writes_output_with_mocked_logic(tmp_path: Path, monkeypatch):
    import main as main_mod

    monkeypatch.setattr(
        main_mod,
        "run_grader_logic",
        lambda task, data, source=None: (
            [{"title": "RBI", "source": "x"}]
            if task == "route"
            else (("YES", "ok") if task == "grade" else "SAFE")
        ),
    )
    out = tmp_path / "out.json"
    assert main_mod.main(["--input", "missing.json", "--output", str(out)]) == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload[0]["verdict"] == "PASSED"


def test_main_text_format(tmp_path: Path, monkeypatch, capsys):
    import main as main_mod

    monkeypatch.setattr(
        main_mod,
        "run_grader_logic",
        lambda task, data, source=None: (
            [{"title": "RBI", "source": "x"}]
            if task == "route"
            else (("YES", "ok") if task == "grade" else "SAFE")
        ),
    )
    out = tmp_path / "out.json"
    assert main_mod.main(["--input", "missing.json", "--output", str(out), "--format", "text"]) == 0
    assert "PASSED: RBI" in capsys.readouterr().out
