"""CLI entrypoint for the Grader Agent fact-checking pipeline."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Allow running as `python grader-agent/src/main.py` from repo root or this dir.
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from grader_format import format_grader_text
from graph import run_grader_logic
from schemas import SchemaError, parse_news_items

from sentinel_logging import configure_logging
from sentinel_metrics import MetricsRegistry

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


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = argparse.ArgumentParser(description="Grader Agent fact-checking pipeline")
    parser.add_argument(
        "--input",
        default="news_input.json",
        help="Path to news JSON list (falls back to built-in samples if missing)",
    )
    parser.add_argument(
        "--output",
        default="grader_results.json",
        help="Where to write verdict JSON",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Print JSON (default) or a text verdict list to stdout",
    )
    args = parser.parse_args(argv)

    metrics = MetricsRegistry()
    logger.info("[Agentic Sentinel] Initializing Fact-Checking Protocol")

    news_items = load_news_items(args.input)
    routed_items = run_grader_logic("route", news_items)
    metrics.incr("grader.routed", len(routed_items))
    logger.info("Router selected %s relevant items", len(routed_items))

    results = []
    for item in routed_items:
        logger.info("Processing: %s", item["title"])
        status, reason = run_grader_logic("grade", item["title"], item.get("source", ""))
        h_status = run_grader_logic("check_hallucination", item["title"], item.get("source", ""))

        if status == "YES" and h_status == "SAFE":
            logger.info("[Sentinel Verdict] PASSED: %s", reason)
            metrics.incr("grader.passed")
            results.append({**item, "verdict": "PASSED"})
        else:
            logger.info("[Sentinel Verdict] FAILED: %s", reason)
            metrics.incr("grader.failed")
            results.append({**item, "verdict": "FAILED"})

    write_results(args.output, results)
    if args.format == "text":
        print(format_grader_text(results))
    logger.info(
        "Scan complete. Results=%s metrics=%s",
        args.output,
        metrics.snapshot(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
