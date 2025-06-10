#!/usr/bin/env python3
"""
创建密码已知的测试用户
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import async_session_maker
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select


async def create_known_user():
    """创建密码已知的测试用户"""
    async with async_session_maker() as session:
        try:
            # 检查是否已存在testuser
            result = await session.execute(
                select(User).where(User.username == "testuser")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("✅ testuser 用户已存在")
                print("=" * 50)
                print("🔑 测试账号信息:")
                print(f"用户名: testuser")
                print(f"邮箱: test@example.com") 
                print(f"密码: 123456")
                print("=" * 50)
                return
            
            # 创建新的测试用户
            test_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=get_password_hash("123456"),
                is_active=True,
                is_superuser=False,
                full_name="测试用户"
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print("🎉 测试用户创建成功!")
            print("=" * 50)
            print("🔑 测试账号信息:")
            print(f"用户名: testuser")
            print(f"邮箱: test@example.com") 
            print(f"密码: 123456")
            print("=" * 50)
            print("请使用以上信息登录系统！")
            
        except Exception as e:
            print(f"❌ 创建测试用户失败: {e}")
            await session.rollback()


async def check_admin_user():
    """检查admin用户并重置密码"""
    async with async_session_maker() as session:
        try:
            # 查找admin用户
            result = await session.execute(
                select(User).where(User.username == "admin")
            )
            admin_user = result.scalar_one_or_none()
            
            if admin_user:
                # 重置admin密码为123456
                admin_user.hashed_password = get_password_hash("123456")
                await session.commit()
                
                print("🔧 admin用户密码已重置!")
                print("=" * 50)
                print("🔑 Admin账号信息:")
                print(f"用户名: admin")
                print(f"邮箱: {admin_user.email}") 
                print(f"密码: 123456")
                print("=" * 50)
            else:
                print("❌ 未找到admin用户")
                
        except Exception as e:
            print(f"❌ 重置admin密码失败: {e}")
            await session.rollback()


async def main():
    """主函数"""
    print("🚀 开始创建/重置测试账号...")
    print()
    
    # 重置admin密码
    await check_admin_user()
    print()
    
    # 创建testuser
    await create_known_user()
    print()
    
    print("✅ 所有操作完成！")
    print("您现在可以使用以下任一账号登录：")
    print("1. admin / 123456")
    print("2. testuser / 123456")


if __name__ == "__main__":
    asyncio.run(main()) 