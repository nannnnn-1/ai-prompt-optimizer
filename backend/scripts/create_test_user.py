#!/usr/bin/env python3
"""
创建测试用户脚本
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_async_session
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select


async def create_test_user():
    """创建测试用户"""
    from app.database import async_session_maker
    async with async_session_maker() as session:
        try:
            # 检查是否已存在测试用户
            result = await session.execute(
                select(User).where(User.username == "admin")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("✅ 测试用户已存在:")
                print(f"   用户名: {existing_user.username}")
                print(f"   邮箱: {existing_user.email}")
                print("   密码: admin123")
                return
            
            # 创建测试用户
            test_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print("🎉 测试用户创建成功!")
            print("=" * 40)
            print("测试账号信息:")
            print(f"用户名: admin")
            print(f"邮箱: admin@example.com") 
            print(f"密码: admin123")
            print("=" * 40)
            
        except Exception as e:
            print(f"❌ 创建测试用户失败: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(create_test_user()) 