import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { triageEmergency, addIncidentEvent, sendAlerts, getNearestHospital, resolveIncident } from '../lib/api';
import { speak, startListening, stopSpeaking } from '../lib/tts';
import StepCard from '../components/StepCard';
import Metronome from '../components/Metronome';

export default function Incident() {
  const { incidentId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [currentLocation] = useState(location.state?.location || { lat: 0, lng: 0 });
  const [triage, setTriage] = useState(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [hospital, setHospital] = useState(null);
  const [alertsSent, setAlertsSent] = useState(false);

  useEffect(() => {
    // Auto-start voice input
    handleStartListening();
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  const handleTriage = async (text) => {
    setLoading(true);
    
    try {
      const response = await triageEmergency(text);
      const result = response.data;
      
      setTriage(result);
      
      // Log initial event
      await addIncidentEvent(parseInt(incidentId), `Triage: ${result.type} (${result.severity})`);
      
      // Speak first step
      if (result.steps.length > 0) {
        speak(result.steps[0].title + '. ' + result.steps[0].detail);
      }
      
      // Auto-send alerts
      await sendEmergencyAlerts(result);
      
      // Get nearest hospital
      await loadNearestHospital();
      
    } catch (error) {
      console.error('Triage error:', error);
      alert('Error processing emergency. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const sendEmergencyAlerts = async (triageResult) => {
    try {
      const message = `Emergency: ${triageResult.type.replace('_', ' ')}. ${triageResult.bring.join(', ')}.`;
      await sendAlerts(
        parseInt(incidentId),
        currentLocation.lat,
        currentLocation.lng,
        message
      );
      setAlertsSent(true);
    } catch (error) {
      console.error('Failed to send alerts:', error);
    }
  };

  const loadNearestHospital = async () => {
    try {
      const response = await getNearestHospital(currentLocation.lat, currentLocation.lng);
      setHospital(response.data);
    } catch (error) {
      console.error('Failed to get hospital:', error);
    }
  };

  const handleNextStep = async () => {
    if (!triage) return;
    
    const nextIndex = currentStepIndex + 1;
    if (nextIndex < triage.steps.length) {
      setCurrentStepIndex(nextIndex);
      const step = triage.steps[nextIndex];
      
      // Speak next step
      speak(step.title + '. ' + step.detail);
      
      // Log event
      await addIncidentEvent(parseInt(incidentId), `Completed: ${triage.steps[currentStepIndex].title}`);
    }
  };

  const handleEndIncident = async () => {
    try {
      await resolveIncident(parseInt(incidentId));
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

  const currentStep = triage.steps[currentStepIndex];

  return (
    <div className="min-h-screen bg-gray-900 pb-20">
      {/* Header */}
      <div className="bg-red-600 text-white p-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">{triage.type.replace('_', ' ').toUpperCase()}</h1>
            <p className="text-sm opacity-90">{triage.severity} • Step {currentStepIndex + 1} of {triage.steps.length}</p>
          </div>
          <button
            onClick={handleCall911}
            className="bg-white text-red-600 px-6 py-2 rounded-lg font-bold hover:bg-gray-100 transition"
          >
            📞 CALL 911
          </button>
        </div>
      </div>

      {/* Alert Status */}
      {alertsSent && (
        <div className="bg-green-900/50 border-t-4 border-green-500 p-4">
          <div className="max-w-4xl mx-auto flex items-center">
            <span className="mr-3">✅</span>
            <span className="text-green-200">Nearby contacts have been alerted</span>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Current Step */}
        <StepCard
          step={currentStep}
          onComplete={handleNextStep}
          isLast={currentStepIndex === triage.steps.length - 1}
        />

        {/* CPR Metronome */}
        {currentStep.cadence_bpm && (
          <Metronome bpm={currentStep.cadence_bpm} />
        )}

        {/* Bring Items */}
        {triage.bring.length > 0 && (
          <div className="bg-blue-900/30 border border-blue-600 rounded-lg p-4">
            <h3 className="text-blue-200 font-semibold mb-2">📦 Items Needed:</h3>
            <ul className="list-disc list-inside text-blue-100 space-y-1">
              {triage.bring.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Hospital Info */}
        {hospital && (
          <div className="bg-purple-900/30 border border-purple-600 rounded-lg p-4">
            <h3 className="text-purple-200 font-semibold mb-2">🏥 Nearest Hospital:</h3>
            <p className="text-white font-medium">{hospital.hospital_name}</p>
            <p className="text-gray-300 text-sm">{hospital.hospital_address}</p>
            <p className="text-gray-400 text-sm mt-1">
              {hospital.distance_km} km • ~{hospital.eta_minutes} min
            </p>
            <a
              href={hospital.directions_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition text-sm"
            >
              Get Directions →
            </a>
          </div>
        )}

        {/* All Steps Overview */}
        <div className="bg-gray-800/50 rounded-lg p-4">
          <h3 className="text-white font-semibold mb-3">All Steps:</h3>
          <div className="space-y-2">
            {triage.steps.map((step, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg ${
                  index === currentStepIndex
                    ? 'bg-blue-600 text-white'
                    : index < currentStepIndex
                    ? 'bg-green-900/30 text-green-200'
                    : 'bg-gray-700/30 text-gray-400'
                }`}
              >
                <div className="flex items-center">
                  <span className="mr-2">
                    {index < currentStepIndex ? '✓' : index === currentStepIndex ? '▶' : '○'}
                  </span>
                  <span className="font-medium">{step.title}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* End Session */}
        <button
          onClick={handleEndIncident}
          className="w-full bg-gray-700 text-white py-3 rounded-lg hover:bg-gray-600 transition"
        >
          End Session & View Summary
        </button>
      </div>
    </div>
  );
}