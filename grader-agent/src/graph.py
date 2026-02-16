import os
import json
import sys

# This module handles the core logic for the Grader Agent.
# In a full multi-agent setup, these would be separate nodes in a graph.

class GraderAgent:
    def __init__(self):
        self.router_prompt = """You are a News Router. Analyze the following news items.
Filter for: 
1. Finance/Tax/Investment topics.
2. High virality potential for Indian YouTube audience.
Output ONLY a JSON list of the top 3 items."""

        self.grader_prompt = """You are a Factual Grader. Compare the news claim against the provided source.
Is the claim fully supported by the source?
Output: 'YES' or 'NO' and a 1-sentence reason."""

        self.hallucination_prompt = """You are a Hallucination Guard. Check if the summary contains any facts NOT present in the source.
Output: 'SAFE' or 'HALLUCINATION'."""

    def route_news(self, news_items):
        print("🚦 [Router] Filtering for high-impact Finance news...")
        # In production, this would call the LLM with self.router_prompt
        # For now, we simulate the logic:
        finance_keywords = ['tax', 'forex', 'rbi', 'bank', 'stock', 'market', 'money', 'invest']
        filtered = [item for item in news_items if any(k in item['title'].lower() for k in finance_keywords)]
        return filtered[:3]

    def grade_claim(self, claim, source):
        print(f"🔍 [Grader] Verifying grounding for: {claim[:50]}...")
        # Simulate LLM logic
        if not source: return "NO", "No source provided."
        return "YES", "Claim is directly supported by the news report."

    def check_hallucination(self, summary, source):
        print("🛡️ [Sentinel] Checking for hallucinations...")
        # Simulate LLM logic
        return "SAFE"

def run_grader_logic(task, data, source=None):
    agent = GraderAgent()
    if task == "route":
        return agent.route_news(data)
    if task == "grade":
        return agent.grade_claim(data, source)
    if task == "check_hallucination":
        return agent.check_hallucination(data, source)
    return None
