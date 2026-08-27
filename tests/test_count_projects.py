from pathlib import Path

from scripts.count_projects import count_projects, main


def test_count_projects_list():
    assert count_projects([{"project_name": "A"}, {"project_name": "B"}, "skip"]) == 2


def test_count_projects_object():
    assert count_projects({"scenes": []}) == 1
    assert count_projects("nope") == 0


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text('[{"project_name": "One"}, {"project_name": "Two"}]', encoding="utf-8")
    assert main(["--scripts-file", str(path)]) == 0
    assert '"project_count": 2' in capsys.readouterr().out
