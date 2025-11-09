import React, { useState, useEffect, useRef } from 'react';

export default function Metronome({ bpm }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [beat, setBeat] = useState(false);
  const intervalRef = useRef(null);
  const audioContextRef = useRef(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    if (isPlaying) {
      startMetronome();
    } else if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      setBeat(false);
    }
  }, [isPlaying, bpm]);

  const startMetronome = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    const intervalMs = (60_000) / bpm;

    intervalRef.current = setInterval(() => {
      setBeat(prev => !prev);
      playClick();
    }, intervalMs);
  };

  const playClick = () => {
    if (!audioContextRef.current) return;

    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.type = 'square';
    oscillator.frequency.setValueAtTime(1000, ctx.currentTime);

    gainNode.gain.setValueAtTime(0.3, ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.start();
    oscillator.stop(ctx.currentTime + 0.1);
  };

  const toggleMetronome = () => {
    setIsPlaying(prev => !prev);
  };

  return (
    <div className="mt-6 p-4 rounded-xl bg-slate-900/60 border border-red-500/40 shadow-lg">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-xs text-red-300/80 font-semibold uppercase tracking-wide">
            CPR Compression Guide
          </p>
          <p className="text-sm text-slate-100">
            Follow the beat for {bpm} compressions/min
          </p>
        </div>

        <div
          className={`w-10 h-10 rounded-full border-2 flex items-center justify-center transition-all duration-150 ${
            beat ? 'bg-red-500 border-red-300 shadow-[0_0_25px_rgba(248,113,113,0.8)] scale-110' 
                 : 'bg-slate-950/80 border-red-500/60'
          }`}
        >
          <div className="w-2 h-2 rounded-full bg-red-100" />
        </div>
      </div>

      <button
        onClick={toggleMetronome}
        className={`w-full mt-4 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all border border-red-500/50 flex items-center justify-center gap-2
          ${isPlaying 
            ? 'bg-red-600 hover:bg-red-700 text-white' 
            : 'bg-white hover:bg-gray-100 text-red-900'
        }`}
      >
        {isPlaying ? '⏸ Pause Metronome' : '▶ Start Metronome'}
      </button>

      <p className="text-xs text-red-200 mt-3 text-center">
        Push hard and fast to the beat • Let chest recoil completely
      </p>
    </div>
  );
}
