import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Space } from 'antd';
import { 
  RocketOutlined, 
  HistoryOutlined, 
  TrophyOutlined, 
  ClockCircleOutlined,
  BulbOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { ROUTES } from '../constants';

const { Title, Paragraph } = Typography;

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  return (
    <div style={{ padding: '24px', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      {/* 欢迎区域 */}
      <Card style={{ marginBottom: '24px' }}>
        <Title level={2}>
          欢迎回来, {user?.full_name || user?.username}! 👋
        </Title>
        <Paragraph type="secondary">
          让我们开始优化你的提示词，创造更好的AI交互体验
        </Paragraph>
        <Button 
          type="primary" 
          size="large"
          icon={<RocketOutlined />}
          onClick={() => navigate(ROUTES.OPTIMIZER)}
        >
          开始优化
        </Button>
      </Card>

      {/* 统计数据 */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="优化次数"
              value={0}
              prefix={<RocketOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="历史记录"
              value={0}
              prefix={<HistoryOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="质量提升"
              value={0}
              suffix="%"
              prefix={<TrophyOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="累计时间"
              value={0}
              suffix="分钟"
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* 快速操作 */}
      <Card title="快速操作">
        <Row gutter={16}>
          <Col xs={24} md={8}>
            <Card 
              hoverable
              onClick={() => navigate(ROUTES.OPTIMIZER)}
              style={{ textAlign: 'center' }}
            >
              <RocketOutlined style={{ fontSize: '48px', color: '#1890ff', marginBottom: '16px' }} />
              <Title level={4}>开始优化</Title>
              <Paragraph type="secondary">
                优化你的提示词，提升AI回复质量
              </Paragraph>
              <Button type="primary">开始使用</Button>
            </Card>
          </Col>
          <Col xs={24} md={8}>
            <Card 
              hoverable
              onClick={() => navigate(ROUTES.HISTORY)}
              style={{ textAlign: 'center' }}
            >
              <HistoryOutlined style={{ fontSize: '48px', color: '#52c41a', marginBottom: '16px' }} />
              <Title level={4}>查看历史</Title>
              <Paragraph type="secondary">
                回顾之前的优化记录和结果
              </Paragraph>
              <Button type="primary">开始使用</Button>
            </Card>
          </Col>
          <Col xs={24} md={8}>
            <Card 
              hoverable
              onClick={() => navigate(ROUTES.EXAMPLES)}
              style={{ textAlign: 'center' }}
            >
              <TrophyOutlined style={{ fontSize: '48px', color: '#faad14', marginBottom: '16px' }} />
              <Title level={4}>浏览案例</Title>
              <Paragraph type="secondary">
                学习优秀的提示词案例
              </Paragraph>
              <Button type="primary">开始使用</Button>
            </Card>
          </Col>
        </Row>
      </Card>

      {/* 最近活动 */}
      <Card title="最近活动" style={{ marginTop: '24px' }}>
        <div style={{ textAlign: 'center', padding: '48px 0' }}>
          <BulbOutlined style={{ fontSize: '64px', color: '#d9d9d9', marginBottom: '16px' }} />
          <Title level={4} type="secondary">暂无活动记录</Title>
          <Paragraph type="secondary">
            开始使用AI提示词优化器来查看活动记录
          </Paragraph>
        </div>
      </Card>
    </div>
  );
}; 