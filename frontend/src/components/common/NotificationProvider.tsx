import React, { useEffect } from 'react';
import { notification } from 'antd';
import { useUIStore } from '../../store/uiStore';
import type { NotificationInstance } from 'antd/es/notification/interface';

export const NotificationProvider: React.FC = () => {
  const { notifications, removeNotification } = useUIStore();
  const [api, contextHolder] = notification.useNotification();

  useEffect(() => {
    // 显示新的通知
    notifications.forEach((notif) => {
      const config = {
        key: notif.id,
        message: notif.title,
        description: notif.message,
        duration: notif.duration ? notif.duration / 1000 : 4, // 转换为秒
        onClose: () => removeNotification(notif.id),
      };

      switch (notif.type) {
        case 'success':
          api.success(config);
          break;
        case 'error':
          api.error(config);
          break;
        case 'warning':
          api.warning(config);
          break;
        case 'info':
        default:
          api.info(config);
          break;
      }
    });
  }, [notifications, api, removeNotification]);

  return <>{contextHolder}</>;
}; 