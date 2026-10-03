import React, { useCallback } from 'react';
import { UploadCloud } from 'lucide-react';

export const FileUpload = () => {
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    // Handle file drop
  }, []);

  return (
    <div 
      className="border-2 border-dashed border-dark-border rounded-xl p-12 flex flex-col items-center justify-center text-center bg-dark-card/50 hover:bg-dark-card transition-colors cursor-pointer"
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
    >
      <div className="w-16 h-16 bg-dark-surface rounded-full flex items-center justify-center mb-4">
        <UploadCloud size={32} className="text-gray-400" />
      </div>
      <h3 className="text-lg font-medium text-white mb-2">Drag & drop your file here</h3>
      <p className="text-gray-400 text-sm mb-6">or click to browse from your computer</p>
      <button className="px-6 py-2 bg-dark-surface hover:bg-dark-border rounded-lg text-sm font-medium transition-colors">
        Select File
      </button>
    </div>
  );
};

export default FileUpload;
