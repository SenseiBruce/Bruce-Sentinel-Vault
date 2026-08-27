from pathlib import Path

from scripts.list_project_names import list_project_names, main


def test_list_project_names():
    assert list_project_names([{"project_name": "  Alpha  "}, {"project_name": ""}]) == ["Alpha"]
    assert list_project_names({"project_name": "Solo"}) == ["Solo"]
    assert list_project_names("nope") == []


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text('[{"project_name": "Finance"}]', encoding="utf-8")
    assert main(["--scripts-file", str(path)]) == 0
    out = capsys.readouterr().out
    assert '"count": 1' in out
    assert "Finance" in out
