import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentLocation, requestLocationPermission, requestMicrophonePermission } from '../lib/permissions';
import { createIncident } from '../lib/api';

export default function Home() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [permissionsGranted, setPermissionsGranted] = useState(false);

  useEffect(() => {
    checkPermissions();
  }, []);

  const checkPermissions = async () => {
    const locationOk = await requestLocationPermission();
    const micOk = await requestMicrophonePermission();
    setPermissionsGranted(locationOk && micOk);
  };

  const handleSOS = async () => {
    setLoading(true);
    
    try {
      // Get current location
      const location = await getCurrentLocation();
      
      // Create incident
      const response = await createIncident(location.lat, location.lng);
      const incidentId = response.data.id;
      
      // Navigate to incident screen
      navigate(`/incident/${incidentId}`, {
        state: { location }
      });
    } catch (error) {
      console.error('Error starting SOS:', error);
      alert('Failed to start emergency session. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-b from-gray-900 to-black">
      <div className="max-w-md w-full text-center space-y-8">
        {/* Logo/Header */}
        <div className="space-y-2">
          <div className="text-6xl mb-4">🚑</div>
          <h1 className="text-4xl font-bold text-white">MediAssist AI</h1>
          <p className="text-gray-400">Emergency First-Aid Coach</p>
        </div>

        {/* Permission Status */}
        {!permissionsGranted && (
          <div className="bg-yellow-900/30 border border-yellow-600 rounded-lg p-4 text-yellow-200 text-sm">
            <p className="font-semibold mb-2">⚠️ Permissions Required</p>
            <p>This app needs access to your location and microphone to provide emergency assistance.</p>
            <button
              onClick={checkPermissions}
              className="mt-3 bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition"
            >
              Grant Permissions
            </button>
          </div>
        )}

        {/* SOS Button */}
        <div className="py-8">
          <button
            onClick={handleSOS}
            disabled={loading || !permissionsGranted}
            className={`
              w-64 h-64 rounded-full 
              bg-red-600 hover:bg-red-700 
              text-white font-bold text-2xl
              shadow-2xl
              transform transition-all duration-200
              ${loading ? 'scale-95 opacity-75' : 'hover:scale-105'}
              ${!permissionsGranted ? 'opacity-50 cursor-not-allowed' : 'emergency-pulse'}
              disabled:cursor-not-allowed
            `}
          >
            {loading ? (
              <div className="flex flex-col items-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
                <span className="text-lg">Starting...</span>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <span className="text-6xl mb-2">🆘</span>
                <span>EMERGENCY</span>
                <span className="text-sm font-normal mt-2">Tap to Start</span>
              </div>
            )}
          </button>
        </div>

        {/* Quick Info */}
        <div className="bg-gray-800/50 rounded-lg p-6 space-y-3 text-left">
          <h3 className="text-lg font-semibold text-white mb-3">What This App Does:</h3>
          <div className="space-y-2 text-sm text-gray-300">
            <div className="flex items-start">
              <span className="mr-3">🤖</span>
              <span>AI-guided first aid instructions</span>
            </div>
            <div className="flex items-start">
              <span className="mr-3">📍</span>
              <span>Alerts nearby trusted contacts</span>
            </div>
            <div className="flex items-start">
              <span className="mr-3">🏥</span>
              <span>Routes to nearest emergency room</span>
            </div>
            <div className="flex items-start">
              <span className="mr-3">⏱️</span>
              <span>Every second counts - act fast!</span>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="text-xs text-gray-500 space-y-1">
          <p className="font-semibold text-red-400">⚠️ ALWAYS CALL 911 FIRST</p>
          <p>This app provides guidance while waiting for emergency services. It is not a substitute for professional medical care.</p>
        </div>

        {/* Navigation */}
        <div className="pt-4 flex gap-4 justify-center flex-wrap">
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition shadow-lg"
          >
            🧠 AI Dashboard
          </button>
          <button
            onClick={() => navigate('/contacts')}
            className="text-blue-400 hover:text-blue-300 text-sm underline self-center"
          >
            Manage Contacts
          </button>
        </div>
      </div>
    </div>
  );
}
