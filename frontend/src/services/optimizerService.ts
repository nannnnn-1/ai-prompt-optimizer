import { apiClient } from './apiClient';
import { useUIStore } from '../store/uiStore';

// 优化请求接口
export interface OptimizationRequest {
  original_prompt: string;
  optimization_type: 'general' | 'code' | 'writing' | 'analysis';
  user_context?: string;
  preferences?: {
    focus_areas?: string[];
    target_audience?: string;
    tone?: string;
  };
}

// 优化结果接口
export interface OptimizationResult {
  id: number;
  original_prompt: string;
  optimized_prompt: string;
  quality_score_before: number;
  quality_score_after: number;
  improvements: Improvement[];
  processing_time: number;
  created_at: string;
}

// 改进点接口
export interface Improvement {
  id: string;
  type: 'structure' | 'clarity' | 'context' | 'specificity' | 'completeness';
  description: string;
  category: string;
  impact: 'high' | 'medium' | 'low';
  before_text?: string;
  after_text?: string;
}

// 质量评估接口
export interface QualityEvaluation {
  overall_score: number;
  detailed_scores: {
    clarity: number;
    completeness: number;
    structure: number;
    specificity: number;
    actionability: number;
  };
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  improvement_suggestions: string[];
}

// 历史记录接口
export interface OptimizationHistory {
  id: number;
  original_prompt: string;
  optimized_prompt: string;
  quality_improvement: number;
  optimization_type: string;
  created_at: string;
}

class OptimizerService {
  /**
   * 优化提示词
   */
  async optimizePrompt(request: OptimizationRequest): Promise<OptimizationResult> {
    const { setLoading, addNotification } = useUIStore.getState();
    
    try {
      setLoading('optimize', true);
      
      // 添加开始优化的通知
      addNotification({
        type: 'info',
        title: '开始优化',
        message: '正在分析和优化您的提示词...',
        duration: 2000,
      });

      const result = await apiClient.post<OptimizationResult>(
        '/v1/optimizer/optimize',
        request
      );

      // 添加成功通知
      addNotification({
        type: 'success',
        title: '优化完成',
        message: `质量评分从 ${result.quality_score_before} 提升到 ${result.quality_score_after}`,
        duration: 4000,
      });

      return result;
    } catch (error) {
      // 错误处理已在apiClient中完成
      throw error;
    } finally {
      setLoading('optimize', false);
    }
  }

  /**
   * 评估提示词质量
   */
  async evaluateQuality(prompt: string): Promise<QualityEvaluation> {
    const { setLoading } = useUIStore.getState();
    
    try {
      setLoading('load', true);
      
      const result = await apiClient.post<QualityEvaluation>(
        '/v1/optimizer/evaluate',
        { prompt }
      );

      return result;
    } catch (error) {
      throw error;
    } finally {
      setLoading('load', false);
    }
  }

  /**
   * 获取优化历史
   */
  async getOptimizationHistory(params?: {
    page?: number;
    limit?: number;
    type?: string;
  }): Promise<{
    data: OptimizationHistory[];
    total: number;
    page: number;
    limit: number;
  }> {
    const { setLoading } = useUIStore.getState();
    
    try {
      setLoading('load', true);
      
      const result = await apiClient.get('/v1/optimizer/history', {
        params,
        cache: true, // 缓存历史记录
      });

      return result;
    } catch (error) {
      throw error;
    } finally {
      setLoading('load', false);
    }
  }

  /**
   * 获取优化详情
   */
  async getOptimizationDetail(id: number): Promise<OptimizationResult> {
    const { setLoading } = useUIStore.getState();
    
    try {
      setLoading('load', true);
      
      const result = await apiClient.get<OptimizationResult>(
        `/v1/optimizer/${id}`,
        { cache: true }
      );

      return result;
    } catch (error) {
      throw error;
    } finally {
      setLoading('load', false);
    }
  }

  /**
   * 保存优化结果
   */
  async saveOptimization(data: {
    optimization_id: number;
    user_notes?: string;
    is_favorite?: boolean;
  }): Promise<void> {
    const { setLoading, addNotification } = useUIStore.getState();
    
    try {
      setLoading('save', true);
      
      await apiClient.post('/v1/optimizer/save', data);

      addNotification({
        type: 'success',
        title: '保存成功',
        message: '优化结果已保存到您的收藏夹',
      });
    } catch (error) {
      throw error;
    } finally {
      setLoading('save', false);
    }
  }

  /**
   * 复制提示词到剪贴板
   */
  async copyToClipboard(text: string): Promise<void> {
    const { addNotification } = useUIStore.getState();
    
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        textArea.remove();
      }

      addNotification({
        type: 'success',
        title: '复制成功',
        message: '提示词已复制到剪贴板',
        duration: 2000,
      });
    } catch (error) {
      addNotification({
        type: 'error',
        title: '复制失败',
        message: '请手动选择并复制文本',
      });
    }
  }

  /**
   * 分享优化结果
   */
  async shareOptimization(id: number): Promise<string> {
    const { setLoading, addNotification } = useUIStore.getState();
    
    try {
      setLoading('load', true);
      
      const result = await apiClient.post<{ share_url: string }>(
        `/v1/optimizer/${id}/share`
      );

      await this.copyToClipboard(result.share_url);

      addNotification({
        type: 'success',
        title: '分享链接已生成',
        message: '分享链接已复制到剪贴板',
      });

      return result.share_url;
    } catch (error) {
      throw error;
    } finally {
      setLoading('load', false);
    }
  }

  /**
   * 获取推荐的优化策略
   */
  async getRecommendations(prompt: string): Promise<{
    strategies: string[];
    examples: Array<{
      title: string;
      before: string;
      after: string;
      improvement: string;
    }>;
  }> {
    try {
      const result = await apiClient.post('/v1/optimizer/recommendations', {
        prompt,
      });

      return result;
    } catch (error) {
      throw error;
    }
  }
}

// 创建单例实例
export const optimizerService = new OptimizerService(); 