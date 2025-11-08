import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getIncidentSummary } from '../lib/api';

export default function Summary() {
  const { incidentId } = useParams<{ incidentId: string }>();
  const navigate = useNavigate();
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const response = await getIncidentSummary(parseInt(incidentId!));
      setSummary(response.data);
    } catch (error) {
      console.error('Failed to load summary:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    // Convert to text and download
    if (!summary) return;
    
    const text = JSON.stringify(summary, null, 2);
    const blob = new Blob([text], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `incident-${incidentId}-summary.json`;
    a.click();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">Loading summary...</div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">Failed to load summary</div>
      </div>
    );
  }

  const durationMin = summary.duration_seconds ? Math.floor(summary.duration_seconds / 60) : 0;
  const durationSec = summary.duration_seconds ? summary.duration_seconds % 60 : 0;

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <div className="bg-green-600 text-white p-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-xl font-bold">✓ Incident Complete</h1>
          <p className="text-sm opacity-90">Summary Report</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Overview */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-white text-2xl font-bold mb-4">Incident Overview</h2>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-400">Type</p>
              <p className="text-white font-semibold text-lg">
                {summary.type.replace('_', ' ').toUpperCase()}
              </p>
            </div>
            <div>
              <p className="text-gray-400">Severity</p>
              <p className={`font-semibold text-lg ${
                summary.severity === 'critical' ? 'text-red-400' :
                summary.severity === 'urgent' ? 'text-orange-400' :
                'text-yellow-400'
              }`}>
                {summary.severity.toUpperCase()}
              </p>
            </div>
            <div>
              <p className="text-gray-400">Duration</p>
              <p className="text-white font-semibold">
                {durationMin}m {durationSec}s
              </p>
            </div>
            <div>
              <p className="text-gray-400">Steps Completed</p>
              <p className="text-white font-semibold">{summary.total_steps}</p>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-white text-xl font-bold mb-4">Timeline</h3>
          <div className="space-y-3">
            {summary.timeline.map((event: any, index: number) => {
              const elapsed = event.elapsed_seconds;
              const min = Math.floor(elapsed / 60);
              const sec = elapsed % 60;
              
              return (
                <div key={index} className="flex items-start border-l-4 border-blue-600 pl-4 py-2">
                  <div className="min-w-[80px] text-blue-400 font-mono text-sm">
                    +{min}:{sec.toString().padStart(2, '0')}
                  </div>
                  <div className="flex-1">
                    <p className="text-white">{event.step}</p>
                    {event.metadata && (
                      <p className="text-gray-400 text-sm mt-1">
                        {JSON.stringify(event.metadata)}
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <button
            onClick={handleDownload}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition"
          >
            📥 Download Report
          </button>
          
          <button
            onClick={() => navigate('/')}
            className="w-full bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 rounded-lg transition"
          >
            ← Back to Home
          </button>
        </div>

        {/* EMS Note */}
        <div className="bg-purple-900/30 border border-purple-600 rounded-lg p-4 text-purple-200 text-sm">
          <p className="font-semibold mb-2">📋 For EMS/Medical Personnel:</p>
          <p>
            This report can be shared with emergency responders to provide context on
            first aid steps performed before their arrival.
          </p>
        </div>
      </div>
    </div>
  );
}
