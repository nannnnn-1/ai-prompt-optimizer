import React, { useState, useCallback } from 'react';
import { Select, Row, Col, Button, Modal, Form, Input, Typography, Card, Space, Tooltip } from 'antd';
import { SettingOutlined, InfoCircleOutlined } from '@ant-design/icons';

const { Option } = Select;
const { Text, Title } = Typography;
const { TextArea } = Input;

export interface OptimizationConfig {
  type: 'general' | 'code' | 'writing' | 'analysis';
  level: 'quick' | 'standard' | 'detailed';
  audience: 'beginner' | 'professional' | 'expert';
  preferences: {
    language?: string;
    style?: string;
    format?: string;
    context?: string;
  };
}

export interface OptimizationOptionsProps {
  config: OptimizationConfig;
  onChange: (config: OptimizationConfig) => void;
  disabled?: boolean;
  className?: string;
}

// 选项配置
const OPTIMIZATION_TYPES = [
  {
    value: 'general',
    label: '通用优化',
    description: '适用于大多数场景的通用优化策略',
    icon: '🌟'
  },
  {
    value: 'code',
    label: '代码相关',
    description: '针对编程、技术问题的专业优化',
    icon: '💻'
  },
  {
    value: 'writing',
    label: '写作助手',
    description: '优化写作、文档、创意类提示词',
    icon: '✍️'
  },
  {
    value: 'analysis',
    label: '分析解读',
    description: '数据分析、逻辑推理类优化',
    icon: '📊'
  }
];

const OPTIMIZATION_LEVELS = [
  {
    value: 'quick',
    label: '快速优化',
    description: '基础优化，速度快',
    time: '< 30秒'
  },
  {
    value: 'standard',
    label: '标准优化',
    description: '平衡速度和质量',
    time: '30-60秒'
  },
  {
    value: 'detailed',
    label: '详细优化',
    description: '深度优化，质量最高',
    time: '1-2分钟'
  }
];

const TARGET_AUDIENCES = [
  {
    value: 'beginner',
    label: '初学者',
    description: '简单易懂的表达方式'
  },
  {
    value: 'professional',
    label: '专业人士',
    description: '专业术语和标准表达'
  },
  {
    value: 'expert',
    label: '专家级别',
    description: '高级概念和深度内容'
  }
];

const OptimizationOptions: React.FC<OptimizationOptionsProps> = ({
  config,
  onChange,
  disabled = false,
  className
}) => {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [form] = Form.useForm();

  // 更新配置
  const updateConfig = useCallback((updates: Partial<OptimizationConfig>) => {
    onChange({ ...config, ...updates });
  }, [config, onChange]);

  // 处理高级设置
  const handleAdvancedSettings = useCallback(() => {
    form.setFieldsValue(config.preferences);
    setShowAdvanced(true);
  }, [config.preferences, form]);

  const handleAdvancedOk = useCallback(() => {
    form.validateFields().then(values => {
      updateConfig({
        preferences: { ...config.preferences, ...values }
      });
      setShowAdvanced(false);
    });
  }, [form, config.preferences, updateConfig]);

  // 重置为默认配置
  const handleReset = useCallback(() => {
    const defaultConfig: OptimizationConfig = {
      type: 'general',
      level: 'standard',
      audience: 'professional',
      preferences: {}
    };
    onChange(defaultConfig);
  }, [onChange]);

  return (
    <div className={`optimization-options ${className || ''}`}>
      <Card 
        title={
          <Space>
            <SettingOutlined />
            <span>优化选项</span>
          </Space>
        }
        size="small"
        extra={
          <Button 
            type="link" 
            size="small" 
            onClick={handleReset}
            disabled={disabled}
          >
            重置
          </Button>
        }
      >
        <Row gutter={[16, 16]}>
          {/* 优化类型 */}
          <Col span={8}>
            <div className="option-group">
              <Text strong className="option-label">
                优化类型
                <Tooltip title="选择适合您场景的优化策略">
                  <InfoCircleOutlined className="ml-1 text-gray-400" />
                </Tooltip>
              </Text>
              <Select
                value={config.type}
                onChange={(type) => updateConfig({ type })}
                disabled={disabled}
                className="w-full mt-1"
                placeholder="选择优化类型"
              >
                {OPTIMIZATION_TYPES.map(item => (
                  <Option key={item.value} value={item.value}>
                    <Space>
                      <span>{item.icon}</span>
                      <div>
                        <div>{item.label}</div>
                        <Text type="secondary" className="text-xs">
                          {item.description}
                        </Text>
                      </div>
                    </Space>
                  </Option>
                ))}
              </Select>
            </div>
          </Col>

          {/* 优化等级 */}
          <Col span={8}>
            <div className="option-group">
              <Text strong className="option-label">
                优化等级
                <Tooltip title="选择优化的深度和耗时">
                  <InfoCircleOutlined className="ml-1 text-gray-400" />
                </Tooltip>
              </Text>
              <Select
                value={config.level}
                onChange={(level) => updateConfig({ level })}
                disabled={disabled}
                className="w-full mt-1"
                placeholder="选择优化等级"
              >
                {OPTIMIZATION_LEVELS.map(item => (
                  <Option key={item.value} value={item.value}>
                    <div>
                      <div className="flex justify-between">
                        <span>{item.label}</span>
                        <Text type="secondary" className="text-xs">
                          {item.time}
                        </Text>
                      </div>
                      <Text type="secondary" className="text-xs">
                        {item.description}
                      </Text>
                    </div>
                  </Option>
                ))}
              </Select>
            </div>
          </Col>

          {/* 目标受众 */}
          <Col span={8}>
            <div className="option-group">
              <Text strong className="option-label">
                目标受众
                <Tooltip title="选择提示词的目标使用群体">
                  <InfoCircleOutlined className="ml-1 text-gray-400" />
                </Tooltip>
              </Text>
              <Select
                value={config.audience}
                onChange={(audience) => updateConfig({ audience })}
                disabled={disabled}
                className="w-full mt-1"
                placeholder="选择目标受众"
              >
                {TARGET_AUDIENCES.map(item => (
                  <Option key={item.value} value={item.value}>
                    <div>
                      <div>{item.label}</div>
                      <Text type="secondary" className="text-xs">
                        {item.description}
                      </Text>
                    </div>
                  </Option>
                ))}
              </Select>
            </div>
          </Col>
        </Row>

        {/* 高级设置按钮 */}
        <div className="mt-4 text-center">
          <Button 
            type="dashed" 
            onClick={handleAdvancedSettings}
            disabled={disabled}
            icon={<SettingOutlined />}
          >
            高级设置
          </Button>
        </div>

        {/* 当前配置预览 */}
        <div className="mt-4 p-3 bg-gray-50 rounded">
          <Text type="secondary" className="text-xs block mb-2">当前配置：</Text>
          <Space size="small" wrap>
            <Text className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
              {OPTIMIZATION_TYPES.find(t => t.value === config.type)?.label}
            </Text>
            <Text className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
              {OPTIMIZATION_LEVELS.find(l => l.value === config.level)?.label}
            </Text>
            <Text className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
              {TARGET_AUDIENCES.find(a => a.value === config.audience)?.label}
            </Text>
            {Object.keys(config.preferences).length > 0 && (
              <Text className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded">
                已设置偏好
              </Text>
            )}
          </Space>
        </div>
      </Card>

      {/* 高级设置弹窗 */}
      <Modal
        title="高级设置"
        open={showAdvanced}
        onOk={handleAdvancedOk}
        onCancel={() => setShowAdvanced(false)}
        width={600}
        okText="保存"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="language"
                label="首选语言"
                tooltip="指定AI回答时使用的语言"
              >
                <Select placeholder="选择语言">
                  <Option value="zh">中文</Option>
                  <Option value="en">English</Option>
                  <Option value="auto">自动检测</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="style"
                label="回答风格"
                tooltip="指定AI回答的语言风格"
              >
                <Select placeholder="选择风格">
                  <Option value="formal">正式</Option>
                  <Option value="casual">轻松</Option>
                  <Option value="academic">学术</Option>
                  <Option value="creative">创意</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="format"
            label="输出格式"
            tooltip="指定期望的回答格式"
          >
            <Select placeholder="选择格式">
              <Option value="text">纯文本</Option>
              <Option value="markdown">Markdown</Option>
              <Option value="list">列表形式</Option>
              <Option value="step">步骤说明</Option>
              <Option value="code">代码示例</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="context"
            label="额外上下文"
            tooltip="提供额外的背景信息或特殊要求"
          >
            <TextArea
              rows={4}
              placeholder="请输入额外的上下文信息或特殊要求..."
              maxLength={500}
              showCount
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default OptimizationOptions; 