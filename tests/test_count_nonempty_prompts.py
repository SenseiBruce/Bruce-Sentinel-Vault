from pathlib import Path

from scripts.count_nonempty_prompts import count_nonempty_prompts, main


def test_count_nonempty_prompts():
    assert (
        count_nonempty_prompts(
            {
                "scenes": [
                    {"image_prompt": "Close-up chart"},
                    {"narration": "ok", "image_prompt": "  "},
                    {},
                ]
            }
        )
        == 1
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"image_prompt": ""}, {"image_prompt": "ok"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"nonempty_prompt_count": 1' in capsys.readouterr().out
