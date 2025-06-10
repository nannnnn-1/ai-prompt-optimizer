import React, { useState, useCallback } from 'react';
import { Card, Typography, Tag, Badge, Collapse, Space, Button, Descriptions } from 'antd';
import { 
  CheckCircleOutlined, 
  BulbOutlined, 
  ArrowRightOutlined,
  EditOutlined,
  FileTextOutlined,
  ToolOutlined,
  FormatPainterOutlined
} from '@ant-design/icons';

const { Text, Title, Paragraph } = Typography;
const { Panel } = Collapse;

export interface Improvement {
  id: string;
  type: string;
  description: string;
  beforeText?: string;
  afterText?: string;
  category: 'structure' | 'clarity' | 'content' | 'format';
  impact: 'high' | 'medium' | 'low';
}

export interface ImprovementListProps {
  improvements: Improvement[];
  expanded?: boolean;
  showDetails?: boolean;
  className?: string;
}

// 分类配置
const CATEGORY_CONFIG = {
  structure: {
    label: '结构优化',
    color: 'blue',
    icon: <ToolOutlined />
  },
  clarity: {
    label: '清晰度提升',
    color: 'green',
    icon: <CheckCircleOutlined />
  },
  content: {
    label: '内容完善',
    color: 'purple',
    icon: <FileTextOutlined />
  },
  format: {
    label: '格式规范',
    color: 'orange',
    icon: <FormatPainterOutlined />
  }
};

// 影响程度配置
const IMPACT_CONFIG = {
  high: {
    label: '高',
    color: '#ff4d4f',
    badge: 'error'
  },
  medium: {
    label: '中',
    color: '#faad14',
    badge: 'warning'
  },
  low: {
    label: '低',
    color: '#52c41a',
    badge: 'success'
  }
};

const ImprovementList: React.FC<ImprovementListProps> = ({
  improvements,
  expanded = false,
  showDetails = true,
  className
}) => {
  const [expandedPanels, setExpandedPanels] = useState<string[]>(
    expanded ? improvements.map(item => item.id) : []
  );

  // 处理展开/收起
  const handlePanelChange = useCallback((keys: string | string[]) => {
    setExpandedPanels(Array.isArray(keys) ? keys : [keys]);
  }, []);

  // 全部展开/收起
  const handleExpandAll = useCallback(() => {
    if (expandedPanels.length === improvements.length) {
      setExpandedPanels([]);
    } else {
      setExpandedPanels(improvements.map(item => item.id));
    }
  }, [expandedPanels.length, improvements]);

  // 按分类分组改进点
  const groupedImprovements = improvements.reduce((acc, improvement) => {
    if (!acc[improvement.category]) {
      acc[improvement.category] = [];
    }
    acc[improvement.category].push(improvement);
    return acc;
  }, {} as Record<string, Improvement[]>);

  // 统计信息
  const stats = {
    total: improvements.length,
    byImpact: improvements.reduce((acc, item) => {
      acc[item.impact] = (acc[item.impact] || 0) + 1;
      return acc;
    }, {} as Record<string, number>),
    byCategory: Object.entries(groupedImprovements).map(([category, items]) => ({
      category,
      count: items.length,
      ...CATEGORY_CONFIG[category as keyof typeof CATEGORY_CONFIG]
    }))
  };

  return (
    <Card 
      title={
        <Space>
          <CheckCircleOutlined className="text-green-500" />
          <span>改进列表</span>
          <Text type="secondary" className="text-sm">
            ({improvements.length} 项改进)
          </Text>
        </Space>
      }
      extra={
        showDetails && (
          <Button 
            type="link" 
            size="small"
            onClick={handleExpandAll}
          >
            {expandedPanels.length === improvements.length ? '收起全部' : '展开全部'}
          </Button>
        )
      }
      className={`improvement-list ${className || ''}`}
    >
      {/* 统计概览 */}
      <div className="mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="grid grid-cols-2 gap-4">
          {/* 按影响程度统计 */}
          <div>
            <Text type="secondary" className="text-xs block mb-2">按影响程度：</Text>
            <Space size="small" wrap>
              {Object.entries(stats.byImpact).map(([impact, count]) => (
                <Badge 
                  key={impact}
                  count={count}
                  color={IMPACT_CONFIG[impact as keyof typeof IMPACT_CONFIG].color}
                  size="small"
                >
                  <Tag className="px-2">
                    {IMPACT_CONFIG[impact as keyof typeof IMPACT_CONFIG].label}影响
                  </Tag>
                </Badge>
              ))}
            </Space>
          </div>
          
          {/* 按分类统计 */}
          <div>
            <Text type="secondary" className="text-xs block mb-2">按类型分布：</Text>
            <Space size="small" wrap>
              {stats.byCategory.map(({ category, count, label, color }) => (
                <Tag key={category} color={color} className="text-xs">
                  {label} ({count})
                </Tag>
              ))}
            </Space>
          </div>
        </div>
      </div>

      {/* 改进项列表 */}
      {showDetails ? (
        <Collapse 
          activeKey={expandedPanels}
          onChange={handlePanelChange}
          size="small"
          ghost
        >
          {improvements.map((improvement) => {
            const categoryConfig = CATEGORY_CONFIG[improvement.category];
            const impactConfig = IMPACT_CONFIG[improvement.impact];
            
            return (
              <Panel
                key={improvement.id}
                header={
                  <div className="flex justify-between items-center w-full">
                    <Space>
                      {categoryConfig.icon}
                      <Text strong className="text-sm">
                        {improvement.type}
                      </Text>
                      <Tag color={categoryConfig.color} size="small">
                        {categoryConfig.label}
                      </Tag>
                    </Space>
                    <Badge 
                      color={impactConfig.color}
                      text={
                        <Text className="text-xs">
                          {impactConfig.label}影响
                        </Text>
                      }
                    />
                  </div>
                }
              >
                <div className="pl-6">
                  <Paragraph className="mb-3 text-gray-700">
                    {improvement.description}
                  </Paragraph>
                  
                  {improvement.beforeText && improvement.afterText && (
                    <Descriptions 
                      size="small" 
                      column={1} 
                      bordered
                      className="mt-3"
                    >
                      <Descriptions.Item 
                        label={
                          <Text type="secondary" className="text-xs">
                            优化前
                          </Text>
                        }
                      >
                        <div className="bg-red-50 p-2 rounded border-l-4 border-red-300">
                          <Text className="text-sm font-mono">
                            {improvement.beforeText}
                          </Text>
                        </div>
                      </Descriptions.Item>
                      <Descriptions.Item 
                        label={
                          <Text type="secondary" className="text-xs">
                            优化后
                          </Text>
                        }
                      >
                        <div className="bg-green-50 p-2 rounded border-l-4 border-green-300">
                          <Text className="text-sm font-mono">
                            {improvement.afterText}
                          </Text>
                        </div>
                      </Descriptions.Item>
                    </Descriptions>
                  )}
                </div>
              </Panel>
            );
          })}
        </Collapse>
      ) : (
        <div className="space-y-2">
          {improvements.map((improvement) => {
            const categoryConfig = CATEGORY_CONFIG[improvement.category];
            const impactConfig = IMPACT_CONFIG[improvement.impact];
            
            return (
              <div 
                key={improvement.id} 
                className="flex items-start justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-start space-x-3 flex-1">
                  <div className="flex-shrink-0 mt-1">
                    {categoryConfig.icon}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <Text strong className="text-sm">
                        {improvement.type}
                      </Text>
                      <Tag color={categoryConfig.color} size="small">
                        {categoryConfig.label}
                      </Tag>
                    </div>
                    <Text type="secondary" className="text-xs">
                      {improvement.description}
                    </Text>
                  </div>
                </div>
                <Badge 
                  color={impactConfig.color}
                  text={
                    <Text className="text-xs">
                      {impactConfig.label}
                    </Text>
                  }
                />
              </div>
            );
          })}
        </div>
      )}

      {improvements.length === 0 && (
        <div className="text-center py-8">
          <BulbOutlined className="text-4xl text-gray-300 mb-2" />
          <Text type="secondary">暂无改进建议</Text>
        </div>
      )}
    </Card>
  );
};

export default ImprovementList; 