#!/usr/bin/env python3
"""
Test script for LLM functionality (Gemini API)
"""
import os
from dotenv import load_dotenv
from app.services.llm import classify_and_plan

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API with sample emergency scenarios"""

    print("=" * 60)
    print("Testing MediAssist AI - LLM Functionality (Gemini API)")
    print("=" * 60)

    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("\n⚠️  WARNING: GEMINI_API_KEY not set in .env file")
        print("The system will fall back to keyword matching.\n")
    else:
        print(f"\n✓ GEMINI_API_KEY found: {api_key[:20]}...\n")

    # Test scenarios
    test_cases = [
        {
            "description": "Person collapsed and not breathing",
            "age_group": "adult"
        },
        {
            "description": "Someone is choking on food",
            "age_group": "adult"
        },
        {
            "description": "Severe bleeding from a cut on the arm",
            "age_group": "adult"
        },
        {
            "description": "Got burned by hot water",
            "age_group": "child"
        },
        {
            "description": "Person fainted and fell down",
            "age_group": "elderly"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"Test Case {i}: {test['description']}")
        print(f"Age Group: {test['age_group']}")
        print("-" * 60)

        try:
            result = classify_and_plan(
                text=test['description'],
                locale="en",
                age_group=test['age_group']
            )

            print(f"\n🔍 Classification Result:")
            print(f"  Type: {result.get('type', 'unknown')}")
            print(f"  Severity: {result.get('severity', 'unknown')}")

            if 'ai_reasoning' in result:
                print(f"  AI Reasoning: {result['ai_reasoning']}")

            print(f"\n📋 First Aid Steps ({len(result.get('steps', []))} steps):")
            for idx, step in enumerate(result.get('steps', []), 1):
                print(f"  {idx}. {step['title']}")
                print(f"     → {step['detail']}")
                if 'timer_s' in step:
                    print(f"     ⏱️  {step['timer_s']}s")
                if 'cadence_bpm' in step:
                    print(f"     💓 {step['cadence_bpm']} BPM")

            print(f"\n🎒 Items to Bring: {', '.join(result.get('bring', []))}")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_gemini_api()
