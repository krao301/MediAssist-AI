"""
First Aid Instruction Generator
Generates step-by-step instructions for MINOR emergencies
Uses LLM to provide context-aware guidance
"""

import os
import google.generativeai as genai
from typing import Dict, List, Any


def generate_first_aid_instructions(
    emergency_type: str,
    severity: str,
    user_description: str = None,
    age_group: str = None
) -> Dict[str, Any]:
    """
    Generate first aid instructions for MINOR emergencies
    
    Args:
        emergency_type: Type of emergency (e.g., "minor_burn", "small_cut")
        severity: Severity level (should be MINOR/MODERATE for this function)
        user_description: Original user description of the situation
        age_group: Optional age group (child, adult, elderly)
    
    Returns:
        Dict with text instructions and voice-friendly version
    """
    
    # Initialize Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _get_fallback_instructions(emergency_type)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    # Build prompt
    prompt = f"""You are a medical first aid instructor. Generate clear, step-by-step first aid instructions.

Emergency Type: {emergency_type}
Severity: {severity}
User Description: {user_description or "Not provided"}
Age Group: {age_group or "Adult"}

Generate:
1. Brief assessment (1-2 sentences)
2. Numbered steps (5-8 steps maximum)
3. Warning signs to watch for
4. When to call 911

Format as JSON:
{{
    "assessment": "Brief assessment",
    "steps": [
        "Step 1: Do this",
        "Step 2: Do that"
    ],
    "warning_signs": ["Sign 1", "Sign 2"],
    "call_911_if": "Conditions requiring emergency services",
    "voice_text": "Natural flowing text for text-to-speech"
}}

Be concise, clear, and reassuring. Use simple language."""

    try:
        response = model.generate_content(prompt)
        
        # Parse JSON response
        import json
        result = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        
        return {
            "success": True,
            "emergency_type": emergency_type,
            "severity": severity,
            **result
        }
    
    except Exception as e:
        print(f"⚠️ Failed to generate instructions with LLM: {e}")
        return _get_fallback_instructions(emergency_type)


def _get_fallback_instructions(emergency_type: str) -> Dict[str, Any]:
    """
    Fallback instructions when LLM is unavailable
    Basic first aid for common emergencies
    """
    
    instructions_db = {
        "minor_burn": {
            "assessment": "Minor burn affecting small area without blisters or charred skin.",
            "steps": [
                "Cool the burn under cool (not cold) running water for 10-20 minutes",
                "Remove jewelry or tight clothing near the burn before swelling occurs",
                "Cover with sterile, non-stick bandage or clean cloth",
                "Take over-the-counter pain reliever if needed",
                "Keep the area clean and dry",
                "Apply aloe vera or burn cream if available"
            ],
            "warning_signs": [
                "Burn larger than 3 inches",
                "Blisters forming",
                "Signs of infection (increased pain, swelling, redness)",
                "Burn on face, hands, feet, or genitals"
            ],
            "call_911_if": "Burn is larger than palm, shows white/charred tissue, or if victim has difficulty breathing",
            "voice_text": "You have a minor burn. First, cool the affected area under running water for 10 to 20 minutes. Remove any jewelry near the burn. Cover with a clean bandage. Take pain medication if needed. Watch for blisters or signs of infection. Call 911 if the burn is larger than your palm or shows white or charred tissue."
        },
        
        "small_cut": {
            "assessment": "Minor cut with controlled bleeding and clean edges.",
            "steps": [
                "Wash your hands thoroughly with soap and water",
                "Stop the bleeding by applying gentle pressure with clean cloth",
                "Clean the wound with water (avoid hydrogen peroxide)",
                "Apply antibiotic ointment if available",
                "Cover with sterile bandage or gauze",
                "Change bandage daily and keep wound clean and dry"
            ],
            "warning_signs": [
                "Bleeding doesn't stop after 10 minutes",
                "Cut is deep or shows muscle/bone",
                "Edges won't stay together",
                "Signs of infection (redness, warmth, pus)"
            ],
            "call_911_if": "Bleeding is severe, wound is deep, or cut was caused by dirty/rusty object",
            "voice_text": "You have a small cut. First, wash your hands thoroughly. Apply pressure with a clean cloth to stop bleeding. Clean the wound with water. Apply antibiotic ointment and cover with a bandage. Change the bandage daily. Call 911 if bleeding doesn't stop after 10 minutes or if the cut is very deep."
        },
        
        "sprain": {
            "assessment": "Joint injury with pain and swelling, but joint still functional.",
            "steps": [
                "Rest: Stop activity and avoid putting weight on injured area",
                "Ice: Apply ice pack for 15-20 minutes every 2-3 hours",
                "Compression: Wrap with elastic bandage (not too tight)",
                "Elevation: Keep injured area raised above heart level",
                "Take over-the-counter pain reliever as directed",
                "Gradually resume activity after 48-72 hours"
            ],
            "warning_signs": [
                "Severe pain when bearing weight",
                "Numbness or tingling",
                "Inability to move joint",
                "Visible deformity"
            ],
            "call_911_if": "You hear a popping sound, see bone deformity, or cannot move the joint at all",
            "voice_text": "You have a sprain. Remember R-I-C-E: Rest the injured area. Apply Ice for 15 to 20 minutes every few hours. Compress with an elastic bandage. Elevate above your heart. Take pain medication as needed. Call 911 if you heard a popping sound or cannot move the joint."
        },
        
        "nosebleed": {
            "assessment": "Nosebleed without signs of severe injury or trauma.",
            "steps": [
                "Sit up straight and lean forward slightly",
                "Pinch the soft part of nose firmly for 10 minutes",
                "Breathe through your mouth during this time",
                "Release and check if bleeding has stopped",
                "If bleeding continues, pinch for another 10 minutes",
                "Apply cold compress on bridge of nose",
                "Avoid blowing nose or picking for several hours"
            ],
            "warning_signs": [
                "Bleeding lasts more than 30 minutes",
                "Heavy bleeding affecting breathing",
                "Frequent nosebleeds",
                "Nosebleed after head injury"
            ],
            "call_911_if": "Bleeding is heavy and continuous for 30 minutes, or nosebleed followed a head injury",
            "voice_text": "You have a nosebleed. Sit up straight and lean forward. Pinch the soft part of your nose firmly for 10 minutes while breathing through your mouth. Apply a cold compress to the bridge of your nose. Avoid blowing your nose. Call 911 if bleeding continues heavily for 30 minutes."
        },
        
        "minor_allergic_reaction": {
            "assessment": "Localized allergic reaction without breathing difficulty or severe swelling.",
            "steps": [
                "Remove allergen or stop exposure if possible",
                "Wash affected area with soap and water",
                "Apply cool compress to reduce itching and swelling",
                "Take antihistamine (like Benadryl) as directed",
                "Apply calamine lotion or hydrocortisone cream for itching",
                "Monitor for worsening symptoms"
            ],
            "warning_signs": [
                "Swelling of face, lips, or tongue",
                "Difficulty breathing or swallowing",
                "Dizziness or feeling faint",
                "Rapid spread of rash"
            ],
            "call_911_if": "Person has difficulty breathing, severe swelling, or shows signs of anaphylaxis",
            "voice_text": "You have a minor allergic reaction. Remove the allergen if possible. Wash the affected area. Apply a cool compress. Take an antihistamine like Benadryl as directed. Apply calamine lotion for itching. Monitor symptoms closely. Call 911 immediately if you develop difficulty breathing or severe swelling of the face or throat."
        }
    }
    
    # Default fallback
    default = {
        "assessment": "Medical situation requiring first aid attention.",
        "steps": [
            "Stay calm and assess the situation",
            "Ensure the area is safe for you and the person",
            "Call for help if symptoms worsen",
            "Keep the person comfortable and reassured",
            "Monitor vital signs (breathing, pulse) if possible",
            "Do not move the person unless necessary for safety"
        ],
        "warning_signs": [
            "Symptoms getting worse",
            "Person becomes unresponsive",
            "Difficulty breathing",
            "Severe pain"
        ],
        "call_911_if": "Symptoms worsen or person becomes unresponsive",
        "voice_text": "Stay calm and assess the situation. Ensure safety. Keep the person comfortable. Monitor their condition closely. Call 911 if symptoms worsen or the person becomes unresponsive."
    }
    
    instructions = instructions_db.get(emergency_type, default)
    
    return {
        "success": True,
        "emergency_type": emergency_type,
        "severity": "MINOR",
        "source": "fallback_database",
        **instructions
    }


def format_instructions_for_sms(instructions: Dict[str, Any]) -> str:
    """
    Format instructions as concise SMS message
    
    Args:
        instructions: Instruction dict from generate_first_aid_instructions
    
    Returns:
        SMS-formatted text (max 320 chars for 2-part SMS)
    """
    emergency = instructions.get("emergency_type", "").replace("_", " ").title()
    steps = instructions.get("steps", [])
    
    # Take first 3-4 most critical steps
    key_steps = steps[:4]
    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(key_steps)])
    
    message = f"🏥 FIRST AID: {emergency}\n\n{steps_text}\n\n⚠️ Call 911 if: {instructions.get('call_911_if', 'symptoms worsen')}"
    
    # Truncate if too long
    if len(message) > 320:
        message = message[:317] + "..."
    
    return message
