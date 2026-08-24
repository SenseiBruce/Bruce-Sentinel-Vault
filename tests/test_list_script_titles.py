import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from list_script_titles import list_script_titles, main  # noqa: E402


def test_extracts_titles():
    payload = [
        {"project_name": " Alpha "},
        {"project_name": ""},
        "skip",
        {"project_name": "Beta"},
    ]
    assert list_script_titles(payload) == ["Alpha", "Beta"]


def test_non_list():
    assert list_script_titles({"project_name": "X"}) == []


def test_cli_example():
    assert main([]) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(json.dumps([{"project_name": "Demo"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["titles"] == ["Demo"]


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
