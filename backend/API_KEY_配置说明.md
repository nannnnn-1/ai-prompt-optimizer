# 硅基流动API Key配置说明

## 配置步骤

### 1. 创建环境变量文件
在 `backend` 目录下创建 `.env` 文件：

```bash
# 在backend目录下执行
touch .env
```

### 2. 设置API Key
在 `.env` 文件中添加以下内容：

```env
# 硅基流动API Key (请替换为您的真实API Key)
OPENAI_API_KEY=sk-your-siliconflow-api-key-here

# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./app.db
DATABASE_URL_SYNC=sqlite:///./app.db

# 应用配置
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production

# JWT配置  
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 日志配置
LOG_LEVEL=INFO
```

### 3. 验证配置
配置完成后，系统将：
- 自动使用硅基流动的API端点：`https://api.siliconflow.cn/v1`
- 使用qwen模型：`Qwen/Qwen2.5-7B-Instruct`
- 支持真实的AI提示词优化功能

### 4. 测试连接
启动服务后访问健康检查接口：
```bash
curl http://localhost:8000/api/v1/optimizer/health
```

正常情况下应该返回：
```json
{
  "status": "healthy",
  "model": "Qwen/Qwen2.5-7B-Instruct",
  "api_available": true
}
```

## 支持的qwen模型

当前配置支持以下qwen模型（在config.py中可修改）：
- `Qwen/Qwen2.5-7B-Instruct` （默认）
- `Qwen/Qwen2.5-14B-Instruct`
- `Qwen/Qwen2.5-32B-Instruct`
- `Qwen/Qwen2.5-72B-Instruct`

## 注意事项

1. **API Key安全**：请妥善保管您的API Key，不要提交到版本控制系统
2. **模型选择**：建议使用7B或14B模型，性能和成本平衡较好
3. **费用控制**：硅基流动按token计费，建议监控使用量
4. **模型切换**：如需切换模型，修改 `config.py` 中的 `OPENAI_MODEL` 值 