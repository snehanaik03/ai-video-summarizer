import { Sparkles } from 'lucide-react';

export const Header = () => {
  return (
    <header className="h-14 border-b border-dark-border bg-dark-bg/80 backdrop-blur-sm sticky top-0 z-20">
      <div className="h-full flex items-center justify-between px-6">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-accent" />
          <span className="text-sm font-medium text-gray-400">AI Study Companion</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500 hidden sm:inline">Portfolio Project by</span>
          <span className="text-xs font-semibold bg-gradient-to-r from-accent to-blue-400 bg-clip-text text-transparent">
            Sneha Uday Naik
          </span>
        </div>
      </div>
      <div className="h-[1px] bg-gradient-to-r from-transparent via-accent/50 to-transparent"></div>
    </header>
  );
};

export default Header;
