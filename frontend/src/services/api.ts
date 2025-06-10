import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_BASE_URL, STORAGE_KEYS, ERROR_MESSAGES } from '../constants';
import type { ApiResponse } from '../types';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response;
      },
      (error) => {
        const { response } = error;
        
        if (!response) {
          // 网络错误
          throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
        }

        switch (response.status) {
          case 401:
            // 未授权，清除token并跳转到登录页
            localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
            localStorage.removeItem(STORAGE_KEYS.USER_INFO);
            window.location.href = '/login';
            throw new Error(ERROR_MESSAGES.UNAUTHORIZED);
          
          case 403:
            throw new Error(ERROR_MESSAGES.FORBIDDEN);
          
          case 404:
            throw new Error(ERROR_MESSAGES.NOT_FOUND);
          
          case 422:
            // 验证错误
            const detail = response.data.detail;
            if (Array.isArray(detail)) {
              const errorMessages = detail.map((err: any) => err.msg).join(', ');
              throw new Error(errorMessages);
            }
            throw new Error(ERROR_MESSAGES.VALIDATION_ERROR);
          
          case 500:
            throw new Error(ERROR_MESSAGES.SERVER_ERROR);
          
          default:
            throw new Error(response.data.message || ERROR_MESSAGES.UNKNOWN_ERROR);
        }
      }
    );
  }

  // GET请求
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  // POST请求
  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  // PUT请求
  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  // PATCH请求
  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  // DELETE请求
  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // 上传文件
  async upload<T = any>(url: string, file: File, config?: AxiosRequestConfig): Promise<T> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await this.client.post<T>(url, formData, {
      ...config,
      headers: {
        ...config?.headers,
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }

  // 获取当前实例（用于特殊情况）
  getInstance(): AxiosInstance {
    return this.client;
  }
}

// 创建API客户端实例
export const apiClient = new ApiClient();

// 导出便捷方法
export const api = {
  get: apiClient.get.bind(apiClient),
  post: apiClient.post.bind(apiClient),
  put: apiClient.put.bind(apiClient),
  patch: apiClient.patch.bind(apiClient),
  delete: apiClient.delete.bind(apiClient),
  upload: apiClient.upload.bind(apiClient),
}; 