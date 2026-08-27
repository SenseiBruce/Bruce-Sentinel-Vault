import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_scripts import count_scripts, main  # noqa: E402


def test_counts_list():
    assert count_scripts([{}, {}]) == 2
    assert count_scripts({}) == 0


def test_cli_example():
    assert main([]) == 0


def test_cli_custom(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(json.dumps([{"project_name": "A"}]), encoding="utf-8")
    assert main([str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["scripts"] == 1


def test_missing(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1
