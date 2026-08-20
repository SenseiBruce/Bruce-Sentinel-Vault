"""CLI entrypoint for the Grader Agent fact-checking pipeline."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

# Allow running as `python grader-agent/src/main.py` from repo root or this dir.
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from graph import run_grader_logic
from schemas import SchemaError, parse_news_items

from sentinel_logging import configure_logging

logger = logging.getLogger(__name__)


def load_news_items(input_file: str = "news_input.json") -> list[dict]:
    if os.path.exists(input_file):
        with open(input_file, encoding="utf-8") as handle:
            raw = json.load(handle)
    else:
        raw = [
            {"title": "India's Forex reserves hit record high", "source": "RBI Report"},
            {
                "title": "New 12.75L Tax Slab Confirmed by Ministry",
                "source": "Finance Bill 2026",
            },
            {"title": "DeepSeek Coder v3 released", "source": "TechCrunch"},
            {
                "title": "RBI bans new credit card issuance for HDFC",
                "source": "News18",
            },
        ]
    try:
        items = parse_news_items(raw)
    except SchemaError as exc:
        raise SystemExit(f"Invalid news input: {exc}") from exc
    return [item.model_dump() for item in items]


def write_results(path: str, results: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)


def main(argv=None) -> int:
    configure_logging()
    logger.info("[Agentic Sentinel] Initializing Fact-Checking Protocol")

    news_items = load_news_items()
    routed_items = run_grader_logic("route", news_items)
    logger.info("Router selected %s relevant items", len(routed_items))

    results = []
    for item in routed_items:
        logger.info("Processing: %s", item["title"])
        status, reason = run_grader_logic("grade", item["title"], item.get("source", ""))
        h_status = run_grader_logic(
            "check_hallucination", item["title"], item.get("source", "")
        )

        if status == "YES" and h_status == "SAFE":
            logger.info("[Sentinel Verdict] PASSED: %s", reason)
            results.append({**item, "verdict": "PASSED"})
        else:
            logger.info("[Sentinel Verdict] FAILED: %s", reason)
            results.append({**item, "verdict": "FAILED"})

    write_results("grader_results.json", results)
    logger.info("Scan complete. Results saved to grader_results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
