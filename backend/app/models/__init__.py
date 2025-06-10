"""
数据模型模块
"""

# 统一导入所有模型，避免循环导入
from .base import BaseModel, TimestampMixin
from .user import User, LoginHistory
from .optimization import Optimization, OptimizationImprovement, OptimizationExample, OptimizationTemplate

__all__ = [
    "BaseModel",
    "TimestampMixin", 
    "User",
    "LoginHistory",
    "Optimization",
    "OptimizationImprovement", 
    "OptimizationExample",
    "OptimizationTemplate"
] 