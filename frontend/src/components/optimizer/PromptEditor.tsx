import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Input, Typography, Button, Space, Dropdown, message } from 'antd';
import { 
  CopyOutlined, 
  DeleteOutlined, 
  ClearOutlined,
  HistoryOutlined,
  FullscreenOutlined
} from '@ant-design/icons';

const { TextArea } = Input;
const { Text } = Typography;

export interface PromptEditorProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  maxLength?: number;
  showCharCount?: boolean;
  disabled?: boolean;
  onFocus?: () => void;
  onBlur?: () => void;
  className?: string;
}

const PromptEditor: React.FC<PromptEditorProps> = ({
  value,
  onChange,
  placeholder = "请输入您的提示词...\n\n示例：\n- 帮我写一篇关于AI的文章\n- 解释什么是机器学习\n- 写一个Python函数计算斐波那契数列",
  maxLength = 10000,
  showCharCount = true,
  disabled = false,
  onFocus,
  onBlur,
  className
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const textAreaRef = useRef<any>(null);

  // 保存输入历史
  const saveToHistory = useCallback((text: string) => {
    if (text.trim() && text.length > 10) {
      setHistory(prev => {
        const newHistory = [text, ...prev.filter(item => item !== text)];
        return newHistory.slice(0, 5); // 保持最近5条记录
      });
    }
  }, []);

  // 处理输入变化
  const handleChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    onChange(newValue);
  }, [onChange]);

  // 处理焦点事件
  const handleFocus = useCallback(() => {
    setIsFocused(true);
    onFocus?.();
  }, [onFocus]);

  const handleBlur = useCallback(() => {
    setIsFocused(false);
    saveToHistory(value);
    onBlur?.();
  }, [onBlur, value, saveToHistory]);

  // 快捷键处理
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    // Ctrl+Enter 快捷提交（由父组件处理）
    if (e.ctrlKey && e.key === 'Enter') {
      e.preventDefault();
      // 触发自定义事件
      const customEvent = new CustomEvent('prompt-submit', { detail: value });
      document.dispatchEvent(customEvent);
    }
    
    // Ctrl+A 全选
    if (e.ctrlKey && e.key === 'a') {
      e.preventDefault();
      textAreaRef.current?.select();
    }
  }, [value]);

  // 复制到剪贴板
  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(value);
      message.success('已复制到剪贴板');
    } catch (error) {
      message.error('复制失败');
    }
  }, [value]);

  // 从剪贴板粘贴
  const handlePaste = useCallback(async () => {
    try {
      const text = await navigator.clipboard.readText();
      onChange(text);
      message.success('已从剪贴板粘贴');
    } catch (error) {
      message.error('粘贴失败');
    }
  }, [onChange]);

  // 清空内容
  const handleClear = useCallback(() => {
    onChange('');
    textAreaRef.current?.focus();
  }, [onChange]);

  // 使用历史记录
  const handleUseHistory = useCallback((historyText: string) => {
    onChange(historyText);
    textAreaRef.current?.focus();
  }, [onChange]);

  // 全屏编辑
  const handleFullscreen = useCallback(() => {
    if (textAreaRef.current) {
      textAreaRef.current.requestFullscreen?.();
    }
  }, []);

  // 历史记录下拉菜单
  const historyMenuItems = history.map((item, index) => ({
    key: index,
    label: (
      <div className="max-w-xs truncate" title={item}>
        {item.length > 50 ? `${item.substring(0, 50)}...` : item}
      </div>
    ),
    onClick: () => handleUseHistory(item)
  }));

  // 字符统计信息
  const charStats = {
    current: value.length,
    max: maxLength,
    percentage: (value.length / maxLength) * 100,
    words: value.trim().split(/\s+/).filter(word => word.length > 0).length,
    lines: value.split('\n').length
  };

  return (
    <div className={`prompt-editor ${className || ''}`}>
      {/* 工具栏 */}
      <div className="flex justify-between items-center mb-3">
        <div className="flex items-center space-x-2">
          <Text type="secondary" className="text-sm">
            提示词编辑器
          </Text>
          {showCharCount && (
            <Text 
              type={charStats.percentage > 90 ? "warning" : "secondary"}
              className="text-xs"
            >
              {charStats.current}/{charStats.max} 字符 • {charStats.words} 词 • {charStats.lines} 行
            </Text>
          )}
        </div>
        
        <Space size="small">
          <Button 
            size="small" 
            icon={<CopyOutlined />} 
            onClick={handleCopy}
            disabled={!value}
            title="复制内容 (Ctrl+C)"
          />
          <Button 
            size="small" 
            icon={<DeleteOutlined />} 
            onClick={handlePaste}
            title="粘贴内容 (Ctrl+V)"
          />
          <Button 
            size="small" 
            icon={<ClearOutlined />} 
            onClick={handleClear}
            disabled={!value}
            title="清空内容"
          />
          {history.length > 0 && (
            <Dropdown
              menu={{ items: historyMenuItems }}
              placement="bottomRight"
              trigger={['click']}
            >
              <Button 
                size="small" 
                icon={<HistoryOutlined />}
                title="历史记录"
              />
            </Dropdown>
          )}
          <Button 
            size="small" 
            icon={<FullscreenOutlined />} 
            onClick={handleFullscreen}
            title="全屏编辑"
          />
        </Space>
      </div>

      {/* 文本输入区域 */}
      <div className="relative">
        <TextArea
          ref={textAreaRef}
          value={value}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          maxLength={maxLength}
          autoSize={{ minRows: 8, maxRows: 20 }}
          className={`prompt-textarea ${isFocused ? 'focused' : ''}`}
          style={{
            fontFamily: 'Monaco, "JetBrains Mono", "Courier New", monospace',
            fontSize: '14px',
            lineHeight: '1.6',
            border: isFocused ? '2px solid #1890ff' : '1px solid #d9d9d9',
            borderRadius: '6px',
            transition: 'border-color 0.2s ease'
          }}
        />
        
        {/* 字符计数指示器 */}
        {showCharCount && (
          <div className="absolute bottom-2 right-2 bg-white bg-opacity-80 px-2 py-1 rounded text-xs">
            <span 
              className={charStats.percentage > 90 ? 'text-orange-500' : 'text-gray-500'}
            >
              {charStats.current}/{charStats.max}
            </span>
          </div>
        )}
      </div>

      {/* 提示信息 */}
      <div className="flex justify-between items-center mt-2">
        <Text type="secondary" className="text-xs">
          支持 Ctrl+Enter 快速提交，Ctrl+A 全选
        </Text>
        {charStats.percentage > 80 && (
          <Text type="warning" className="text-xs">
            {charStats.percentage > 95 ? '字符即将达到上限' : '字符数较多，请注意'}
          </Text>
        )}
      </div>
    </div>
  );
};

export default PromptEditor; 