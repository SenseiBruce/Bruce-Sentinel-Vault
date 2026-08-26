from pathlib import Path

from scripts.count_blank_narrations import count_blank_narrations, main


def test_count_blank_narrations():
    assert (
        count_blank_narrations(
            {
                "scenes": [
                    {"narration": "Hello"},
                    {"narration": "  "},
                    {"image_prompt": "only prompt"},
                ]
            }
        )
        == 2
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"narration": ""}, {"narration": "ok"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"blank_narration_count": 1' in capsys.readouterr().out
