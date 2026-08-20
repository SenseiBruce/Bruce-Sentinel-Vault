"""Unit tests for GraderAgent routing and grading (mocked Gemini + DDGS)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "grader-agent" / "src"))

from graph import GraderAgent, run_grader_logic  # noqa: E402


class FakeGemini:
    def __init__(self, response: str):
        self.response = response
        self.calls: list[list[dict]] = []

    def generate_response(self, messages):
        self.calls.append(messages)
        return self.response


class FakeDDGS:
    def __init__(self, results=None, raise_error: bool = False):
        self.results = results or [{"body": "Source body about forex reserves."}]
        self.raise_error = raise_error
        self.queries: list[str] = []

    def text(self, query, max_results=3):
        self.queries.append(query)
        if self.raise_error:
            raise RuntimeError("search down")
        return self.results[:max_results]


SAMPLE_NEWS = [
    {"title": "India's Forex reserves hit record high", "source": "RBI Report"},
    {"title": "DeepSeek Coder v3 released", "source": "TechCrunch"},
    {"title": "RBI bans new credit card issuance for HDFC", "source": "News18"},
]


def test_route_news_parses_json_list_from_gemini():
    payload = [
        {
            "title": "India's Forex reserves hit record high",
            "source": "RBI Report",
            "reasoning": "Finance + viral",
        }
    ]
    gemini = FakeGemini(f"Here you go:\n{json.dumps(payload)}\n")
    agent = GraderAgent(gemini=gemini, ddgs=FakeDDGS())

    routed = agent.route_news(SAMPLE_NEWS)

    assert routed == payload
    assert len(gemini.calls) == 1
    assert "News Router" in gemini.calls[0][0]["content"]


def test_route_news_falls_back_to_keywords_on_bad_json():
    gemini = FakeGemini("not-json-at-all")
    agent = GraderAgent(gemini=gemini, ddgs=FakeDDGS())

    routed = agent.route_news(SAMPLE_NEWS)

    titles = [item["title"] for item in routed]
    assert "India's Forex reserves hit record high" in titles
    assert "RBI bans new credit card issuance for HDFC" in titles
    assert "DeepSeek Coder v3 released" not in titles
    assert len(routed) <= 3


def test_grade_claim_yes_shape():
    gemini = FakeGemini("YES Claim matches the RBI source.")
    agent = GraderAgent(gemini=gemini, ddgs=FakeDDGS())

    status, reason = agent.grade_claim(
        "Forex reserves hit a record",
        source="RBI says forex reserves hit a record.",
    )

    assert status == "YES"
    assert "matches" in reason.lower()


def test_grade_claim_no_shape_and_retriever_used_when_source_missing():
    gemini = FakeGemini("NO Unsupported by retrieved context.")
    ddgs = FakeDDGS(results=[{"body": "Unrelated weather report."}])
    agent = GraderAgent(gemini=gemini, ddgs=ddgs)

    status, reason = agent.grade_claim("Forex reserves hit a record", source=None)

    assert status == "NO"
    assert "Unsupported" in reason
    assert ddgs.queries == ["Forex reserves hit a record"]


def test_check_hallucination_safe_and_unsafe():
    safe_agent = GraderAgent(gemini=FakeGemini("SAFE"), ddgs=FakeDDGS())
    bad_agent = GraderAgent(
        gemini=FakeGemini("HALLUCINATION invented number"),
        ddgs=FakeDDGS(),
    )

    assert safe_agent.check_hallucination("summary", "source") == "SAFE"
    assert bad_agent.check_hallucination("summary", "source") == "HALLUCINATION"


def test_retrieve_context_returns_empty_on_search_error():
    agent = GraderAgent(gemini=FakeGemini(""), ddgs=FakeDDGS(raise_error=True))
    assert agent.retrieve_context("anything") == ""


def test_run_grader_logic_dispatches_with_injected_agent():
    gemini = FakeGemini("YES Grounded.")
    agent = GraderAgent(gemini=gemini, ddgs=FakeDDGS())

    status, reason = run_grader_logic(
        "grade",
        "claim",
        source="source",
        agent=agent,
    )
    assert status == "YES"
    assert reason == "Grounded."
    assert run_grader_logic("unknown", [], agent=agent) is None
