import React, { useState, useEffect, useCallback } from 'react';
import { 
  Row, 
  Col, 
  Card, 
  Typography, 
  Input, 
  Button, 
  Select, 
  Radio, 
  message, 
  Spin, 
  Tag,
  Progress,
  Space,
  Tooltip,
  Modal
} from 'antd';
import { 
  BulbOutlined, 
  ThunderboltOutlined, 
  CopyOutlined, 
  ClearOutlined,
  HistoryOutlined,
  SaveOutlined,
  ShareAltOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons';
import { useUIStore } from '../store/uiStore';
import { optimizerService } from '../services/optimizerService';
import type { 
  OptimizationRequest, 
  OptimizationResult, 
  QualityEvaluation,
  OptimizationImprovement 
} from '../types';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

export const Optimizer: React.FC = () => {
  // 状态管理
  const [originalPrompt, setOriginalPrompt] = useState('');
  const [optimizedPrompt, setOptimizedPrompt] = useState('');
  const [optimizationType, setOptimizationType] = useState<'general' | 'code' | 'writing' | 'analysis'>('general');
  const [userContext, setUserContext] = useState('');
  const [currentResult, setCurrentResult] = useState<OptimizationResult | null>(null);
  const [qualityEvaluation, setQualityEvaluation] = useState<QualityEvaluation | null>(null);
  const [helpModalVisible, setHelpModalVisible] = useState(false);

  // UI状态
  const { loading, setLoading, setModal, addNotification } = useUIStore();
  const isOptimizing = loading.optimize;
  const isEvaluating = loading.load;

  // 自动保存定时器
  const [autoSaveTimer, setAutoSaveTimer] = useState<NodeJS.Timeout | null>(null);

  // 优化处理
  const handleOptimize = useCallback(async () => {
    if (!originalPrompt.trim()) {
      addNotification({
        type: 'warning',
        title: '请输入提示词',
        message: '请先输入需要优化的提示词内容',
      });
      return;
    }

    setLoading('optimize', true);
    
    try {
      const request: OptimizationRequest = {
        original_prompt: originalPrompt,
        optimization_type: optimizationType,
        user_context: userContext || undefined,
      };

      // 执行优化
      const result = await optimizerService.optimizePrompt(request);
      
      // 设置结果
      setCurrentResult(result);
      setOptimizedPrompt(result.optimized_prompt);

      // 成功通知
      addNotification({
        type: 'success',
        title: '优化完成',
        message: `质量评分从 ${result.quality_score_before} 提升到 ${result.quality_score_after}`,
      });

      // 异步获取质量评估（不阻塞主流程）
      if (result.optimized_prompt) {
        optimizerService.evaluateQuality(result.optimized_prompt)
          .then(evaluation => {
            setQualityEvaluation(evaluation);
          })
          .catch(error => {
            console.warn('质量评估失败:', error);
            // 质量评估失败不影响主流程
          });
      }

    } catch (error) {
      console.error('优化失败:', error);
      addNotification({
        type: 'error',
        title: '优化失败',
        message: (error as any)?.message || '优化过程中发生错误，请稍后重试',
      });
    } finally {
      setLoading('optimize', false);
    }
  }, [originalPrompt, optimizationType, userContext, setLoading, addNotification]);

  // 清空内容
  const handleClear = useCallback(() => {
    Modal.confirm({
      title: '确认清空',
      content: '确定要清空所有内容吗？此操作不可撤销。',
      onOk: () => {
        setOriginalPrompt('');
        setOptimizedPrompt('');
        setUserContext('');
        setCurrentResult(null);
        setQualityEvaluation(null);
      },
    });
  }, []);

  // 复制优化结果
  const handleCopy = useCallback(async () => {
    if (!currentResult?.optimized_prompt) return;
    
    try {
      await navigator.clipboard.writeText(currentResult.optimized_prompt);
      addNotification({
        type: 'success',
        title: '复制成功',
        message: '优化后的提示词已复制到剪贴板',
      });
    } catch (error) {
      console.error('复制失败:', error);
      addNotification({
        type: 'error',
        title: '复制失败',
        message: '无法复制到剪贴板，请手动复制',
      });
    }
  }, [currentResult, addNotification]);

  // 保存结果
  const handleSave = useCallback(async () => {
    if (!currentResult) return;
    
    try {
      // TODO: 实现保存功能
      console.log('保存功能待实现:', currentResult);
      addNotification({
        type: 'info',
        title: '保存功能',
        message: '保存功能正在开发中',
      });
    } catch (error) {
      console.error('保存失败:', error);
      addNotification({
        type: 'error',
        title: '保存失败',
        message: '保存失败，请稍后重试',
      });
    }
  }, [currentResult, addNotification]);

  // 分享结果
  const handleShare = useCallback(async () => {
    if (!currentResult) return;
    
    try {
      // TODO: 实现分享功能
      console.log('分享功能待实现:', currentResult);
      addNotification({
        type: 'info',
        title: '分享功能',
        message: '分享功能正在开发中',
      });
    } catch (error) {
      console.error('分享失败:', error);
      addNotification({
        type: 'error',
        title: '分享失败',
        message: '分享失败，请稍后重试',
      });
    }
  }, [currentResult, addNotification]);

  // 自动保存草稿
  const handlePromptChange = useCallback((value: string) => {
    setOriginalPrompt(value);
    
    // 清除之前的定时器
    if (autoSaveTimer) {
      clearTimeout(autoSaveTimer);
    }
    
    // 设置新的自动保存定时器
    const timer = setTimeout(() => {
      localStorage.setItem('prompt_draft', value);
    }, 1000);
    
    setAutoSaveTimer(timer);
  }, [autoSaveTimer]);

  // 组件挂载时恢复草稿
  useEffect(() => {
    const draft = localStorage.getItem('prompt_draft');
    if (draft) {
      setOriginalPrompt(draft);
    }
    
    // 清理定时器
    return () => {
      if (autoSaveTimer) {
        clearTimeout(autoSaveTimer);
      }
    };
  }, []);

  // 渲染改进点
  const renderImprovements = (improvements: OptimizationImprovement[]) => {
    if (!improvements || improvements.length === 0) {
      return <Text type="secondary">暂无改进点信息</Text>;
    }

    return improvements.map((improvement, index) => (
      <div key={`improvement-${index}`} style={{ marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
          <Text strong>{index + 1}. {improvement.type}</Text>
          <Tag color="blue" style={{ marginLeft: '8px' }}>
            改进
          </Tag>
        </div>
        <Text type="secondary">{improvement.description}</Text>
        {improvement.before_text && improvement.after_text && (
          <div style={{ marginTop: '8px', fontSize: '12px' }}>
            <div>
              <Text type="secondary">优化前：</Text>
              <Text code>{improvement.before_text}</Text>
            </div>
            <div style={{ marginTop: '4px' }}>
              <Text type="secondary">优化后：</Text>
              <Text code>{improvement.after_text}</Text>
            </div>
          </div>
        )}
      </div>
    ));
  };

  return (
    <div style={{ padding: '24px', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Row gutter={[24, 24]}>
        {/* 左侧输入区域 */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <BulbOutlined />
                原始提示词
              </Space>
            }
            extra={
              <Tooltip title="查看优化建议">
                <Button 
                  type="text" 
                  icon={<QuestionCircleOutlined />}
                  onClick={() => setHelpModalVisible(true)}
                />
              </Tooltip>
            }
          >
            <div style={{ marginBottom: '16px' }}>
              <TextArea
                value={originalPrompt}
                onChange={(e) => handlePromptChange(e.target.value)}
                placeholder="请输入您需要优化的提示词..."
                autoSize={{ minRows: 8, maxRows: 15 }}
                maxLength={5000}
                showCount
                style={{ marginBottom: '16px' }}
              />
            </div>

            <div style={{ marginBottom: '16px' }}>
              <Text strong>优化类型：</Text>
              <Radio.Group 
                value={optimizationType} 
                onChange={(e) => setOptimizationType(e.target.value)}
                style={{ marginTop: '8px' }}
              >
                <Radio.Button value="general">通用优化</Radio.Button>
                <Radio.Button value="code">代码相关</Radio.Button>
                <Radio.Button value="writing">写作优化</Radio.Button>
                <Radio.Button value="analysis">分析任务</Radio.Button>
              </Radio.Group>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <Text strong>使用场景 (可选)：</Text>
              <TextArea
                value={userContext}
                onChange={(e) => setUserContext(e.target.value)}
                placeholder="请描述使用场景，帮助我们更好地优化..."
                autoSize={{ minRows: 2, maxRows: 4 }}
                maxLength={500}
                showCount
                style={{ marginTop: '8px' }}
              />
            </div>

            <Space>
              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                onClick={handleOptimize}
                loading={isOptimizing}
                disabled={!originalPrompt.trim()}
                size="large"
              >
                {isOptimizing ? '优化中...' : '开始优化'}
              </Button>
              
              <Button
                icon={<ClearOutlined />}
                onClick={handleClear}
                disabled={isOptimizing}
              >
                清空
              </Button>
              
              <Button
                icon={<HistoryOutlined />}
                onClick={() => window.open('/history', '_blank')}
              >
                历史记录
              </Button>
            </Space>
          </Card>
        </Col>

        {/* 右侧结果区域 */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <ThunderboltOutlined />
                优化结果
              </Space>
            }
            extra={
              currentResult && (
                <Space>
                  <Tooltip title="复制优化后的提示词">
                    <Button 
                      icon={<CopyOutlined />} 
                      onClick={handleCopy}
                    />
                  </Tooltip>
                  <Tooltip title="保存到收藏夹">
                    <Button 
                      icon={<SaveOutlined />} 
                      onClick={handleSave}
                      loading={loading.save}
                    />
                  </Tooltip>
                  <Tooltip title="分享结果">
                    <Button 
                      icon={<ShareAltOutlined />} 
                      onClick={handleShare}
                    />
                  </Tooltip>
                </Space>
              )
            }
          >
            {isOptimizing ? (
              <div style={{ textAlign: 'center', padding: '60px 0' }}>
                <Spin size="large" />
                <div style={{ marginTop: '16px' }}>
                  <Text>正在分析和优化您的提示词...</Text>
                </div>
              </div>
            ) : optimizedPrompt ? (
              <>
                <div style={{ marginBottom: '24px' }}>
                  <TextArea
                    value={optimizedPrompt}
                    readOnly
                    autoSize={{ minRows: 8, maxRows: 15 }}
                    style={{ 
                      backgroundColor: '#f8f9fa',
                      border: '2px solid #52c41a'
                    }}
                  />
                </div>

                {/* 质量评分 */}
                {qualityEvaluation && (
                  <div style={{ marginBottom: '24px' }}>
                    <Title level={5}>质量评分</Title>
                    <Row gutter={16}>
                      <Col span={12}>
                        <div style={{ textAlign: 'center' }}>
                          <Progress
                            type="circle"
                            percent={qualityEvaluation.overall_score * 10}
                            format={() => qualityEvaluation.overall_score}
                            strokeColor="#52c41a"
                            size={100}
                          />
                          <div style={{ marginTop: '8px' }}>
                            <Text strong>综合评分</Text>
                          </div>
                        </div>
                      </Col>
                      <Col span={12}>
                        <div style={{ textAlign: 'center' }}>
                          {(() => {
                            const score = qualityEvaluation.overall_score;
                            const grade = score >= 9 ? 'A' : score >= 7 ? 'B' : score >= 5 ? 'C' : 'D';
                            const color = grade === 'A' ? '#52c41a' : 
                                         grade === 'B' ? '#faad14' : 
                                         grade === 'C' ? '#fa8c16' : '#ff4d4f';
                            return (
                              <div style={{ 
                                fontSize: '48px', 
                                fontWeight: 'bold',
                                color: color
                              }}>
                                {grade}
                              </div>
                            );
                          })()}
                          <Text strong>等级</Text>
                        </div>
                      </Col>
                    </Row>
                  </div>
                )}

                {/* 改进点 */}
                {currentResult?.improvements && currentResult.improvements.length > 0 && (
                  <div>
                    <Title level={5}>改进点说明</Title>
                    <div style={{ 
                      maxHeight: '300px', 
                      overflowY: 'auto',
                      padding: '12px',
                      backgroundColor: '#fafafa',
                      borderRadius: '6px'
                    }}>
                      {renderImprovements(currentResult.improvements)}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div style={{ 
                textAlign: 'center', 
                padding: '60px 0',
                color: '#999'
              }}>
                <BulbOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
                <div>
                  <Text type="secondary">输入提示词并点击"开始优化"查看结果</Text>
                </div>
              </div>
            )}
          </Card>
        </Col>
      </Row>

      {/* 帮助模态框 */}
      <Modal
        title="优化建议"
        open={helpModalVisible}
        onCancel={() => setHelpModalVisible(false)}
        footer={null}
        width={600}
      >
        <div>
          <Title level={5}>如何编写更好的提示词？</Title>
          <div style={{ marginBottom: '16px' }}>
            <Text strong>1. 明确目标：</Text>
            <Text>清楚地说明你希望AI完成什么任务</Text>
          </div>
          <div style={{ marginBottom: '16px' }}>
            <Text strong>2. 提供上下文：</Text>
            <Text>给出必要的背景信息和约束条件</Text>
          </div>
          <div style={{ marginBottom: '16px' }}>
            <Text strong>3. 具体化要求：</Text>
            <Text>避免模糊的描述，使用具体的例子</Text>
          </div>
          <div style={{ marginBottom: '16px' }}>
            <Text strong>4. 设定格式：</Text>
            <Text>指定输出的格式和结构</Text>
          </div>
          <div>
            <Text strong>5. 迭代优化：</Text>
            <Text>根据结果不断调整和完善提示词</Text>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Optimizer; 