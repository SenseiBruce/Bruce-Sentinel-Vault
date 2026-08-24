"""Format grader verdicts as JSON or plain text."""

from __future__ import annotations


def format_grader_text(results: list[dict]) -> str:
    if not results:
        return "No grader results."
    lines = []
    for item in results:
        verdict = item.get("verdict", "UNKNOWN")
        title = item.get("title", "")
        source = item.get("source")
        suffix = f" ({source})" if source else ""
        lines.append(f"{verdict}: {title}{suffix}")
    return "\n".join(lines)
