import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Space } from 'antd';
import { 
  RocketOutlined, 
  HistoryOutlined, 
  TrophyOutlined, 
  ClockCircleOutlined,
  ArrowRightOutlined 
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { ROUTES } from '../constants';

const { Title, Paragraph } = Typography;

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const stats = [
    {
      title: '优化次数',
      value: 0,
      icon: <RocketOutlined className="text-blue-500" />,
      color: 'bg-blue-50',
    },
    {
      title: '历史记录',
      value: 0,
      icon: <HistoryOutlined className="text-green-500" />,
      color: 'bg-green-50',
    },
    {
      title: '质量提升',
      value: 0,
      suffix: '%',
      icon: <TrophyOutlined className="text-yellow-500" />,
      color: 'bg-yellow-50',
    },
    {
      title: '累计时间',
      value: 0,
      suffix: '分钟',
      icon: <ClockCircleOutlined className="text-purple-500" />,
      color: 'bg-purple-50',
    },
  ];

  const quickActions = [
    {
      title: '开始优化',
      description: '优化你的提示词，提升AI回复质量',
      icon: <RocketOutlined />,
      color: 'bg-blue-500',
      action: () => navigate(ROUTES.OPTIMIZER),
    },
    {
      title: '查看历史',
      description: '回顾之前的优化记录和结果',
      icon: <HistoryOutlined />,
      color: 'bg-green-500',
      action: () => navigate(ROUTES.HISTORY),
    },
    {
      title: '浏览案例',
      description: '学习优秀的提示词案例',
      icon: <TrophyOutlined />,
      color: 'bg-yellow-500',
      action: () => navigate(ROUTES.EXAMPLES),
    },
  ];

  return (
    <div className="space-y-6">
      {/* 欢迎区域 */}
      <Card>
        <div className="flex items-center justify-between">
          <div>
            <Title level={2} className="mb-2">
              欢迎回来, {user?.full_name || user?.username}! 👋
            </Title>
            <Paragraph className="text-gray-600 mb-0">
              让我们开始优化你的提示词，创造更好的AI交互体验
            </Paragraph>
          </div>
          <Button 
            type="primary" 
            size="large"
            icon={<RocketOutlined />}
            onClick={() => navigate(ROUTES.OPTIMIZER)}
          >
            开始优化
          </Button>
        </div>
      </Card>

      {/* 统计数据 */}
      <Row gutter={[16, 16]}>
        {stats.map((stat, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <Card>
              <div className="flex items-center">
                <div className={`w-12 h-12 rounded-lg ${stat.color} flex items-center justify-center mr-4`}>
                  {stat.icon}
                </div>
                <div>
                  <Statistic
                    title={stat.title}
                    value={stat.value}
                    suffix={stat.suffix}
                    valueStyle={{ fontSize: '1.5rem', fontWeight: 'bold' }}
                  />
                </div>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      {/* 快速操作 */}
      <Card title="快速操作" className="mt-6">
        <Row gutter={[16, 16]}>
          {quickActions.map((action, index) => (
            <Col xs={24} md={8} key={index}>
              <Card 
                hoverable
                className="h-full cursor-pointer"
                onClick={action.action}
              >
                <div className="text-center">
                  <div className={`w-16 h-16 rounded-full ${action.color} flex items-center justify-center mx-auto mb-4`}>
                    <span className="text-white text-2xl">{action.icon}</span>
                  </div>
                  <Title level={4} className="mb-2">
                    {action.title}
                  </Title>
                  <Paragraph className="text-gray-600">
                    {action.description}
                  </Paragraph>
                  <Button type="text" icon={<ArrowRightOutlined />}>
                    开始使用
                  </Button>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>

      {/* 最近活动 */}
      <Card title="最近活动">
        <div className="text-center py-8">
          <div className="text-gray-400 mb-4">
            <HistoryOutlined style={{ fontSize: '3rem' }} />
          </div>
          <Title level={4} className="text-gray-500 mb-2">
            暂无活动记录
          </Title>
          <Paragraph className="text-gray-400 mb-4">
            开始使用提示词优化功能来查看活动记录
          </Paragraph>
          <Button 
            type="primary" 
            onClick={() => navigate(ROUTES.OPTIMIZER)}
          >
            立即开始
          </Button>
        </div>
      </Card>
    </div>
  );
}; 