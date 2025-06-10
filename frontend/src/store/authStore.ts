import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '../services/auth';
import { STORAGE_KEYS, SUCCESS_MESSAGES } from '../constants';
import type { User, UserLogin, UserRegister } from '../types';

interface AuthState {
  // 状态
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;

  // 方法
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserRegister) => Promise<void>;
  logout: () => void;
  getCurrentUser: () => Promise<void>;
  clearError: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // 初始状态
      user: null,
      token: null,
      isAuthenticated: false,
      loading: false,
      error: null,

      // 登录方法
      login: async (credentials: UserLogin) => {
        try {
          set({ loading: true, error: null });
          
          const tokenResponse = await authService.login(credentials);
          const token = tokenResponse.access_token;
          
          // 保存token
          localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token);
          
          // 获取用户信息
          const user = await authService.getCurrentUser();
          
          set({
            user,
            token,
            isAuthenticated: true,
            loading: false,
            error: null,
          });

          // 可选：显示成功消息
          console.log(SUCCESS_MESSAGES.LOGIN_SUCCESS);
        } catch (error) {
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            loading: false,
            error: error instanceof Error ? error.message : '登录失败',
          });
          throw error;
        }
      },

      // 注册方法
      register: async (userData: UserRegister) => {
        try {
          set({ loading: true, error: null });
          
          const user = await authService.register(userData);
          
          set({
            loading: false,
            error: null,
          });

          console.log(SUCCESS_MESSAGES.REGISTER_SUCCESS);
        } catch (error) {
          set({
            loading: false,
            error: error instanceof Error ? error.message : '注册失败',
          });
          throw error;
        }
      },

      // 退出登录方法
      logout: () => {
        try {
          authService.logout().catch(() => {
            // 忽略登出API错误，确保本地清理
          });
        } finally {
          // 清除本地存储
          localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
          localStorage.removeItem(STORAGE_KEYS.USER_INFO);
          
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            loading: false,
            error: null,
          });

          console.log(SUCCESS_MESSAGES.LOGOUT_SUCCESS);
        }
      },

      // 获取当前用户信息
      getCurrentUser: async () => {
        try {
          set({ loading: true, error: null });
          
          const user = await authService.getCurrentUser();
          
          set({
            user,
            isAuthenticated: true,
            loading: false,
            error: null,
          });
        } catch (error) {
          // 如果获取用户信息失败，清除认证状态
          get().logout();
          set({
            loading: false,
            error: error instanceof Error ? error.message : '获取用户信息失败',
          });
        }
      },

      // 清除错误
      clearError: () => {
        set({ error: null });
      },

      // 设置加载状态
      setLoading: (loading: boolean) => {
        set({ loading });
      },
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
); 