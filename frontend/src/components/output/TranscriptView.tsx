import React from 'react';
import { Search } from 'lucide-react';

interface TranscriptViewProps {
  transcript: string;
}

export const TranscriptView: React.FC<TranscriptViewProps> = ({ transcript }) => {
  return (
    <div className="bg-dark-card rounded-xl border border-dark-border flex flex-col h-[600px]">
      <div className="p-4 border-b border-dark-border flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
          <input 
            type="text" 
            placeholder="Search in transcript..." 
            className="w-full bg-dark-surface border border-dark-border rounded-lg py-2 pl-9 pr-4 text-sm text-white focus:outline-none focus:border-accent"
          />
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">{transcript}</p>
      </div>
    </div>
  );
};

export default TranscriptView;
