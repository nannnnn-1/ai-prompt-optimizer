import { create } from 'zustand';

// 通知类型
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  timestamp: number;
}

// 错误信息
export interface ErrorInfo {
  type: 'network' | 'validation' | 'server' | 'unknown';
  message: string;
  details?: string;
  timestamp: number;
  code?: string | number;
}

// 加载状态
export interface LoadingState {
  global: boolean;
  optimize: boolean;
  save: boolean;
  load: boolean;
  [key: string]: boolean;
}

// 模态框状态
export interface ModalState {
  confirmDialog: boolean;
  settingsModal: boolean;
  helpModal: boolean;
  [key: string]: boolean;
}

// UI状态接口
export interface UIState {
  loading: LoadingState;
  error: ErrorInfo | null;
  notifications: Notification[];
  modals: ModalState;
  
  // Actions
  setLoading: (key: keyof LoadingState, loading: boolean) => void;
  setError: (error: ErrorInfo | null) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
  setModal: (key: keyof ModalState, open: boolean) => void;
  clearError: () => void;
}

// 生成唯一ID
const generateId = () => Math.random().toString(36).substr(2, 9);

// 创建UI Store
export const useUIStore = create<UIState>((set, get) => ({
  loading: {
    global: false,
    optimize: false,
    save: false,
    load: false,
  },
  error: null,
  notifications: [],
  modals: {
    confirmDialog: false,
    settingsModal: false,
    helpModal: false,
  },

  setLoading: (key, loading) => {
    set((state) => ({
      loading: {
        ...state.loading,
        [key]: loading,
      },
    }));
  },

  setError: (error) => {
    set({ error });
  },

  addNotification: (notification) => {
    const newNotification: Notification = {
      ...notification,
      id: generateId(),
      timestamp: Date.now(),
      duration: notification.duration || 4000,
    };

    set((state) => ({
      notifications: [...state.notifications, newNotification],
    }));

    // 自动移除通知
    if (newNotification.duration && newNotification.duration > 0) {
      setTimeout(() => {
        get().removeNotification(newNotification.id);
      }, newNotification.duration);
    }
  },

  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },

  clearNotifications: () => {
    set({ notifications: [] });
  },

  setModal: (key, open) => {
    set((state) => ({
      modals: {
        ...state.modals,
        [key]: open,
      },
    }));
  },

  clearError: () => {
    set({ error: null });
  },
})); 