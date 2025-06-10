import React from 'react';
import { Layout, Button, Avatar, Dropdown, Space } from 'antd';
import { UserOutlined, LogoutOutlined, SettingOutlined, MenuFoldOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { ROUTES } from '../../constants';
import type { MenuProps } from 'antd';

const { Header: AntHeader } = Layout;

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout, isAuthenticated } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人资料',
      onClick: () => navigate(ROUTES.PROFILE),
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '设置',
      onClick: () => navigate(ROUTES.SETTINGS),
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: handleLogout,
    },
  ];

  return (
    <AntHeader className="bg-white shadow-sm border-b border-gray-200 px-6 flex items-center justify-between">
      {/* 左侧 - Logo和标题 */}
      <div className="flex items-center space-x-4">
        <div 
          className="flex items-center cursor-pointer"
          onClick={() => navigate(ROUTES.HOME)}
        >
          <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center mr-3">
            <span className="text-white font-bold text-lg">AI</span>
          </div>
          <h1 className="text-xl font-bold text-gray-800 hidden sm:block">
            AI提示词优化器
          </h1>
        </div>
      </div>

      {/* 右侧 - 用户菜单 */}
      <div className="flex items-center space-x-4">
        {isAuthenticated ? (
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Space className="cursor-pointer hover:bg-gray-50 px-3 py-2 rounded-lg">
              <Avatar 
                size="small" 
                icon={<UserOutlined />} 
                className="bg-primary-500"
              />
              <span className="text-gray-700 hidden sm:inline">
                {user?.full_name || user?.username}
              </span>
            </Space>
          </Dropdown>
        ) : (
          <Space>
            <Button 
              type="text" 
              onClick={() => navigate(ROUTES.LOGIN)}
            >
              登录
            </Button>
            <Button 
              type="primary" 
              onClick={() => navigate(ROUTES.REGISTER)}
            >
              注册
            </Button>
          </Space>
        )}
      </div>
    </AntHeader>
  );
}; 