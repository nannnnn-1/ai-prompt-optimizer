"""
API v1主路由
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, users

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
) 