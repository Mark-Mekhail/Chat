import { ChatMessage } from '../../types/ChatMessage';
import { LoadingIndicator } from './LoadingIndicator';
import styles from './Message.module.css';

interface MessageProps {
  message: ChatMessage;
  isStreaming?: boolean;
}

export function Message({ message, isStreaming = false }: MessageProps) {
  return (
    <div className={`${styles.message} ${styles[message.role]} ${isStreaming ? styles.streaming : ''}`}>
      <div className={styles['message-content']}>
        {message.content}
        {isStreaming && (
          <span className={styles['cursor-blink']}>_</span>
        )}
      </div>
      <div className={styles['message-timestamp']}>
        {message.timestamp?.toLocaleTimeString()}
        {isStreaming && <LoadingIndicator small />}
      </div>
    </div>
  );
}
