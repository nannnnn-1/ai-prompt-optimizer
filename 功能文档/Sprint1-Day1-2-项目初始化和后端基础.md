# Sprint 1 Day 1-2: 项目初始化和后端基础

## 📋 功能概述

### 开发目标
完成项目的基础设施搭建，包括后端FastAPI项目初始化、开发环境配置、代码质量工具设置，以及核心数据模型的创建。

### 开发范围
- 后端项目结构搭建
- 开发环境配置
- 代码质量工具配置
- 数据库连接设置
- 基础数据模型创建
- 基础API路由框架

---

## 🎯 具体任务分解

### Day 1: 环境搭建和项目初始化

#### 任务1.1: 后端项目结构创建
**目标**: 创建标准的FastAPI项目结构
**预期时间**: 2小时

**文件结构**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── dependencies.py      # 依赖注入
│   │
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py
│   │
│   ├── core/               # 核心业务逻辑
│   │   └── __init__.py
│   │
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   └── base.py
│   │
│   ├── schemas/            # Pydantic模式
│   │   ├── __init__.py
│   │   └── common.py
│   │
│   ├── services/           # 业务服务层
│   │   └── __init__.py
│   │
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── exceptions.py
│
├── tests/                  # 测试代码
│   ├── __init__.py
│   └── conftest.py
│
├── requirements.txt        # 依赖列表
├── pyproject.toml         # 项目配置
├── .env.example           # 环境变量示例
├── .gitignore             # Git忽略文件
└── README.md              # 项目说明
```

#### 任务1.2: 依赖包管理
**目标**: 配置Python依赖和虚拟环境
**预期时间**: 1小时

**核心依赖**:
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
alembic==1.13.0
asyncpg==0.29.0
aiosqlite==0.19.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.25.0

# 开发依赖
pytest==7.4.0
pytest-asyncio==0.21.0
black==23.0.0
isort==5.12.0
flake8==6.0.0
mypy==1.7.0
pre-commit==3.5.0
```

#### 任务1.3: 开发工具配置
**目标**: 配置代码质量和开发工具
**预期时间**: 1小时

**配置文件**:
- `.pre-commit-config.yaml`: Git hooks配置
- `pyproject.toml`: Python项目配置
- `.flake8`: 代码检查配置
- `mypy.ini`: 类型检查配置

### Day 2: 基础框架搭建

#### 任务2.1: FastAPI应用初始化
**目标**: 创建基础的FastAPI应用
**预期时间**: 2小时

**核心文件**:
- `app/main.py`: 应用入口点
- `app/config.py`: 配置管理
- `app/dependencies.py`: 依赖注入

#### 任务2.2: 数据库连接配置
**目标**: 设置SQLAlchemy异步数据库连接
**预期时间**: 2小时

**功能包括**:
- 异步数据库引擎配置
- 会话管理
- 连接池设置
- 环境变量配置

#### 任务2.3: 基础模型创建
**目标**: 创建核心数据模型
**预期时间**: 2小时

**模型包括**:
- Base基础模型
- User用户模型
- Optimization优化记录模型

---

## 🔧 技术实现方案

### 1. FastAPI应用配置

#### 主应用文件 (main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.config import settings

app = FastAPI(
    title="AI Prompt Optimizer API",
    description="AI提示词优化器后端API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Prompt Optimizer API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### 配置管理 (config.py)
```python
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # 应用配置
    DEBUG: bool = False
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    DATABASE_URL_SYNC: str = "sqlite:///./app.db"
    
    # AI服务配置
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 2. 数据库配置

#### 数据库连接 (database.py)
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# 创建会话工厂
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 基础模型类
class Base(DeclarativeBase):
    pass

# 获取数据库会话
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 3. 基础数据模型

#### 基础模型 (models/base.py)
```python
from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime

class TimestampMixin:
    """时间戳混入类"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

class BaseModel(Base, TimestampMixin):
    """基础模型类"""
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
```

#### 用户模型 (models/user.py)
```python
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from typing import List

class User(BaseModel):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 关系
    optimizations: Mapped[List["Optimization"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
```

### 4. API路由框架

#### 主路由 (api/v1/router.py)
```python
from fastapi import APIRouter
from app.api.v1.endpoints import auth, optimizer, health

api_router = APIRouter()

# 健康检查
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

# 认证相关
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# 优化相关
api_router.include_router(
    optimizer.router,
    prefix="/optimizer",
    tags=["optimizer"]
)
```

---

## 🧪 测试用例

### 1. 应用启动测试
```python
def test_app_startup():
    """测试应用能否正常启动"""
    from app.main import app
    assert app is not None
    assert app.title == "AI Prompt Optimizer API"

def test_health_endpoint():
    """测试健康检查接口"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

### 2. 数据库连接测试
```python
import pytest
from app.database import get_async_session

@pytest.mark.asyncio
async def test_database_connection():
    """测试数据库连接"""
    async for session in get_async_session():
        assert session is not None
        # 执行简单查询
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1
```

### 3. 模型创建测试
```python
@pytest.mark.asyncio
async def test_user_model_creation():
    """测试用户模型创建"""
    from app.models.user import User
    
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword"
    )
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True
```

---

## ✅ 验收标准

### Day 1 完成标准
- [ ] 后端项目目录结构创建完成
- [ ] Python虚拟环境配置成功
- [ ] 所有依赖包安装完成
- [ ] 代码质量工具配置完成
- [ ] Pre-commit hooks设置成功

### Day 2 完成标准
- [ ] FastAPI应用可以正常启动
- [ ] 健康检查接口返回正确响应
- [ ] 数据库连接配置成功
- [ ] 基础数据模型创建完成
- [ ] 基础API路由结构搭建完成

### 整体验收标准
- [ ] 后端服务能够在开发环境正常运行
- [ ] 访问 http://localhost:8000/docs 可以看到API文档
- [ ] 访问 http://localhost:8000/health 返回健康状态
- [ ] 数据库表结构创建成功
- [ ] 所有单元测试通过
- [ ] 代码格式化和检查通过

---

## 🚀 启动命令

### 开发环境启动
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate
# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 数据库初始化
```bash
# 创建迁移文件
alembic init migrations

# 生成初始迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 代码质量检查
```bash
# 代码格式化
black app tests

# 导入排序
isort app tests

# 代码检查
flake8 app tests

# 类型检查
mypy app

# 运行测试
pytest
```

---

## 📋 注意事项

### 环境要求
- Python 3.11+
- SQLite (开发环境)
- Redis (可选，用于缓存)

### 开发注意事项
1. 所有异步函数都要使用 `async/await`
2. 数据库操作必须使用异步会话
3. 配置信息通过环境变量管理
4. 遵循PEP 8代码规范
5. 所有公共函数都要有类型注解

### 安全考虑
1. 敏感配置不要硬编码
2. 数据库连接使用连接池
3. API接口要有适当的错误处理
4. 日志中不要包含敏感信息

---

## 📊 预期产出

### 代码文件
- 完整的后端项目结构 (约20个文件)
- 基础的FastAPI应用 (可运行)
- 数据库模型定义 (User, Optimization基础结构)
- API路由框架 (健康检查接口)

### 配置文件
- requirements.txt (依赖管理)
- pyproject.toml (项目配置)
- .env.example (环境变量模板)
- 代码质量工具配置文件

### 测试文件
- 基础测试框架
- 关键功能的单元测试
- 测试配置文件

**预计代码行数**: 约500-800行
**预计文件数量**: 约25-30个文件

---

**文档创建时间**: 2024年12月
**预计开发时间**: 2天 (16工时)
**开发优先级**: P0 (最高优先级)

> 此功能文档将指导Sprint 1前两天的开发工作，确保后端基础框架的高质量搭建。 