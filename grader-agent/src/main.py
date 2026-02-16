import os
import json
import sys
from graph import run_grader_logic

def main():
    print("📡 [Agentic Sentinel] Initializing Fact-Checking Protocol...")
    
    # 1. Load News Input (In real use, this could be from a file or web search)
    input_file = "news_input.json"
    if os.path.exists(input_file):
        with open(input_file, "r") as f:
            news_items = json.load(f)
    else:
        # Fallback dummy news
        news_items = [
            {"title": "India's Forex reserves hit record high", "source": "RBI Report"},
            {"title": "New 12.75L Tax Slab Confirmed by Ministry", "source": "Finance Bill 2026"},
            {"title": "DeepSeek Coder v3 released", "source": "TechCrunch"},
            {"title": "RBI bans new credit card issuance for HDFC", "source": "News18"}
        ]

    # 2. Route News
    routed_items = run_grader_logic("route", news_items)
    print(f"✅ Router selected {len(routed_items)} relevant items.")

    # 3. Process & Grade
    results = []
    for item in routed_items:
        print(f"\n--- Processing: {item['title']} ---")
        
        # Grade Factual Grounding
        status, reason = run_grader_logic("grade", item['title'], item.get('source', ""))
        
        # Hallucination Check
        h_status = run_grader_logic("check_hallucination", item['title'], item.get('source', ""))
        
        if status == "YES" and h_status == "SAFE":
            print(f"🛡️ [Sentinel Verdict] PASSED: {reason}")
            results.append({**item, "verdict": "PASSED"})
        else:
            print(f"❌ [Sentinel Verdict] FAILED: {reason}")
            results.append({**item, "verdict": "FAILED"})

    # 4. Export results
    with print_to_file("grader_results.json"):
        print(json.dumps(results, indent=2))
    
    print("\n🏁 Scan Complete. Results saved to grader_results.json")

class print_to_file:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, "w")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

if __name__ == "__main__":
    main()
