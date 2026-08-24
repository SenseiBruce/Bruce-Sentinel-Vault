import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_news_json import main, validate_file  # noqa: E402


def test_valid_news(tmp_path: Path):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "RBI hold", "source": "Mint"}]), encoding="utf-8")
    code, message = validate_file(path)
    assert code == 0
    assert "1 news item" in message


def test_invalid_blank_title(tmp_path: Path):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "   "}]), encoding="utf-8")
    code, message = validate_file(path)
    assert code == 1
    assert "Invalid" in message


def test_cli_success(tmp_path: Path):
    path = tmp_path / "news.json"
    path.write_text(json.dumps([{"title": "Tax update"}]), encoding="utf-8")
    assert main([str(path)]) == 0


def test_missing_file(tmp_path: Path):
    code, message = validate_file(tmp_path / "nope.json")
    assert code == 1
    assert "not found" in message.lower()
