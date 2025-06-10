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
    <Layout className="min-h-screen">
      <Header />
      <Layout>
        {showSidebar && <Sidebar />}
        <Layout className="bg-gray-50">
          <Content className="mx-4 my-6">
            <div className="min-h-[calc(100vh-200px)] bg-white rounded-lg shadow-sm p-6">
              {children}
            </div>
          </Content>
          <Footer className="text-center text-gray-500">
            AI提示词优化器 ©2024 Created with ❤️
          </Footer>
        </Layout>
      </Layout>
    </Layout>
  );
}; 