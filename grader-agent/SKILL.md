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

## Components
1. **Router:** Filters incoming news/data for relevance and virality potential.
2. **Grader:** Compares claims against source text to verify grounding.
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

## Logic Source
Based on the Agentic RAG principles (Router -> Retriever -> Grader -> Hallucination Check).
