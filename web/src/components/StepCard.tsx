import { useState, useEffect } from 'react';

interface StepCardProps {
  step: {
    title: string;
    detail: string;
    timer_s?: number;
    cadence_bpm?: number;
  };
  onComplete: () => void;
  isLast: boolean;
}

export default function StepCard({ step, onComplete, isLast }: StepCardProps) {
  const [timeRemaining, setTimeRemaining] = useState(step.timer_s || 0);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    if (started && step.timer_s && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(time => time - 1);
      }, 1000);
      
      return () => clearTimeout(timer);
    }
    
    if (started && timeRemaining === 0 && step.timer_s) {
      // Timer finished, but don't auto-proceed
    }
  }, [timeRemaining, started, step.timer_s]);

  const handleStart = () => {
    setStarted(true);
  };

  return (
    <div className="bg-gradient-to-br from-blue-900 to-blue-800 rounded-xl p-6 shadow-2xl border border-blue-600">
      <div className="flex items-start justify-between mb-4">
        <h2 className="text-2xl font-bold text-white">{step.title}</h2>
        {step.timer_s && (
          <div className={`text-3xl font-bold px-4 py-2 rounded-lg ${
            timeRemaining <= 10 && timeRemaining > 0 ? 'bg-red-600 animate-pulse' : 'bg-blue-700'
          }`}>
            {timeRemaining > 0 ? `${timeRemaining}s` : '✓'}
          </div>
        )}
      </div>
      
      <p className="text-lg text-blue-100 leading-relaxed mb-6">
        {step.detail}
      </p>
      
      {step.cadence_bpm && (
        <div className="bg-blue-700/50 rounded-lg p-3 mb-4">
          <p className="text-blue-200 font-semibold">
            ♥ Target: {step.cadence_bpm} compressions/minute
          </p>
        </div>
      )}
      
      <div className="flex gap-3">
        {step.timer_s && !started && (
          <button
            onClick={handleStart}
            className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition"
          >
            ▶ Start Timer
          </button>
        )}
        
        <button
          onClick={onComplete}
          className={`flex-1 font-bold py-3 px-6 rounded-lg transition ${
            isLast 
              ? 'bg-purple-600 hover:bg-purple-700 text-white' 
              : 'bg-white hover:bg-gray-100 text-blue-900'
          }`}
        >
          {isLast ? '✓ Complete' : 'Next Step →'}
        </button>
      </div>
    </div>
  );
}
