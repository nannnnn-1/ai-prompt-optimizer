import React, { useState } from 'react';
import { Form, Input, Button, Card, Alert, Divider } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { ROUTES } from '../constants';
import type { UserLogin } from '../types';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login, loading, error, clearError } = useAuthStore();
  const [form] = Form.useForm();

  const handleSubmit = async (values: UserLogin) => {
    try {
      clearError();
      await login(values);
      navigate(ROUTES.DASHBOARD);
    } catch (error) {
      // 错误已经在store中处理
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <Card className="w-full max-w-md shadow-lg">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">AI</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-800">欢迎回来</h1>
          <p className="text-gray-600 mt-2">登录到AI提示词优化器</p>
        </div>

        {error && (
          <Alert
            message={error}
            type="error"
            closable
            onClose={clearError}
            className="mb-4"
          />
        )}

        <Form
          form={form}
          name="login"
          onFinish={handleSubmit}
          autoComplete="off"
          size="large"
        >
          <Form.Item
            name="username"
            rules={[
              { required: true, message: '请输入用户名' },
              { min: 3, message: '用户名至少3个字符' },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="用户名"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6个字符' },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              className="w-full"
            >
              登录
            </Button>
          </Form.Item>
        </Form>

        <Divider />

        <div className="text-center">
          <span className="text-gray-600">还没有账户？</span>
          <Link to={ROUTES.REGISTER} className="text-primary-500 hover:text-primary-600 ml-1">
            立即注册
          </Link>
        </div>
      </Card>
    </div>
  );
}; 