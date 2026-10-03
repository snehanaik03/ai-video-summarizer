import React from 'react';
import { RotateCcw, Save } from 'lucide-react';
import { Quiz, QuizResult as QuizResultType } from '../../types';

interface QuizResultsProps {
  result: QuizResultType;
  quiz: Quiz;
  onRetake: () => void;
}

export const QuizResults: React.FC<QuizResultsProps> = ({ result, onRetake }) => {
  const getMessage = () => {
    if (result.percentage >= 90) return "Excellent!";
    if (result.percentage >= 70) return "Good job!";
    return "Keep studying!";
  };

  return (
    <div className="bg-dark-card rounded-xl border border-dark-border p-8 max-w-2xl mx-auto text-center">
      <h2 className="text-3xl font-bold text-white mb-2">Quiz Completed!</h2>
      <p className="text-gray-400 mb-8">{getMessage()}</p>

      <div className="relative w-48 h-48 mx-auto mb-8 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#1e293b" strokeWidth="8" />
          <circle 
            cx="50" cy="50" r="45" 
            fill="none" 
            stroke={result.percentage >= 70 ? "#10b981" : "#f59e0b"} 
            strokeWidth="8" 
            strokeDasharray={`${result.percentage * 2.827} 282.7`} 
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-bold text-white">{result.percentage}%</span>
          <span className="text-sm text-gray-400">Score</span>
        </div>
      </div>

      <p className="text-lg text-white mb-8">
        You scored <span className="font-bold">{result.score}</span> out of <span className="font-bold">{result.total}</span> questions correctly.
      </p>

      <div className="flex justify-center gap-4">
        <button 
          onClick={onRetake}
          className="flex items-center gap-2 px-6 py-3 bg-dark-surface hover:bg-dark-border rounded-xl text-white font-medium transition-colors"
        >
          <RotateCcw size={18} />
          Retake Quiz
        </button>
        <button className="flex items-center gap-2 px-6 py-3 bg-accent hover:bg-blue-600 rounded-xl text-white font-medium transition-colors">
          <Save size={18} />
          Save Results
        </button>
      </div>
    </div>
  );
};

export default QuizResults;
