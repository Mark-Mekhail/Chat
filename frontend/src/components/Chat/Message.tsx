import { ChatMessage } from '../../types/ChatMessage';
import styles from './Message.module.css';

interface MessageProps {
  message: ChatMessage;
}

export function Message({ message }: MessageProps) {
  return (
    <div className={`${styles.message} ${styles[message.role]}`}>
      <div className={styles['message-content']}>{message.content}</div>
      <div className={styles['message-timestamp']}>
        {message.timestamp?.toLocaleTimeString()}
      </div>
    </div>
  );
}
