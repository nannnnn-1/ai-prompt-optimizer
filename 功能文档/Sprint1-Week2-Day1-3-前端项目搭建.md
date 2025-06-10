# AI提示词优化器 - 前端项目搭建功能文档

## Week 2 Day 1-3: 前端项目搭建

### 📋 阶段目标

构建现代化、响应式的前端应用，实现与后端API的无缝集成，为用户提供直观、高效的AI提示词优化体验。

---

## 🎯 核心功能需求

### 1. 项目基础架构

#### 1.1 技术栈选择
- **前端框架**: React 18 + TypeScript
- **构建工具**: Vite (快速开发，热重载)
- **状态管理**: Zustand (轻量级状态管理)
- **路由管理**: React Router v6
- **UI组件库**: Ant Design 5.x (企业级UI设计语言)
- **样式方案**: Tailwind CSS + CSS Modules
- **HTTP客户端**: Axios (API请求)
- **表单处理**: React Hook Form + Zod (表单验证)
- **代码规范**: ESLint + Prettier + Husky

#### 1.2 项目结构设计
```
frontend/
├── public/                    # 静态资源
├── src/
│   ├── components/           # 通用组件
│   │   ├── common/          # 基础组件
│   │   ├── layout/          # 布局组件
│   │   └── ui/              # UI组件
│   ├── pages/               # 页面组件
│   │   ├── auth/           # 认证相关页面
│   │   ├── dashboard/      # 仪表板
│   │   ├── optimizer/      # 优化器页面
│   │   └── profile/        # 用户资料
│   ├── hooks/              # 自定义Hooks
│   ├── services/           # API服务层
│   ├── store/              # 状态管理
│   ├── types/              # TypeScript类型定义
│   ├── utils/              # 工具函数
│   ├── constants/          # 常量定义
│   └── styles/             # 全局样式
├── tests/                   # 测试文件
├── docs/                   # 文档
└── package.json            # 项目配置
```

### 2. 核心页面和组件

#### 2.1 认证系统界面
- **登录页面** (`/login`)
  - 用户名/密码登录表单
  - 记住登录状态
  - 忘记密码链接
  - 注册页面跳转
  
- **注册页面** (`/register`)
  - 用户名、邮箱、密码注册表单
  - 实时表单验证
  - 用户协议确认
  - 登录页面跳转

- **用户资料页面** (`/profile`)
  - 个人信息管理
  - 密码修改
  - 偏好设置
  - 账户安全

#### 2.2 主要功能界面
- **仪表板** (`/dashboard`)
  - 用户统计概览
  - 最近优化历史
  - 快速操作入口
  - 系统通知

- **提示词优化器** (`/optimizer`)
  - 输入区域 (原始提示词)
  - 优化参数配置
  - 实时优化结果展示
  - 优化建议和解释
  - 保存/分享功能

- **历史记录** (`/history`)
  - 优化历史列表
  - 搜索和筛选
  - 批量操作
  - 导出功能

#### 2.3 通用组件
- **布局组件**
  - 顶部导航栏
  - 侧边栏菜单
  - 面包屑导航
  - 页脚信息

- **业务组件**
  - 用户头像和下拉菜单
  - 搜索框组件
  - 数据表格
  - 分页组件
  - 加载状态
  - 错误边界

### 3. 响应式设计规范

#### 3.1 断点设计
- **移动端**: < 768px
- **平板端**: 768px - 1024px  
- **桌面端**: > 1024px
- **大屏端**: > 1440px

#### 3.2 适配策略
- 移动优先的响应式设计
- Flexbox + CSS Grid布局
- 可折叠的侧边栏
- 自适应的表格和卡片
- 触摸友好的交互元素

---

## 🛠 技术实现方案

### 1. 开发环境配置

#### 1.1 项目初始化
```bash
# 使用Vite创建React+TypeScript项目
npm create vite@latest ai-prompt-optimizer-frontend -- --template react-ts

# 进入项目目录
cd ai-prompt-optimizer-frontend

# 安装依赖
npm install

# 安装核心依赖包
npm install antd @ant-design/icons
npm install zustand
npm install react-router-dom
npm install axios
npm install react-hook-form @hookform/resolvers zod
npm install tailwindcss postcss autoprefixer
npm install @types/node

# 安装开发依赖
npm install -D eslint prettier husky lint-staged
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser
npm install -D @vitejs/plugin-react
```

#### 1.2 配置文件设置
- **Vite配置** (`vite.config.ts`)
- **TypeScript配置** (`tsconfig.json`)
- **Tailwind配置** (`tailwind.config.js`)
- **ESLint配置** (`.eslintrc.js`)
- **Prettier配置** (`.prettierrc`)
- **环境变量** (`.env.development`, `.env.production`)

### 2. 核心功能模块

#### 2.1 API服务层
```typescript
// services/api.ts - API客户端配置
// services/auth.ts - 认证相关API
// services/user.ts - 用户管理API
// services/optimizer.ts - 优化器API
```

#### 2.2 状态管理设计
```typescript
// store/authStore.ts - 认证状态
interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
}

// store/optimizerStore.ts - 优化器状态
interface OptimizerState {
  currentPrompt: string
  optimizedPrompt: string
  isOptimizing: boolean
  history: OptimizationRecord[]
  optimize: (prompt: string, options: OptimizeOptions) => Promise<void>
}
```

#### 2.3 路由配置
```typescript
// App.tsx - 主路由配置
const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { path: "/", element: <Dashboard /> },
      { path: "/optimizer", element: <Optimizer /> },
      { path: "/history", element: <History /> },
      { path: "/profile", element: <Profile /> },
    ],
  },
  {
    path: "/auth",
    children: [
      { path: "/auth/login", element: <Login /> },
      { path: "/auth/register", element: <Register /> },
    ],
  },
])
```

### 3. UI/UX设计规范

#### 3.1 设计系统
- **主色调**: #1890ff (Ant Design蓝)
- **辅助色**: #52c41a (成功绿), #faad14 (警告黄), #ff4d4f (错误红)
- **中性色**: #f0f2f5 (背景灰), #001529 (深色)
- **字体**: -apple-system, BlinkMacSystemFont, 'Segoe UI'
- **圆角**: 6px (常规), 8px (卡片), 4px (按钮)
- **阴影**: 0 2px 8px rgba(0,0,0,0.15)

#### 3.2 组件规范
- **按钮**: 统一高度32px，主要/次要/危险类型
- **输入框**: 统一高度32px，聚焦状态蓝色边框
- **卡片**: 白色背景，圆角8px，subtle阴影
- **表格**: 斑马纹，悬停效果，排序图标
- **表单**: 垂直布局，标签在上，验证提示

---

## 📱 页面详细设计

### 1. 登录页面 (`/auth/login`)

#### 1.1 页面布局
```
┌─────────────────────────────────┐
│        Logo + 标题              │
│                                 │
│    ┌─────────────────────┐      │
│    │   用户名输入框      │      │
│    ├─────────────────────┤      │
│    │   密码输入框        │      │
│    ├─────────────────────┤      │
│    │ □ 记住我  忘记密码? │      │
│    ├─────────────────────┤      │
│    │     登录按钮        │      │
│    └─────────────────────┘      │
│                                 │
│      还没有账户？去注册         │
└─────────────────────────────────┘
```

#### 1.2 功能特性
- 表单验证（必填项、格式检查）
- 登录状态记住功能
- 错误信息显示
- 加载状态指示
- 自动跳转到目标页面

### 2. 提示词优化器页面 (`/optimizer`)

#### 2.1 页面布局
```
┌─────────────────────────────────────────────────────┐
│  导航栏                                             │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────────────────┐│
│ │                 │  │                             ││
│ │   原始提示词    │  │       优化结果             ││
│ │   输入区域      │  │       显示区域             ││
│ │                 │  │                             ││
│ │                 │  │                             ││
│ └─────────────────┘  └─────────────────────────────┘│
│ ┌─────────────────┐  ┌─────────────────────────────┐│
│ │   优化参数      │  │      优化建议和解释        ││
│ │   配置面板      │  │      详细说明              ││
│ └─────────────────┘  └─────────────────────────────┘│
│              [保存] [分享] [重新优化]               │
└─────────────────────────────────────────────────────┘
```

#### 2.2 功能特性
- 多行文本输入，支持markdown
- 实时字符计数
- 优化参数可视化配置
- 优化过程动画反馈
- 结果对比显示
- 一键复制功能
- 历史记录保存

### 3. 仪表板页面 (`/dashboard`)

#### 3.1 页面布局
```
┌─────────────────────────────────────────────────────┐
│  欢迎消息 + 用户信息                                │
├─────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│ │ 总优化  │ │ 本月优化│ │ 成功率  │ │ 用户等级│    │
│ │ 次数    │ │ 次数    │ │         │ │         │    │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘    │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────────────────┐│
│ │   最近优化历史  │  │       快速操作             ││
│ │   (列表)        │  │   ┌───────────────────┐   ││
│ │                 │  │   │   开始新的优化    │   ││
│ │                 │  │   ├───────────────────┤   ││
│ │                 │  │   │   查看所有历史    │   ││
│ │                 │  │   ├───────────────────┤   ││
│ │                 │  │   │   案例库管理      │   ││
│ └─────────────────┘  │   └───────────────────┘   ││
│                      └─────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

#### 3.2 功能特性
- 数据统计可视化
- 最近活动时间线
- 快速操作入口
- 个性化推荐
- 系统公告展示

---

## 🔧 开发计划

### Day 1: 项目基础搭建
#### 上午 (4小时)
- [ ] 创建Vite + React + TypeScript项目
- [ ] 配置开发环境 (ESLint, Prettier, Husky)
- [ ] 设置Tailwind CSS + Ant Design
- [ ] 创建基础项目结构和文件夹

#### 下午 (4小时)
- [ ] 配置路由系统 (React Router)
- [ ] 创建基础布局组件 (Header, Sidebar, Footer)
- [ ] 设置API服务层基础架构
- [ ] 配置状态管理 (Zustand store)

### Day 2: 认证系统界面
#### 上午 (4小时)
- [ ] 开发登录页面组件
- [ ] 实现表单验证和提交逻辑
- [ ] 集成后端认证API
- [ ] 处理认证状态管理

#### 下午 (4小时)
- [ ] 开发注册页面组件
- [ ] 实现用户资料页面
- [ ] 添加路由守卫和权限控制
- [ ] 测试认证流程完整性

### Day 3: 主要功能界面
#### 上午 (4小时)
- [ ] 开发仪表板页面
- [ ] 实现数据统计展示
- [ ] 创建优化器页面基础布局
- [ ] 设计优化器输入组件

#### 下午 (4小时)
- [ ] 完善优化器界面细节
- [ ] 添加响应式设计
- [ ] 创建历史记录页面
- [ ] 进行整体测试和优化

---

## 📋 验收标准

### 功能性需求
- [x] 项目可以正常启动和热重载
- [x] 认证系统完整可用 (登录/注册/登出)
- [x] 主要页面基础布局完成
- [x] 与后端API成功集成
- [x] 路由和导航正常工作
- [x] 响应式设计在不同设备上正常

### 技术性需求
- [x] TypeScript类型检查无错误
- [x] ESLint代码规范检查通过
- [x] 构建过程无警告和错误
- [x] 组件结构清晰，可维护性好
- [x] 状态管理方案合理有效

### 用户体验需求
- [x] 界面美观，符合现代设计标准
- [x] 交互流畅，无明显卡顿
- [x] 错误处理完善，提示信息友好
- [x] 加载状态明确，用户体验良好
- [x] 无障碍性考虑，支持键盘导航

---

## 🔄 后续迭代计划

### Week 2 Day 4-7: 深度功能开发
- 提示词优化器核心功能
- 实时预览和编辑
- 高级配置选项
- 批量处理能力

### Week 3: 优化和完善
- 性能优化
- 国际化支持
- 主题切换
- 离线功能

### Week 4: 测试和部署
- 单元测试覆盖
- E2E测试
- 性能测试
- 生产环境部署

---

## 📊 技术债务管理

### 已知限制
- 初期不支持多语言
- 暂不考虑离线功能
- 移动端体验待优化
- 无障碍性支持有限

### 优化计划
- 代码分割和懒加载
- 图片资源优化
- Bundle体积控制
- SEO优化考虑

---

**文档版本**: v1.0  
**创建时间**: 2025-06-10  
**最后更新**: 2025-06-10  
**负责人**: AI Assistant 