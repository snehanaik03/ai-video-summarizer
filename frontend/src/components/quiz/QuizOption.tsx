import React from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';

interface QuizOptionProps {
  label: string;
  text: string;
  isSelected: boolean;
  isCorrect: boolean;
  isRevealed?: boolean;
  onSelect: () => void;
}

export const QuizOption: React.FC<QuizOptionProps> = ({ label, text, isSelected, isCorrect, isRevealed, onSelect }) => {
  let containerClasses = "flex items-center p-4 border rounded-xl cursor-pointer transition-all duration-200 ";
  let icon = null;

  if (isRevealed) {
    if (isCorrect) {
      containerClasses += "bg-green-500/10 border-green-500 text-white";
      icon = <CheckCircle2 className="text-green-500 ml-auto" size={20} />;
    } else if (isSelected && !isCorrect) {
      containerClasses += "bg-red-500/10 border-red-500 text-white";
      icon = <XCircle className="text-red-500 ml-auto" size={20} />;
    } else {
      containerClasses += "bg-dark-surface border-dark-border text-gray-400 opacity-50 cursor-not-allowed";
    }
  } else {
    if (isSelected) {
      containerClasses += "bg-accent/10 border-accent text-white";
    } else {
      containerClasses += "bg-dark-surface border-dark-border text-gray-300 hover:border-gray-500 hover:bg-dark-surface/80";
    }
  }

  return (
    <button 
      onClick={onSelect}
      disabled={isRevealed}
      className={`w-full text-left ${containerClasses}`}
    >
      <div className="flex items-center gap-4 w-full">
        <span className={`w-8 h-8 flex items-center justify-center rounded-lg text-sm font-bold ${
          isSelected ? 'bg-accent text-white' : 'bg-dark-card text-gray-400'
        }`}>
          {label}
        </span>
        <span className="flex-1 text-sm md:text-base">{text}</span>
        {icon}
      </div>
    </button>
  );
};

export default QuizOption;
