"""
认证服务
提供用户认证相关的业务逻辑
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status
from app.models.user import User, LoginHistory
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    verify_refresh_token
)
from app.config import settings
import json


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register_user(self, user_data: UserRegister) -> UserResponse:
        """
        用户注册
        
        Args:
            user_data: 用户注册数据
            
        Returns:
            用户响应对象
            
        Raises:
            HTTPException: 用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        stmt = select(User).where(User.username == user_data.username)
        existing_user = await self.db.execute(stmt)
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        stmt = select(User).where(User.email == user_data.email)
        existing_email = await self.db.execute(stmt)
        if existing_email.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,
            is_superuser=False,
            email_verified=False,
            login_count=0,
            optimization_count=0
        )
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        return UserResponse.from_orm(db_user)

    async def create_user(self, user_data, is_superuser: bool = False) -> UserResponse:
        """
        创建用户（支持管理员创建）
        
        Args:
            user_data: 用户数据
            is_superuser: 是否为超级管理员
            
        Returns:
            用户响应对象
        """
        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,
            is_superuser=is_superuser,
            email_verified=True if is_superuser else False,  # 管理员用户默认验证邮箱
            login_count=0,
            optimization_count=0
        )
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        return UserResponse.from_orm(db_user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            email: 邮箱地址
            
        Returns:
            用户对象或None
        """
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def authenticate_user(self, login_data: UserLogin, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Optional[User]:
        """
        用户认证
        
        Args:
            login_data: 登录数据
            ip_address: IP地址
            user_agent: 用户代理
            
        Returns:
            认证成功的用户对象或None
        """
        # 查找用户
        stmt = select(User).where(User.username == login_data.username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        success = False
        if user and verify_password(login_data.password, user.hashed_password):
            if user.is_active:
                success = True
                # 更新登录信息
                user.last_login = datetime.utcnow()
                user.login_count += 1
                await self.db.commit()
        
        # 记录登录历史
        if user:
            login_record = LoginHistory(
                user_id=user.id,
                login_time=datetime.utcnow(),
                ip_address=ip_address,
                user_agent=user_agent,
                success=success
            )
            self.db.add(login_record)
            await self.db.commit()
        
        return user if success else None
    
    async def create_tokens(self, user: User) -> Token:
        """
        为用户创建访问令牌和刷新令牌
        
        Args:
            user: 用户对象
            
        Returns:
            Token对象
        """
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        刷新访问令牌
        
        Args:
            refresh_token: 刷新令牌
            
        Returns:
            新的Token对象
            
        Raises:
            HTTPException: 刷新令牌无效
        """
        user_id = verify_refresh_token(refresh_token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        
        # 验证用户是否存在且活跃
        stmt = select(User).where(User.id == int(user_id))
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )
        
        return await self.create_tokens(user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户对象或None
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
            
        Returns:
            用户对象或None
        """
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> bool:
        """
        更新用户偏好设置
        
        Args:
            user_id: 用户ID
            preferences: 偏好设置字典
            
        Returns:
            是否更新成功
        """
        try:
            preferences_json = json.dumps(preferences, ensure_ascii=False)
            stmt = update(User).where(User.id == user_id).values(preferences=preferences_json)
            await self.db.execute(stmt)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False
    
    async def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户偏好设置
        
        Args:
            user_id: 用户ID
            
        Returns:
            偏好设置字典
        """
        stmt = select(User.preferences).where(User.id == user_id)
        result = await self.db.execute(stmt)
        preferences_json = result.scalar_one_or_none()
        
        if preferences_json:
            try:
                return json.loads(preferences_json)
            except json.JSONDecodeError:
                return {}
        return {}
    
    async def deactivate_user(self, user_id: int) -> bool:
        """
        停用用户账户
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否停用成功
        """
        try:
            stmt = update(User).where(User.id == user_id).values(is_active=False)
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.rowcount > 0
        except Exception:
            await self.db.rollback()
            return False
    
    async def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        修改用户密码
        
        Args:
            user_id: 用户ID
            current_password: 当前密码
            new_password: 新密码
            
        Returns:
            是否修改成功
        """
        # 获取用户
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # 验证当前密码
        if not verify_password(current_password, user.hashed_password):
            return False
        
        # 更新密码
        try:
            new_hashed_password = get_password_hash(new_password)
            stmt = update(User).where(User.id == user_id).values(hashed_password=new_hashed_password)
            await self.db.execute(stmt)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False 