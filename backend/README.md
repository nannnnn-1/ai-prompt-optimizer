# AI提示词优化器 - 后端服务

基于FastAPI构建的AI提示词优化器后端API服务。

## 🚀 快速开始

### 环境要求

- Python 3.11+
- SQLite (开发环境)
- Redis (可选，用于缓存)

### 安装和运行

1. **创建虚拟环境**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 复制环境变量模板
cp env.example .env

# 编辑.env文件，设置必要的配置
```

4. **运行服务**
```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者直接运行
python -m app.main
```

5. **访问服务**
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health
- 根路径: http://localhost:8000/

## 📋 API接口

### 基础接口

- `GET /` - 根路径欢迎信息
- `GET /health` - 简单健康检查
- `GET /api/v1/health/` - 详细健康检查
- `GET /api/v1/health/db` - 数据库健康检查
- `GET /api/v1/health/detailed` - 完整系统状态检查

### 即将推出的接口

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/optimizer/optimize` - 提示词优化
- `GET /api/v1/optimizer/history` - 优化历史

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_main.py

# 显示测试覆盖率
pytest --cov=app tests/

# 运行测试并生成详细报告
pytest -v --tb=short
```

## 🏗 项目结构

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
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── health.py
│   │
│   ├── core/               # 核心业务逻辑
│   │   └── __init__.py
│   │
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
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
│   ├── conftest.py
│   └── test_main.py
│
├── requirements.txt        # 依赖列表
├── pyproject.toml         # 项目配置
├── env.example            # 环境变量示例
├── .gitignore             # Git忽略文件
└── README.md              # 项目说明
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEBUG` | 调试模式 | `True` |
| `SECRET_KEY` | 密钥 | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | 数据库连接URL | `sqlite+aiosqlite:///./app.db` |
| `OPENAI_API_KEY` | OpenAI API密钥 | `None` |
| `OPENAI_MODEL` | OpenAI模型 | `gpt-3.5-turbo` |

### 数据库配置

默认使用SQLite数据库，文件位于项目根目录的`app.db`。生产环境建议使用PostgreSQL。

## 🔧 开发指南

### 代码质量

项目使用以下工具确保代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查

```bash
# 运行代码格式化
black app tests

# 排序导入
isort app tests

# 代码检查
flake8 app tests

# 类型检查
mypy app
```

### 添加新的API端点

1. 在`app/api/v1/endpoints/`中创建新的端点文件
2. 在`app/api/v1/router.py`中注册新的路由
3. 编写相应的测试文件

### 数据库迁移

```bash
# 初始化Alembic (仅首次)
alembic init migrations

# 生成迁移文件
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head
```

## 📊 监控和日志

### 健康检查端点

- `/health` - 基础健康检查
- `/api/v1/health/db` - 数据库连接检查
- `/api/v1/health/detailed` - 详细系统状态

### 日志配置

日志级别通过`LOG_LEVEL`环境变量控制，支持：`DEBUG`, `INFO`, `WARNING`, `ERROR`

## 🚀 部署

### Docker部署

```bash
# 构建镜像
docker build -t ai-prompt-optimizer-backend .

# 运行容器
docker run -p 8000:8000 ai-prompt-optimizer-backend
```

### 生产环境注意事项

1. 设置强密码作为`SECRET_KEY`
2. 使用PostgreSQL作为生产数据库
3. 设置`DEBUG=False`
4. 配置反向代理(Nginx)
5. 设置HTTPS

## 📝 更新日志

### v1.0.0 (当前版本)
- ✅ 基础FastAPI框架搭建
- ✅ 数据库连接和模型定义
- ✅ 健康检查API
- ✅ 基础测试框架
- ✅ 代码质量工具配置

### 即将推出
- 🔄 用户认证系统
- 🔄 提示词优化核心功能
- 🔄 AI服务集成
- 🔄 缓存系统

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

---

**开发团队**: AI Prompt Optimizer Team  
**创建时间**: 2024年12月  
**版本**: v1.0.0 