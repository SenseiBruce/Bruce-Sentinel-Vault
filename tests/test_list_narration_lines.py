from pathlib import Path

from scripts.list_narration_lines import list_narration_lines, main


def test_list_narration_lines():
    assert list_narration_lines([{"scenes": [{"narration": "  Hello.  "}, {"narration": ""}]}]) == [
        "Hello."
    ]
    assert list_narration_lines({"scenes": [{"narration": "Solo"}]}) == ["Solo"]
    assert list_narration_lines("nope") == []


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text('[{"scenes": [{"narration": "Markets opened higher."}]}]', encoding="utf-8")
    assert main(["--scripts-file", str(path)]) == 0
    out = capsys.readouterr().out
    assert '"count": 1' in out
    assert "Markets opened higher." in out
