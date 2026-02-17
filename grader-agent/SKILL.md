---
name: grader-agent
description: Multi-agent workflow for Fact-Checking, Routing, and Hallucination grading based on the Agentic RAG logic.
metadata:
  {
    "openclaw": { "emoji": "🛡️", "requires": { "anyBins": ["python3"] } },
  }
---

# Grader Agent (Sentinel)

The Grader Agent is a multi-agent workflow designed to ensure the highest factual accuracy for our content creation pipeline. It acts as the "Sentinel" for Capital Architects.

## Status: PRODUCTION READY ✅

This skill provides a three-stage pipeline:
1. **Router:** Identifies high-impact Finance/Tax topics.
2. **Grader:** Verifies factual grounding against provided sources using Gemini.
3. **Hallucination Guard:** Ensures generated content doesn't invent "facts".

## Components
1. **Router:** Filters incoming news/data for relevance and virality potential.
2. **Grader:** Compares claims against source text to verify grounding using real LLM analysis.
3. **Hallucination Guard:** Ensures the final output doesn't contain invented facts.

## Usage
Run the main script to process a batch of news items:

```bash
python3 skills/grader-agent/src/main.py
```

### Custom Input
Place a `news_input.json` in the workspace with the following format:
```json
[
  {
    "title": "News headline here",
    "source": "Supporting text or source name"
  }
]
```

## Integration
This skill is used by the main agent during heartbeats or manual research sessions to validate "Hot Topics" before they are passed to the `VideoFactory`.

## Logic Update (Feb 17):
- Replaced mock logic with real **Gemini Pro** integration in `graph.py`.
- Added path resolution for core project classes.
- Integrated `security_utils` for input sanitization in core classes.

## Logic Source
Based on the Agentic RAG principles (Router -> Retriever -> Grader -> Hallucination Check).
