import { apiClient } from './client';
import { User } from '../types';

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await apiClient.post<{ access_token: string; token_type: string }>('/auth/login', {
      email,
      password,
    });
    return response.data;
  },
  register: async (email: string, password: string, full_name: string) => {
    const response = await apiClient.post<User>('/auth/register', {
      email,
      password,
      full_name,
    });
    return response.data;
  },
  getProfile: async () => {
    const response = await apiClient.get<User>('/auth/profile');
    return response.data;
  },
};
