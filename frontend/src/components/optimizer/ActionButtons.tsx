import React, { useCallback, useState } from 'react';
import { Button, Space, Dropdown, Modal, Typography, message } from 'antd';
import {
  SendOutlined,
  EyeOutlined,
  ClearOutlined,
  ImportOutlined,
  DownOutlined,
  FileTextOutlined,
  CodeOutlined,
  BulbOutlined
} from '@ant-design/icons';

const { Text } = Typography;

export interface ActionState {
  isOptimizing: boolean;
  isPreviewLoading: boolean;
  canSubmit: boolean;
  hasContent: boolean;
}

export interface ActionButtonsProps {
  state: ActionState;
  onOptimize: () => void;
  onPreview: () => void;
  onClear: () => void;
  onImportExample: (example: string) => void;
  disabled?: boolean;
  className?: string;
}

// 示例提示词
const EXAMPLE_PROMPTS = [
  {
    key: 'general',
    label: '通用示例',
    icon: <BulbOutlined />,
    examples: [
      {
        title: '文章写作',
        content: '请帮我写一篇关于人工智能发展历程的文章，要求：\n1. 包含主要里程碑事件\n2. 分析技术发展趋势\n3. 讨论未来展望\n4. 字数控制在1500字左右'
      },
      {
        title: '问题解答',
        content: '请详细解释什么是机器学习，包括：\n1. 基本概念和定义\n2. 主要算法类型\n3. 实际应用场景\n4. 与人工智能的关系'
      },
      {
        title: '学习指导',
        content: '我想学习前端开发，请为我制定一个3个月的学习计划，包括：\n1. 学习路径和顺序\n2. 推荐的学习资源\n3. 实践项目建议\n4. 阶段性目标设定'
      }
    ]
  },
  {
    key: 'code',
    label: '代码相关',
    icon: <CodeOutlined />,
    examples: [
      {
        title: 'Python函数',
        content: '请写一个Python函数来实现二分查找算法，要求：\n1. 函数签名清晰\n2. 包含详细注释\n3. 处理边界情况\n4. 提供使用示例'
      },
      {
        title: '代码优化',
        content: '请帮我优化以下Python代码的性能：\n[在这里粘贴你的代码]\n\n优化要求：\n1. 提高执行效率\n2. 减少内存使用\n3. 保持代码可读性\n4. 解释优化思路'
      },
      {
        title: 'Bug调试',
        content: '我的代码出现了以下错误：\n[错误信息]\n\n代码如下：\n[代码内容]\n\n请帮我：\n1. 分析错误原因\n2. 提供修复方案\n3. 给出预防建议'
      }
    ]
  },
  {
    key: 'writing',
    label: '写作助手',
    icon: <FileTextOutlined />,
    examples: [
      {
        title: '商业提案',
        content: '请帮我写一份AI项目的商业提案，包括：\n1. 项目背景和目标\n2. 技术方案和实施计划\n3. 预期收益和风险分析\n4. 资源需求和时间安排'
      },
      {
        title: '技术文档',
        content: '请为我们的API接口编写技术文档，要求：\n1. 接口描述清晰\n2. 参数说明详细\n3. 包含请求和响应示例\n4. 错误码说明'
      },
      {
        title: '邮件撰写',
        content: '请帮我写一封项目进度汇报邮件给上级，内容包括：\n1. 项目当前状态\n2. 已完成的工作\n3. 遇到的问题和解决方案\n4. 下一步计划'
      }
    ]
  }
];

const ActionButtons: React.FC<ActionButtonsProps> = ({
  state,
  onOptimize,
  onPreview,
  onClear,
  onImportExample,
  disabled = false,
  className
}) => {
  const [showExampleModal, setShowExampleModal] = useState(false);

  // 处理示例导入
  const handleImportExample = useCallback((example: string) => {
    Modal.confirm({
      title: '导入示例',
      content: '导入示例将覆盖当前输入的内容，是否继续？',
      onOk: () => {
        onImportExample(example);
        message.success('示例已导入');
      }
    });
  }, [onImportExample]);

  // 示例下拉菜单
  const exampleMenuItems = EXAMPLE_PROMPTS.map(category => ({
    key: category.key,
    label: category.label,
    icon: category.icon,
    children: category.examples.map((example, index) => ({
      key: `${category.key}-${index}`,
      label: example.title,
      onClick: () => handleImportExample(example.content)
    }))
  }));

  // 更多操作菜单
  const moreMenuItems = [
    {
      key: 'clear',
      label: '清空输入',
      icon: <ClearOutlined />,
      onClick: onClear,
      disabled: !state.hasContent
    },
    {
      key: 'examples',
      label: '导入示例',
      icon: <ImportOutlined />,
      children: exampleMenuItems
    }
  ];

  return (
    <div className={`action-buttons flex justify-between items-center ${className || ''}`}>
      {/* 左侧：辅助操作 */}
      <Space>
        <Button
          icon={<ClearOutlined />}
          onClick={onClear}
          disabled={disabled || !state.hasContent}
          title="清空输入内容"
        >
          清空
        </Button>
        
        <Dropdown
          menu={{ items: exampleMenuItems }}
          placement="topLeft"
          trigger={['click']}
        >
          <Button icon={<ImportOutlined />} disabled={disabled}>
            导入示例 <DownOutlined />
          </Button>
        </Dropdown>
      </Space>

      {/* 右侧：主要操作 */}
      <Space>
        <Button
          icon={<EyeOutlined />}
          onClick={onPreview}
          loading={state.isPreviewLoading}
          disabled={disabled || !state.canSubmit}
          title="预览优化效果"
        >
          {state.isPreviewLoading ? '预览中...' : '预览优化'}
        </Button>

        <Button
          type="primary"
          size="large"
          icon={<SendOutlined />}
          onClick={onOptimize}
          loading={state.isOptimizing}
          disabled={disabled || !state.canSubmit}
          title="开始优化提示词 (Ctrl+Enter)"
        >
          {state.isOptimizing ? '优化中...' : '开始优化'}
        </Button>
      </Space>
    </div>
  );
};

export default ActionButtons; 