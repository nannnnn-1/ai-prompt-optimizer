"""
提示词优化API接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import time

from app.models.user import User
from app.models.optimization import Optimization, OptimizationImprovement
from app.schemas.optimization import (
    OptimizationRequest,
    OptimizationResponse,
    QualityEvaluationRequest,
    QualityEvaluationResponse,
    OptimizationSuggestionResponse,
    BatchOptimizationRequest,
    BatchOptimizationResponse
)
from app.core.ai_client import ai_client, AIServiceException
from app.core.dependencies import get_current_user, get_db
from app.utils.exceptions import PromptOptimizerException

router = APIRouter(prefix="/optimizer", tags=["optimizer"])


@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_prompt(
    request: OptimizationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    优化提示词
    
    Args:
        request: 优化请求参数
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        优化结果
    """
    try:
        # 调用AI服务进行优化
        result = await ai_client.optimize_prompt(
            original_prompt=request.original_prompt,
            optimization_type=request.optimization_type
        )
        
        # 保存优化记录到数据库
        optimization = Optimization(
            user_id=current_user.id,
            original_prompt=request.original_prompt,
            optimized_prompt=result.optimized_prompt,
            quality_score_before=result.quality_score_before,
            quality_score_after=result.quality_score_after,
            optimization_type=request.optimization_type,
            ai_model_used=ai_client.model,
            processing_time=result.processing_time,
            prompt_tokens=result.usage_stats.prompt_tokens,
            completion_tokens=result.usage_stats.completion_tokens,
            total_tokens=result.usage_stats.total_tokens,
            cost_estimate=result.usage_stats.cost_estimate
        )
        
        db.add(optimization)
        await db.flush()  # 获取生成的ID
        
        # 保存改进说明 
        improvements = []
        for improvement_data in result.improvements:
            improvement = OptimizationImprovement(
                optimization_id=optimization.id,
                improvement_type=improvement_data["type"],
                description=improvement_data["description"]
            )
            db.add(improvement)
            improvements.append(improvement)
        
        await db.commit()
        
        # 构造响应
        return OptimizationResponse(
            id=optimization.id,
            original_prompt=optimization.original_prompt,
            optimized_prompt=optimization.optimized_prompt,
            quality_score_before=optimization.quality_score_before,
            quality_score_after=optimization.quality_score_after,
            optimization_type=optimization.optimization_type,
            improvements=[
                {
                    "type": imp.improvement_type,
                    "description": imp.description
                } for imp in improvements
            ],
            processing_time=optimization.processing_time,
            token_usage={
                "prompt_tokens": optimization.prompt_tokens,
                "completion_tokens": optimization.completion_tokens,
                "total_tokens": optimization.total_tokens,
                "cost_estimate": optimization.cost_estimate
            },
            created_at=optimization.created_at
        )
        
    except AIServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI服务不可用: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"优化失败: {str(e)}"
        )


@router.post("/evaluate", response_model=QualityEvaluationResponse)
async def evaluate_prompt_quality(
    request: QualityEvaluationRequest
):
    """
    评估提示词质量
    
    Args:
        request: 评估请求
        
    Returns:
        质量评估结果
    """
    try:
        analysis = await ai_client.analyze_prompt_quality(request.prompt)
        
        return QualityEvaluationResponse(
            overall_score=analysis["overall_score"],
            detailed_scores=analysis["scores"],
            issues=analysis["issues"],
            suggestions=analysis["suggestions"],
            processing_time=analysis["processing_time"]
        )
        
    except AIServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI服务不可用: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评估失败: {str(e)}"
        )


@router.post("/suggestions", response_model=OptimizationSuggestionResponse)
async def get_optimization_suggestions(
    request: QualityEvaluationRequest
):
    """
    获取优化建议（不执行实际优化）
    
    Args:
        request: 评估请求
        
    Returns:
        优化建议列表
    """
    try:
        suggestions = await ai_client.get_optimization_suggestions(request.prompt)
        
        return OptimizationSuggestionResponse(
            suggestions=suggestions
        )
        
    except AIServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI服务不可用: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取建议失败: {str(e)}"
        )


@router.post("/batch-optimize", response_model=BatchOptimizationResponse)
async def batch_optimize_prompts(
    request: BatchOptimizationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    批量优化提示词
    
    Args:
        request: 批量优化请求
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        批量优化结果
    """
    try:
        # 限制批量处理数量
        if len(request.prompts) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="批量处理最多支持10个提示词"
            )
        
        # 执行批量优化
        results = await ai_client.batch_optimize(
            prompts=request.prompts,
            optimization_type=request.optimization_type
        )
        
        # 保存所有结果到数据库
        optimization_responses = []
        
        for i, result in enumerate(results):
            optimization = Optimization(
                user_id=current_user.id,
                original_prompt=request.prompts[i],
                optimized_prompt=result.optimized_prompt,
                quality_score_before=result.quality_score_before,
                quality_score_after=result.quality_score_after,
                optimization_type=request.optimization_type,
                ai_model_used=ai_client.model,
                processing_time=result.processing_time,
                prompt_tokens=result.usage_stats.prompt_tokens,
                completion_tokens=result.usage_stats.completion_tokens,
                total_tokens=result.usage_stats.total_tokens,
                cost_estimate=result.usage_stats.cost_estimate
            )
            
            db.add(optimization)
            await db.flush()
            
            # 保存改进说明
            improvements = []
            for improvement_data in result.improvements:
                improvement = OptimizationImprovement(
                    optimization_id=optimization.id,
                    improvement_type=improvement_data["type"],
                    description=improvement_data["description"]
                )
                db.add(improvement)
                improvements.append(improvement)
            
            optimization_responses.append(OptimizationResponse(
                id=optimization.id,
                original_prompt=optimization.original_prompt,
                optimized_prompt=optimization.optimized_prompt,
                quality_score_before=optimization.quality_score_before,
                quality_score_after=optimization.quality_score_after,
                optimization_type=optimization.optimization_type,
                improvements=[
                    {
                        "type": imp.improvement_type,
                        "description": imp.description
                    } for imp in improvements
                ],
                processing_time=optimization.processing_time,
                token_usage={
                    "prompt_tokens": optimization.prompt_tokens,
                    "completion_tokens": optimization.completion_tokens,
                    "total_tokens": optimization.total_tokens,
                    "cost_estimate": optimization.cost_estimate
                },
                created_at=optimization.created_at
            ))
        
        await db.commit()
        
        return BatchOptimizationResponse(
            results=optimization_responses,
            total_count=len(optimization_responses),
            success_count=len(optimization_responses),
            failed_count=0
        )
        
    except AIServiceException as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI服务不可用: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量优化失败: {str(e)}"
        )


@router.get("/health")
async def check_ai_health():
    """
    检查AI服务健康状态
    
    Returns:
        AI服务状态信息
    """
    try:
        health_status = await ai_client.health_check()
        return health_status
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"健康检查失败: {str(e)}"
        ) 