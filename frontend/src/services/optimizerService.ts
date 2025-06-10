import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../constants';
import type {
  OptimizationRequest,
  OptimizationResult,
  QualityEvaluation,
} from '../types';

class OptimizerService {
  /**
   * 优化提示词
   */
  async optimizePrompt(request: OptimizationRequest): Promise<OptimizationResult> {
    const response = await axios.post<OptimizationResult>(
      `${API_BASE_URL}${API_ENDPOINTS.OPTIMIZER.OPTIMIZE}`,
      request,
      {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000,
      }
    );

    return response.data;
  }

  /**
   * 评估提示词质量
   */
  async evaluateQuality(prompt: string): Promise<QualityEvaluation> {
    const response = await axios.post<QualityEvaluation>(
      `${API_BASE_URL}${API_ENDPOINTS.OPTIMIZER.EVALUATE}`,
      { prompt },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000,
      }
    );

    return response.data;
  }
}

export const optimizerService = new OptimizerService();