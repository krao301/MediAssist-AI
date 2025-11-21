import { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { triageEmergency, addIncidentEvent, getNearestHospital, resolveIncident } from '../lib/api';
import { speak, startListening, stopSpeaking } from '../lib/tts';

interface TriageResult {
  type: string;
  severity: string;
  bring: string[];
  requires_sos?: boolean;
  sos_number?: string;
  clarifying_questions?: string[];
  possible_emergencies?: Array<{ type: string; confidence: number }>;
  message?: string;
  first_aid_instructions?: {
    assessment: string;
    steps: string[];
    warning_signs: string[];
    call_911_if: string;
    voice_text: string;
  };
}

// Helper function to extract age group from text
const extractAgeGroup = (text: string): string | undefined => {
  const lowerText = text.toLowerCase();

  // Elderly keywords
  if (/(elderly|grandpa|grandma|grandfather|grandmother|senior|old man|old woman|aged|\d{7,9}|80|90)/i.test(lowerText)) {
    return 'elderly';
  }

  // Child keywords
  if (/(child|kid|baby|infant|toddler|boy|girl|son|daughter|young|minor|\d{1,2}\s*(year|month|week)\s*old)/i.test(lowerText)) {
    return 'child';
  }

  // If no age mentioned, return undefined so backend can ask
  return undefined;
};

export default function Incident() {
  const { incidentId } = useParams<{ incidentId: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const [currentLocation] = useState(location.state?.location || { lat: 0, lng: 0 });
  const [triage, setTriage] = useState<TriageResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [hospital, setHospital] = useState<any>(null);

  useEffect(() => {
    // Auto-start voice input
    handleStartListening();
  }, []);

  const handleStartListening = () => {
    setListening(true);
    startListening(
      (text) => {
        setTranscript(text);
        setListening(false);
        handleTriage(text);
      },
      (error) => {
        console.error('Speech recognition error:', error);
        setListening(false);
        // Fallback: ask user to type
        const fallback = prompt('What happened? (Voice recognition failed, please type):');
        if (fallback) {
          setTranscript(fallback);
          handleTriage(fallback);
        }
      }
    );
  };

  const handleTriage = async (text: string) => {
    setLoading(true);

    try {
      // Extract age group from text or ask user
      const ageGroup = extractAgeGroup(text);

      // Pass location and age group to triage API
      const response = await triageEmergency(text, 'en', ageGroup, currentLocation.lat, currentLocation.lng);
      const result = response.data;

      setTriage(result);

      // Log initial event along with structured metadata for summaries
      const eventMetadata = {
        user_input: text,
        type: result.type,
        severity: result.severity,
        requires_sos: result.requires_sos,
        requires_helpers: result.requires_helpers,
        helper_instructions: result.helper_instructions,
        protocols: result.bring,
        symptoms: result.symptoms,
        contraindications: result.contraindications,
        voice_text: result.first_aid_instructions?.voice_text,
        first_aid_instructions: result.first_aid_instructions,
        clarifying_questions: result.clarifying_questions,
        message: result.message,
        timestamp: result.timestamp,
      };

      await addIncidentEvent(
        parseInt(incidentId!),
        `Triage: ${result.type} (${result.severity})`,
        eventMetadata
      );

      // CRITICAL FLOW: Announce emergency response
      if (result.requires_sos) {
        speak('Critical emergency detected. Emergency services and nearby responders have been alerted. Help is on the way.');
        
        // Get nearest hospital for display
        try {
          const hospitalResponse = await getNearestHospital(currentLocation.lat, currentLocation.lng);
          setHospital(hospitalResponse.data);
        } catch (error) {
          console.error('Failed to get hospital:', error);
        }
      } 
      // MINOR FLOW: Provide first aid instructions with voice
      else if (result.first_aid_instructions) {
        // Auto-play voice instructions
        speak(result.first_aid_instructions.voice_text);
      }

    } catch (error) {
      console.error('Triage error:', error);
      alert('Error processing emergency. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleEndIncident = async () => {
    try {
      await resolveIncident(parseInt(incidentId!));
      stopSpeaking();
      navigate(`/summary/${incidentId}`);
    } catch (error) {
      console.error('Failed to end incident:', error);
    }
  };

  const handleCall911 = () => {
    window.location.href = 'tel:911';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-red-500 mx-auto mb-4"></div>
          <p className="text-white text-xl">Analyzing emergency...</p>
          {transcript && <p className="text-gray-400 mt-2">"{transcript}"</p>}
        </div>
      </div>
    );
  }

  if (listening) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🎤</div>
          <p className="text-white text-xl">Listening...</p>
          <p className="text-gray-400 mt-2">Describe what happened</p>
        </div>
      </div>
    );
  }

  if (!triage) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <p className="text-white text-xl">Starting emergency session...</p>
        </div>
      </div>
    );
  }

  // Handle clarification needed
  if (triage.type === 'needs_clarification' || triage.type === 'needs_age_clarification') {
    return (
      <div className="min-h-screen bg-gray-900 pb-20">
        <div className="bg-yellow-600 text-white p-4 sticky top-0 z-10 shadow-lg">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-xl font-bold">⚠️ Need More Information</h1>
            <p className="text-sm opacity-90">Please provide additional details</p>
          </div>
        </div>

        <div className="max-w-4xl mx-auto p-6 space-y-6">
          {/* Message */}
          {triage.message && (
            <div className="bg-yellow-900/30 border-l-4 border-yellow-500 p-4 rounded-lg">
              <p className="text-yellow-100 text-lg">{triage.message}</p>
            </div>
          )}

          {/* Clarifying Questions */}
          {triage.clarifying_questions && triage.clarifying_questions.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-white text-xl font-semibold mb-4">❓ Please Answer These Questions:</h2>
              <ul className="space-y-3">
                {triage.clarifying_questions.map((question, i) => (
                  <li key={i} className="text-gray-200 text-lg flex items-start">
                    <span className="text-yellow-400 font-bold mr-3">{i + 1}.</span>
                    <span>{question}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Possible Emergencies */}
          {triage.possible_emergencies && triage.possible_emergencies.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-white text-lg font-semibold mb-3">🔍 Possible Emergency Types:</h3>
              <div className="space-y-2">
                {triage.possible_emergencies.map((emergency, i) => (
                  <div key={i} className="flex items-center justify-between bg-gray-700/50 p-3 rounded-lg">
                    <span className="text-gray-200">{emergency.type.replace('_', ' ')}</span>
                    <span className="text-yellow-400 font-semibold">{(emergency.confidence * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Input for more details */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-white text-lg font-semibold mb-4">💬 Provide More Details:</h3>
            <div className="space-y-4">
              <button
                onClick={handleStartListening}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition"
              >
                <span className="text-2xl">🎤</span>
                <span>Speak Your Response</span>
              </button>
              <div className="text-center text-gray-400 text-sm">or</div>
              <button
                onClick={() => {
                  const response = prompt('Please type your response:');
                  if (response) {
                    setTranscript(response);
                    handleTriage(response);
                  }
                }}
                className="w-full bg-gray-700 hover:bg-gray-600 text-white py-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition"
              >
                <span className="text-2xl">⌨️</span>
                <span>Type Your Response</span>
              </button>
            </div>
          </div>

          {/* Previous input display */}
          {transcript && (
            <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
              <p className="text-gray-400 text-sm mb-1">Your previous input:</p>
              <p className="text-white">"{transcript}"</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // RENDER: CRITICAL EMERGENCY - Show "Help is on the way"
  if (triage.requires_sos) {
    return (
      <div className="min-h-screen bg-gray-900">
        {/* Header */}
        <div className="bg-red-600 text-white p-4 sticky top-0 z-10 shadow-lg">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold">🚨 CRITICAL EMERGENCY</h1>
              <p className="text-sm opacity-90">{triage.type.replace('_', ' ').toUpperCase()} • {triage.severity}</p>
            </div>
            <button
              onClick={handleCall911}
              className="bg-white text-red-600 px-6 py-2 rounded-lg font-bold hover:bg-gray-100 transition"
            >
              📞 CALL 911
            </button>
          </div>
        </div>

        <div className="max-w-4xl mx-auto p-6 space-y-6">
          {/* Main Status Card */}
          <div className="bg-gradient-to-br from-red-900/50 to-orange-900/50 border-2 border-red-500 rounded-xl p-8 text-center space-y-6">
            <div className="text-6xl mb-4 animate-pulse">�</div>
            <h2 className="text-3xl font-bold text-white mb-4">Help Is On The Way</h2>
            <p className="text-xl text-red-100">Emergency response has been initiated</p>
          </div>

          {/* Status Updates */}
          <div className="space-y-4">
            <div className="bg-green-900/30 border-l-4 border-green-500 p-4 rounded-lg flex items-center">
              <span className="text-2xl mr-4">✅</span>
              <div>
                <p className="text-green-200 font-semibold">Emergency Contacts Alerted</p>
                <p className="text-green-300 text-sm">Call + SMS sent with your location</p>
              </div>
            </div>

            <div className="bg-green-900/30 border-l-4 border-green-500 p-4 rounded-lg flex items-center">
              <span className="text-2xl mr-4">✅</span>
              <div>
                <p className="text-green-200 font-semibold">Hospital Notified</p>
                <p className="text-green-300 text-sm">Nearest hospital has been informed</p>
              </div>
            </div>

            <div className="bg-green-900/30 border-l-4 border-green-500 p-4 rounded-lg flex items-center">
              <span className="text-2xl mr-4">✅</span>
              <div>
                <p className="text-green-200 font-semibold">Nearby Responders Alerted</p>
                <p className="text-green-300 text-sm">People within 500m notified with instructions</p>
              </div>
            </div>
          </div>

          {/* Hospital Info */}
          {hospital && (
            <div className="bg-purple-900/30 border border-purple-600 rounded-lg p-6">
              <h3 className="text-purple-200 font-semibold mb-3 text-lg">🏥 Nearest Hospital:</h3>
              <p className="text-white font-medium text-xl">{hospital.hospital_name}</p>
              <p className="text-gray-300">{hospital.hospital_address}</p>
              <p className="text-gray-400 mt-2">
                📍 {hospital.distance_km} km • ⏱️ ~{hospital.eta_minutes} min ETA
              </p>
              <a
                href={hospital.directions_url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 block bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition font-semibold text-center"
              >
                🗺️ Get Directions
              </a>
            </div>
          )}

          {/* Important Info */}
          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6">
            <h3 className="text-white font-semibold mb-3 text-lg">ℹ️ What's Happening:</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start">
                <span className="mr-3">•</span>
                <span>Emergency services have been contacted</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3">•</span>
                <span>Your emergency contacts received your location and situation</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3">•</span>
                <span>Nearby trained responders are being alerted</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3">•</span>
                <span>Hospital is preparing for your arrival</span>
              </li>
            </ul>
          </div>

          {/* Action Button */}
          <button
            onClick={handleEndIncident}
            className="w-full bg-gray-700 text-white py-4 rounded-lg hover:bg-gray-600 transition font-semibold"
          >
            View Emergency Summary
          </button>
        </div>
      </div>
    );
  }

  // RENDER: MINOR EMERGENCY - Show First Aid Instructions
  if (triage.first_aid_instructions) {
    const instructions = triage.first_aid_instructions;

    return (
      <div className="min-h-screen bg-gray-900">
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 sticky top-0 z-10 shadow-lg">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold">🏥 FIRST AID INSTRUCTIONS</h1>
              <p className="text-sm opacity-90">{triage.type.replace('_', ' ').toUpperCase()} • {triage.severity}</p>
            </div>
            <button
              onClick={handleCall911}
              className="bg-white text-blue-600 px-6 py-2 rounded-lg font-bold hover:bg-gray-100 transition"
            >
              📞 CALL 911
            </button>
          </div>
        </div>

        <div className="max-w-4xl mx-auto p-6 space-y-6">
          {/* Assessment */}
          <div className="bg-blue-900/30 border-l-4 border-blue-500 p-5 rounded-lg">
            <h3 className="text-blue-200 font-semibold mb-2 text-lg">📋 Assessment:</h3>
            <p className="text-blue-100 text-lg">{instructions.assessment}</p>
          </div>

          {/* Voice Control */}
          <div className="bg-gray-800 rounded-lg p-4 flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-3xl mr-3">�</span>
              <div>
                <p className="text-white font-semibold">Voice Instructions</p>
                <p className="text-gray-400 text-sm">Playing automatically</p>
              </div>
            </div>
            <button
              onClick={() => speak(instructions.voice_text)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition"
            >
              🔄 Replay
            </button>
          </div>

          {/* Step-by-Step Instructions */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-white font-semibold mb-4 text-xl">📝 Follow These Steps:</h3>
            <ol className="space-y-4">
              {instructions.steps.map((step, index) => (
                <li key={index} className="flex items-start">
                  <span className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4 flex-shrink-0">
                    {index + 1}
                  </span>
                  <span className="text-gray-200 text-lg pt-1">{step}</span>
                </li>
              ))}
            </ol>
          </div>

          {/* Warning Signs */}
          <div className="bg-yellow-900/30 border-l-4 border-yellow-500 p-5 rounded-lg">
            <h3 className="text-yellow-200 font-semibold mb-3 text-lg">⚠️ Warning Signs to Watch For:</h3>
            <ul className="space-y-2">
              {instructions.warning_signs.map((sign, index) => (
                <li key={index} className="flex items-start text-yellow-100">
                  <span className="mr-3">•</span>
                  <span>{sign}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* When to Call 911 */}
          <div className="bg-red-900/30 border-2 border-red-500 p-5 rounded-lg">
            <h3 className="text-red-200 font-semibold mb-3 text-lg">🚨 Call 911 Immediately If:</h3>
            <p className="text-red-100 text-lg">{instructions.call_911_if}</p>
            <button
              onClick={handleCall911}
              className="mt-4 w-full bg-red-600 hover:bg-red-700 text-white py-3 rounded-lg font-bold transition text-lg"
            >
              📞 CALL 911 NOW
            </button>
          </div>

          {/* End Session */}
          <button
            onClick={handleEndIncident}
            className="w-full bg-gray-700 text-white py-4 rounded-lg hover:bg-gray-600 transition font-semibold"
          >
            Mark as Resolved
          </button>
        </div>
      </div>
    );
  }

  // Fallback (shouldn't reach here)
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="text-center">
        <p className="text-white text-xl">Loading emergency guidance...</p>
      </div>
    </div>
  );
}
