import axios, { AxiosError } from 'axios';
import type { AxiosInstance, AxiosRequestConfig } from 'axios';
import { useUIStore } from '../store/uiStore';
import type { ErrorInfo } from '../store/uiStore';

// API响应格式
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  code?: number;
}

// 请求配置
export interface RequestConfig extends AxiosRequestConfig {
  retry?: number;
  retryDelay?: number;
  cache?: boolean;
  skipErrorHandling?: boolean;
}

class ApiClient {
  private instance: AxiosInstance;

  constructor(baseURL: string = '/api') {
    // 创建axios实例
    this.instance = axios.create({
      baseURL,
      timeout: 30000, // 30秒超时
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 添加认证token
        const token = localStorage.getItem('token');
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response) => {
        return response;
      },
      (error: AxiosError) => {
        return this.handleResponseError(error);
      }
    );
  }

  private async handleResponseError(error: AxiosError): Promise<AxiosError> {
    // 处理特定的HTTP状态码
    if (error.response) {
      switch (error.response.status) {
        case 401:
          this.handleUnauthorized();
          break;
        case 403:
          this.handleForbidden();
          break;
        case 404:
          this.handleNotFound();
          break;
        case 500:
        case 502:
        case 503:
        case 504:
          this.handleServerError();
          break;
      }
    } else {
      // 网络错误
      this.handleNetworkError();
    }

    // 统一错误处理
    this.handleError(error);

    return Promise.reject(error);
  }

  private handleUnauthorized() {
    // 清除认证信息
    localStorage.removeItem('token');
    useUIStore.getState().addNotification({
      type: 'error',
      title: '登录已过期',
      message: '请重新登录',
    });
  }

  private handleForbidden() {
    useUIStore.getState().addNotification({
      type: 'error',
      title: '访问被拒绝',
      message: '您没有权限执行此操作',
    });
  }

  private handleNotFound() {
    useUIStore.getState().addNotification({
      type: 'error',
      title: '资源不存在',
      message: '请求的资源未找到',
    });
  }

  private handleServerError() {
    useUIStore.getState().addNotification({
      type: 'error',
      title: '服务器错误',
      message: '服务器暂时无法处理您的请求，请稍后重试',
    });
  }

  private handleNetworkError() {
    useUIStore.getState().addNotification({
      type: 'error',
      title: '网络错误',
      message: '请检查您的网络连接',
    });
  }

  private handleError(error: AxiosError) {
    const errorInfo: ErrorInfo = {
      type: error.response ? 'server' : 'network',
      message: this.getErrorMessage(error),
      timestamp: Date.now(),
      code: error.response?.status,
      details: error.message,
    };

    useUIStore.getState().setError(errorInfo);
  }

  private getErrorMessage(error: AxiosError): string {
    const response = error.response;
    
    if (response?.data && typeof response.data === 'object') {
      const data = response.data as any;
      if (data.message) {
        return data.message;
      }
    }
    
    if (error.message) {
      return error.message;
    }
    
    return '未知错误';
  }

  // GET请求
  async get<T = any>(url: string, config: RequestConfig = {}): Promise<T> {
    const response = await this.instance.get<ApiResponse<T>>(url, config);
    return response.data.data;
  }

  // POST请求
  async post<T = any>(url: string, data?: any, config: RequestConfig = {}): Promise<T> {
    const response = await this.instance.post<ApiResponse<T>>(url, data, config);
    return response.data.data;
  }

  // PUT请求
  async put<T = any>(url: string, data?: any, config: RequestConfig = {}): Promise<T> {
    const response = await this.instance.put<ApiResponse<T>>(url, data, config);
    return response.data.data;
  }

  // DELETE请求
  async delete<T = any>(url: string, config: RequestConfig = {}): Promise<T> {
    const response = await this.instance.delete<ApiResponse<T>>(url, config);
    return response.data.data;
  }
}

// 创建默认实例
export const apiClient = new ApiClient(); 