import React from 'react';
import NoteCard from './NoteCard';
import { Summary } from '../../types';

interface NotesListProps {
  notes: Summary[];
  onDelete: (id: string) => void;
}

export const NotesList: React.FC<NotesListProps> = ({ notes, onDelete }) => {
  if (notes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-32 h-32 mb-6 bg-dark-surface rounded-full flex items-center justify-center">
          <svg className="w-16 h-16 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h3 className="text-xl font-medium text-white mb-2">No saved notes yet</h3>
        <p className="text-gray-400">Your saved summaries will appear here.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {notes.map(note => (
        <NoteCard key={note.id} note={note} onDelete={() => onDelete(note.id)} />
      ))}
    </div>
  );
};

export default NotesList;
