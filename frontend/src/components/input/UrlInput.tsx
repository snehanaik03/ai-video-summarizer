import React, { useState } from 'react';
import { Link2, Sparkles } from 'lucide-react';
import SourceOptions from './SourceOptions';

interface UrlInputProps {
  onSubmit: (urls: string[], isPremium: boolean, separateSpeaker: boolean) => void;
  isLoading?: boolean;
  urls?: string[];
  setUrls?: React.Dispatch<React.SetStateAction<string[]>>;
}

export const UrlInput: React.FC<UrlInputProps> = ({ 
  onSubmit, 
  isLoading,
  urls: externalUrls,
  setUrls: externalSetUrls
}) => {
  const [internalUrls, setInternalUrls] = useState<string[]>(['']);
  const urls = externalUrls !== undefined ? externalUrls : internalUrls;
  const setUrls = externalSetUrls !== undefined ? externalSetUrls : setInternalUrls;
  const [isPremium, setIsPremium] = useState(false);
  const [separateSpeaker, setSeparateSpeaker] = useState(false);

  const handleSubmit = () => {
    const validUrls = urls.filter(u => u.trim() !== '');
    if (validUrls.length > 0) {
      onSubmit(validUrls, isPremium, separateSpeaker);
    }
  };

  return (
    <div className="w-full">
      <div className="flex gap-6 border-b border-dark-border mb-6">
        <button className="pb-2 text-accent border-b-2 border-accent font-medium">YouTube Video</button>
        <button className="pb-2 text-gray-400 hover:text-gray-200">YouTube Playlist</button>
      </div>

      <div className="space-y-4 mb-4">
        {urls.map((url, index) => (
          <div key={index} className="relative flex items-center">
            <Link2 className="absolute left-4 text-gray-500" size={20} />
            <input
              type="text"
              value={url}
              onChange={(e) => {
                const newUrls = [...urls];
                newUrls[index] = e.target.value;
                setUrls(newUrls);
              }}
              placeholder="Paste the YouTube video link, for example: https://www.youtube.com/watch?v=example"
              className="w-full bg-dark-card border border-dark-border rounded-xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-accent transition-colors"
            />
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between mb-6">
        <SourceOptions 
          isPremium={isPremium} 
          setIsPremium={setIsPremium}
          separateSpeaker={separateSpeaker}
          setSeparateSpeaker={setSeparateSpeaker}
          onAddLink={() => setUrls([...urls, ''])}
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={isLoading || urls.every(u => u.trim() === '')}
        className="w-full bg-gradient-to-r from-accent to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-xl py-4 font-bold text-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-accent/20"
      >
        {isLoading ? (
          <span className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></span>
        ) : (
          <>
            <Sparkles size={20} />
            Generate Summary
          </>
        )}
      </button>
    </div>
  );
};

export default UrlInput;
