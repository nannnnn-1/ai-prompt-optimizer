"""
提示词优化相关的数据库模型
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User


class Optimization(BaseModel):
    """优化记录模型"""
    __tablename__ = "optimizations"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 提示词内容
    original_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    optimized_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 质量评分
    quality_score_before: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality_score_after: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # 优化相关信息
    optimization_type: Mapped[str] = mapped_column(String(50), default="general", nullable=False)
    ai_model_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    processing_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Token使用统计
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cost_estimate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # 关系
    user: Mapped["User"] = relationship("User", back_populates="optimizations")
    improvements: Mapped[List["OptimizationImprovement"]] = relationship("OptimizationImprovement", back_populates="optimization", cascade="all, delete-orphan")


class OptimizationImprovement(BaseModel):
    """优化改进点模型"""
    __tablename__ = "optimization_improvements"
    
    optimization_id: Mapped[int] = mapped_column(Integer, ForeignKey("optimizations.id"), nullable=False)
    
    # 改进信息
    improvement_type: Mapped[str] = mapped_column(String(100), nullable=False)  # 结构性改进、清晰度改进等
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 改进前后对比（可选）
    before_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    after_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 关系
    optimization: Mapped["Optimization"] = relationship("Optimization", back_populates="improvements")


class OptimizationExample(BaseModel):
    """优化案例模型"""
    __tablename__ = "optimization_examples"
    
    # 案例基本信息
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    difficulty_level: Mapped[str] = mapped_column(String(20), default="beginner")  # beginner, intermediate, advanced
    
    # 提示词内容
    original_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    optimized_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 案例描述
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    optimization_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 标签和分类
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # JSON字符串格式存储标签
    
    # 统计信息
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    like_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 质量评分
    quality_score_before: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality_score_after: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # 状态
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否为精选案例
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)     # 是否公开
    
    # 创建者信息
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 关系
    creator: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])


class OptimizationTemplate(BaseModel):
    """优化模板模型"""
    __tablename__ = "optimization_templates"
    
    # 模板基本信息
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    optimization_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # 模板内容
    template_content: Mapped[str] = mapped_column(Text, nullable=False)  # 模板的提示词内容
    instruction: Mapped[str] = mapped_column(Text, nullable=False)       # 使用说明
    
    # 描述信息
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    use_cases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 适用场景
    
    # 参数配置
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON格式存储参数配置
    
    # 统计信息
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_system_template: Mapped[bool] = mapped_column(Boolean, default=False)  # 系统内置模板
    
    # 创建者信息
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 关系
    creator: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by]) 