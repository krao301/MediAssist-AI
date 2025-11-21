import { useState, useEffect } from 'react';
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

  const timeline = Array.isArray(summary.timeline) ? summary.timeline : [];

  const renderTimelineDetails = (metadata: any) => {
    if (!metadata) return null;

    const protocols: string[] = Array.isArray(metadata.protocols)
      ? metadata.protocols
      : Array.isArray(metadata.bring)
        ? metadata.bring
        : [];
    const clarifying: string[] = Array.isArray(metadata.clarifying_questions)
      ? metadata.clarifying_questions
      : [];
    const instructions = metadata.first_aid_instructions;
    const steps: string[] = Array.isArray(instructions?.steps) ? instructions.steps : [];
    const warningSigns: string[] = Array.isArray(instructions?.warning_signs)
      ? instructions.warning_signs
      : [];

    return (
      <div className="space-y-3 mt-2">
        {metadata.user_input && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Message Received</p>
            <div className="bg-gray-900/50 border border-gray-700 rounded-md p-3 text-gray-100 text-sm">
              {metadata.user_input}
            </div>
          </div>
        )}

        {metadata.message && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Message</p>
            <p className="text-gray-300">{metadata.message}</p>
          </div>
        )}

        {(metadata.type || metadata.severity) && (
          <div className="flex gap-4 text-sm text-gray-300">
            {metadata.type && (
              <span>
                <span className="text-gray-500">Type:</span> {metadata.type}
              </span>
            )}
            {metadata.severity && (
              <span>
                <span className="text-gray-500">Severity:</span> {metadata.severity}
              </span>
            )}
          </div>
        )}

        {(metadata.requires_sos || metadata.requires_helpers) && (
          <div className="text-sm text-gray-300">
            {metadata.requires_sos && <p>🚨 SOS triggered</p>}
            {metadata.requires_helpers && <p>👥 Nearby responders alerted</p>}
          </div>
        )}

        {protocols.length > 0 && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Protocols / Supplies</p>
            <ul className="text-gray-200 text-sm list-disc list-inside space-y-1">
              {protocols.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {clarifying.length > 0 && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Clarification Requested</p>
            <ul className="text-gray-300 text-sm list-disc list-inside space-y-1">
              {clarifying.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {metadata.helper_instructions && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Helper Instructions</p>
            <p className="text-gray-300 text-sm leading-relaxed">{metadata.helper_instructions}</p>
          </div>
        )}

        {instructions?.voice_text && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Voice Guidance</p>
            <p className="text-gray-200 text-sm leading-relaxed">{instructions.voice_text}</p>
          </div>
        )}

        {steps.length > 0 && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">First Aid Steps</p>
            <ol className="text-gray-200 text-sm list-decimal list-inside space-y-1">
              {steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ol>
          </div>
        )}

        {warningSigns.length > 0 && (
          <div>
            <p className="text-xs uppercase tracking-wider text-gray-500">Warning Signs</p>
            <ul className="text-gray-300 text-sm list-disc list-inside space-y-1">
              {warningSigns.map((sign, idx) => (
                <li key={idx}>{sign}</li>
              ))}
            </ul>
          </div>
        )}

        {instructions?.call_911_if && (
          <div className="bg-red-900/30 border border-red-700 rounded-md p-3 text-red-100 text-sm">
            <p className="font-semibold mb-1">Call 911 if:</p>
            <p>{instructions.call_911_if}</p>
          </div>
        )}
      </div>
    );
  };

  // Find latest triage event to use as fallback classification
  const latestTriageEvent = [...timeline].reverse().find((event: any) =>
    typeof event?.step === 'string' && event.step.toLowerCase().startsWith('triage')
  );

  let fallbackType: string | undefined;
  let fallbackSeverity: string | undefined;

  if (latestTriageEvent) {
    if (latestTriageEvent.metadata) {
      fallbackType = latestTriageEvent.metadata.type ?? fallbackType;
      fallbackSeverity = latestTriageEvent.metadata.severity ?? fallbackSeverity;
    }

    if (!fallbackType || !fallbackSeverity) {
      const match = latestTriageEvent.step.match(/Triage:\s*([^()]+)(?:\(([^)]+)\))?/i);
      if (match) {
        const [, typeText, severityText] = match;
        fallbackType = fallbackType || typeText?.trim().replace(/\s+/g, '_');
        fallbackSeverity = fallbackSeverity || severityText?.trim();
      }
    }
  }

  const durationMin = summary.duration_seconds ? Math.floor(summary.duration_seconds / 60) : 0;
  const durationSec = summary.duration_seconds ? summary.duration_seconds % 60 : 0;
  const resolvedType = (summary.type || fallbackType || '').toString();
  const resolvedSeverity = (summary.severity || fallbackSeverity || '').toString();
  const incidentType = resolvedType
    ? resolvedType.replace(/_/g, ' ').toUpperCase()
    : 'UNKNOWN';
  const severity = resolvedSeverity ? resolvedSeverity.toUpperCase() : 'UNKNOWN';

  const severityClassMap: Record<string, string> = {
    CRITICAL: 'text-red-400',
    SEVERE: 'text-orange-400',
    URGENT: 'text-orange-400',
    MODERATE: 'text-yellow-300',
    MILD: 'text-green-300',
  };
  const severityClass = severityClassMap[severity] || 'text-yellow-400';

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
                {incidentType}
              </p>
            </div>
            <div>
              <p className="text-gray-400">Severity</p>
              <p className={`font-semibold text-lg ${severityClass}`}>
                {severity}
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
            {timeline.map((event: any, index: number) => {
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
                    {renderTimelineDetails(event.metadata)}
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
