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
    # 临时注释掉认证，用于测试
    # current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    优化提示词
    
    Args:
        request: 优化请求参数
        db: 数据库会话
        
    Returns:
        优化结果
    """
    try:
        # 临时使用固定用户ID（用于测试）
        from sqlalchemy import select
        
        # 查找第一个用户或创建默认用户
        result = await db.execute(select(User).limit(1))
        current_user = result.scalar_one_or_none()
        
        if not current_user:
            # 创建默认测试用户
            current_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password="$2b$12$dummy",  # 临时密码hash
                is_active=True
            )
            db.add(current_user)
            await db.flush()
        
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


# ==================== 历史记录相关API ====================

@router.get("/history", response_model=dict)
async def get_optimization_history(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户的优化历史记录
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数限制
        category: 分类筛选
        sort_by: 排序字段
        sort_order: 排序顺序
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        历史记录列表和分页信息
    """
    try:
        from sqlalchemy import select, desc, asc
        
        # 构建查询
        query = select(Optimization).where(Optimization.user_id == current_user.id)
        
        # 分类筛选
        if category:
            query = query.where(Optimization.optimization_type == category)
        
        # 排序
        if sort_by == 'created_at':
            if sort_order == 'asc':
                query = query.order_by(asc(Optimization.created_at))
            else:
                query = query.order_by(desc(Optimization.created_at))
        elif sort_by == 'quality_score':
            if sort_order == 'asc':
                query = query.order_by(asc(Optimization.quality_score_after))
            else:
                query = query.order_by(desc(Optimization.quality_score_after))
        else:
            # 默认按创建时间倒序
            query = query.order_by(desc(Optimization.created_at))
        
        # 获取总数
        count_query = select(Optimization).where(Optimization.user_id == current_user.id)
        if category:
            count_query = count_query.where(Optimization.optimization_type == category)
        
        total_result = await db.execute(count_query)
        total = len(total_result.fetchall())
        
        # 分页
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        optimizations = result.scalars().all()
        
        # 转换为响应格式
        records = []
        for opt in optimizations:
            # 获取该优化记录的改进说明
            improvements_query = select(OptimizationImprovement).where(
                OptimizationImprovement.optimization_id == opt.id
            )
            improvements_result = await db.execute(improvements_query)
            improvements = improvements_result.scalars().all()
            
            records.append({
                "id": opt.id,
                "original_prompt": opt.original_prompt,
                "optimized_prompt": opt.optimized_prompt,
                "quality_score_before": opt.quality_score_before,
                "quality_score_after": opt.quality_score_after,
                "optimization_type": opt.optimization_type,
                "created_at": opt.created_at,
                "improvements": [
                    {
                        "type": imp.improvement_type,
                        "description": imp.description
                    } for imp in improvements
                ],
                "processing_time": opt.processing_time
            })
        
        return {
            "records": records,
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "pageSize": limit
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取历史记录失败: {str(e)}"
        )


@router.get("/history/{optimization_id}", response_model=dict)
async def get_optimization_detail(
    optimization_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取单条优化记录详情
    
    Args:
        optimization_id: 优化记录ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        优化记录详情
    """
    try:
        from sqlalchemy import select
        
        # 查询优化记录
        query = select(Optimization).where(
            Optimization.id == optimization_id,
            Optimization.user_id == current_user.id
        )
        result = await db.execute(query)
        optimization = result.scalar_one_or_none()
        
        if not optimization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="优化记录不存在"
            )
        
        # 获取改进说明
        improvements_query = select(OptimizationImprovement).where(
            OptimizationImprovement.optimization_id == optimization.id
        )
        improvements_result = await db.execute(improvements_query)
        improvements = improvements_result.scalars().all()
        
        return {
            "id": optimization.id,
            "original_prompt": optimization.original_prompt,
            "optimized_prompt": optimization.optimized_prompt,
            "quality_score_before": optimization.quality_score_before,
            "quality_score_after": optimization.quality_score_after,
            "optimization_type": optimization.optimization_type,
            "created_at": optimization.created_at,
            "improvements": [
                {
                    "type": imp.improvement_type,
                    "description": imp.description
                } for imp in improvements
            ],
            "processing_time": optimization.processing_time,
            "token_usage": {
                "prompt_tokens": optimization.prompt_tokens,
                "completion_tokens": optimization.completion_tokens,
                "total_tokens": optimization.total_tokens,
                "cost_estimate": optimization.cost_estimate
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取优化详情失败: {str(e)}"
        )


@router.post("/history/save", response_model=dict)
async def save_optimization_result(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    保存优化结果（用于前端手动保存）
    
    Args:
        data: 保存的数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        保存结果
    """
    try:
        # 注意：实际的保存逻辑在optimize端点中已经实现
        # 这里主要是为了前端API调用的兼容性
        return {"message": "保存成功", "success": True}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存失败: {str(e)}"
        )


@router.delete("/history/{optimization_id}")
async def delete_optimization_record(
    optimization_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除优化记录
    
    Args:
        optimization_id: 优化记录ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        删除结果
    """
    try:
        from sqlalchemy import select, delete
        
        # 查询优化记录是否存在且属于当前用户
        query = select(Optimization).where(
            Optimization.id == optimization_id,
            Optimization.user_id == current_user.id
        )
        result = await db.execute(query)
        optimization = result.scalar_one_or_none()
        
        if not optimization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="优化记录不存在"
            )
        
        # 删除相关的改进说明
        improvements_delete = delete(OptimizationImprovement).where(
            OptimizationImprovement.optimization_id == optimization_id
        )
        await db.execute(improvements_delete)
        
        # 删除优化记录
        optimization_delete = delete(Optimization).where(
            Optimization.id == optimization_id
        )
        await db.execute(optimization_delete)
        
        await db.commit()
        
        return {"message": "删除成功", "success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败: {str(e)}"
        )


@router.get("/history/stats", response_model=dict)
async def get_optimization_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户的优化统计数据
    
    Args:
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        统计数据
    """
    try:
        from sqlalchemy import select, func
        
        # 获取总优化次数
        total_query = select(func.count(Optimization.id)).where(
            Optimization.user_id == current_user.id
        )
        total_result = await db.execute(total_query)
        total_optimizations = total_result.scalar() or 0
        
        # 获取平均质量提升
        avg_query = select(
            func.avg(Optimization.quality_score_after - Optimization.quality_score_before)
        ).where(Optimization.user_id == current_user.id)
        avg_result = await db.execute(avg_query)
        avg_improvement = avg_result.scalar() or 0
        
        # 获取最常用的优化类型
        type_query = select(
            Optimization.optimization_type,
            func.count(Optimization.optimization_type).label('count')
        ).where(
            Optimization.user_id == current_user.id
        ).group_by(Optimization.optimization_type).order_by(
            func.count(Optimization.optimization_type).desc()
        ).limit(1)
        
        type_result = await db.execute(type_query)
        most_used_type_row = type_result.first()
        most_used_type = most_used_type_row[0] if most_used_type_row else "general"
        
        # 获取最近的活动
        recent_query = select(Optimization).where(
            Optimization.user_id == current_user.id
        ).order_by(Optimization.created_at.desc()).limit(5)
        
        recent_result = await db.execute(recent_query)
        recent_optimizations = recent_result.scalars().all()
        
        recent_activity = [
            {
                "id": opt.id,
                "original_prompt": opt.original_prompt[:100] + "..." if len(opt.original_prompt) > 100 else opt.original_prompt,
                "optimization_type": opt.optimization_type,
                "quality_score_before": opt.quality_score_before,
                "quality_score_after": opt.quality_score_after,
                "created_at": opt.created_at
            } for opt in recent_optimizations
        ]
        
        return {
            "totalOptimizations": total_optimizations,
            "averageQualityImprovement": round(float(avg_improvement), 2),
            "mostUsedType": most_used_type,
            "recentActivity": recent_activity
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        )


@router.post("/history/{optimization_id}/share", response_model=dict)
async def share_optimization(
    optimization_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    分享优化结果
    
    Args:
        optimization_id: 优化记录ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        分享链接
    """
    try:
        from sqlalchemy import select
        import uuid
        
        # 查询优化记录
        query = select(Optimization).where(
            Optimization.id == optimization_id,
            Optimization.user_id == current_user.id
        )
        result = await db.execute(query)
        optimization = result.scalar_one_or_none()
        
        if not optimization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="优化记录不存在"
            )
        
        # 生成分享链接（这里简化处理，实际项目中可能需要更复杂的逻辑）
        share_id = str(uuid.uuid4())
        share_url = f"https://yourapp.com/shared/{share_id}"
        
        return {
            "shareUrl": share_url,
            "shareId": share_id,
            "message": "分享链接生成成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"分享失败: {str(e)}"
        )


@router.post("/history/recommendations", response_model=list)
async def get_optimization_recommendations(
    request: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取优化建议
    
    Args:
        request: 请求参数
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        推荐结果列表
    """
    try:
        # 这里可以基于用户的历史记录提供个性化建议
        # 简化实现，返回一些通用建议
        recommendations = [
            {
                "type": "clarity",
                "title": "提高清晰度",
                "description": "使用更具体、明确的表述",
                "priority": "high"
            },
            {
                "type": "structure",
                "title": "改进结构",
                "description": "使用分步骤或分层次的结构",
                "priority": "medium"
            },
            {
                "type": "context",
                "title": "增加上下文",
                "description": "提供更多背景信息和约束条件",
                "priority": "medium"
            }
        ]
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取建议失败: {str(e)}"
        ) 