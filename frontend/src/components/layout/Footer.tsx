import { Github, Linkedin, Heart } from 'lucide-react';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-dark-border bg-dark-card/50 mt-auto">
      <div className="h-[1px] bg-gradient-to-r from-transparent via-accent/40 to-transparent"></div>
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="text-sm text-gray-400 flex items-center gap-1 justify-center md:justify-start">
              Built with <Heart size={14} className="text-red-500 animate-pulse" /> by
              <span className="font-semibold bg-gradient-to-r from-accent to-blue-400 bg-clip-text text-transparent">
                Sneha Uday Naik 
              </span>
            </p>
            <p className="text-xs text-gray-600 mt-1">
              &copy; {currentYear} AI Study Companion. All rights reserved.
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <a 
              href="https://github.com/snehanaik03" 
              target="_blank" 
              rel="noopener noreferrer"
              className="p-2 text-gray-500 hover:text-white hover:bg-dark-surface rounded-lg transition-all duration-200"
              aria-label="GitHub"
            >
              <Github size={18} />
            </a>
            <a 
              href="https://www.linkedin.com/in/sneha-naik03/?isSelfProfile=false" 
              target="_blank" 
              rel="noopener noreferrer"
              className="p-2 text-gray-500 hover:text-blue-500 hover:bg-dark-surface rounded-lg transition-all duration-200"
              aria-label="LinkedIn"
            >
              <Linkedin size={18} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
