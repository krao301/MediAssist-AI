import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';

interface LearningStats {
  success: boolean;
  overall_accuracy: number;
  total_predictions: number;
  predictions_with_feedback: number;
  correct_predictions: number;
  accuracy_by_type: Record<string, { correct: number; total: number; accuracy: number }>;
  common_mistakes: Array<{
    predicted: string;
    actual: string;
    count: number;
  }>;
  recent_improvement: {
    last_7_days_accuracy: number;
    previous_7_days_accuracy: number;
    improvement: number;
    trend: string;
  };
  feedback_coverage: number;
  summary: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/learning/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch learning stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 to-black">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 to-black">
        <div className="text-white">Failed to load dashboard</div>
      </div>
    );
  }

  const accuracyColor = stats.overall_accuracy >= 90 ? 'text-green-400' : 
                       stats.overall_accuracy >= 75 ? 'text-yellow-400' : 'text-red-400';
  
  const trendIcon = stats.recent_improvement.trend === 'improving' ? '📈' :
                   stats.recent_improvement.trend === 'declining' ? '📉' : '➡️';

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300 mb-4"
          >
            ← Back to Home
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">🧠 AI Learning Dashboard</h1>
          <p className="text-gray-400">Real-time AI performance and continuous learning</p>
        </div>

        {/* Hero Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 border border-blue-500 rounded-lg p-6">
            <div className="text-3xl mb-2">🎯</div>
            <div className={`text-4xl font-bold ${accuracyColor} mb-1`}>
              {stats.overall_accuracy.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-300">Overall Accuracy</div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/50 to-purple-800/30 border border-purple-500 rounded-lg p-6">
            <div className="text-3xl mb-2">📊</div>
            <div className="text-4xl font-bold text-purple-300 mb-1">
              {stats.total_predictions}
            </div>
            <div className="text-sm text-gray-300">Total Predictions</div>
          </div>

          <div className="bg-gradient-to-br from-green-900/50 to-green-800/30 border border-green-500 rounded-lg p-6">
            <div className="text-3xl mb-2">✅</div>
            <div className="text-4xl font-bold text-green-300 mb-1">
              {stats.correct_predictions}
            </div>
            <div className="text-sm text-gray-300">Correct Predictions</div>
          </div>

          <div className="bg-gradient-to-br from-orange-900/50 to-orange-800/30 border border-orange-500 rounded-lg p-6">
            <div className="text-3xl mb-2">{trendIcon}</div>
            <div className={`text-4xl font-bold ${stats.recent_improvement.improvement >= 0 ? 'text-green-300' : 'text-red-300'} mb-1`}>
              {stats.recent_improvement.improvement >= 0 ? '+' : ''}{stats.recent_improvement.improvement.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-300">Last 7 Days</div>
          </div>
        </div>

        {/* Learning Trend */}
        {stats.total_predictions > 0 && (
          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">📈 Learning Trend</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Last 7 Days</span>
                <span className="text-blue-400 font-semibold">{stats.recent_improvement.last_7_days_accuracy.toFixed(1)}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Previous 7 Days</span>
                <span className="text-gray-400 font-semibold">{stats.recent_improvement.previous_7_days_accuracy.toFixed(1)}%</span>
              </div>
              <div className="flex items-center justify-between pt-3 border-t border-gray-700">
                <span className="text-white font-semibold">Improvement</span>
                <span className={`font-bold text-xl ${stats.recent_improvement.improvement >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {stats.recent_improvement.improvement >= 0 ? '+' : ''}{stats.recent_improvement.improvement.toFixed(1)}% {trendIcon}
                </span>
              </div>
            </div>
            <div className="mt-4 p-4 bg-blue-900/30 border border-blue-700 rounded-lg">
              <p className="text-sm text-blue-200">
                <strong>💡 Insight:</strong> The AI is {stats.recent_improvement.trend}! 
                {stats.recent_improvement.trend === 'improving' && ' Keep collecting feedback to accelerate learning.'}
                {stats.recent_improvement.trend === 'stable' && ' More training data needed to see improvement.'}
                {stats.recent_improvement.trend === 'declining' && ' Review recent feedback for quality issues.'}
              </p>
            </div>
          </div>
        )}

        {/* Accuracy by Emergency Type */}
        {Object.keys(stats.accuracy_by_type).length > 0 && (
          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">🔍 Accuracy by Emergency Type</h2>
            <div className="space-y-3">
              {Object.entries(stats.accuracy_by_type).map(([type, data]) => {
                const percentage = data.accuracy * 100;
                const barColor = percentage >= 90 ? 'bg-green-500' : 
                               percentage >= 75 ? 'bg-yellow-500' : 'bg-red-500';
                
                return (
                  <div key={type}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-white font-medium capitalize">{type.replace(/_/g, ' ')}</span>
                      <span className="text-gray-400 text-sm">
                        {data.correct}/{data.total} ({percentage.toFixed(1)}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-3">
                      <div
                        className={`${barColor} h-3 rounded-full transition-all duration-500`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Common Mistakes */}
        {stats.common_mistakes.length > 0 && (
          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">⚠️ Common Mistakes</h2>
            <p className="text-gray-400 text-sm mb-4">
              The AI learns from these patterns to improve future predictions
            </p>
            <div className="space-y-3">
              {stats.common_mistakes.map((mistake, idx) => (
                <div key={idx} className="bg-red-900/20 border border-red-700 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-red-400 font-semibold capitalize">
                          Predicted: {mistake.predicted.replace(/_/g, ' ')}
                        </span>
                        <span className="text-gray-500">→</span>
                        <span className="text-green-400 font-semibold capitalize">
                          Actual: {mistake.actual.replace(/_/g, ' ')}
                        </span>
                      </div>
                      <div className="text-gray-400 text-sm">
                        Occurred {mistake.count} time{mistake.count !== 1 ? 's' : ''}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Feedback Coverage */}
        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6">
          <h2 className="text-2xl font-bold text-white mb-4">📝 Feedback Coverage</h2>
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-300">Predictions with Feedback</span>
              <span className="text-blue-400 font-semibold">
                {stats.predictions_with_feedback}/{stats.total_predictions} ({stats.feedback_coverage.toFixed(1)}%)
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-4">
              <div
                className="bg-blue-500 h-4 rounded-full transition-all duration-500"
                style={{ width: `${stats.feedback_coverage}%` }}
              ></div>
            </div>
          </div>
          <p className="text-sm text-gray-400">
            {stats.feedback_coverage < 50 && '💡 Collect more feedback to accelerate learning!'}
            {stats.feedback_coverage >= 50 && stats.feedback_coverage < 80 && '👍 Good feedback coverage. Keep it up!'}
            {stats.feedback_coverage >= 80 && '🌟 Excellent feedback coverage! AI is learning rapidly.'}
          </p>
        </div>

        {/* Summary */}
        <div className="mt-8 bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-4xl">🤖</span>
            <h2 className="text-2xl font-bold text-white">AI Status</h2>
          </div>
          <p className="text-gray-300 text-lg">{stats.summary}</p>
          {stats.total_predictions === 0 && (
            <div className="mt-4 p-4 bg-yellow-900/30 border border-yellow-700 rounded-lg">
              <p className="text-yellow-200 text-sm">
                <strong>🚀 Getting Started:</strong> Run demo scenarios from the home screen to see the AI in action!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
