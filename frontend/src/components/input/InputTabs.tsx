import React from 'react';
import { Globe, Video, Headphones, FileText, AlignLeft } from 'lucide-react';

export type TabType = 'youtube' | 'video' | 'audio' | 'file' | 'text';

interface InputTabsProps {
  activeTab: TabType;
  onChange: (tab: TabType) => void;
}

export const InputTabs: React.FC<InputTabsProps> = ({ activeTab, onChange }) => {
  const tabs: { id: TabType; label: string; icon: React.ReactNode }[] = [
    { id: 'youtube', label: 'YouTube', icon: <Globe size={16} /> },
    { id: 'video', label: 'Video', icon: <Video size={16} /> },
    { id: 'audio', label: 'Audio', icon: <Headphones size={16} /> },
    { id: 'file', label: 'PDF, Image & More Files', icon: <FileText size={16} /> },
    { id: 'text', label: 'Long Text', icon: <AlignLeft size={16} /> },
  ];

  return (
    <div className="flex flex-wrap gap-2 mb-6">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            activeTab === tab.id
              ? 'bg-accent text-white'
              : 'bg-dark-surface text-gray-400 hover:text-white hover:bg-dark-border'
          }`}
        >
          {tab.icon}
          {tab.label}
        </button>
      ))}
    </div>
  );
};

export default InputTabs;
