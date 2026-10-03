import React from 'react';
import { Lightbulb } from 'lucide-react';
import { MCQQuestion } from '../../types';
import QuizOption from './QuizOption';

interface QuizCardProps {
  question: MCQQuestion;
  selectedIndex?: number;
  onSelect: (index: number) => void;
  showExplanation?: boolean;
}

export const QuizCard: React.FC<QuizCardProps> = ({ question, selectedIndex, onSelect, showExplanation }) => {
  const isAnswered = selectedIndex !== undefined;

  const getDifficultyColor = (diff: string) => {
    switch(diff) {
      case 'Easy': return 'bg-green-500/20 text-green-500';
      case 'Medium': return 'bg-yellow-500/20 text-yellow-500';
      case 'Hard': return 'bg-red-500/20 text-red-500';
      default: return 'bg-gray-500/20 text-gray-500';
    }
  };

  return (
    <div className="animate-slide-up">
      <div className="flex gap-2 mb-4">
        <span className={`text-xs font-bold px-2 py-1 rounded ${getDifficultyColor(question.difficulty)}`}>
          {question.difficulty}
        </span>
        <span className="text-xs font-bold px-2 py-1 rounded bg-purple-500/20 text-purple-400">
          {question.concept_tested}
        </span>
      </div>
      
      <h4 className="text-xl font-medium text-white mb-6 leading-relaxed">
        {question.question}
      </h4>

      <div className="space-y-3">
        {question.options.map((option, idx) => (
          <QuizOption
            key={idx}
            label={String.fromCharCode(65 + idx)}
            text={option}
            isSelected={selectedIndex === idx}
            isCorrect={idx === question.correct_index}
            isRevealed={isAnswered || showExplanation}
            onSelect={() => !isAnswered && onSelect(idx)}
          />
        ))}
      </div>

      {(isAnswered || showExplanation) && (
        <div className="mt-6 bg-accent/10 border border-accent/20 rounded-lg p-4 animate-in fade-in slide-in-from-top-2">
          <h5 className="flex items-center gap-2 text-accent font-semibold mb-2">
            <Lightbulb size={18} />
            Explanation
          </h5>
          <p className="text-gray-300 text-sm leading-relaxed">
            {question.explanation}
          </p>
        </div>
      )}
    </div>
  );
};

export default QuizCard;
