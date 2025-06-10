import React, { useMemo } from 'react';
import { Card, Progress, Row, Col, Typography, Space, Tag, Statistic } from 'antd';
import { 
  StarOutlined, 
  TrophyOutlined, 
  ArrowUpOutlined, 
  ArrowDownOutlined 
} from '@ant-design/icons';

const { Text, Title } = Typography;

export interface DetailedScores {
  clarity: number;
  completeness: number;
  structure: number;
  specificity: number;
  actionability: number;
}

export interface QualityScore {
  overall: number;
  detailed: DetailedScores;
  grade: string;
  improvement?: number;
}

export interface QualityScoreCardProps {
  beforeScore?: QualityScore;
  afterScore: QualityScore;
  showComparison?: boolean;
  loading?: boolean;
  className?: string;
}

// 评分标签映射
const SCORE_LABELS: Record<keyof DetailedScores, string> = {
  clarity: '清晰度',
  completeness: '完整性',
  structure: '结构化',
  specificity: '具体性',
  actionability: '可执行性'
};

// 获取评分颜色
const getScoreColor = (score: number): string => {
  if (score >= 9) return '#52c41a'; // 绿色 - 优秀
  if (score >= 8) return '#73d13d'; // 浅绿 - 良好
  if (score >= 7) return '#faad14'; // 黄色 - 中等
  if (score >= 6) return '#fa8c16'; // 橙色 - 及格
  return '#f5222d'; // 红色 - 需改进
};

// 获取等级颜色
const getGradeColor = (grade: string): string => {
  switch (grade) {
    case '优秀': return 'green';
    case '良好': return 'blue';
    case '中等': return 'gold';
    case '及格': return 'orange';
    case '需改进': return 'red';
    default: return 'default';
  }
};

const QualityScoreCard: React.FC<QualityScoreCardProps> = ({
  beforeScore,
  afterScore,
  showComparison = false,
  loading = false,
  className
}) => {
  // 计算改进幅度
  const improvement = useMemo(() => {
    if (!beforeScore) return null;
    return {
      overall: afterScore.overall - beforeScore.overall,
      detailed: Object.keys(afterScore.detailed).reduce((acc, key) => {
        const k = key as keyof DetailedScores;
        acc[k] = afterScore.detailed[k] - beforeScore.detailed[k];
        return acc;
      }, {} as DetailedScores)
    };
  }, [beforeScore, afterScore]);

  // 圆形进度条配置
  const circleProgressProps = {
    type: "circle" as const,
    size: 120,
    strokeWidth: 8,
    format: (percent?: number) => (
      <div className="text-center">
        <div className="text-2xl font-bold text-gray-800">
          {(percent! / 10).toFixed(1)}
        </div>
        <div className="text-xs text-gray-500">
          / 10
        </div>
      </div>
    )
  };

  return (
    <Card 
      title={
        <Space>
          <TrophyOutlined className="text-yellow-500" />
          <span>质量评分</span>
        </Space>
      }
      loading={loading}
      className={`quality-score-card ${className || ''}`}
    >
      <Row gutter={24}>
        {/* 总体评分 */}
        <Col xs={24} md={12} lg={8}>
          <div className="text-center">
            <Progress
              {...circleProgressProps}
              percent={afterScore.overall * 10}
              strokeColor={getScoreColor(afterScore.overall)}
              trailColor="#f0f0f0"
            />
            <div className="mt-3">
              <Tag 
                color={getGradeColor(afterScore.grade)} 
                className="text-sm px-3 py-1"
              >
                {afterScore.grade}
              </Tag>
              {improvement && (
                <div className="mt-2">
                  <Statistic
                    value={improvement.overall}
                    precision={1}
                    valueStyle={{ 
                      color: improvement.overall >= 0 ? '#3f8600' : '#cf1322',
                      fontSize: '14px'
                    }}
                    prefix={
                      improvement.overall >= 0 ? 
                        <ArrowUpOutlined /> : 
                        <ArrowDownOutlined />
                    }
                    suffix="分"
                    title={
                      <Text type="secondary" className="text-xs">
                        较优化前
                      </Text>
                    }
                  />
                </div>
              )}
            </div>
          </div>
        </Col>

        {/* 详细评分 */}
        <Col xs={24} md={12} lg={16}>
          <div className="detailed-scores">
            <Title level={5} className="mb-4">详细评分</Title>
            <div className="space-y-3">
              {Object.entries(afterScore.detailed).map(([key, value]) => {
                const k = key as keyof DetailedScores;
                const improvementValue = improvement?.detailed[k] || 0;
                
                return (
                  <div key={key} className="score-item">
                    <div className="flex justify-between items-center mb-1">
                      <Text className="font-medium">{SCORE_LABELS[k]}</Text>
                      <div className="flex items-center space-x-2">
                        <Text strong className="text-sm">
                          {value.toFixed(1)}/10
                        </Text>
                        {showComparison && improvement && (
                          <Text 
                            className={`text-xs ${
                              improvementValue >= 0 ? 'text-green-600' : 'text-red-600'
                            }`}
                          >
                            {improvementValue >= 0 ? '+' : ''}{improvementValue.toFixed(1)}
                          </Text>
                        )}
                      </div>
                    </div>
                    <Progress
                      percent={value * 10}
                      showInfo={false}
                      strokeColor={getScoreColor(value)}
                      trailColor="#f0f0f0"
                      size="small"
                    />
                  </div>
                );
              })}
            </div>
          </div>
        </Col>
      </Row>

      {/* 对比模式下的统计信息 */}
      {showComparison && beforeScore && improvement && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <Title level={5} className="mb-3">优化效果</Title>
          <Row gutter={16}>
            <Col span={8}>
              <Statistic
                title="总体提升"
                value={improvement.overall}
                precision={1}
                valueStyle={{ 
                  color: improvement.overall >= 0 ? '#3f8600' : '#cf1322'
                }}
                prefix={
                  improvement.overall >= 0 ? 
                    <ArrowUpOutlined /> : 
                    <ArrowDownOutlined />
                }
                suffix="分"
              />
            </Col>
            <Col span={8}>
              <Statistic
                title="提升幅度"
                value={((improvement.overall / beforeScore.overall) * 100)}
                precision={1}
                valueStyle={{ color: '#1890ff' }}
                suffix="%"
              />
            </Col>
            <Col span={8}>
              <Statistic
                title="最大提升项"
                value={(() => {
                  const maxKey = Object.entries(improvement.detailed)
                    .reduce((a, b) => a[1] > b[1] ? a : b)[0];
                  return SCORE_LABELS[maxKey as keyof DetailedScores];
                })()}
                valueStyle={{ color: '#722ed1' }}
              />
            </Col>
          </Row>
        </div>
      )}

      {/* 评分说明 */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <Text type="secondary" className="text-xs block mb-2">评分说明：</Text>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
            <span>9-10分：优秀</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>
            <span>8-9分：良好</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-yellow-500 rounded mr-2"></div>
            <span>7-8分：中等</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-orange-500 rounded mr-2"></div>
            <span>6-7分：及格</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default QualityScoreCard; 