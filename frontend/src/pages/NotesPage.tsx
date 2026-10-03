import { useEffect, useState } from 'react';
import { Search, Filter } from 'lucide-react';
import { notesApi } from '../api/notes';
import { Summary } from '../types';
import NotesList from '../components/notes/NotesList';
import { useAuth } from '../hooks/useAuth';

export const NotesPage = () => {
  const [notes, setNotes] = useState<Summary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      notesApi.getNotes()
        .then((data) => setNotes(data.items))
        .catch(console.error)
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  const handleDelete = async (id: string) => {
    try {
      await notesApi.deleteNote(id);
      setNotes(notes.filter(n => n.id !== id));
    } catch (error) {
      console.error('Failed to delete note', error);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
        <h2 className="text-3xl font-bold text-white mb-4">Sign in to view your notes</h2>
        <p className="text-gray-400 mb-8 max-w-md">Save summaries, access them anytime, and review your generated quizzes by creating a free account.</p>
        <button className="px-8 py-3 bg-accent hover:bg-blue-600 text-white font-medium rounded-lg transition-colors">
          Sign In
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">My Notes</h1>
          <p className="text-gray-400">Manage your saved summaries and study materials.</p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
            <input 
              type="text" 
              placeholder="Search notes..." 
              className="bg-dark-surface border border-dark-border rounded-lg py-2 pl-10 pr-4 text-white focus:outline-none focus:border-accent w-full md:w-64"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-dark-surface border border-dark-border rounded-lg text-white hover:bg-dark-border transition-colors">
            <Filter size={18} />
            Filter
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
        </div>
      ) : (
        <NotesList notes={notes} onDelete={handleDelete} />
      )}
    </div>
  );
};

export default NotesPage;
