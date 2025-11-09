# MediAssist AI - LLM Optimization Guide

## 🎯 Overview

This guide documents the **highly optimized LLM system** for MediAssist AI emergency medical triage. The system uses advanced prompt engineering, RAG (Retrieval Augmented Generation), conversational AI, and fine-tuning strategies to provide accurate, life-saving emergency guidance.

---

## 🚀 Key Features

### 1. **Multi-Level Severity Classification**
- **CRITICAL**: Life-threatening (cardiac arrest, choking, stroke)
  - Immediate SOS to 7166170427
  - Nearby helper notifications
  - Real-time CPR/first-aid guidance

- **SEVERE**: Serious injury/illness (severe bleeding, breathing difficulty)
  - SOS call to 7166170427
  - Nearby helper alerts
  - Step-by-step first aid

- **MODERATE**: Needs first aid (burns, sprains, moderate injuries)
  - Nearby helper notifications (optional)
  - Detailed first-aid steps
  - Hospital routing

- **MILD**: Self-care capable (minor cuts, bruises)
  - **Conversational AI follow-up**
  - AI asks clarifying questions
  - Provides self-help guidance
  - Escalates if severity increases

### 2. **Advanced Prompt Engineering**
- **Few-shot learning** with 5+ examples per category
- **Context-aware prompts** with patient age, location, time
- **Chain-of-thought reasoning** for classification
- **Confidence scoring** (0.0 - 1.0)
- **Red flag detection** for life-threatening symptoms

### 3. **RAG (Retrieval Augmented Generation)**
- **Medical Knowledge Base** with 7+ emergency categories
- Each category includes:
  - Symptom keywords
  - Severity level
  - Step-by-step first aid instructions
  - Contraindications (what NOT to do)
  - Items to bring
  - Helper instructions
  - Timing for each step
  - CPR cadence (BPM) where applicable

### 4. **Conversational AI for MILD Cases**
- Asks follow-up questions to assess severity
- Provides tips and self-care guidance
- Escalates to SEVERE/CRITICAL if user's answers indicate worsening
- Example flow:
  ```
  User: "I cut my finger cooking"
  AI: "Is the bleeding stopping with pressure? How deep is the cut?"
  User: "Yes, it's stopping. About 1cm long, not deep"
  AI: "Good! Here's how to clean and bandage it..."
  ```

### 5. **Emergency SOS Routing**
- **POC Emergency Number**: 7166170427 (instead of 911 for testing)
- Automatic SOS triggered for CRITICAL/SEVERE cases
- SMS alert with:
  - Emergency type
  - Victim information
  - GPS coordinates with Google Maps link
  - Timestamp

### 6. **Nearby Helper Notifications**
- **Free geolocation service** (OpenStreetMap Overpass API)
- Finds:
  - User's saved contacts within 500m radius
  - Public emergency resources (hospitals, police, fire stations)
- Sends SMS with:
  - Distance to emergency
  - First-aid instructions for helpers
  - Navigation link
  - Urgency level

### 7. **Knowledge Graph Structure**
```
Emergency Type
  ├── Keywords (for fallback matching)
  ├── Severity Level
  ├── SOS Required (boolean)
  ├── Helpers Required (boolean)
  ├── Steps (array)
  │   ├── Title
  │   ├── Detail
  │   ├── Timer (seconds)
  │   ├── Critical flag
  │   └── Cadence (BPM for CPR)
  ├── Contraindications
  ├── Symptoms
  └── Helper Instructions
```

---

## 📊 Training Dataset Structure

### Dataset Specifications
- **Total Examples**: 20,000 rows
- **Format**: JSON Lines (.jsonl) for Gemini Fine-Tuning API
- **Distribution**:
  - CRITICAL: 4,000 examples (20%)
  - SEVERE: 6,000 examples (30%)
  - MODERATE: 6,000 examples (30%)
  - MILD: 4,000 examples (20%)

### Data Sources
1. Medical emergency call transcripts (anonymized)
2. First-aid training materials (AHA, Red Cross)
3. Emergency medicine textbooks
4. CDC emergency guidelines
5. Poison control center data
6. EMS response logs

### Example Training Record
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{
        "text": "Emergency: My grandfather collapsed and isn't breathing. Age: elderly."
      }]
    },
    {
      "role": "model",
      "parts": [{
        "text": "{\"emergency_type\": \"cardiac_arrest\", \"severity\": \"CRITICAL\", \"confidence\": 0.95, \"requires_sos\": true, \"requires_helpers\": true, \"reasoning\": \"Collapse with no breathing in elderly patient indicates cardiac arrest - immediate CPR and 911 required\", \"key_symptoms\": [\"collapsed\", \"not breathing\", \"elderly\"], \"red_flags\": [\"unconscious\", \"respiratory arrest\"]}"
      }]
    }
  ]
}
```

---

## 🧠 How It Works

### 1. User Input (Voice/Text)
```
"My friend collapsed and isn't breathing"
```

### 2. Enhanced Gemini Prompt
```
You are MediAssist AI, an expert emergency medical triage system.

CRITICAL CONTEXT:
- Current time: 2025-01-08T14:30:00
- Patient age group: adult
- Location: Lat: 42.9634, Lng: -78.7384

FEW-SHOT EXAMPLES:
[5+ examples showing input → classification]

USER'S EMERGENCY: "My friend collapsed and isn't breathing"

RESPOND WITH JSON:
{
  "emergency_type": "cardiac_arrest",
  "severity": "CRITICAL",
  "confidence": 0.95,
  "requires_sos": true,
  "requires_helpers": true,
  "reasoning": "...",
  "key_symptoms": ["collapsed", "not breathing"],
  "red_flags": ["unconscious", "respiratory arrest"]
}
```

### 3. RAG Retrieval
- Gemini classifies as "cardiac_arrest"
- System retrieves from knowledge base:
  - 4 critical first-aid steps
  - CPR cadence: 110 BPM
  - Items to bring: AED, water, blanket
  - Helper instructions: "Start CPR immediately..."
  - Contraindications: "Do NOT give food/water..."

### 4. Emergency Actions
```
IF severity == CRITICAL:
  1. Send SOS to 7166170427 with GPS location
  2. Find nearby contacts within 500m
  3. Send helper notifications with first-aid instructions
  4. Display step-by-step guidance to user
  5. Start CPR metronome if cardiac arrest

ELIF severity == MILD:
  1. Ask follow-up question
  2. Provide self-care tips
  3. Monitor for escalation
```

### 5. Response to User
```json
{
  "type": "cardiac_arrest",
  "severity": "CRITICAL",
  "sos_number": "7166170427",
  "steps": [
    {
      "title": "Check responsiveness immediately",
      "detail": "Tap shoulders firmly...",
      "timer_s": 10,
      "critical": true
    },
    ...
  ],
  "helper_instructions": "You are responding to CARDIAC ARREST...",
  "nearby_helpers": [
    {
      "name": "John Doe",
      "distance_meters": 250,
      "notified": true
    }
  ]
}
```

---

## 🛠️ Implementation Files

### Core LLM Files
1. **`app/services/llm_enhanced.py`** (Main LLM service)
   - `classify_emergency_enhanced()` - Main classification function
   - `generate_follow_up_response()` - Conversational AI
   - `MEDICAL_KNOWLEDGE_BASE` - RAG knowledge base
   - `FEW_SHOT_EXAMPLES` - Prompt engineering examples

2. **`app/services/nearby_helpers.py`** (Helper notifications)
   - `NearbyHelperService` - Find and notify nearby contacts
   - `notify_emergency_services()` - SOS to 7166170427
   - `find_public_helpers_nearby()` - OpenStreetMap API integration

3. **`app/services/geo.py`** (Geolocation)
   - `haversine_distance()` - Distance calculation
   - `contacts_within_radius()` - Find nearby contacts
   - `find_nearest_hospital()` - Hospital routing

4. **`app/services/notify.py`** (Twilio SMS)
   - `send_sms_alert()` - Send SMS via Twilio
   - `send_voice_call()` - Voice call (optional)

### Testing & Training
5. **`test_enhanced_llm.py`** - Comprehensive test suite
6. **`training_data_template.json`** - Dataset structure for 20k rows

---

## 🧪 Running Tests

```bash
# Activate virtual environment
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Run enhanced LLM tests
python test_enhanced_llm.py
```

### Expected Output
```
✅ All CRITICAL scenarios correctly classified and routed to SOS
✅ MILD cases correctly trigger conversational mode
✅ Severity escalation working correctly
✅ Helper notification structure complete
✅ Knowledge base comprehensive
✅ API integration test complete
```

---

## 📈 Fine-Tuning Process

### Step 1: Generate 20k Training Dataset
```python
# Use training_data_template.json as reference
# Generate variations using:
# - Medical databases
# - Emergency call transcripts
# - Synthetic data generation with GPT-4

# Output format: .jsonl
# Each line = one training example
```

### Step 2: Fine-Tune Gemini Model
```python
import google.generativeai as genai

# Upload training dataset
training_file = genai.upload_file('mediassist_training_20k.jsonl')

# Create fine-tuning job
job = genai.create_tuning_job(
    source_model='models/gemini-1.0-pro-001',
    training_data=training_file,
    id='mediassist-emergency-triage-v1',
    epoch_count=5,
    learning_rate_multiplier=1.0
)

# Monitor progress
print(job.status)

# Use fine-tuned model
model = genai.GenerativeModel('tunedModels/mediassist-emergency-triage-v1')
```

### Step 3: Evaluate Performance
- **Accuracy**: Correct classification rate
- **Precision**: For CRITICAL cases (minimize false negatives)
- **Recall**: Catch all true emergencies
- **F1-Score**: Balance of precision/recall
- **Latency**: Response time < 2 seconds

### Target Metrics
```
Accuracy: > 95%
Precision (CRITICAL): > 98%
Recall (CRITICAL): > 99%
Latency: < 1.5s p95
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Gemini API
GEMINI_API_KEY=your_actual_gemini_api_key

# Twilio (SMS/Voice)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_FROM_NUMBER=+1234567890

# Google Maps (Hospital routing)
MAPS_API_KEY=your_google_maps_key
```

### Adjustable Parameters
```python
# In llm_enhanced.py

# Emergency SOS number (POC)
EMERGENCY_SOS_NUMBER = "7166170427"

# Nearby helper radius (meters)
search_radius_meters = 500

# Confidence threshold for escalation
confidence_threshold = 0.7

# Max helpers to notify
max_helpers = 5
```

---

## 📱 Integration with Frontend

### API Endpoint (to be created)
```python
@app.post("/triage/enhanced")
async def triage_enhanced(request: TriageRequest):
    result = classify_emergency_enhanced(
        text=request.text,
        locale=request.locale,
        age_group=request.age_group,
        location={"lat": request.latitude, "lng": request.longitude}
    )

    # If CRITICAL/SEVERE, trigger SOS
    if result['requires_sos']:
        notify_emergency_services(result, ...)

    # If helpers needed, notify nearby
    if result['requires_helpers']:
        notify_nearby_helpers(result, ...)

    return result
```

### Frontend Usage
```typescript
// User speaks into microphone
const transcript = await recognizeSpeech();

// Send to enhanced triage API
const response = await fetch('/triage/enhanced', {
  method: 'POST',
  body: JSON.stringify({
    text: transcript,
    age_group: 'adult',
    latitude: currentLocation.lat,
    longitude: currentLocation.lng
  })
});

const result = await response.json();

// If MILD, show conversational follow-up
if (result.needs_follow_up) {
  showFollowUpQuestion(result.follow_up_question);
}

// If CRITICAL, show SOS confirmation
if (result.requires_sos) {
  showSOSAlert(result.sos_number);
}

// Display first-aid steps
renderSteps(result.steps);
```

---

## 🎓 Medical Knowledge Base Categories

Currently supported emergency types:

1. **cardiac_arrest** (CRITICAL)
2. **choking** (CRITICAL)
3. **severe_bleeding** (SEVERE)
4. **burn** (MODERATE)
5. **minor_cut** (MILD)
6. **fainting** (MODERATE)
7. **breathing_difficulty** (SEVERE)

### Adding New Categories
```python
MEDICAL_KNOWLEDGE_BASE["new_emergency"] = {
    "keywords": ["symptom1", "symptom2"],
    "severity": Severity.SEVERE,
    "requires_sos": True,
    "requires_helpers": True,
    "steps": [
        {
            "title": "Step 1",
            "detail": "Instructions...",
            "timer_s": 30,
            "critical": True
        }
    ],
    "bring": ["item1", "item2"],
    "helper_instructions": "Instructions for helpers...",
    "symptoms": ["symptom list"],
    "contraindications": ["what not to do"]
}
```

---

## 🚀 Next Steps for Production

1. **Generate 20k Training Dataset**
   - Use medical databases (MIMIC-III, eICU)
   - Synthetic generation with GPT-4
   - Quality assurance by medical professionals

2. **Fine-Tune Gemini Model**
   - Use Google's Gemini fine-tuning API
   - Train for 5+ epochs
   - Validate on holdout set

3. **Implement Real-Time Features**
   - WebSocket connection for live updates
   - Push notifications to helpers
   - Voice call integration (Twilio)

4. **Add More Emergency Types**
   - Stroke (FAST protocol)
   - Seizures
   - Allergic reactions
   - Poisoning
   - Fractures
   - Heat stroke/hypothermia

5. **Multilingual Support**
   - Train on Spanish, French, Mandarin
   - Locale-specific first-aid protocols

6. **Medical Professional Review**
   - Validate all first-aid instructions
   - Get AHA/Red Cross certification
   - Legal compliance (HIPAA if storing data)

---

## 📝 Notes

- **POC Emergency Number**: 7166170427 (not real 911)
- **Free APIs Used**:
  - OpenStreetMap Overpass API (public emergency facilities)
  - Google Gemini API (free tier: 60 req/min)
  - Twilio (paid but affordable for POC)
- **Safety**: Always err on side of caution - escalate severity if uncertain
- **Testing**: Never call real 911 during testing - use 7166170427

---

## 🙏 Credits

- **Medical Protocols**: American Heart Association (AHA)
- **First Aid Guidelines**: Red Cross, CDC
- **AI Model**: Google Gemini Pro
- **Geolocation**: OpenStreetMap
- **SMS/Voice**: Twilio

---

**Built with ❤️ for UB Hacking Fall 2025**
**Version**: 1.0.0 (Enhanced LLM System)
