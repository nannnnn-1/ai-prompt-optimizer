#!/usr/bin/env python3
"""
初始化超级管理员用户脚本
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate
from app.core.security import get_password_hash


async def create_superuser():
    """创建超级管理员用户"""
    print("=== AI提示词优化器 - 创建超级管理员 ===")
    
    # 获取用户输入
    username = input("请输入超级管理员用户名: ").strip()
    if not username:
        print("❌ 用户名不能为空")
        return
    
    email = input("请输入超级管理员邮箱: ").strip()
    if not email:
        print("❌ 邮箱不能为空")
        return
    
    password = input("请输入超级管理员密码: ").strip()
    if not password:
        print("❌ 密码不能为空")
        return
    
    full_name = input("请输入超级管理员姓名（可选）: ").strip() or None
    
    # 验证密码强度
    if len(password) < 8:
        print("❌ 密码至少需要8个字符")
        return
    
    if not any(c.isupper() for c in password):
        print("❌ 密码必须包含至少一个大写字母")
        return
    
    if not any(c.islower() for c in password):
        print("❌ 密码必须包含至少一个小写字母")
        return
    
    if not any(c.isdigit() for c in password):
        print("❌ 密码必须包含至少一个数字")
        return
    
    try:
        async with async_session_maker() as db:
            auth_service = AuthService(db)
            
            # 检查用户是否已存在
            existing_user = await auth_service.get_user_by_username(username)
            if existing_user:
                print(f"❌ 用户名 '{username}' 已存在")
                return
            
            existing_email = await auth_service.get_user_by_email(email)
            if existing_email:
                print(f"❌ 邮箱 '{email}' 已存在")
                return
            
            # 创建用户数据
            user_data = UserCreate(
                username=username,
                email=email,
                password=password,
                full_name=full_name
            )
            
            # 创建超级管理员用户
            superuser = await auth_service.create_user(user_data, is_superuser=True)
            
            print(f"✅ 超级管理员用户创建成功！")
            print(f"   用户名: {superuser.username}")
            print(f"   邮箱: {superuser.email}")
            print(f"   姓名: {superuser.full_name}")
            print(f"   创建时间: {superuser.created_at}")
            print(f"   用户ID: {superuser.id}")
            
    except Exception as e:
        print(f"❌ 创建超级管理员失败: {str(e)}")
        return
    
    print("\n🎉 超级管理员账户创建完成！现在可以使用此账户登录系统。")


if __name__ == "__main__":
    asyncio.run(create_superuser()) 