# backend/services/analyzer.py
import time


def analyze_transcript(transcript: str) -> dict:
    """Simulates running a full analysis pipeline on a transcript."""
    print("STEP 2: Analyzing transcript with LLM...")
    time.sleep(5)  # Simulate LLM processing time

    analysis = {
        "summary": "Client was concerned about price but scheduled a demo.",
        "sentiment": "NEUTRAL",
        "entities": [
            {"text": "price", "type": "KEYWORD"},
            {"text": "next Tuesday", "type": "DATE"},
        ],
        "full_transcript": transcript,
    }
    print("   -> Analysis complete.")
    return analysis
