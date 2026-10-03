import React, { useState } from 'react';
import { Brain, ChevronRight, ChevronLeft } from 'lucide-react';
import { Quiz, QuizResult } from '../../types';
import QuizCard from '../quiz/QuizCard';
import QuizResults from '../quiz/QuizResults';
import { useSubmitQuiz } from '../../hooks/useQuiz';

interface QuizPanelProps {
  quiz: Quiz;
}

export const QuizPanel: React.FC<QuizPanelProps> = ({ quiz }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [result, setResult] = useState<QuizResult | null>(null);
  
  const submitMutation = useSubmitQuiz();

  const handleSelect = (optionIndex: number) => {
    setAnswers(prev => ({ ...prev, [currentIndex]: optionIndex }));
  };

  const handleNext = () => {
    if (currentIndex < quiz.questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  };

  const handleSubmit = () => {
    submitMutation.mutate({ quizId: quiz.id, answers }, {
      onSuccess: (data) => setResult(data)
    });
  };

  if (result) {
    return <QuizResults result={result} quiz={quiz} onRetake={() => { setResult(null); setAnswers({}); setCurrentIndex(0); }} />;
  }

  const currentQuestion = quiz.questions[currentIndex];
  const isAnswered = answers[currentIndex] !== undefined;

  return (
    <div className="bg-dark-card rounded-xl border border-dark-border p-6 max-w-3xl mx-auto animate-slide-up shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Brain className="text-accent" />
          Test Your Knowledge
        </h3>
        <span className="text-sm text-gray-400 font-medium bg-dark-surface px-3 py-1 rounded-full">
          Question {currentIndex + 1} of {quiz.questions.length}
        </span>
      </div>

      <div className="w-full bg-dark-surface h-1.5 rounded-full mb-8 overflow-hidden">
        <div 
          className="bg-accent h-full transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / quiz.questions.length) * 100}%` }}
        />
      </div>

      <QuizCard 
        question={currentQuestion} 
        selectedIndex={answers[currentIndex]} 
        onSelect={handleSelect} 
      />

      <div className="flex justify-between items-center mt-8 pt-6 border-t border-dark-border">
        <button
          onClick={handlePrev}
          disabled={currentIndex === 0}
          className="flex items-center gap-2 px-4 py-2 bg-dark-surface rounded-lg text-white disabled:opacity-50 hover:bg-dark-border transition-all duration-200"
        >
          <ChevronLeft size={20} />
          Previous
        </button>
        
        {currentIndex === quiz.questions.length - 1 ? (
          <button
            onClick={handleSubmit}
            disabled={Object.keys(answers).length !== quiz.questions.length || submitMutation.isPending}
            className="flex items-center gap-2 px-6 py-2 bg-accent hover:bg-blue-600 rounded-lg text-white font-medium disabled:opacity-50 transition-all duration-200 btn-glow shadow-md shadow-accent/20"
          >
            {submitMutation.isPending ? 'Submitting...' : 'Submit Quiz'}
          </button>
        ) : (
          <button
            onClick={handleNext}
            disabled={!isAnswered}
            className="flex items-center gap-2 px-4 py-2 bg-accent hover:bg-blue-600 rounded-lg text-white disabled:opacity-50 transition-all duration-200 btn-glow"
          >
            Next
            <ChevronRight size={20} />
          </button>
        )}
      </div>
    </div>
  );
};

export default QuizPanel;
