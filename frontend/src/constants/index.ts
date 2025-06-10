// API相关常量
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    ME: '/api/v1/auth/me',
    REFRESH: '/api/v1/auth/refresh',
    LOGOUT: '/api/v1/auth/logout',
  },
  // 用户管理
  USERS: {
    LIST: '/api/v1/users/',
    PROFILE: (id: number) => `/api/v1/users/${id}`,
    UPDATE: (id: number) => `/api/v1/users/${id}`,
    DELETE: (id: number) => `/api/v1/users/${id}`,
  },
  // 提示词优化
  OPTIMIZER: {
    OPTIMIZE: '/api/v1/optimizer/optimize',
    EVALUATE: '/api/v1/optimizer/evaluate',
    HISTORY: '/api/v1/optimizer/history',
  },
  // 案例库
  EXAMPLES: {
    LIST: '/api/v1/examples/',
    DETAIL: (id: number) => `/api/v1/examples/${id}`,
    SEARCH: '/api/v1/examples/search',
  },
  // 健康检查
  HEALTH: '/api/v1/health/',
} as const;

// 本地存储键名
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  USER_INFO: 'user_info',
  THEME: 'theme',
  LANGUAGE: 'language',
  PREFERENCES: 'user_preferences',
} as const;

// 路由路径
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  OPTIMIZER: '/optimizer',
  HISTORY: '/history',
  EXAMPLES: '/examples',
  SETTINGS: '/settings',
  PROFILE: '/profile',
} as const;

// 主题配置
export const THEME_CONFIG = {
  COLORS: {
    PRIMARY: '#1890ff',
    SUCCESS: '#52c41a',
    WARNING: '#faad14',
    ERROR: '#ff4d4f',
    INFO: '#1890ff',
  },
  BREAKPOINTS: {
    MOBILE: 320,
    TABLET: 768,
    DESKTOP: 1024,
    WIDE: 1440,
  },
} as const;

// 表单验证配置
export const VALIDATION_RULES = {
  USERNAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 20,
    PATTERN: /^[a-zA-Z0-9_]+$/,
  },
  PASSWORD: {
    MIN_LENGTH: 8,
    MAX_LENGTH: 128,
    PATTERN: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/,
  },
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  },
  PROMPT: {
    MIN_LENGTH: 1,
    MAX_LENGTH: 10000,
  },
} as const;

// 优化类型配置
export const OPTIMIZATION_CONFIG = {
  TYPES: [
    { value: 'general', label: '通用优化', description: '适用于大多数场景的通用优化' },
    { value: 'code', label: '代码相关', description: '针对编程和代码生成场景' },
    { value: 'writing', label: '写作相关', description: '针对文章、文档等写作场景' },
    { value: 'analysis', label: '分析相关', description: '针对数据分析和研究场景' },
  ],
  QUALITY_LEVELS: [
    { min: 0, max: 3, label: '需要改进', color: '#ff4d4f' },
    { min: 4, max: 6, label: '一般', color: '#faad14' },
    { min: 7, max: 8, label: '良好', color: '#52c41a' },
    { min: 9, max: 10, label: '优秀', color: '#1890ff' },
  ],
} as const;

// 分页配置
export const PAGINATION_CONFIG = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 100,
} as const;

// 错误消息
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络错误，请检查您的网络连接',
  UNAUTHORIZED: '未授权，请重新登录',
  FORBIDDEN: '权限不足，无法访问此资源',
  NOT_FOUND: '请求的资源不存在',
  SERVER_ERROR: '服务器错误，请稍后重试',
  VALIDATION_ERROR: '输入数据验证失败',
  UNKNOWN_ERROR: '未知错误，请联系管理员',
} as const;

// 成功消息
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: '登录成功！',
  REGISTER_SUCCESS: '注册成功！',
  LOGOUT_SUCCESS: '退出登录成功！',
  SAVE_SUCCESS: '保存成功！',
  DELETE_SUCCESS: '删除成功！',
  UPDATE_SUCCESS: '更新成功！',
  OPTIMIZATION_SUCCESS: '优化完成！',
} as const; 