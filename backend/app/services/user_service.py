from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.user import User, LoginHistory
from app.schemas.auth import UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        is_active: Optional[bool] = None
    ) -> List[User]:
        """获取用户列表"""
        query = select(User)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        # 获取当前用户
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        # 更新字段
        update_data = user_update.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(**update_data)
                .returning(User)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.scalar_one()
        
        return user
    
    async def update_user_status(self, user_id: int, is_active: bool) -> Optional[User]:
        """更新用户状态"""
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=is_active, updated_at=datetime.utcnow())
            .returning(User)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        return result.scalar_one()
    
    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        await self.db.delete(user)
        await self.db.commit()
        return True
    
    async def get_login_history(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[LoginHistory]:
        """获取用户登录历史"""
        query = (
            select(LoginHistory)
            .where(LoginHistory.user_id == user_id)
            .order_by(LoginHistory.login_time.desc())
            .offset(skip)
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_user_count(self, is_active: Optional[bool] = None) -> int:
        """获取用户总数"""
        from sqlalchemy import func
        
        query = select(func.count(User.id))
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        result = await self.db.execute(query)
        return result.scalar()
    
    async def get_active_users_today(self) -> int:
        """获取今日活跃用户数"""
        from sqlalchemy import func, and_
        
        today = datetime.utcnow().date()
        query = (
            select(func.count(func.distinct(LoginHistory.user_id)))
            .where(
                and_(
                    func.date(LoginHistory.login_time) == today,
                    LoginHistory.success == True
                )
            )
        )
        
        result = await self.db.execute(query)
        return result.scalar() or 0 