export interface User {
  id: string;
  email: string;
  full_name: string;
  tier: string;
  created_at: string;
}

export interface Summary {
  id: string;
  source_type: string;
  source_url: string;
  title: string;
  thumbnail_url: string;
  transcript: string;
  summary_text: string;
  detailed_summary: string;
  processing_tier: string;
  created_at: string;
}

export interface MCQQuestion {
  question: string;
  options: string[];
  correct_answer: string;
  correct_index: number;
  explanation: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  concept_tested: string;
}

export interface Quiz {
  id: string;
  summary_id: string;
  questions: MCQQuestion[];
  created_at: string;
}

export interface QuestionResult {
  question_index: number;
  selected_index: number;
  correct_index: number;
  is_correct: boolean;
}

export interface QuizResult {
  quiz_id: string;
  score: number;
  total: number;
  percentage: number;
  results: QuestionResult[];
}

export interface SummarizeRequest {
  urls: string[];
  processing_tier: string;
  separate_speaker: boolean;
}
