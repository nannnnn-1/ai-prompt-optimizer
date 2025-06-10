"""
FastAPI依赖注入
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.config import Settings, get_settings


async def get_db() -> AsyncSession:
    """
    获取数据库会话依赖
    
    Returns:
        AsyncSession: 数据库会话
    """
    async for session in get_async_session():
        yield session


def get_app_settings() -> Settings:
    """
    获取应用设置依赖
    
    Returns:
        Settings: 应用设置
    """
    return get_settings() 