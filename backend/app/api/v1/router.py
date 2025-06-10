"""
API v1主路由
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
) 