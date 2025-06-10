"""
用户数据模型
"""

from sqlalchemy import String, Boolean, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.optimization import Optimization


class User(BaseModel):
    """用户模型"""
    
    __tablename__ = "users"
    
    # 基本信息
    username: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        index=True, 
        comment="用户名"
    )
    email: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        index=True, 
        comment="邮箱"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), 
        comment="密码哈希"
    )
    
    # 状态信息
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        comment="是否激活"
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        comment="是否超级用户"
    )
    
    # 用户详细信息
    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="用户全名"
    )
    
    # 认证相关字段
    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="邮箱是否已验证"
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="最后登录时间"
    )
    login_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="登录次数"
    )
    
    # 用户偏好设置 (JSON格式)
    preferences: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="用户偏好设置JSON"
    )
    
    # 统计信息
    optimization_count: Mapped[int] = mapped_column(
        default=0, 
        comment="优化次数"
    )
    
    # 关系映射
    # optimizations: Mapped[List["Optimization"]] = relationship(
    #     back_populates="user", 
    #     cascade="all, delete-orphan",
    #     lazy="selectin"
    # )
    login_history: Mapped[List["LoginHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class LoginHistory(BaseModel):
    """登录历史记录模型"""
    
    __tablename__ = "login_history"
    
    # 关联用户
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        comment="用户ID"
    )
    
    # 登录信息
    login_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="登录时间"
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),  # 支持IPv6
        comment="IP地址"
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="用户代理"
    )
    success: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="登录是否成功"
    )
    logout_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="退出时间"
    )
    
    # 关系
    user: Mapped["User"] = relationship(back_populates="login_history")
    
    def __repr__(self) -> str:
        return f"<LoginHistory(id={self.id}, user_id={self.user_id}, login_time='{self.login_time}')>" 