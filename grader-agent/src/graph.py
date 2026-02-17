import os
import json
import sys

# Add path to common classes
sys.path.append("/Users/kinshuk.prasad/Documents/Project X/gemini-youtube-automation/src/classes")
from Gemini import Gemini
from duckduckgo_search import DDGS

# This module handles the core logic for the Grader Agent.
# It uses the Gemini class for factual verification and routing.

class GraderAgent:
    def __init__(self):
        self.gemini = Gemini()
        self.ddgs = DDGS()
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

    def retrieve_context(self, query):
        print(f"📡 [Retriever] Searching for: {query}...")
        try:
            results = self.ddgs.text(query, max_results=3)
            return "\n".join([r['body'] for r in results])
        except Exception as e:
            print(f"Search error: {e}")
            return ""

    def route_news(self, news_items):
        print("🚦 [Router] Filtering for high-impact Finance news...")
        prompt = f"{self.router_prompt}\n\nNews Items: {json.dumps(news_items)}"
        response = self.gemini.generate_response([{"role": "user", "content": prompt}])
        
        try:
            # Try to extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end != -1:
                return json.loads(response[json_start:json_end])
            return []
        except Exception as e:
            print(f"Error parsing router JSON: {e}")
            # Fallback keyword logic
            finance_keywords = ['tax', 'forex', 'rbi', 'bank', 'stock', 'market', 'money', 'invest']
            filtered = [item for item in news_items if any(k in item['title'].lower() for k in finance_keywords)]
            return filtered[:3]

    def grade_claim(self, claim, source=None):
        print(f"🔍 [Grader] Verifying grounding for: {claim[:50]}...")
        
        # If no source provided, use Retriever
        if not source:
            source = self.retrieve_context(claim)
            
        prompt = self.grader_prompt.format(claim=claim, source=source)
        response = self.gemini.generate_response([{"role": "user", "content": prompt}])
        
        if response.startswith("YES"):
            return "YES", response[3:].strip()
        return "NO", response.strip()

    def check_hallucination(self, summary, source):
        print("🛡️ [Sentinel] Checking for hallucinations...")
        prompt = self.hallucination_prompt.format(summary=summary, source=source)
        response = self.gemini.generate_response([{"role": "user", "content": prompt}])
        
        if "SAFE" in response.upper():
            return "SAFE"
        return "HALLUCINATION"

def run_grader_logic(task, data, source=None):
    agent = GraderAgent()
    if task == "route":
        return agent.route_news(data)
    if task == "grade":
        return agent.grade_claim(data, source)
    if task == "check_hallucination":
        return agent.check_hallucination(data, source)
    return None
