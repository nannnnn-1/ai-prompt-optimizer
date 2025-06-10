import React from 'react';
import { Layout, Button, Avatar, Dropdown, Space, Typography } from 'antd';
import { UserOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { ROUTES } from '../../constants';
import type { MenuProps } from 'antd';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

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
    <AntHeader 
      style={{ 
        backgroundColor: '#fff', 
        padding: '0 24px', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        borderBottom: '1px solid #f0f0f0',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        height: '64px'
      }}
    >
      {/* 左侧 - Logo和标题 */}
      <div 
        style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}
        onClick={() => navigate(ROUTES.HOME)}
      >
        <div 
          style={{ 
            width: '32px', 
            height: '32px', 
            backgroundColor: '#1890ff', 
            borderRadius: '8px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            marginRight: '12px' 
          }}
        >
          <Text style={{ color: 'white', fontWeight: 'bold', fontSize: '18px' }}>AI</Text>
        </div>
        <Text strong style={{ fontSize: '20px', color: '#262626' }}>
          AI提示词优化器
        </Text>
      </div>

      {/* 右侧 - 用户菜单 */}
      <div>
        {isAuthenticated ? (
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <div style={{ cursor: 'pointer' }}>
              <Space>
                <Avatar 
                  size="small" 
                  icon={<UserOutlined />} 
                  style={{ backgroundColor: '#1890ff' }}
                />
                <Text style={{ color: '#262626' }}>
                  {user?.full_name || user?.username || '用户'}
                </Text>
              </Space>
            </div>
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