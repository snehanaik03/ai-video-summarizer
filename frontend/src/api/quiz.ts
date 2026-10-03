import { apiClient } from './client';
import { Quiz, QuizResult } from '../types';

export const quizApi = {
  generateQuiz: async (summaryId: string) => {
    const response = await apiClient.post<Quiz>(`/quiz/generate/${summaryId}`);
    return response.data;
  },
  getQuiz: async (quizId: string) => {
    const response = await apiClient.get<Quiz>(`/quiz/${quizId}`);
    return response.data;
  },
  submitQuiz: async (quizId: string, answers: Record<number, number>) => {
    const response = await apiClient.post<QuizResult>(`/quiz/${quizId}/submit`, { answers });
    return response.data;
  },
};
