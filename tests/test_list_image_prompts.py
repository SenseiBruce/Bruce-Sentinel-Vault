from pathlib import Path

from scripts.list_image_prompts import list_image_prompts, main


def test_list_image_prompts_from_example():
    payload = [
        {
            "project_name": "Demo",
            "scenes": [
                {"narration": "a", "image_prompt": "  glowing rupee  "},
                {"narration": "b", "image_prompt": ""},
                {"narration": "c"},
            ],
        }
    ]
    assert list_image_prompts(payload) == ["glowing rupee"]
    assert list_image_prompts({"scenes": [{"image_prompt": "solo"}]}) == ["solo"]
    assert list_image_prompts("nope") == []


def test_cli_reads_scripts_file(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '[{"project_name": "X", "scenes": [{"image_prompt": "chart"}]}]',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    out = capsys.readouterr().out
    assert '"count": 1' in out
    assert "chart" in out
