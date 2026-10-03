import { useMutation, useQuery } from '@tanstack/react-query';
import { summarizeApi } from '../api/summarize';
import { SummarizeRequest } from '../types';

export const useSummarizeYouTube = () => {
  return useMutation({
    mutationFn: (request: SummarizeRequest) => summarizeApi.summarizeYouTube(request),
  });
};

export const useGetSummary = (id: string | undefined) => {
  return useQuery({
    queryKey: ['summary', id],
    queryFn: () => summarizeApi.getSummary(id!),
    enabled: !!id,
  });
};
