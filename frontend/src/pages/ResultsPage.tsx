import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Bookmark } from 'lucide-react';
import { useGetSummary } from '../hooks/useSummarize';
import { useGenerateQuiz } from '../hooks/useQuiz';
import SummaryDisplay from '../components/output/SummaryDisplay';
import TranscriptView from '../components/output/TranscriptView';
import QuizPanel from '../components/output/QuizPanel';

type ResultTab = 'summary' | 'transcript' | 'quiz';

export const ResultsPage = () => {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<ResultTab>('summary');
  
  const { data: summary, isLoading: isLoadingSummary, error } = useGetSummary(id);
  const generateQuizMutation = useGenerateQuiz();
  const [quiz, setQuiz] = useState<any>(null);

  const handleTabChange = (tab: ResultTab) => {
    setActiveTab(tab);
    if (tab === 'quiz' && !quiz && summary) {
      generateQuizMutation.mutate(summary.id, {
        onSuccess: (data) => setQuiz(data)
      });
    }
  };

  if (isLoadingSummary) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <h2 className="text-2xl font-bold text-red-500 mb-4">Error loading summary</h2>
        <Link to="/app" className="text-accent hover:underline flex items-center gap-2">
          <ArrowLeft size={16} /> Back to Summarizer
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-8 page-transition">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <Link to="/app" className="inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white mb-4 transition-colors">
            <ArrowLeft size={16} /> Back
          </Link>
          <div className="flex items-center gap-4">
            {summary.thumbnail_url && (
              <img src={summary.thumbnail_url} alt="Thumbnail" className="w-24 h-16 object-cover rounded-lg border border-dark-border" />
            )}
            <h1 className="text-xl md:text-2xl font-bold text-white line-clamp-2">{summary.title}</h1>
          </div>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-dark-surface hover:bg-dark-border rounded-lg text-white text-sm font-medium transition-colors whitespace-nowrap">
          <Bookmark size={16} />
          Save to Notes
        </button>
      </div>

      <div className="flex border-b border-dark-border mb-6">
        <button
          onClick={() => handleTabChange('summary')}
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${activeTab === 'summary' ? 'text-accent' : 'text-gray-400 hover:text-gray-200'}`}
        >
          Summary
          {activeTab === 'summary' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent" />}
        </button>
        <button
          onClick={() => handleTabChange('transcript')}
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${activeTab === 'transcript' ? 'text-accent' : 'text-gray-400 hover:text-gray-200'}`}
        >
          Transcript
          {activeTab === 'transcript' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent" />}
        </button>
        <button
          onClick={() => handleTabChange('quiz')}
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${activeTab === 'quiz' ? 'text-accent' : 'text-gray-400 hover:text-gray-200'}`}
        >
          Quiz
          {activeTab === 'quiz' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent" />}
        </button>
      </div>

      <div className="mt-6">
        {activeTab === 'summary' && <SummaryDisplay summary={summary} />}
        {activeTab === 'transcript' && <TranscriptView transcript={summary.transcript} />}
        {activeTab === 'quiz' && (
          generateQuizMutation.isPending ? (
            <div className="flex flex-col items-center justify-center py-20">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent mb-4"></div>
              <p className="text-gray-400">Generating intelligent quiz questions...</p>
            </div>
          ) : quiz ? (
            <QuizPanel quiz={quiz} />
          ) : (
            <div className="text-center py-20 text-red-400">Failed to generate quiz.</div>
          )
        )}
      </div>
    </div>
  );
};

export default ResultsPage;
