import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_scripts_json import main, validate_file  # noqa: E402


def test_example_scripts_are_valid():
    code, message = validate_file(ROOT / "scripts.example.json")
    assert code == 0
    assert "valid" in message


def test_invalid_scripts(tmp_path: Path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps([{"project_name": "   ", "scenes": []}]), encoding="utf-8")
    code, message = validate_file(path)
    assert code == 1
    assert "Invalid" in message


def test_cli_success():
    assert main([str(ROOT / "scripts.example.json")]) == 0


def test_missing_file(tmp_path: Path):
    code, message = validate_file(tmp_path / "nope.json")
    assert code == 1
    assert "not found" in message.lower()


def test_invalid_json(tmp_path: Path):
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    code, message = validate_file(path)
    assert code == 1
    assert "Invalid JSON" in message
