# Sprint 1 Day 3-5: 后端核心框架 - 功能文档

## 📋 功能概述

### 开发目标
在已建立的基础框架上，开发完整的用户认证系统、权限管理机制、用户管理API和核心业务模型，为后续的AI优化功能奠定坚实的基础。

### 开发范围
- 用户认证系统 (JWT Token认证)
- 用户注册、登录、注销功能
- 权限管理和访问控制
- 用户管理相关API
- 优化记录数据模型
- 数据库迁移和种子数据
- API中间件和依赖注入
- 安全性增强

---

## 🎯 具体任务分解

### Day 3: 用户认证系统

#### 任务3.1: JWT认证服务
**目标**: 实现完整的JWT Token认证机制
**预期时间**: 3小时

**实现功能**:
- JWT Token生成和验证
- Token刷新机制
- Token黑名单管理
- 密码加密和验证

**文件创建**:
```
app/
├── core/
│   ├── security.py          # 安全相关工具
│   └── auth.py              # 认证服务
├── schemas/
│   ├── user.py              # 用户相关Schema
│   └── auth.py              # 认证相关Schema
└── services/
    └── auth_service.py      # 认证业务逻辑
```

#### 任务3.2: 用户数据模型完善
**目标**: 完善用户相关数据模型
**预期时间**: 2小时

**模型包括**:
- User模型增强 (添加认证相关字段)
- UserProfile模型 (用户配置信息)
- LoginHistory模型 (登录历史记录)

#### 任务3.3: 认证API端点
**目标**: 实现用户认证相关API接口
**预期时间**: 3小时

**API端点**:
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户注销
- `POST /api/v1/auth/refresh` - Token刷新
- `GET /api/v1/auth/me` - 获取当前用户信息

### Day 4: 用户管理和权限控制

#### 任务4.1: 权限管理系统
**目标**: 实现基于角色的权限管理
**预期时间**: 3小时

**权限系统设计**:
- Role模型 (角色管理)
- Permission模型 (权限定义)
- UserRole关联 (用户角色关系)
- 权限装饰器和中间件

#### 任务4.2: 用户管理API
**目标**: 实现用户管理相关接口
**预期时间**: 2小时

**API端点**:
- `GET /api/v1/users/` - 获取用户列表 (管理员)
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户信息
- `DELETE /api/v1/users/{user_id}` - 删除用户 (软删除)
- `PUT /api/v1/users/{user_id}/password` - 修改密码

#### 任务4.3: 中间件和依赖注入
**目标**: 实现认证中间件和依赖注入
**预期时间**: 3小时

**实现内容**:
- 认证中间件 (验证Token)
- 权限检查装饰器
- 依赖注入函数 (获取当前用户)
- 异常处理优化

### Day 5: 业务模型和数据库优化

#### 任务5.1: 核心业务模型
**目标**: 创建提示词优化相关数据模型
**预期时间**: 3小时

**数据模型**:
- Optimization模型 (优化记录)
- PromptTemplate模型 (提示词模板)
- OptimizationHistory模型 (优化历史)
- UserFavorite模型 (用户收藏)

#### 任务5.2: 数据库迁移和种子数据
**目标**: 设置数据库迁移和初始数据
**预期时间**: 2小时

**迁移文件**:
- 用户认证相关表
- 权限管理相关表
- 业务数据相关表
- 索引和约束优化

#### 任务5.3: API性能优化
**目标**: 优化API性能和错误处理
**预期时间**: 3小时

**优化内容**:
- 数据库查询优化
- 响应缓存机制
- 请求验证增强
- 日志系统完善

---

## 🔧 技术实现方案

### 1. JWT认证系统

#### 安全工具模块 (core/security.py)
```python
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """创建访问令牌"""
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
    """创建刷新令牌"""
    expire = datetime.utcnow() + timedelta(days=7)  # 7天有效期
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)

def verify_token(token: str) -> Optional[str]:
    """验证令牌并返回用户ID"""
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
```

#### 认证Schema (schemas/auth.py)
```python
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
    
    class Config:
        from_attributes = True
```

### 2. 权限管理系统

#### 权限模型 (models/auth.py)
```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

# 用户角色关联表
user_role_association = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# 角色权限关联表
role_permission_association = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Role(Base):
    """角色模型"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    users = relationship("User", secondary=user_role_association, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission_association, back_populates="roles")

class Permission(Base):
    """权限模型"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    resource = Column(String(50), nullable=False)  # 资源名称
    action = Column(String(50), nullable=False)    # 操作名称
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    roles = relationship("Role", secondary=role_permission_association, back_populates="permissions")
```

#### 权限装饰器 (core/permissions.py)
```python
from functools import wraps
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.services.auth_service import AuthService

def require_permissions(*required_permissions: str):
    """权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取当前用户和数据库会话
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录"
                )
            
            # 检查权限
            auth_service = AuthService(db)
            user_permissions = await auth_service.get_user_permissions(current_user.id)
            
            for permission in required_permissions:
                if permission not in user_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"缺少权限: {permission}"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_roles(*required_roles: str):
    """角色检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录"
                )
            
            # 检查角色
            auth_service = AuthService(db)
            user_roles = await auth_service.get_user_roles(current_user.id)
            
            for role in required_roles:
                if role not in user_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"缺少角色: {role}"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### 3. 业务数据模型

#### 优化记录模型 (models/optimization.py)
```python
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Optimization(Base):
    """提示词优化记录"""
    __tablename__ = "optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 优化内容
    original_prompt = Column(Text, nullable=False)  # 原始提示词
    optimized_prompt = Column(Text, nullable=False)  # 优化后提示词
    optimization_type = Column(String(50), default="general")  # 优化类型
    
    # 质量评分
    original_score = Column(Float, default=0.0)  # 原始质量分
    optimized_score = Column(Float, default=0.0)  # 优化后质量分
    improvement_score = Column(Float, default=0.0)  # 改进分数
    
    # 优化详情
    optimization_techniques = Column(JSON)  # 使用的优化技巧
    explanation = Column(Text)  # 优化说明
    suggestions = Column(JSON)  # 改进建议
    
    # 元数据
    is_public = Column(Boolean, default=False)  # 是否公开
    is_favorite = Column(Boolean, default=False)  # 用户是否收藏
    tags = Column(JSON)  # 标签
    category = Column(String(50))  # 分类
    
    # AI服务信息
    model_used = Column(String(50))  # 使用的AI模型
    tokens_used = Column(Integer, default=0)  # 消耗的Token数
    processing_time = Column(Float)  # 处理时间(秒)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="optimizations")
    history = relationship("OptimizationHistory", back_populates="optimization", cascade="all, delete-orphan")

class OptimizationHistory(Base):
    """优化历史记录"""
    __tablename__ = "optimization_history"
    
    id = Column(Integer, primary_key=True, index=True)
    optimization_id = Column(Integer, ForeignKey("optimizations.id"), nullable=False, index=True)
    
    # 历史内容
    prompt_version = Column(Text, nullable=False)  # 提示词版本
    score = Column(Float)  # 该版本的分数
    changes_made = Column(JSON)  # 进行的更改
    notes = Column(Text)  # 备注
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    optimization = relationship("Optimization", back_populates="history")

class PromptTemplate(Base):
    """提示词模板"""
    __tablename__ = "prompt_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # NULL表示系统模板
    
    # 模板内容
    title = Column(String(200), nullable=False)
    description = Column(Text)
    template_content = Column(Text, nullable=False)
    variables = Column(JSON)  # 模板变量定义
    
    # 分类和标签
    category = Column(String(50), index=True)
    tags = Column(JSON)
    difficulty_level = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    
    # 统计信息
    usage_count = Column(Integer, default=0)  # 使用次数
    rating = Column(Float, default=0.0)  # 平均评分
    rating_count = Column(Integer, default=0)  # 评分次数
    
    # 状态
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)  # 是否为特色模板
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="prompt_templates")
```

---

## 🧪 测试用例

### 1. 认证系统测试
```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAuth:
    """认证系统测试"""
    
    def test_user_registration(self):
        """测试用户注册"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
            "full_name": "Test User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data  # 不返回密码
    
    def test_user_login(self):
        """测试用户登录"""
        # 先注册用户
        self.test_user_registration()
        
        login_data = {
            "username": "testuser",
            "password": "TestPass123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_protected_route_without_token(self):
        """测试无Token访问受保护路由"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_protected_route_with_token(self):
        """测试带Token访问受保护路由"""
        # 登录获取Token
        login_response = client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "TestPass123"
        })
        token = login_response.json()["access_token"]
        
        # 使用Token访问保护路由
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
```

### 2. 权限系统测试
```python
# tests/test_permissions.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPermissions:
    """权限系统测试"""
    
    def test_admin_access(self):
        """测试管理员权限"""
        # 创建管理员用户和普通用户
        admin_token = self.create_admin_user()
        user_token = self.create_regular_user()
        
        # 管理员访问用户列表
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 200
        
        # 普通用户访问用户列表应该被拒绝
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 403
    
    def test_user_can_access_own_data(self):
        """测试用户可以访问自己的数据"""
        token = self.create_regular_user()
        user_id = self.get_user_id_from_token(token)
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(f"/api/v1/users/{user_id}", headers=headers)
        assert response.status_code == 200
    
    def test_user_cannot_access_others_data(self):
        """测试用户不能访问他人数据"""
        token1 = self.create_regular_user("user1", "user1@test.com")
        token2 = self.create_regular_user("user2", "user2@test.com")
        user2_id = self.get_user_id_from_token(token2)
        
        # 用户1尝试访问用户2的数据
        headers = {"Authorization": f"Bearer {token1}"}
        response = client.get(f"/api/v1/users/{user2_id}", headers=headers)
        assert response.status_code == 403
```

### 3. 业务模型测试
```python
# tests/test_optimization_models.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.optimization import Optimization, PromptTemplate
from app.models.user import User

@pytest.mark.asyncio
async def test_optimization_creation(db_session: AsyncSession):
    """测试优化记录创建"""
    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    db_session.add(user)
    await db_session.commit()
    
    # 创建优化记录
    optimization = Optimization(
        user_id=user.id,
        original_prompt="写一个函数",
        optimized_prompt="请帮我用Python编写一个函数，该函数能够...",
        optimization_type="clarity",
        original_score=3.2,
        optimized_score=8.7,
        improvement_score=5.5,
        optimization_techniques=["添加上下文", "明确需求", "指定输出格式"],
        explanation="通过添加具体上下文和明确需求描述，大幅提升了提示词的清晰度和可操作性。"
    )
    
    db_session.add(optimization)
    await db_session.commit()
    
    assert optimization.id is not None
    assert optimization.user_id == user.id
    assert optimization.improvement_score == 5.5

@pytest.mark.asyncio
async def test_prompt_template_creation(db_session: AsyncSession):
    """测试提示词模板创建"""
    template = PromptTemplate(
        title="代码评审模板",
        description="用于代码评审的标准化提示词模板",
        template_content="请对以下{language}代码进行评审，重点关注{focus_areas}...",
        variables={
            "language": {"type": "string", "description": "编程语言"},
            "focus_areas": {"type": "array", "description": "关注领域"}
        },
        category="code_review",
        tags=["代码", "评审", "质量"],
        difficulty_level="intermediate"
    )
    
    db_session.add(template)
    await db_session.commit()
    
    assert template.id is not None
    assert template.category == "code_review"
    assert len(template.tags) == 3
```

---

## ✅ 验收标准

### Day 3 完成标准
- [ ] JWT认证系统实现完成，包括Token生成、验证、刷新
- [ ] 用户注册、登录、注销API正常工作
- [ ] 密码加密存储，验证机制正确
- [ ] 认证相关的异常处理完善
- [ ] 认证系统单元测试通过率100%

### Day 4 完成标准
- [ ] 权限管理系统实现完成，支持角色和权限管理
- [ ] 用户管理API全部实现并测试通过
- [ ] 权限装饰器和中间件正常工作
- [ ] 管理员和普通用户权限区分明确
- [ ] 依赖注入系统完善，支持当前用户获取

### Day 5 完成标准
- [ ] 核心业务数据模型创建完成
- [ ] 数据库迁移脚本正确执行
- [ ] 种子数据插入成功，包括默认角色和权限
- [ ] API性能优化完成，响应时间满足要求
- [ ] 日志系统完善，关键操作可追踪

### 整体验收标准
- [ ] 用户可以成功注册、登录，获取有效Token
- [ ] 受保护的API需要有效Token才能访问
- [ ] 不同角色用户的权限控制正确
- [ ] 数据库表结构完整，关系正确
- [ ] 所有API端点文档生成正确
- [ ] 单元测试覆盖率达到90%以上
- [ ] 集成测试验证主要业务流程
- [ ] API响应时间在可接受范围内 (< 200ms)

---

## 🚀 启动和测试命令

### 数据库迁移
```bash
# 进入后端目录
cd backend

# 激活环境
conda activate fastapi

# 创建迁移文件
alembic revision --autogenerate -m "Add authentication and user management"

# 执行迁移
alembic upgrade head

# 插入种子数据 (可选)
python scripts/seed_data.py
```

### 开发环境启动
```bash
# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 查看API文档
# http://localhost:8000/docs
```

### 测试执行
```bash
# 运行所有测试
pytest tests/ -v

# 运行认证相关测试
pytest tests/test_auth.py -v

# 运行权限相关测试
pytest tests/test_permissions.py -v

# 测试覆盖率
pytest tests/ --cov=app --cov-report=html
```

### API测试示例
```bash
# 用户注册
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"TestPass123","full_name":"Test User"}'

# 用户登录
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"TestPass123"}'

# 获取当前用户信息 (需要Token)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📋 注意事项

### 安全考虑
1. **密码安全**: 使用bcrypt进行密码哈希，不存储明文密码
2. **Token安全**: JWT Token包含过期时间，刷新Token机制防止长期有效
3. **权限验证**: 每个需要权限的API都要进行严格的权限检查
4. **输入验证**: 所有用户输入都要进行验证和清理
5. **错误信息**: 避免泄露敏感信息，错误消息要适当

### 性能考虑
1. **数据库索引**: 为常用查询字段添加索引
2. **查询优化**: 避免N+1查询问题，使用join或批量查询
3. **缓存策略**: 对用户权限信息进行适当缓存
4. **连接池**: 合理配置数据库连接池大小

### 开发规范
1. **类型注解**: 所有函数都要有完整的类型注解
2. **文档字符串**: 重要函数和类要有清晰的文档说明
3. **异常处理**: 合理处理各种异常情况
4. **日志记录**: 记录关键操作和错误信息
5. **测试覆盖**: 确保关键功能有充分的测试覆盖

---

## 📊 预期产出

### 新增文件
- 认证相关: 8个文件 (core/security.py, services/auth_service.py等)
- 权限管理: 6个文件 (models/auth.py, core/permissions.py等)
- 业务模型: 4个文件 (models/optimization.py等)
- API接口: 5个文件 (api/v1/endpoints/auth.py等)
- 测试文件: 6个文件 (test_auth.py, test_permissions.py等)
- 数据库迁移: 3个文件 (alembic迁移脚本)

### 代码量预估
- 核心功能代码: 约1500行
- 测试代码: 约800行
- 配置和工具: 约300行
- 总计: 约2600行代码

### API端点
- 认证相关: 5个端点
- 用户管理: 5个端点
- 系统功能: 3个端点
- 总计: 13个新API端点

**文档创建时间**: 2024年12月
**预计开发时间**: 3天 (24工时)
**开发优先级**: P0 (最高优先级)

> 此功能文档将指导Sprint 1后3天的开发工作，确保用户认证和权限管理系统的高质量实现。 