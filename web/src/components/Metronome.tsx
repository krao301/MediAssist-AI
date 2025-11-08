import React, { useState, useEffect, useRef } from 'react';

interface MetronomeProps {
  bpm: number;
}

export default function Metronome({ bpm }: MetronomeProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [beat, setBeat] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  useEffect(() => {
    // Initialize Audio Context for beep sound
    if (typeof window !== 'undefined') {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (isPlaying) {
      const interval = 60000 / bpm;
      
      intervalRef.current = setInterval(() => {
        playBeep();
        setBeat(true);
        setTimeout(() => setBeat(false), 150);
      }, interval);
      
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }
  }, [isPlaying, bpm]);

  const playBeep = () => {
    if (!audioContextRef.current) return;
    
    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
    
    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + 0.1);
  };

  const toggleMetronome = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="bg-gradient-to-br from-red-900 to-red-800 rounded-xl p-6 shadow-2xl border border-red-600">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-white mb-2">CPR Metronome</h3>
          <p className="text-red-200">{bpm} BPM • {(60 / bpm).toFixed(1)}s per beat</p>
        </div>
        
        <div className={`w-20 h-20 rounded-full flex items-center justify-center transition-all ${
          beat ? 'metronome-beat bg-white scale-110' : 'bg-red-700'
        }`}>
          <span className="text-3xl">{beat ? '💥' : '♥'}</span>
        </div>
      </div>
      
      <button
        onClick={toggleMetronome}
        className={`w-full mt-4 font-bold py-3 px-6 rounded-lg transition ${
          isPlaying 
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
