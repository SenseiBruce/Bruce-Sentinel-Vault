from pathlib import Path

from scripts.total_image_prompts import count_image_prompts, main


def test_count_image_prompts():
    total = count_image_prompts(
        {
            "scenes": [
                {"image_prompt": "  A rupee chart "},
                {"narration": "no prompt"},
                {"image_prompt": ""},
            ]
        }
    )
    assert total == 1


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"image_prompt": "neon city"}, {"image_prompt": "market floor"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"total_image_prompts": 2' in capsys.readouterr().out
