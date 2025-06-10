// 用户相关类型
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserRegister {
  username: string;
  email: string;
  password: string;
  full_name: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// API响应类型
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// 提示词优化相关类型
export interface OptimizationRequest {
  original_prompt: string;
  optimization_type: 'general' | 'code' | 'writing' | 'analysis';
  user_context?: string;
}

export interface OptimizationImprovement {
  type: string;
  description: string;
  before_text?: string;
  after_text?: string;
}

export interface OptimizationResult {
  id: number;
  original_prompt: string;
  optimized_prompt: string;
  quality_score_before: number;
  quality_score_after: number;
  improvements: OptimizationImprovement[];
  processing_time: number;
  created_at: string;
}

export interface QualityEvaluation {
  overall_score: number;
  detailed_scores: {
    clarity: number;
    completeness: number;
    structure: number;
    specificity: number;
    actionability: number;
  };
  issues: string[];
  suggestions: string[];
}

// UI状态类型
export interface LoadingState {
  loading: boolean;
  error: string | null;
}

export interface Theme {
  mode: 'light' | 'dark';
  primaryColor: string;
}

// 表单类型
export interface FormField {
  value: string;
  error?: string;
  touched?: boolean;
}

// 路由类型
export type RouteKey = 'home' | 'login' | 'register' | 'dashboard' | 'optimizer' | 'history' | 'examples' | 'settings';

// 常量类型
export const OPTIMIZATION_TYPES = ['general', 'code', 'writing', 'analysis'] as const;
export type OptimizationType = typeof OPTIMIZATION_TYPES[number];

export const USER_ROLES = ['user', 'admin', 'superuser'] as const;
export type UserRole = typeof USER_ROLES[number]; 