"""
FastAPI主应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.api.v1.router import api_router
from app.config import settings
from app.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    # 启动时执行
    print("🚀 正在启动AI提示词优化器后端服务...")
    
    # 创建数据库表
    await create_tables()
    print("✅ 数据库表创建完成")
    
    yield
    
    # 关闭时执行
    print("🛑 AI提示词优化器后端服务已关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title="AI提示词优化器 API",
    description="基于AI的提示词智能优化后端服务",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["根路径"])
async def root():
    """根路径欢迎信息"""
    return {
        "message": "欢迎使用AI提示词优化器API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "文档已禁用",
        "health": "/api/v1/health/"
    }


@app.get("/health", tags=["健康检查"])
async def simple_health_check():
    """简单健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    ) 