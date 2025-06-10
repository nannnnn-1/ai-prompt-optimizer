"""
用户数据模型
"""

from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
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
    
    # 用户偏好设置
    preferred_optimization_type: Mapped[str] = mapped_column(
        String(50), 
        default="general", 
        comment="偏好的优化类型"
    )
    theme: Mapped[str] = mapped_column(
        String(20), 
        default="light", 
        comment="界面主题"
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
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>" 