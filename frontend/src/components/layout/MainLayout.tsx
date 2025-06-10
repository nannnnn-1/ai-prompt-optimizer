import React from 'react';
import { Layout } from 'antd';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

const { Content, Footer } = Layout;

interface MainLayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ 
  children, 
  showSidebar = true 
}) => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header />
      <Layout style={{ marginTop: '64px' }}>
        {showSidebar && <Sidebar />}
        <Layout style={{ 
          marginLeft: showSidebar ? 200 : 0,
          backgroundColor: '#f5f5f5'
        }}>
          <Content style={{ padding: '0', minHeight: 'calc(100vh - 64px)' }}>
            {children}
          </Content>
          <Footer style={{ 
            textAlign: 'center', 
            backgroundColor: '#f5f5f5',
            color: '#8c8c8c',
            borderTop: '1px solid #f0f0f0'
          }}>
            AI提示词优化器 ©2024 Created with ❤️
          </Footer>
        </Layout>
      </Layout>
    </Layout>
  );
}; 