import { apiClient } from './client';
import { Summary } from '../types';

export const notesApi = {
  getNotes: async (page: number = 1, limit: number = 20) => {
    const skip = (page - 1) * limit;
    const response = await apiClient.get<{ items: Summary[]; total: number }>(`/notes?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  getNote: async (id: string) => {
    const response = await apiClient.get<Summary>(`/notes/${id}`);
    return response.data;
  },
  deleteNote: async (id: string) => {
    const response = await apiClient.delete(`/notes/${id}`);
    return response.data;
  },
};
