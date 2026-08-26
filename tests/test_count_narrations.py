from pathlib import Path

from scripts.count_narrations import count_narrations, main


def test_count_narrations():
    assert (
        count_narrations(
            {
                "scenes": [
                    {"narration": "  Hello markets "},
                    {"image_prompt": "no narration"},
                    {"narration": ""},
                ]
            }
        )
        == 1
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"narration": "one"}, {"narration": "two"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"narration_count": 2' in capsys.readouterr().out
