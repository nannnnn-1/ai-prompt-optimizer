import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { MainLayout } from './components/layout/MainLayout';
import { Login } from './pages/Login';
import Register from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Optimizer } from './pages/Optimizer';
import { useAuthStore } from './store/authStore';
import { ROUTES } from './constants';

// 主题配置
const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 8,
    colorBgContainer: '#ffffff',
  },
};

// 私有路由组件
const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to={ROUTES.LOGIN} replace />;
};

// 公共路由组件（已登录用户重定向到仪表板）
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return !isAuthenticated ? <>{children}</> : <Navigate to={ROUTES.DASHBOARD} replace />;
};

export default function App() {
  const { getCurrentUser, isAuthenticated } = useAuthStore();

  useEffect(() => {
    // 应用启动时检查是否有有效的认证状态
    const token = localStorage.getItem('access_token');
    if (token && !isAuthenticated) {
      getCurrentUser();
    }
  }, [getCurrentUser, isAuthenticated]);

  return (
    <ConfigProvider locale={zhCN} theme={theme}>
      <Router>
        <Routes>
          {/* 公共路由 */}
          <Route 
            path={ROUTES.LOGIN} 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />
          
          <Route 
            path={ROUTES.REGISTER} 
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            } 
          />

          {/* 私有路由 */}
          <Route 
            path={ROUTES.DASHBOARD} 
            element={
              <PrivateRoute>
                <MainLayout>
                  <Dashboard />
                </MainLayout>
              </PrivateRoute>
            } 
          />

          {/* 提示词优化页面 */}
          <Route 
            path={ROUTES.OPTIMIZER} 
            element={
              <PrivateRoute>
                <MainLayout>
                  <Optimizer />
                </MainLayout>
              </PrivateRoute>
            } 
          />

          <Route 
            path={ROUTES.HISTORY} 
            element={
              <PrivateRoute>
                <MainLayout>
                  <div className="text-center p-8">
                    <h2>历史记录页面</h2>
                    <p>功能开发中...</p>
                  </div>
                </MainLayout>
              </PrivateRoute>
            } 
          />

          <Route 
            path={ROUTES.EXAMPLES} 
            element={
              <PrivateRoute>
                <MainLayout>
                  <div className="text-center p-8">
                    <h2>案例库页面</h2>
                    <p>功能开发中...</p>
                  </div>
                </MainLayout>
              </PrivateRoute>
            } 
          />

          <Route 
            path={ROUTES.SETTINGS} 
            element={
              <PrivateRoute>
                <MainLayout>
                  <div className="text-center p-8">
                    <h2>设置页面</h2>
                    <p>功能开发中...</p>
                  </div>
                </MainLayout>
              </PrivateRoute>
            } 
          />

          {/* 默认重定向 */}
          <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.DASHBOARD} replace />} />
          <Route path="*" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
        </Routes>
      </Router>
    </ConfigProvider>
  );
}
