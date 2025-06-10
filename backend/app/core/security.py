"""
安全相关工具模块
提供JWT Token生成验证、密码加密验证等功能
"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    创建访问令牌
    
    Args:
        subject: 令牌主题(通常是用户ID)
        expires_delta: 过期时间增量
        
    Returns:
        编码后的JWT令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    创建刷新令牌
    
    Args:
        subject: 令牌主题(通常是用户ID)
        
    Returns:
        编码后的JWT刷新令牌
    """
    expire = datetime.utcnow() + timedelta(days=7)  # 7天有效期
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
        
    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    获取密码哈希
    
    Args:
        password: 明文密码
        
    Returns:
        哈希后的密码
    """
    return pwd_context.hash(password)


def verify_token(token: str) -> Optional[str]:
    """
    验证令牌并返回用户ID
    
    Args:
        token: JWT令牌
        
    Returns:
        用户ID或None(如果令牌无效)
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            return None
        return user_id
    except JWTError:
        return None


def verify_refresh_token(token: str) -> Optional[str]:
    """
    验证刷新令牌并返回用户ID
    
    Args:
        token: JWT刷新令牌
        
    Returns:
        用户ID或None(如果令牌无效)
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            return None
        return user_id
    except JWTError:
        return None


def decode_token(token: str) -> Optional[dict]:
    """
    解码令牌获取payload
    
    Args:
        token: JWT令牌
        
    Returns:
        令牌payload或None
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None 