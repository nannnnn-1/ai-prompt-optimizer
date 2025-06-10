"""
通用数据模式
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime


class BaseResponse(BaseModel):
    """基础响应模式"""
    
    success: bool = Field(True, description="请求是否成功")
    message: str = Field("", description="响应消息")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="响应时间戳")


class ErrorResponse(BaseResponse):
    """错误响应模式"""
    
    success: bool = Field(False, description="请求失败")
    error_code: str = Field(..., description="错误代码")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")


class SuccessResponse(BaseResponse):
    """成功响应模式"""
    
    data: Optional[Any] = Field(None, description="响应数据")


class PaginationParams(BaseModel):
    """分页参数"""
    
    skip: int = Field(0, ge=0, description="跳过的记录数")
    limit: int = Field(20, ge=1, le=100, description="限制返回的记录数")


class PaginatedResponse(BaseModel):
    """分页响应模式"""
    
    items: list = Field(..., description="数据列表")
    total: int = Field(..., description="总记录数")
    skip: int = Field(..., description="跳过的记录数")
    limit: int = Field(..., description="限制的记录数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")


class HealthResponse(BaseModel):
    """健康检查响应"""
    
    status: str = Field(..., description="健康状态")
    timestamp: str = Field(..., description="检查时间")
    version: str = Field(..., description="版本号")
    environment: str = Field(..., description="环境")
    components: Optional[Dict[str, Any]] = Field(None, description="组件状态") 