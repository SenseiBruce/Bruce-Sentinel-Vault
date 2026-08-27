from pathlib import Path

from scripts.count_blank_prompts import count_blank_prompts, main


def test_count_blank_prompts():
    assert (
        count_blank_prompts(
            {
                "scenes": [
                    {"image_prompt": "Close-up chart"},
                    {"narration": "ok", "image_prompt": "  "},
                    {},
                ]
            }
        )
        == 2
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"image_prompt": ""}, {"image_prompt": "ok"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"blank_prompt_count": 1' in capsys.readouterr().out
