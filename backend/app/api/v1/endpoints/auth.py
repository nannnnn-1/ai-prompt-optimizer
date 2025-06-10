"""
认证相关API端点
"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.schemas.auth import (
    UserRegister, 
    UserLogin, 
    Token, 
    TokenRefresh, 
    UserResponse,
    PasswordUpdate
)
from app.models.user import User
from app.services.auth_service import AuthService
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    用户注册
    
    - **username**: 用户名（3-50个字符，只能包含字母和数字）
    - **email**: 邮箱地址
    - **password**: 密码（至少8个字符，包含大小写字母和数字）
    - **full_name**: 用户全名（可选）
    """
    auth_service = AuthService(db)
    try:
        user = await auth_service.register_user(user_data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败：{str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    用户登录
    
    - **username**: 用户名
    - **password**: 密码
    
    返回访问令牌和刷新令牌
    """
    auth_service = AuthService(db)
    
    # 获取客户端信息
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    # 用户认证
    user = await auth_service.authenticate_user(
        user_credentials, 
        ip_address=ip_address, 
        user_agent=user_agent
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建Token
    tokens = await auth_service.create_tokens(user)
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    """
    auth_service = AuthService(db)
    try:
        new_tokens = await auth_service.refresh_access_token(token_data.refresh_token)
        return new_tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"令牌刷新失败：{str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户信息
    
    需要提供有效的访问令牌
    """
    return UserResponse.from_orm(current_user)


@router.post("/logout", response_model=dict)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    用户退出登录
    
    注意：由于JWT的无状态特性，实际的令牌失效需要在客户端处理
    此接口主要用于记录退出日志和清理服务端资源
    """
    # 这里可以添加退出登录的相关逻辑，如：
    # 1. 记录退出日志
    # 2. 清理用户会话缓存
    # 3. 发送退出通知等
    
    return {
        "message": "退出登录成功",
        "user_id": current_user.id
    }


@router.put("/password", response_model=dict)
async def change_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    修改密码
    
    - **current_password**: 当前密码
    - **new_password**: 新密码（至少8个字符，包含大小写字母和数字）
    """
    auth_service = AuthService(db)
    
    success = await auth_service.change_password(
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误或密码修改失败"
        )
    
    return {
        "message": "密码修改成功",
        "user_id": current_user.id
    } 