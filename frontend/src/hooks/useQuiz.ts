import { useMutation, useQuery } from '@tanstack/react-query';
import { quizApi } from '../api/quiz';

export const useGenerateQuiz = () => {
  return useMutation({
    mutationFn: (summaryId: string | number) => quizApi.generateQuiz(String(summaryId)),
  });
};

export const useGetQuiz = (quizId: string | undefined) => {
  return useQuery({
    queryKey: ['quiz', quizId],
    queryFn: () => quizApi.getQuiz(quizId!),
    enabled: !!quizId,
  });
};

export const useSubmitQuiz = () => {
  return useMutation({
    mutationFn: ({ quizId, answers }: { quizId: string | number; answers: Record<number, number> }) =>
      quizApi.submitQuiz(String(quizId), answers),
  });
};
