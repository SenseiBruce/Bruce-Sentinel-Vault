from pathlib import Path

from scripts.list_scene_image_prompts import list_scene_image_prompts, main


def test_list_scene_image_prompts():
    lines = list_scene_image_prompts(
        {
            "scenes": [
                {"image_prompt": "  A rupee chart "},
                {"narration": "no prompt"},
            ]
        }
    )
    assert lines == ["A rupee chart"]


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text('{"scenes": [{"image_prompt": "neon city"}]}', encoding="utf-8")
    assert main(["--scripts-file", str(path)]) == 0
    out = capsys.readouterr().out
    assert '"count": 1' in out
    assert "neon city" in out
