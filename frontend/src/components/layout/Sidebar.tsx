import React from 'react';
import { Layout, Menu } from 'antd';
import { 
  HomeOutlined, 
  RocketOutlined, 
  HistoryOutlined, 
  BookOutlined, 
  SettingOutlined,
  DashboardOutlined 
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { ROUTES } from '../../constants';
import type { MenuProps } from 'antd';

const { Sider } = Layout;

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems: MenuProps['items'] = [
    {
      key: ROUTES.HOME,
      icon: <HomeOutlined />,
      label: '首页',
      onClick: () => navigate(ROUTES.HOME),
    },
    {
      key: ROUTES.DASHBOARD,
      icon: <DashboardOutlined />,
      label: '仪表板',
      onClick: () => navigate(ROUTES.DASHBOARD),
    },
    {
      key: ROUTES.OPTIMIZER,
      icon: <RocketOutlined />,
      label: '提示词优化',
      onClick: () => navigate(ROUTES.OPTIMIZER),
    },
    {
      key: ROUTES.HISTORY,
      icon: <HistoryOutlined />,
      label: '历史记录',
      onClick: () => navigate(ROUTES.HISTORY),
    },
    {
      key: ROUTES.EXAMPLES,
      icon: <BookOutlined />,
      label: '案例库',
      onClick: () => navigate(ROUTES.EXAMPLES),
    },
    {
      type: 'divider',
    },
    {
      key: ROUTES.SETTINGS,
      icon: <SettingOutlined />,
      label: '设置',
      onClick: () => navigate(ROUTES.SETTINGS),
    },
  ];

  return (
    <Sider 
      width={200} 
      style={{
        backgroundColor: '#fff',
        borderRight: '1px solid #f0f0f0',
        height: 'calc(100vh - 64px)',
        position: 'fixed',
        left: 0,
        top: 64,
        overflow: 'auto',
        zIndex: 999
      }}
      breakpoint="lg"
      collapsedWidth="0"
    >
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        style={{ 
          height: '100%', 
          border: 'none',
          backgroundColor: '#fff'
        }}
        items={menuItems}
      />
    </Sider>
  );
}; 