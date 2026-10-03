import { NavLink } from 'react-router-dom';
import { BookOpen, FolderOpen, Home, Menu } from 'lucide-react';
import { useState } from 'react';

export const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-dark-surface rounded-md text-dark-text"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Menu size={24} />
      </button>

      <div className={`fixed inset-y-0 left-0 z-40 w-60 bg-dark-card border-r border-dark-border transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex flex-col h-full">
          <div className="p-6">
            <NavLink to="/" className="flex items-center gap-2 group">
              <div className="w-8 h-8 bg-gradient-to-br from-accent to-blue-400 rounded-lg flex items-center justify-center shadow-lg shadow-accent/20 group-hover:shadow-accent/40 transition-shadow">
                <BookOpen size={18} className="text-white" />
              </div>
              <span className="font-bold text-lg text-white">StudyAI</span>
            </NavLink>
          </div>

          <nav className="flex-1 px-4 space-y-2">
            <NavLink to="/" className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${isActive ? 'bg-accent/10 text-accent shadow-sm' : 'text-dark-text hover:bg-dark-surface hover:translate-x-0.5'}`}>
              <Home size={18} />
              <span>Home</span>
            </NavLink>
            <NavLink to="/app" className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${isActive ? 'bg-accent/10 text-accent shadow-sm' : 'text-dark-text hover:bg-dark-surface hover:translate-x-0.5'}`}>
              <BookOpen size={18} />
              <span>AI Summarizer</span>
              <span className="ml-auto text-[10px] font-bold bg-accent/20 text-accent px-1.5 py-0.5 rounded">New</span>
            </NavLink>
            <div className="my-4 border-t border-dark-border"></div>
            <NavLink to="/notes" className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${isActive ? 'bg-accent/10 text-accent shadow-sm' : 'text-dark-text hover:bg-dark-surface hover:translate-x-0.5'}`}>
              <FolderOpen size={18} />
              <span>My Notes</span>
            </NavLink>
          </nav>

          <div className="p-4 border-t border-dark-border">
            <div className="text-center">
              <p className="text-xs text-gray-500">Built by</p>
              <p className="text-sm font-semibold bg-gradient-to-r from-accent to-blue-400 bg-clip-text text-transparent">
                Sneha Uday Naik
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 lg:hidden backdrop-blur-sm"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
};

export default Sidebar;
