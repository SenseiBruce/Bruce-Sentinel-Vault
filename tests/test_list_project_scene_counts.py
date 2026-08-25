from pathlib import Path

from scripts.list_project_scene_counts import list_project_scene_counts, main


def test_list_project_scene_counts():
    rows = list_project_scene_counts(
        [
            {"project_name": " Alpha ", "scenes": [{}, {}]},
            {"project_name": "Empty", "scenes": "nope"},
            "skip",
        ]
    )
    assert rows == [
        {"project_name": "Alpha", "scenes": 2},
        {"project_name": "Empty", "scenes": 0},
    ]


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text('{"project_name": "Solo", "scenes": [{}]}', encoding="utf-8")
    assert main(["--scripts-file", str(path)]) == 0
    out = capsys.readouterr().out
    assert '"count": 1' in out
    assert '"scenes": 1' in out
