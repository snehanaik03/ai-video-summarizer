import { FC } from 'react';
import { PlusCircle } from 'lucide-react';

interface SourceOptionsProps {
  isPremium: boolean;
  setIsPremium: (v: boolean) => void;
  separateSpeaker: boolean;
  setSeparateSpeaker: (v: boolean) => void;
  onAddLink?: () => void;
}

export const SourceOptions: FC<SourceOptionsProps> = ({
  isPremium,
  setIsPremium,
  separateSpeaker,
  setSeparateSpeaker,
  onAddLink
}) => {
  return (
    <div className="flex flex-wrap items-center gap-4 text-sm">
      {onAddLink && (
        <button 
          onClick={onAddLink}
          className="flex items-center gap-1.5 text-accent hover:text-blue-400 transition-colors"
        >
          <PlusCircle size={16} />
          Add More Link
        </button>
      )}

      <div className="flex bg-dark-surface rounded-full p-1">
        <button
          onClick={() => setIsPremium(false)}
          className={`px-4 py-1 rounded-full transition-colors ${!isPremium ? 'bg-accent text-white' : 'text-gray-400 hover:text-white'}`}
        >
          Basic
        </button>
        <button
          onClick={() => setIsPremium(true)}
          className={`px-4 py-1 rounded-full transition-colors ${isPremium ? 'bg-accent text-white' : 'text-gray-400 hover:text-white'}`}
        >
          Premium
        </button>
      </div>

      <label 
        onClick={() => setSeparateSpeaker(!separateSpeaker)}
        className="flex items-center gap-2 cursor-pointer select-none"
      >
        <div className={`w-10 h-5 rounded-full p-0.5 transition-colors ${separateSpeaker ? 'bg-accent' : 'bg-dark-surface'}`}>
          <div className={`w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform ${separateSpeaker ? 'translate-x-5' : 'translate-x-0'}`} />
        </div>
        <span className="text-gray-400">Separate Speaker</span>
      </label>
    </div>
  );
};

export default SourceOptions;
