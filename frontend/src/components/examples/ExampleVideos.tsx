import React from 'react';
import { Youtube, MonitorPlay } from 'lucide-react';
import { EXAMPLE_VIDEOS } from '../../utils/constants';

interface ExampleVideosProps {
  onSelect: (url: string) => void;
}

export const ExampleVideos: React.FC<ExampleVideosProps> = ({ onSelect }) => {
  return (
    <div className="mt-12">
      <div className="flex items-center gap-2 mb-4">
        <span className="bg-red-500/20 text-red-500 text-xs font-bold px-2 py-1 rounded">Example</span>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {EXAMPLE_VIDEOS.map((video, i) => (
          <div 
            key={i} 
            onClick={() => onSelect(video.url)}
            className="group cursor-pointer bg-dark-card rounded-xl overflow-hidden border border-dark-border hover:border-accent transition-colors"
          >
            <div className="relative aspect-video w-full overflow-hidden bg-gradient-to-br from-blue-900/40 via-dark-surface to-dark-card flex items-center justify-center">
              <img 
                src={video.thumbnail} 
                alt={video.title} 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
              <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors"></div>
            </div>
            <div className="p-3">
              <p className="text-sm font-medium text-gray-200 line-clamp-2">{video.title}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap gap-4">
        <button className="flex items-center gap-2 px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-sm hover:bg-dark-surface transition-colors">
          <Youtube size={16} className="text-red-500" />
          YouTube Subscriptions
        </button>
        <button className="flex items-center gap-2 px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-sm hover:bg-dark-surface transition-colors">
          <MonitorPlay size={16} className="text-accent" />
          YouTube Extension
        </button>
      </div>
    </div>
  );
};

export default ExampleVideos;
