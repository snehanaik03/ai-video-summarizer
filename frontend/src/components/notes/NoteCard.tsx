import React from 'react';
import { Link } from 'react-router-dom';
import { Trash2, ExternalLink } from 'lucide-react';
import { Summary } from '../../types';

interface NoteCardProps {
  note: Summary;
  onDelete: () => void;
}

export const NoteCard: React.FC<NoteCardProps> = ({ note, onDelete }) => {
  const date = new Date(note.created_at).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  });

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden hover:border-accent transition-colors group flex flex-col h-full">
      <div className="h-40 bg-dark-surface relative overflow-hidden">
        {note.thumbnail_url ? (
          <img src={note.thumbnail_url} alt={note.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-500">No Image</div>
        )}
        <div className="absolute top-2 right-2 flex gap-2">
          <span className="bg-black/60 text-white text-xs font-medium px-2 py-1 rounded backdrop-blur-sm">
            {note.source_type}
          </span>
        </div>
      </div>
      
      <div className="p-4 flex-1 flex flex-col">
        <h4 className="text-white font-medium line-clamp-2 mb-2 group-hover:text-accent transition-colors">
          {note.title}
        </h4>
        <p className="text-sm text-gray-400 mb-4 line-clamp-3 flex-1">
          {note.summary_text.substring(0, 100)}...
        </p>
        
        <div className="flex items-center justify-between mt-auto pt-4 border-t border-dark-border">
          <span className="text-xs text-gray-500">{date}</span>
          <div className="flex gap-2">
            <button onClick={(e) => { e.preventDefault(); onDelete(); }} className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-500/10 rounded transition-colors">
              <Trash2 size={16} />
            </button>
            <Link to={`/results/${note.id}`} className="p-1.5 text-gray-400 hover:text-accent hover:bg-accent/10 rounded transition-colors">
              <ExternalLink size={16} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NoteCard;
