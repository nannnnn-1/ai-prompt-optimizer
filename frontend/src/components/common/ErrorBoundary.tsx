import React, { Component } from 'react';
import type { ReactNode } from 'react';
import { Result, Button } from 'antd';
import { ExclamationCircleOutlined } from '@ant-design/icons';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    // 更新状态以显示错误UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // 记录错误信息
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    // 调用错误处理回调
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
  };

  handleRefresh = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      // 如果有自定义的错误UI，使用它
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // 默认的错误UI
      return (
        <div style={{ 
          padding: '48px 24px', 
          textAlign: 'center',
          minHeight: '400px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <Result
            status="error"
            icon={<ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />}
            title="出现了一些问题"
            subTitle={
              <div>
                <p>抱歉，页面遇到了错误。您可以尝试重新加载页面或联系技术支持。</p>
                {process.env.NODE_ENV === 'development' && this.state.error && (
                  <details style={{ 
                    marginTop: '16px', 
                    textAlign: 'left',
                    background: '#f5f5f5',
                    padding: '12px',
                    borderRadius: '4px',
                    fontSize: '12px'
                  }}>
                    <summary>错误详情 (开发模式)</summary>
                    <pre style={{ 
                      whiteSpace: 'pre-wrap', 
                      marginTop: '8px',
                      fontSize: '11px'
                    }}>
                      {this.state.error.stack}
                    </pre>
                  </details>
                )}
              </div>
            }
            extra={[
              <Button 
                type="primary" 
                key="retry"
                onClick={this.handleRetry}
                style={{ marginRight: '8px' }}
              >
                重试
              </Button>,
              <Button 
                key="refresh"
                onClick={this.handleRefresh}
              >
                刷新页面
              </Button>,
            ]}
          />
        </div>
      );
    }

    return this.props.children;
  }
} 