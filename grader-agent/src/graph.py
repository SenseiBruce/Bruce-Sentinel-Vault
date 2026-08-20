"""Core logic for the Grader Agent (route / grade / hallucination check)."""

from __future__ import annotations

import json
import logging
from typing import Any

from duckduckgo_search import DDGS
from gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class GraderAgent:
    def __init__(self, gemini=None, ddgs=None):
        self.gemini = gemini if gemini is not None else GeminiClient()
        self.ddgs = ddgs if ddgs is not None else DDGS()
        self.router_prompt = """You are a News Router. Analyze the following news items.
Filter for: 
1. Finance/Tax/Investment topics.
2. High virality potential for Indian YouTube audience.
Output ONLY a JSON list of the top 3 items. Include keys: title, source, reasoning."""

        self.grader_prompt = """You are a Factual Grader. Compare the news claim against the provided source.
Claim: {claim}
Source: {source}
Is the claim fully supported by the source?
Output: 'YES' or 'NO' and a 1-sentence reason."""

        self.hallucination_prompt = """You are a Hallucination Guard. Check if the summary contains any facts NOT present in the source.
Summary: {summary}
Source: {source}
Output: 'SAFE' or 'HALLUCINATION'."""

    def retrieve_context(self, query: str) -> str:
        logger.info("[Retriever] Searching for: %s", query)
        try:
            results = self.ddgs.text(query, max_results=3)
            return "\n".join([r["body"] for r in results])
        except Exception:
            logger.exception("Search error for query=%s", query)
            return ""

    def route_news(self, news_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        logger.info("[Router] Filtering for high-impact Finance news")
        prompt = f"{self.router_prompt}\n\nNews Items: {json.dumps(news_items)}"
        response = self.gemini.generate_response([{"role": "user", "content": prompt}])

        try:
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            if json_start != -1 and json_end != -1:
                parsed = json.loads(response[json_start:json_end])
                if isinstance(parsed, list) and parsed:
                    return parsed
        except Exception:
            logger.exception("Error parsing router JSON; using keyword fallback")

        return self._keyword_route(news_items)

    def _keyword_route(self, news_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        finance_keywords = [
            "tax",
            "forex",
            "rbi",
            "bank",
            "stock",
            "market",
            "money",
            "invest",
        ]
        filtered = [
            item
            for item in news_items
            if any(k in item["title"].lower() for k in finance_keywords)
        ]
        return filtered[:3]

    def grade_claim(self, claim: str, source: str | None = None) -> tuple[str, str]:
        logger.info("[Grader] Verifying grounding for: %s", claim[:50])

        if not source:
            source = self.retrieve_context(claim)

        prompt = self.grader_prompt.format(claim=claim, source=source)
        response = self.gemini.generate_response([{"role": "user", "content": prompt}])

        if response.startswith("YES"):
            return "YES", response[3:].strip()
        return "NO", response.strip()

    def check_hallucination(self, summary: str, source: str) -> str:
        logger.info("[Sentinel] Checking for hallucinations")
        prompt = self.hallucination_prompt.format(summary=summary, source=source)
        response = self.gemini.generate_response([{"role": "user", "content": prompt}])

        if "SAFE" in response.upper():
            return "SAFE"
        return "HALLUCINATION"


def run_grader_logic(task: str, data, source=None, agent: GraderAgent | None = None):
    allowed = {"route", "grade", "check_hallucination"}
    if task not in allowed:
        raise ValueError(f"unknown grader task: {task!r}; expected one of {sorted(allowed)}")
    agent = agent or GraderAgent()
    if task == "route":
        return agent.route_news(data)
    if task == "grade":
        return agent.grade_claim(data, source)
    return agent.check_hallucination(data, source)
