import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from count_script_scenes import count_script_scenes, main  # noqa: E402


def test_counts_scenes_across_scripts():
    payload = [
        {"project_name": "A", "scenes": [{}, {}]},
        {"project_name": "B", "scenes": [{}]},
    ]
    summary = count_script_scenes(payload)
    assert summary["scripts"] == 2
    assert summary["scenes"] == 3
    assert summary["entries"][0]["project_name"] == "A"


def test_non_list_payload():
    assert count_script_scenes({"scenes": []})["scenes"] == 0


def test_cli_example_file():
    assert main([]) == 0


def test_missing_file(tmp_path: Path):
    assert main([str(tmp_path / "missing.json")]) == 1


def test_cli_custom_file(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        json.dumps([{"project_name": "Demo", "scenes": [{}, {}]}]),
        encoding="utf-8",
    )
    assert main([str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["scenes"] == 2
