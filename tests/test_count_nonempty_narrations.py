from pathlib import Path

from scripts.count_nonempty_narrations import count_nonempty_narrations, main


def test_count_nonempty_narrations():
    assert (
        count_nonempty_narrations(
            {
                "scenes": [
                    {"narration": "Open on the chart"},
                    {"narration": "  "},
                    {},
                ]
            }
        )
        == 1
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"narration": ""}, {"narration": "ok"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"nonempty_narration_count": 1' in capsys.readouterr().out
