"""
认证相关的Pydantic Schema
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """用户注册Schema"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), '用户名只能包含字母和数字'
        assert len(v) >= 3, '用户名至少3个字符'
        return v
    
    @validator('password')
    def password_validation(cls, v):
        assert len(v) >= 8, '密码至少8个字符'
        assert any(c.isupper() for c in v), '密码必须包含大写字母'
        assert any(c.islower() for c in v), '密码必须包含小写字母'
        assert any(c.isdigit() for c in v), '密码必须包含数字'
        return v


class UserLogin(BaseModel):
    """用户登录Schema"""
    username: str
    password: str


class Token(BaseModel):
    """Token响应Schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    """Token刷新Schema"""
    refresh_token: str


class UserResponse(BaseModel):
    """用户响应Schema"""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """用户更新Schema"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserCreate(BaseModel):
    """管理员创建用户Schema"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), '用户名只能包含字母和数字'
        assert len(v) >= 3, '用户名至少3个字符'
        return v
    
    @validator('password')
    def password_validation(cls, v):
        assert len(v) >= 8, '密码至少8个字符'
        assert any(c.isupper() for c in v), '密码必须包含大写字母'
        assert any(c.islower() for c in v), '密码必须包含小写字母'
        assert any(c.isdigit() for c in v), '密码必须包含数字'
        return v


class PasswordUpdate(BaseModel):
    """密码更新Schema"""
    current_password: str
    new_password: str
    
    @validator('new_password')
    def password_validation(cls, v):
        assert len(v) >= 8, '密码至少8个字符'
        assert any(c.isupper() for c in v), '密码必须包含大写字母'
        assert any(c.islower() for c in v), '密码必须包含小写字母'
        assert any(c.isdigit() for c in v), '密码必须包含数字'
        return v


class UserListResponse(BaseModel):
    """用户列表响应Schema"""
    users: list[UserResponse]
    total: int
    page: int
    page_size: int
    
    
class LoginHistory(BaseModel):
    """登录历史Schema"""
    id: int
    user_id: int
    login_time: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool
    
    class Config:
        from_attributes = True 