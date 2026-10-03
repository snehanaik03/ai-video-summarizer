import { Link } from 'react-router-dom';
import { Youtube, Brain, ClipboardList, Sparkles, ArrowRight, Zap, FileText, HelpCircle } from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="min-h-[calc(100vh-8rem)]">
      {/* Hero Section */}
      <section className="relative px-6 py-20 md:py-28 overflow-hidden">
        {/* Background glow effects */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent/5 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute top-20 right-10 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl pointer-events-none"></div>
        
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <div className="animate-fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 border border-accent/20 rounded-full text-accent text-sm font-medium mb-8">
              <Sparkles size={14} />
              <span>Free & Open Access - No Sign Up Required</span>
            </div>
          </div>
          
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 animate-fade-in leading-tight">
            AI Study Companion:
            <br />
            <span className="bg-gradient-to-r from-accent via-blue-400 to-purple-500 bg-clip-text text-transparent">
              Video Summaries & Quizzes
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 animate-fade-in animation-delay-200">
            Paste any YouTube link and instantly get AI-powered summaries, key insights, 
            and auto-generated quizzes to test your understanding.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in animation-delay-300">
            <Link 
              to="/app"
              className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-accent to-blue-500 hover:from-blue-500 hover:to-accent text-white rounded-xl font-bold text-lg transition-all duration-300 shadow-lg shadow-accent/25 hover:shadow-accent/40 hover:scale-105"
            >
              Try it Now
              <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <a 
              href="#how-it-works"
              className="inline-flex items-center gap-2 px-8 py-4 bg-dark-surface hover:bg-dark-border text-white rounded-xl font-medium text-lg transition-all duration-200"
            >
              Learn More
            </a>
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section id="how-it-works" className="px-6 py-20 bg-dark-card/30">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16 animate-fade-in">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">How it Works</h2>
            <p className="text-gray-400 text-lg max-w-xl mx-auto">
              Three simple steps to transform any video into study material
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 md:gap-12">
            {/* Step 1 */}
            <div className="text-center group animate-slide-up">
              <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-red-500/20 to-red-600/10 border border-red-500/20 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Youtube size={28} className="text-red-500" />
              </div>
              <div className="text-accent font-bold text-sm mb-2">Step 1</div>
              <h3 className="text-xl font-bold text-white mb-3">Paste a Link</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Paste any YouTube video URL. We support standard links, shortened URLs, playlists, and more.
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center group animate-slide-up animation-delay-200">
              <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-accent/20 to-blue-600/10 border border-accent/20 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Brain size={28} className="text-accent" />
              </div>
              <div className="text-accent font-bold text-sm mb-2">Step 2</div>
              <h3 className="text-xl font-bold text-white mb-3">AI Summarizes</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Our AI extracts the transcript and generates a concise, structured summary with key takeaways.
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center group animate-slide-up animation-delay-400">
              <div className="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-purple-500/20 to-purple-600/10 border border-purple-500/20 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <ClipboardList size={28} className="text-purple-500" />
              </div>
              <div className="text-accent font-bold text-sm mb-2">Step 3</div>
              <h3 className="text-xl font-bold text-white mb-3">Take a Quiz</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Auto-generated multiple-choice quizzes test your understanding with instant scoring and explanations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16 animate-fade-in">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Powerful Features</h2>
            <p className="text-gray-400 text-lg max-w-xl mx-auto">
              Everything you need to supercharge your study sessions
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-dark-card border border-dark-border rounded-2xl p-6 hover:border-accent/30 transition-all duration-300 hover:-translate-y-1 group animate-slide-up">
              <div className="w-12 h-12 bg-accent/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-accent/20 transition-colors">
                <Zap size={22} className="text-accent" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Instant Summaries</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Get concise or detailed summaries from any YouTube video in seconds, powered by Google Gemini AI.
              </p>
            </div>

            <div className="bg-dark-card border border-dark-border rounded-2xl p-6 hover:border-accent/30 transition-all duration-300 hover:-translate-y-1 group animate-slide-up animation-delay-100">
              <div className="w-12 h-12 bg-purple-500/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-purple-500/20 transition-colors">
                <HelpCircle size={22} className="text-purple-500" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Smart Quizzes</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Auto-generated MCQs with difficulty levels, explanations, and scoring to reinforce your learning.
              </p>
            </div>

            <div className="bg-dark-card border border-dark-border rounded-2xl p-6 hover:border-accent/30 transition-all duration-300 hover:-translate-y-1 group animate-slide-up animation-delay-200">
              <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-green-500/20 transition-colors">
                <FileText size={22} className="text-green-500" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Save Notes</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Bookmark your favorite summaries and build a personal knowledge library for exam prep.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <div className="bg-gradient-to-br from-dark-card to-dark-surface border border-dark-border rounded-3xl p-10 md:p-14 relative overflow-hidden animate-fade-in-scale">
            <div className="absolute top-0 right-0 w-40 h-40 bg-accent/5 rounded-full blur-2xl pointer-events-none"></div>
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 relative z-10">
              Ready to Study Smarter?
            </h2>
            <p className="text-gray-400 mb-8 relative z-10">
              Start summarizing videos and generating quizzes right now. No sign-up needed.
            </p>
            <Link 
              to="/app"
              className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-accent to-blue-500 hover:from-blue-500 hover:to-accent text-white rounded-xl font-bold text-lg transition-all duration-300 shadow-lg shadow-accent/25 hover:shadow-accent/40 hover:scale-105 relative z-10"
            >
              Get Started Free
              <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
