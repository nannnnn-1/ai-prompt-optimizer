import { api } from './api';
import { API_ENDPOINTS } from '../constants';
import type { User, UserLogin, UserRegister, Token } from '../types';

export const authService = {
  // 用户登录
  async login(credentials: UserLogin): Promise<Token> {
    return api.post<Token>(API_ENDPOINTS.AUTH.LOGIN, credentials);
  },

  // 用户注册
  async register(userData: UserRegister): Promise<User> {
    return api.post<User>(API_ENDPOINTS.AUTH.REGISTER, userData);
  },

  // 获取当前用户信息
  async getCurrentUser(): Promise<User> {
    return api.get<User>(API_ENDPOINTS.AUTH.ME);
  },

  // 刷新token
  async refreshToken(): Promise<Token> {
    return api.post<Token>(API_ENDPOINTS.AUTH.REFRESH);
  },

  // 退出登录
  async logout(): Promise<void> {
    return api.post(API_ENDPOINTS.AUTH.LOGOUT);
  },

  // 检查token是否有效
  async validateToken(): Promise<boolean> {
    try {
      await this.getCurrentUser();
      return true;
    } catch {
      return false;
    }
  },
}; 