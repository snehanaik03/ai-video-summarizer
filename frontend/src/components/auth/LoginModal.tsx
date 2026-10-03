import React, { useState } from 'react';
import { X } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { authApi } from '../../api/auth';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSwitchToRegister: () => void;
}

export const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    try {
      const data = await authApi.login(email, password);
      const user = await authApi.getProfile(); // Need to set user as well, or just token and let AuthContext fetch. 
      // For simplicity here, AuthContext fetches profile on token change.
      login(data.access_token, user);
      onClose();
    } catch (err: any) {
      setError('Invalid email or password');
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
        
        <h2 className="text-2xl font-bold text-white mb-6">Sign In</h2>
        
        {error && <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-lg mb-4 text-sm">{error}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
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
          
          <button 
            type="submit"
            disabled={isLoading}
            className="w-full bg-accent hover:bg-blue-600 text-white font-medium py-2.5 rounded-lg transition-colors mt-2 disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <div className="mt-6 text-center text-sm text-gray-400">
          Don't have an account?{' '}
          <button onClick={onSwitchToRegister} className="text-accent hover:underline">Sign Up</button>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;
