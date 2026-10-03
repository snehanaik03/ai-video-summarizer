import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InputTabs, { TabType } from '../components/input/InputTabs';
import UrlInput from '../components/input/UrlInput';
import FileUpload from '../components/input/FileUpload';
import ExampleVideos from '../components/examples/ExampleVideos';
import { useSummarizeYouTube } from '../hooks/useSummarize';

export const HomePage = () => {
  const [activeTab, setActiveTab] = useState<TabType>('youtube');
  const [urls, setUrls] = useState<string[]>(['']);
  const navigate = useNavigate();
  const summarizeMutation = useSummarizeYouTube();

  const handleGenerate = (targetUrls?: string[], isPremium: boolean = false, separateSpeaker: boolean = false) => {
    const validUrls = (targetUrls || urls).filter(u => u.trim() !== '');
    if (validUrls.length === 0) return;

    const request = {
      urls: validUrls,
      processing_tier: isPremium ? 'premium' : 'basic',
      separate_speaker: separateSpeaker,
    };

    summarizeMutation.mutate(request, {
      onSuccess: (data) => {
        navigate(`/results/${data.id}`);
      },
    });
  };

  const handleExampleSelect = (url: string) => {
    setUrls([url]);
    handleGenerate([url], false, false);
  };

  const errorMessage = (summarizeMutation.error as any)?.response?.data?.message ||
    (summarizeMutation.error as any)?.response?.data?.detail ||
    (summarizeMutation.error as any)?.message;

  return (
    <div className="max-w-5xl mx-auto px-6 py-12 page-transition">
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">Free YouTube Video Summarizer</h1>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto">
          Batch summarize YouTube videos and playlists in seconds. Extract key insights, generate quizzes, and save notes effortlessly.
        </p>
      </div>

      {summarizeMutation.isError && (
        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm flex items-center justify-between animate-fade-in">
          <span>{errorMessage || "Failed to process video. Please verify the URL is accessible."}</span>
          <button 
            onClick={() => summarizeMutation.reset()} 
            className="text-xs underline ml-4 hover:text-red-300 transition-colors"
          >
            Dismiss
          </button>
        </div>
      )}

      <div className="bg-dark-card border border-dark-border rounded-2xl p-6 md:p-8 shadow-2xl animate-slide-up animation-delay-100 card-hover">
        <InputTabs activeTab={activeTab} onChange={setActiveTab} />
        
        {activeTab === 'youtube' ? (
          <UrlInput 
            onSubmit={(u, p, s) => handleGenerate(u, p, s)} 
            isLoading={summarizeMutation.isPending}
            urls={urls}
            setUrls={setUrls}
          />
        ) : (
          <div className="space-y-6">
            <FileUpload />
            <button className="w-full bg-gradient-to-r from-accent to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-xl py-4 font-bold text-lg transition-all shadow-lg shadow-accent/20 btn-glow">
              Generate Summary
            </button>
          </div>
        )}
      </div>

      <div className="animate-fade-in animation-delay-300">
        <ExampleVideos onSelect={handleExampleSelect} />
      </div>
    </div>
  );
};

export default HomePage;
