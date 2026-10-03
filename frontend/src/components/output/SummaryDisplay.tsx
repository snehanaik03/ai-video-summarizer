import { FC, useState } from 'react';
import { Copy, Bookmark, Share2, Check } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Summary } from '../../types';

interface SummaryDisplayProps {
  summary: Summary;
}

export const SummaryDisplay: FC<SummaryDisplayProps> = ({ summary }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const textToCopy = `${summary.title}\n\n${summary.summary_text}\n\n${summary.detailed_summary || ''}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const markdownComponents = {
    h1: ({ ...props }: any) => <h1 className="text-2xl font-bold text-white mt-6 mb-3 border-b border-dark-border pb-2" {...props} />,
    h2: ({ ...props }: any) => <h2 className="text-xl font-bold text-white mt-6 mb-3 flex items-center gap-2" {...props} />,
    h3: ({ ...props }: any) => <h3 className="text-lg font-semibold text-accent mt-5 mb-2" {...props} />,
    h4: ({ ...props }: any) => <h4 className="text-base font-semibold text-blue-300 mt-4 mb-2" {...props} />,
    p: ({ ...props }: any) => <p className="text-gray-300 leading-relaxed mb-4" {...props} />,
    ul: ({ ...props }: any) => <ul className="list-disc list-outside pl-6 space-y-2 mb-4 text-gray-300" {...props} />,
    ol: ({ ...props }: any) => <ol className="list-decimal list-outside pl-6 space-y-2 mb-4 text-gray-300" {...props} />,
    li: ({ ...props }: any) => <li className="leading-relaxed" {...props} />,
    strong: ({ ...props }: any) => <strong className="font-semibold text-white" {...props} />,
    blockquote: ({ ...props }: any) => (
      <blockquote className="border-l-4 border-accent pl-4 py-1 my-4 text-gray-400 italic bg-dark-surface/40 rounded-r-lg" {...props} />
    ),
    table: ({ ...props }: any) => (
      <div className="overflow-x-auto my-6 rounded-xl border border-dark-border shadow-md">
        <table className="w-full text-left text-sm text-gray-300 border-collapse" {...props} />
      </div>
    ),
    thead: ({ ...props }: any) => <thead className="bg-dark-surface text-white text-xs uppercase font-semibold" {...props} />,
    tbody: ({ ...props }: any) => <tbody className="divide-y divide-dark-border" {...props} />,
    tr: ({ ...props }: any) => <tr className="hover:bg-dark-surface/30 transition-colors" {...props} />,
    th: ({ ...props }: any) => <th className="px-4 py-3 font-semibold border-b border-dark-border" {...props} />,
    td: ({ ...props }: any) => <td className="px-4 py-3 align-top border-b border-dark-border/50" {...props} />,
    code: ({ ...props }: any) => (
      <code className="bg-dark-surface px-1.5 py-0.5 rounded text-accent text-xs font-mono" {...props} />
    ),
  };

  return (
    <div className="bg-dark-card rounded-xl border border-dark-border p-6 md:p-8 animate-fade-in shadow-xl">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8 pb-6 border-b border-dark-border">
        <h2 className="text-2xl font-bold text-white leading-tight">{summary.title}</h2>
        <div className="flex items-center gap-2 self-end sm:self-auto shrink-0">
          <button 
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-gray-300 hover:text-white bg-dark-surface hover:bg-dark-border rounded-lg transition-all duration-200" 
            title="Copy Summary"
          >
            {copied ? <Check size={16} className="text-green-400" /> : <Copy size={16} />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </button>
          <button 
            className="p-2 text-gray-400 hover:text-white bg-dark-surface hover:bg-dark-border rounded-lg transition-all duration-200" 
            title="Save to Notes"
          >
            <Bookmark size={18} />
          </button>
          <button 
            className="p-2 text-gray-400 hover:text-white bg-dark-surface hover:bg-dark-border rounded-lg transition-all duration-200" 
            title="Share"
          >
            <Share2 size={18} />
          </button>
        </div>
      </div>

      <div className="space-y-10">
        {/* Executive Overview Section */}
        {summary.summary_text && (
          <section>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <span className="w-1.5 h-6 bg-accent rounded-full"></span>
              Executive Overview
            </h3>
            <div className="bg-dark-surface/40 rounded-xl p-6 border border-dark-border/60">
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                {summary.summary_text}
              </ReactMarkdown>
            </div>
          </section>
        )}

        {/* In-Depth Breakdown Section */}
        {summary.detailed_summary && (
          <section>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <span className="w-1.5 h-6 bg-gradient-to-b from-accent to-purple-500 rounded-full"></span>
              In-Depth Analytical Breakdown
            </h3>
            <div className="bg-dark-surface/20 rounded-xl p-6 md:p-8 border border-dark-border/40">
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                {summary.detailed_summary}
              </ReactMarkdown>
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default SummaryDisplay;
