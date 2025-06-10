from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, get_current_active_superuser
from app.models.user import User
from app.schemas.auth import UserResponse, UserUpdate, UserCreate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db)
):
    """获取用户列表（仅超级管理员）"""
    user_service = UserService(db)
    users = await user_service.get_users(
        skip=skip, 
        limit=limit, 
        is_active=is_active
    )
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取指定用户信息"""
    # 用户只能查看自己的信息，除非是超级管理员
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    # 用户只能更新自己的信息，除非是超级管理员
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return user

@router.post("/admin", response_model=UserResponse)
async def create_admin_user(
    user_create: UserCreate,
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db)
):
    """创建管理员用户（仅超级管理员）"""
    auth_service = AuthService(db)
    
    # 检查用户名和邮箱是否已存在
    if await auth_service.get_user_by_username(user_create.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    if await auth_service.get_user_by_email(user_create.email):
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建管理员用户
    user = await auth_service.create_user(user_create, is_superuser=True)
    return user

@router.put("/{user_id}/status")
async def update_user_status(
    user_id: int,
    is_active: bool,
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db)
):
    """更新用户状态（激活/禁用）"""
    user_service = UserService(db)
    user = await user_service.update_user_status(user_id, is_active)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {"message": f"用户状态已更新为 {'激活' if is_active else '禁用'}"}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db)
):
    """删除用户（仅超级管理员）"""
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    user_service = UserService(db)
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {"message": "用户已删除"}

@router.get("/{user_id}/login-history")
async def get_user_login_history(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户登录历史"""
    # 用户只能查看自己的登录历史，除非是超级管理员
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    user_service = UserService(db)
    history = await user_service.get_login_history(user_id, skip, limit)
    return history 