import React, { useState } from 'react';
import { X } from 'lucide-react';
import { authApi } from '../../api/auth';
import { useAuth } from '../../hooks/useAuth';

interface RegisterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSwitchToLogin: () => void;
}

export const RegisterModal: React.FC<RegisterModalProps> = ({ isOpen, onClose, onSwitchToLogin }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirm) {
      setError('Passwords do not match');
      return;
    }
    setError('');
    setIsLoading(true);
    try {
      const user = await authApi.register(email, password, name);
      // Auto login
      const data = await authApi.login(email, password);
      register(data.access_token, user);
      onClose();
    } catch (err: any) {
      setError('Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-dark-card border border-dark-border rounded-2xl p-8 w-full max-w-md relative animate-in fade-in zoom-in-95">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white">
          <X size={20} />
        </button>
        
        <h2 className="text-2xl font-bold text-white mb-6">Create Account</h2>
        
        {error && <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-lg mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Full Name</label>
            <input 
              type="text" 
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-dark-surface border border-dark-border rounded-lg px-4 py-2.5 text-white focus:border-accent outline-none" 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-dark-surface border border-dark-border rounded-lg px-4 py-2.5 text-white focus:border-accent outline-none" 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
            <input 
              type="password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-dark-surface border border-dark-border rounded-lg px-4 py-2.5 text-white focus:border-accent outline-none" 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Confirm Password</label>
            <input 
              type="password" 
              required
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              className="w-full bg-dark-surface border border-dark-border rounded-lg px-4 py-2.5 text-white focus:border-accent outline-none" 
            />
          </div>
          
          <button 
            type="submit"
            disabled={isLoading}
            className="w-full bg-accent hover:bg-blue-600 text-white font-medium py-2.5 rounded-lg transition-colors mt-2 disabled:opacity-50"
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        
        <div className="mt-6 text-center text-sm text-gray-400">
          Already have an account?{' '}
          <button onClick={onSwitchToLogin} className="text-accent hover:underline">Sign In</button>
        </div>
      </div>
    </div>
  );
};

export default RegisterModal;
