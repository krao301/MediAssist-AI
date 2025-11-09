import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getIncidentSummary } from '../lib/api';

export default function Summary() {
  const { incidentId } = useParams();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const response = await getIncidentSummary(incidentId, 'detailed');
      setSummary(response.data);
    } catch (error) {
      console.error('Failed to load summary', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center">
        <div className="animate-pulse text-slate-400 text-sm">
          Preparing your incident summary...
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center">
        <div className="text-center space-y-3">
          <p className="text-slate-300 text-sm">No summary available for this incident.</p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-600 text-slate-950 text-xs font-semibold"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const {
    incident_id,
    status,
    started_at,
    resolved_at,
    steps,
    patient_info,
    location,
    risk_level,
    summary_text,
  } = summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-3xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between gap-3 mb-4">
          <div>
            <h1 className="text-lg font-semibold text-sky-400">
              Incident Summary
            </h1>
            <p className="text-[11px] text-slate-400">
              Detailed record of first aid actions and context for emergency responders.
            </p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-[10px] text-slate-200"
          >
            ← Back to Home
          </button>
        </div>

        <div className="grid gap-3 mb-4 text-[11px]">
          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3">
            <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
              Incident ID
            </p>
            <p className="font-mono text-sky-300 text-[10px]">
              {incident_id || incidentId}
            </p>
          </div>
          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3 grid grid-cols-2 gap-3">
            <div>
              <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
                Status
              </p>
              <p className="font-semibold text-emerald-400 text-[10px]">
                {status || 'RESOLVED'}
              </p>
            </div>
            <div>
              <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
                Risk Level
              </p>
              <p className="font-semibold text-orange-400 text-[10px]">
                {risk_level || 'MODERATE'}
              </p>
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3 grid grid-cols-2 gap-3">
            <div>
              <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
                Started At
              </p>
              <p className="text-[10px] text-slate-200">
                {started_at || 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
                Resolved At
              </p>
              <p className="text-[10px] text-slate-200">
                {resolved_at || 'N/A'}
              </p>
            </div>
          </div>
        </div>

        {patient_info && (
          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3 mb-3 text-[10px]">
            <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
              Patient Info
            </p>
            <p className="text-slate-200">
              {patient_info}
            </p>
          </div>
        )}

        {location && (
          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3 mb-3 text-[10px]">
            <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
              Location
            </p>
            <p className="text-slate-200">
              {location}
            </p>
          </div>
        )}

        {Array.isArray(steps) && steps.length > 0 && (
          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3 mb-3 text-[10px]">
            <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-2">
              Steps Performed
            </p>
            <ul className="list-disc list-inside space-y-1 text-slate-200">
              {steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ul>
          </div>
        )}

        {summary_text && (
          <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3 mb-3 text-[10px]">
            <p className="text-slate-400 uppercase tracking-wide text-[9px] mb-1">
              Summary
            </p>
            <p className="text-slate-200 whitespace-pre-line">
              {summary_text}
            </p>
          </div>
        )}

        <div className="bg-purple-900/30 border border-purple-600 rounded-lg p-3 text-purple-200 text-[9px]">
          <p className="font-semibold mb-1">📋 For EMS/Medical Personnel:</p>
          <p>
            This report can be shared with emergency responders to provide context on
            first aid steps performed before their arrival.
          </p>
        </div>
      </div>
    </div>
  );
}
