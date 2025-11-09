#!/usr/bin/env python3
"""
Test Gemini API connectivity and response
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_gemini_connection():
    """Test basic Gemini API connectivity"""

    api_key = os.getenv("GEMINI_API_KEY", "")

    print("=" * 80)
    print("TESTING GEMINI API CONNECTION")
    print("=" * 80)

    if not api_key or api_key == "your_gemini_api_key_here":
        print("\n❌ ERROR: GEMINI_API_KEY not configured in .env")
        return False

    print(f"\n✓ API Key configured: {api_key[:20]}...")

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Test with simple prompt (using Gemini 2.5 Flash)
        model = genai.GenerativeModel('gemini-2.5-flash')

        print("\n📡 Sending test request to Gemini API...")

        response = model.generate_content("Respond with only: 'API Working'")

        print(f"\n✅ SUCCESS! Gemini API Response:")
        print(f"   {response.text}")

        # Now test with emergency classification
        print("\n" + "=" * 80)
        print("TESTING EMERGENCY CLASSIFICATION")
        print("=" * 80)

        test_prompt = """You are a medical triage AI. Classify this emergency.

Emergency: "Person collapsed and isn't breathing"

Respond with ONLY a JSON object (no markdown):
{
  "emergency_type": "cardiac_arrest",
  "severity": "CRITICAL",
  "confidence": 0.95,
  "reasoning": "Collapse with no breathing indicates cardiac arrest"
}"""

        print("\n📡 Sending emergency classification test...")

        response = model.generate_content(test_prompt)
        response_text = response.text.strip()

        # Clean markdown if present
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        print(f"\n✅ Gemini Classification Response:")
        print(response_text)

        # Try to parse as JSON
        import json
        try:
            result = json.loads(response_text)
            print(f"\n✅ Valid JSON response!")
            print(f"   Emergency Type: {result.get('emergency_type')}")
            print(f"   Severity: {result.get('severity')}")
            print(f"   Confidence: {result.get('confidence')}")

            return True

        except json.JSONDecodeError as e:
            print(f"\n⚠️  Response is not valid JSON: {e}")
            print(f"   But Gemini API is responding!")
            return True

    except Exception as e:
        print(f"\n❌ ERROR: Gemini API failed")
        print(f"   Error: {str(e)}")
        print(f"\n   Common issues:")
        print(f"   1. Invalid API key")
        print(f"   2. API quota exceeded")
        print(f"   3. Network connectivity")
        print(f"   4. API key lacks permissions")
        return False

if __name__ == "__main__":
    success = test_gemini_connection()

    if success:
        print("\n" + "=" * 80)
        print("✅ GEMINI API IS WORKING CORRECTLY")
        print("=" * 80)
        print("\nYou can now proceed with testing the enhanced LLM system.")
    else:
        print("\n" + "=" * 80)
        print("❌ GEMINI API SETUP NEEDS ATTENTION")
        print("=" * 80)
        print("\nPlease check:")
        print("1. Your .env file has correct GEMINI_API_KEY")
        print("2. API key has permissions enabled")
        print("3. You're not exceeding quota limits")

    print()
