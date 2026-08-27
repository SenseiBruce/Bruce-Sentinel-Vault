from pathlib import Path

from scripts.count_empty_scenes import count_empty_scenes, main


def test_count_empty_scenes():
    assert (
        count_empty_scenes(
            {
                "scenes": [
                    {"narration": "Hello", "image_prompt": ""},
                    {"narration": "  ", "image_prompt": "   "},
                    {"image_prompt": "only prompt"},
                    {},
                ]
            }
        )
        == 2
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '{"scenes": [{"narration": ""}, {"narration": "ok", "image_prompt": "ok"}]}',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"empty_scene_count": 1' in capsys.readouterr().out
