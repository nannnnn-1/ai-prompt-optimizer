import React, { useState } from 'react';
import { Button, Card, Form, Input, message, Typography, Divider } from 'antd';
import { UserOutlined, MailOutlined, LockOutlined, EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import type { UserRegister } from '../types';

const { Title, Text } = Typography;

const Register: React.FC = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { register, loading, error } = useAuthStore();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (values: UserRegister) => {
    try {
      setIsSubmitting(true);
      await register(values);
      message.success('注册成功！欢迎使用AI提示词优化器');
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration failed:', error);
      message.error('注册失败，请重试');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Card className="shadow-2xl border-0 rounded-xl">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <UserOutlined className="text-white text-2xl" />
            </div>
            <Title level={2} className="mb-2 text-gray-800">
              创建账户
            </Title>
            <Text type="secondary" className="text-base">
              加入AI提示词优化器，开始智能优化之旅
            </Text>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <Text type="danger" className="text-sm">
                {error}
              </Text>
            </div>
          )}

          <Form
            form={form}
            name="register"
            onFinish={handleSubmit}
            layout="vertical"
            requiredMark={false}
            className="space-y-1"
          >
            <Form.Item
              name="username"
              label="用户名"
              rules={[
                { required: true, message: '请输入用户名' },
                { min: 3, message: '用户名至少3个字符' },
                { max: 20, message: '用户名最多20个字符' },
                { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线' }
              ]}
            >
              <Input
                prefix={<UserOutlined className="text-gray-400" />}
                placeholder="请输入用户名"
                size="large"
                className="rounded-lg"
              />
            </Form.Item>

            <Form.Item
              name="email"
              label="邮箱地址"
              rules={[
                { required: true, message: '请输入邮箱地址' },
                { type: 'email', message: '请输入有效的邮箱地址' }
              ]}
            >
              <Input
                prefix={<MailOutlined className="text-gray-400" />}
                placeholder="请输入邮箱地址"
                size="large"
                className="rounded-lg"
              />
            </Form.Item>

            <Form.Item
              name="password"
              label="密码"
              rules={[
                { required: true, message: '请输入密码' },
                { min: 6, message: '密码至少6个字符' },
                { max: 50, message: '密码最多50个字符' }
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="text-gray-400" />}
                placeholder="请输入密码"
                size="large"
                className="rounded-lg"
                iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
              />
            </Form.Item>

            <Form.Item
              name="confirmPassword"
              label="确认密码"
              dependencies={['password']}
              rules={[
                { required: true, message: '请确认密码' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('两次输入的密码不一致'));
                  },
                }),
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="text-gray-400" />}
                placeholder="请再次输入密码"
                size="large"
                className="rounded-lg"
                iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
              />
            </Form.Item>

            <Form.Item className="mb-0">
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                loading={loading || isSubmitting}
                className="w-full h-12 rounded-lg font-medium text-base bg-gradient-to-r from-blue-500 to-purple-600 border-0 hover:from-blue-600 hover:to-purple-700"
              >
                {loading || isSubmitting ? '注册中...' : '创建账户'}
              </Button>
            </Form.Item>
          </Form>

          <Divider className="my-6">
            <Text type="secondary" className="text-sm">
              或者
            </Text>
          </Divider>

          <div className="text-center">
            <Text type="secondary" className="text-sm">
              已有账户？
              <Link to="/login" className="text-blue-500 hover:text-blue-600 font-medium ml-1">
                立即登录
              </Link>
            </Text>
          </div>
        </Card>

        <div className="text-center mt-6">
          <Text type="secondary" className="text-xs">
            注册即表示您同意我们的
            <Link to="/terms" className="text-blue-500 hover:text-blue-600 mx-1">
              服务条款
            </Link>
            和
            <Link to="/privacy" className="text-blue-500 hover:text-blue-600 mx-1">
              隐私政策
            </Link>
          </Text>
        </div>
      </div>
    </div>
  );
};

export default Register; 