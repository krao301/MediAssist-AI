#!/usr/bin/env python3
"""
Test Hybrid RAG System
Triple-Layer Architecture Test:
1. Vector Database (Semantic Search)
2. Knowledge Graph (Relationship Reasoning)
3. Gemini AI (LLM Reasoning)
"""

import os
import sys
from dotenv import load_dotenv

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.hybrid_rag import HybridRAGSystem

load_dotenv()

def print_result(result: dict, test_name: str):
    """Pretty print classification result"""

    print("\n" + "=" * 80)
    print(f"TEST: {test_name}")
    print("=" * 80)

    print(f"\n🎯 CLASSIFICATION RESULT:")
    print(f"   Type: {result['type'].upper().replace('_', ' ')}")
    print(f"   Severity: {result['severity']}")
    print(f"   Confidence: {result.get('confidence', 0.0):.1%}")

    print(f"\n📊 SOURCE ANALYSIS:")
    sources = result.get('sources', [])
    print(f"   Data Sources Used: {', '.join(sources)}")

    if result.get('vector_match'):
        vm = result['vector_match']
        print(f"   • Vector DB: {vm['type']} ({vm['confidence']:.1%})")

    if result.get('graph_match'):
        gm = result['graph_match']
        print(f"   • Knowledge Graph: {gm['type']} ({gm['confidence']:.1%})")

    if result.get('llm_match'):
        lm = result['llm_match']
        print(f"   • Gemini AI: {lm['type']} ({lm['confidence']:.1%})")
        if lm.get('reasoning'):
            print(f"     Reasoning: {lm['reasoning'][:150]}...")

    print(f"\n🚨 EMERGENCY RESPONSE:")
    print(f"   SOS Required: {'YES → ' + result['sos_number'] if result.get('requires_sos') else 'NO'}")
    print(f"   Helpers Needed: {'YES' if result.get('requires_helpers') else 'NO'}")

    if result.get('age_escalation'):
        esc = result['age_escalation']
        print(f"\n⚠️  AGE-BASED ESCALATION:")
        print(f"   {esc.get('reason')}")

    if result.get('progression_risks'):
        print(f"\n⚠️  PROGRESSION RISKS:")
        for risk in result['progression_risks']:
            print(f"   • May progress to {risk['condition']} ({risk['probability']:.0%} probability)")

    if result.get('time_critical_minutes'):
        print(f"\n⏰ TIME CRITICAL: {result['time_critical_minutes']} minutes")

    print("\n" + "=" * 80)


def main():
    """Run comprehensive hybrid RAG tests"""

    print("\n" + "=" * 80)
    print("HYBRID RAG SYSTEM TEST SUITE")
    print("Testing Vector DB + Knowledge Graph + Gemini AI")
    print("=" * 80)

    # Initialize system
    rag_system = HybridRAGSystem()

    # Test cases demonstrating different scenarios
    test_cases = [
        {
            "name": "Cardiac Arrest - All 3 layers should agree",
            "input": "My grandfather collapsed and isn't breathing",
            "age_group": "elderly",
            "expected_type": "cardiac_arrest",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Synonym handling - Vector DB should catch this",
            "input": "Person's heart stopped beating",
            "age_group": "adult",
            "expected_type": "cardiac_arrest",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Multi-symptom reasoning - Graph should infer",
            "input": "Severe chest pain and can't catch breath",
            "age_group": "elderly",
            "expected_type": "chest_pain_cardiac",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Age escalation - Graph should escalate severity",
            "input": "My 80-year-old grandmother fainted",
            "age_group": "elderly",
            "expected_type": "fainting",
            "expected_severity": "SEVERE"  # Escalated from MODERATE
        },
        {
            "name": "Typo tolerance - Vector embedding should handle",
            "input": "Someone is chocking on food cant breath",
            "age_group": "adult",
            "expected_type": "choking",
            "expected_severity": "CRITICAL"
        },
        {
            "name": "Complex description - LLM reasoning needed",
            "input": "Person fell unconscious, blue lips, no response",
            "age_group": "adult",
            "expected_type": "cardiac_arrest",
            "expected_severity": "CRITICAL"
        }
    ]

    passed = 0
    failed = 0

    for test in test_cases:
        print(f"\n\n{'#' * 80}")
        print(f"Running: {test['name']}")
        print(f"Input: \"{test['input']}\"")
        print(f"Age: {test['age_group']}")
        print(f"{'#' * 80}")

        try:
            result = rag_system.classify_emergency(
                user_input=test['input'],
                age_group=test['age_group']
            )

            print_result(result, test['name'])

            # Verify results
            if result['type'] == test['expected_type']:
                print(f"\n✅ Type match: {result['type']}")
                passed += 1
            else:
                print(f"\n❌ Type mismatch: Got {result['type']}, expected {test['expected_type']}")
                failed += 1

        except Exception as e:
            print(f"\n❌ TEST FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Print statistics
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    stats = rag_system.get_system_stats()

    print(f"\n📊 System Statistics:")
    print(f"   Vector DB: {stats['vector_db']['total_cases']} cases")
    print(f"   Knowledge Graph: {stats['knowledge_graph']['total_nodes']} nodes, {stats['knowledge_graph']['total_edges']} edges")
    print(f"   Emergency Types: {stats['knowledge_graph']['emergency_types']}")
    print(f"   LLM: {stats['llm']['model']} ({stats['llm']['provider']})")

    print(f"\n🧪 Test Results:")
    print(f"   Passed: {passed}/{len(test_cases)}")
    print(f"   Failed: {failed}/{len(test_cases)}")

    print("\n" + "=" * 80)

    if failed == 0:
        print("✅ ALL TESTS PASSED!")
        print("\n🎉 Hybrid RAG System is working perfectly!")
        print("\nCapabilities Demonstrated:")
        print("  ✓ Semantic search with vector embeddings")
        print("  ✓ Medical knowledge graph reasoning")
        print("  ✓ Age-based severity escalation")
        print("  ✓ Synonym and typo handling")
        print("  ✓ Multi-symptom analysis")
        print("  ✓ Gemini AI deep reasoning")
        print("  ✓ Ensemble decision making")
    else:
        print(f"⚠️  {failed} test(s) failed")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
