import { apiClient } from './client';
import { SummarizeRequest, Summary } from '../types';

export const summarizeApi = {
  summarizeYouTube: async (request: SummarizeRequest) => {
    const response = await apiClient.post<Summary[]>('/summarize/youtube', request);
    return response.data[0];
  },
  summarizeText: async (text: string, processing_tier: string) => {
    const response = await apiClient.post<Summary>('/summarize/text', { text, processing_tier });
    return response.data;
  },
  getSummary: async (id: string) => {
    const response = await apiClient.get<Summary>(`/summarize/${id}`);
    return response.data;
  },
  getSummaryHistory: async () => {
    const response = await apiClient.get<Summary[]>('/summarize/history/list');
    return response.data;
  },
};
