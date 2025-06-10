"""
健康检查API端点
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime
from typing import Dict, Any
from app.dependencies import get_db
from app.config import settings

router = APIRouter()


@router.get("/", summary="基础健康检查")
async def health_check() -> Dict[str, Any]:
    """
    基础健康检查
    
    Returns:
        Dict[str, Any]: 健康状态信息
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production"
    }


@router.get("/db", summary="数据库健康检查")
async def database_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    数据库健康检查
    
    Args:
        db: 数据库会话
        
    Returns:
        Dict[str, Any]: 数据库健康状态
    """
    try:
        # 执行简单查询测试数据库连接
        result = await db.execute(text("SELECT 1 as test"))
        test_result = result.scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "test_query": test_result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/detailed", summary="详细健康检查")
async def detailed_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    详细健康检查
    
    Args:
        db: 数据库会话
        
    Returns:
        Dict[str, Any]: 详细健康状态信息
    """
    health_info = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production",
        "components": {}
    }
    
    # 检查数据库
    try:
        result = await db.execute(text("SELECT 1 as test"))
        test_result = result.scalar()
        health_info["components"]["database"] = {
            "status": "healthy",
            "test_result": test_result
        }
    except Exception as e:
        health_info["status"] = "unhealthy"
        health_info["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # 检查配置
    health_info["components"]["configuration"] = {
        "status": "healthy",
        "debug_mode": settings.DEBUG,
        "has_openai_key": bool(settings.OPENAI_API_KEY)
    }
    
    return health_info 