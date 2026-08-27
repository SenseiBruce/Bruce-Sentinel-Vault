from pathlib import Path

from scripts.count_blank_names import count_blank_names, main


def test_count_blank_names():
    assert (
        count_blank_names(
            [
                {"project_name": "Sample Finance Explainer"},
                {"project_name": "  "},
                {},
            ]
        )
        == 2
    )


def test_cli(tmp_path: Path, capsys):
    path = tmp_path / "scripts.json"
    path.write_text(
        '[{"project_name": ""}, {"project_name": "ok"}]',
        encoding="utf-8",
    )
    assert main(["--scripts-file", str(path)]) == 0
    assert '"blank_name_count": 1' in capsys.readouterr().out
