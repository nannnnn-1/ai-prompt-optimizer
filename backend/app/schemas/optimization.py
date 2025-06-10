"""
提示词优化相关的数据模式
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OptimizationType(str, Enum):
    """优化类型枚举"""
    GENERAL = "general"
    CODE = "code"
    WRITING = "writing"
    ANALYSIS = "analysis"


class OptimizationRequest(BaseModel):
    """优化请求"""
    original_prompt: str = Field(..., min_length=1, max_length=10000, description="原始提示词")
    optimization_type: OptimizationType = Field(default=OptimizationType.GENERAL, description="优化类型")
    user_context: Optional[str] = Field(None, max_length=1000, description="用户上下文")
    
    @validator('original_prompt')
    def validate_prompt_content(cls, v):
        if not v.strip():
            raise ValueError('提示词不能为空')
        return v.strip()


class QualityEvaluationRequest(BaseModel):
    """质量评估请求"""
    prompt: str = Field(..., min_length=1, max_length=10000, description="要评估的提示词")
    
    @validator('prompt')
    def validate_prompt_content(cls, v):
        if not v.strip():
            raise ValueError('提示词不能为空')
        return v.strip()


class BatchOptimizationRequest(BaseModel):
    """批量优化请求"""
    prompts: List[str] = Field(..., min_items=1, max_items=10, description="提示词列表")
    optimization_type: OptimizationType = Field(default=OptimizationType.GENERAL, description="优化类型")
    
    @validator('prompts')
    def validate_prompts(cls, v):
        for prompt in v:
            if not prompt.strip():
                raise ValueError('提示词不能为空')
        return [prompt.strip() for prompt in v]


class ImprovementInfo(BaseModel):
    """改进信息"""
    type: str = Field(..., description="改进类型")
    description: str = Field(..., description="改进描述")


class TokenUsage(BaseModel):
    """Token使用统计"""
    prompt_tokens: int = Field(..., description="输入token数")
    completion_tokens: int = Field(..., description="输出token数")
    total_tokens: int = Field(..., description="总token数")
    cost_estimate: float = Field(..., description="成本估算")


class DetailedScores(BaseModel):
    """详细评分"""
    clarity: int = Field(..., ge=1, le=10, description="清晰度评分")
    completeness: int = Field(..., ge=1, le=10, description="完整性评分")
    structure: int = Field(..., ge=1, le=10, description="结构性评分")
    specificity: int = Field(..., ge=1, le=10, description="具体性评分")
    actionability: int = Field(..., ge=1, le=10, description="可执行性评分")


class OptimizationResponse(BaseModel):
    """优化响应"""
    id: int = Field(..., description="优化记录ID")
    original_prompt: str = Field(..., description="原始提示词")
    optimized_prompt: str = Field(..., description="优化后的提示词")
    quality_score_before: float = Field(..., ge=0, le=10, description="优化前质量评分")
    quality_score_after: float = Field(..., ge=0, le=10, description="优化后质量评分")
    optimization_type: str = Field(..., description="优化类型")
    improvements: List[ImprovementInfo] = Field(..., description="改进说明列表")
    processing_time: float = Field(..., description="处理时间（秒）")
    token_usage: TokenUsage = Field(..., description="Token使用统计")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True


class QualityEvaluationResponse(BaseModel):
    """质量评估响应"""
    overall_score: int = Field(..., ge=0, le=10, description="总体评分")
    detailed_scores: DetailedScores = Field(..., description="详细评分")
    issues: List[str] = Field(..., description="问题列表")
    suggestions: List[str] = Field(..., description="建议列表")
    processing_time: float = Field(..., description="处理时间（秒）")


class OptimizationSuggestionResponse(BaseModel):
    """优化建议响应"""
    suggestions: List[str] = Field(..., description="建议列表")


class BatchOptimizationResponse(BaseModel):
    """批量优化响应"""
    results: List[OptimizationResponse] = Field(..., description="优化结果列表")
    total_count: int = Field(..., description="总数")
    success_count: int = Field(..., description="成功数")
    total_processing_time: float = Field(..., description="总处理时间（秒）")


class OptimizationHistoryQuery(BaseModel):
    """历史记录查询参数"""
    skip: int = Field(default=0, ge=0, description="跳过数量")
    limit: int = Field(default=20, ge=1, le=100, description="返回数量")
    optimization_type: Optional[OptimizationType] = Field(None, description="优化类型筛选")
    search_keyword: Optional[str] = Field(None, max_length=100, description="搜索关键词")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")


class OptimizationHistoryResponse(BaseModel):
    """历史记录响应"""
    items: List[OptimizationResponse] = Field(..., description="历史记录列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")


class OptimizationStats(BaseModel):
    """优化统计信息"""
    total_optimizations: int = Field(..., description="总优化次数")
    average_score_improvement: float = Field(..., description="平均评分提升")
    total_tokens_used: int = Field(..., description="总使用token数")
    total_cost: float = Field(..., description="总成本")
    optimization_types_count: Dict[str, int] = Field(..., description="各类型优化次数")
    recent_activity: List[Dict[str, Any]] = Field(..., description="最近活动")


class AIHealthResponse(BaseModel):
    """AI服务健康状态响应"""
    status: str = Field(..., description="服务状态")
    model: str = Field(..., description="使用的模型")
    response_time: Optional[float] = Field(None, description="响应时间")
    api_available: bool = Field(..., description="API是否可用")
    error: Optional[str] = Field(None, description="错误信息") 