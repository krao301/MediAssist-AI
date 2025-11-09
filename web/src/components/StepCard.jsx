import React, { useState, useEffect } from 'react';

export default function StepCard({ step, onComplete, isLast }) {
  const [timeRemaining, setTimeRemaining] = useState(step.timer_s || 0);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    let timer;
    if (started && timeRemaining > 0) {
      timer = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            onComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [started, timeRemaining, onComplete]);

  const startTimer = () => {
    if (!started) {
      setStarted(true);
    }
  };

  const hasTimer = !!step.timer_s;

  return (
    <div className="bg-slate-900/80 border border-slate-700/80 rounded-2xl p-4 mb-3 shadow-lg backdrop-blur">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-sky-500/10 border border-sky-400/40 flex items-center justify-center text-sky-300 text-sm font-semibold">
          ✓
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-sky-100 tracking-wide mb-1">
            {step.title}
          </h3>
          <p className="text-xs text-slate-300/95 leading-relaxed mb-2">
            {step.detail}
          </p>

          {hasTimer && (
            <div className="flex items-center gap-2 mb-2">
              <div className="h-1.5 flex-1 bg-slate-800/90 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-400/90 transition-all duration-1000"
                  style={{
                    width: `${(timeRemaining / step.timer_s) * 100}%`,
                  }}
                />
              </div>
              <span className="text-[10px] text-emerald-300/90 font-mono">
                {timeRemaining}s
              </span>
            </div>
          )}

          <div className="flex items-center gap-2 mt-1">
            {hasTimer && !started && (
              <button
                onClick={startTimer}
                className="text-[10px] px-2 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-400/40 hover:bg-emerald-500/20 transition-all"
              >
                ▶ Start Timer
              </button>
            )}

            {!hasTimer && (
              <span className="inline-flex items-center text-[10px] px-2 py-1 rounded-full bg-slate-800/90 text-slate-300/95 border border-slate-600/70">
                Manual step • tap "{isLast ? 'Complete' : 'Next Step'}" when done
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="flex gap-2 mt-3 pt-2 border-t border-slate-800/80">
        <button
          onClick={onComplete}
          className={`flex-1 font-bold py-2.5 px-4 rounded-lg text-[11px] transition-all ${
            isLast
              ? 'bg-purple-600 hover:bg-purple-700 text-white shadow-md shadow-purple-500/30'
              : 'bg-sky-500 hover:bg-sky-600 text-slate-950 shadow-md shadow-sky-500/30'
          }`}
        >
          {isLast ? '✓ Complete' : 'Next Step →'}
        </button>
      </div>
    </div>
  );
}
