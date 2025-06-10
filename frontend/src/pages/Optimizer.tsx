import React, { useState } from 'react';
import { Card, Input, Button, Row, Col, Typography, Space, Divider, message, Spin } from 'antd';
import { 
  SendOutlined, 
  ClearOutlined, 
  CopyOutlined, 
  StarOutlined,
  BulbOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';

const { TextArea } = Input;
const { Title, Text, Paragraph } = Typography;

interface OptimizationResult {
  optimizedPrompt: string;
  qualityScore: number;
  improvements: string[];
  suggestions: string[];
}

export const Optimizer: React.FC = () => {
  const [originalPrompt, setOriginalPrompt] = useState('');
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);
  const [isOptimizing, setIsOptimizing] = useState(false);

  const handleOptimize = async () => {
    if (!originalPrompt.trim()) {
      message.warning('请输入要优化的提示词');
      return;
    }

    setIsOptimizing(true);
    
    try {
      // 模拟API调用 - 后续将连接真实后端
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 模拟优化结果
      const mockResult: OptimizationResult = {
        optimizedPrompt: `优化后的提示词：\n\n请作为一个专业的AI助手，帮助我${originalPrompt}。\n\n要求：\n1. 请提供详细的步骤说明\n2. 确保回答准确可靠\n3. 如有疑问请及时询问\n4. 提供相关的最佳实践建议\n\n请按照以上要求进行回应。`,
        qualityScore: 85,
        improvements: [
          '添加了角色定义，明确了AI助手的身份',
          '增加了具体的要求和约束条件',
          '优化了语言表达，更加清晰明确',
          '添加了输出格式的指导'
        ],
        suggestions: [
          '可以进一步添加具体的使用场景',
          '考虑添加输出长度的限制',
          '可以指定回答的语言风格'
        ]
      };
      
      setOptimizationResult(mockResult);
      message.success('提示词优化完成！');
      
    } catch (error) {
      message.error('优化失败，请重试');
      console.error('Optimization error:', error);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleClear = () => {
    setOriginalPrompt('');
    setOptimizationResult(null);
  };

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      message.success('已复制到剪贴板');
    } catch (error) {
      message.error('复制失败');
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <Title level={2} className="mb-2">
          <BulbOutlined className="mr-2 text-primary-500" />
          AI提示词优化器
        </Title>
        <Text type="secondary" className="text-base">
          输入您的提示词，我们将帮助您优化提示词的质量和效果
        </Text>
      </div>

      <Row gutter={[24, 24]}>
        {/* 左侧：原始提示词输入 */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <span>📝 原始提示词</span>
                <Text type="secondary" className="text-sm">
                  ({originalPrompt.length}/2000)
                </Text>
              </Space>
            }
            className="h-full"
          >
            <div className="space-y-4">
              <TextArea
                value={originalPrompt}
                onChange={(e) => setOriginalPrompt(e.target.value)}
                placeholder="请输入您想要优化的提示词...

示例：
- 帮我写一篇关于AI的文章
- 解释什么是机器学习
- 写一个Python函数来计算斐波那契数列"
                rows={12}
                maxLength={2000}
                showCount
                className="resize-none"
              />
              
              <div className="flex justify-between">
                <Button 
                  icon={<ClearOutlined />}
                  onClick={handleClear}
                  disabled={!originalPrompt && !optimizationResult}
                >
                  清空
                </Button>
                
                <Button 
                  type="primary"
                  icon={<SendOutlined />}
                  onClick={handleOptimize}
                  loading={isOptimizing}
                  disabled={!originalPrompt.trim()}
                  size="large"
                >
                  {isOptimizing ? '优化中...' : '开始优化'}
                </Button>
              </div>
            </div>
          </Card>
        </Col>

        {/* 右侧：优化结果展示 */}
        <Col xs={24} lg={12}>
          <Card 
            title="✨ 优化结果"
            className="h-full"
          >
            {isOptimizing ? (
              <div className="flex flex-col items-center justify-center py-16">
                <Spin size="large" />
                <Text className="mt-4 text-gray-500">
                  AI正在分析和优化您的提示词...
                </Text>
              </div>
            ) : optimizationResult ? (
              <div className="space-y-6">
                {/* 质量评分 */}
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <Text strong>质量评分</Text>
                    <div className="flex items-center">
                      <StarOutlined className="text-yellow-500 mr-1" />
                      <Text strong className="text-lg">
                        {optimizationResult.qualityScore}/100
                      </Text>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-green-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${optimizationResult.qualityScore}%` }}
                    />
                  </div>
                </div>

                {/* 优化后的提示词 */}
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <Text strong>优化后的提示词</Text>
                    <Button 
                      size="small" 
                      icon={<CopyOutlined />}
                      onClick={() => handleCopy(optimizationResult.optimizedPrompt)}
                    >
                      复制
                    </Button>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg border">
                    <Paragraph className="mb-0 whitespace-pre-wrap">
                      {optimizationResult.optimizedPrompt}
                    </Paragraph>
                  </div>
                </div>

                {/* 改进点 */}
                <div>
                  <Text strong className="block mb-3">
                    <CheckCircleOutlined className="text-green-500 mr-2" />
                    主要改进点
                  </Text>
                  <ul className="space-y-2">
                    {optimizationResult.improvements.map((improvement, index) => (
                      <li key={index} className="flex items-start">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0" />
                        <Text className="text-sm">{improvement}</Text>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* 优化建议 */}
                <div>
                  <Text strong className="block mb-3">
                    <BulbOutlined className="text-blue-500 mr-2" />
                    进一步建议
                  </Text>
                  <ul className="space-y-2">
                    {optimizationResult.suggestions.map((suggestion, index) => (
                      <li key={index} className="flex items-start">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0" />
                        <Text className="text-sm">{suggestion}</Text>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-16 text-center">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                  <BulbOutlined className="text-2xl text-gray-400" />
                </div>
                <Text className="text-gray-500 mb-2">
                  优化结果将在这里显示
                </Text>
                <Text type="secondary" className="text-sm">
                  请先在左侧输入您的提示词，然后点击"开始优化"
                </Text>
              </div>
            )}
          </Card>
        </Col>
      </Row>

      {/* 使用提示 */}
      <Card className="mt-6" title="💡 使用提示">
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <div className="text-center p-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-blue-600 font-bold">1</span>
              </div>
              <Text strong className="block mb-2">输入提示词</Text>
              <Text type="secondary" className="text-sm">
                在左侧文本框中输入您想要优化的提示词
              </Text>
            </div>
          </Col>
          <Col span={8}>
            <div className="text-center p-4">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-green-600 font-bold">2</span>
              </div>
              <Text strong className="block mb-2">AI智能优化</Text>
              <Text type="secondary" className="text-sm">
                点击"开始优化"，AI将分析并改进您的提示词
              </Text>
            </div>
          </Col>
          <Col span={8}>
            <div className="text-center p-4">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-purple-600 font-bold">3</span>
              </div>
              <Text strong className="block mb-2">查看结果</Text>
              <Text type="secondary" className="text-sm">
                查看优化后的提示词和详细的改进建议
              </Text>
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Optimizer; 