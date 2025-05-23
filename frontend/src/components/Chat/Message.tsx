import { ChatMessage } from '../../types/ChatMessage';
import { LoadingIndicator } from './LoadingIndicator';
import styles from './Message.module.css';

interface MessageProps {
  message: ChatMessage;
  isStreaming?: boolean;
}

export function Message({ message, isStreaming = message.isStreaming }: MessageProps) {
  const showLoadingIndicator = isStreaming && message.content.length === 0;

  return (
    <div
      className={`${styles.message} ${styles[message.role]} ${isStreaming ? styles.streaming : ''}`}
    >
      <div className={styles['message-content']}>
        {message.content}
        {isStreaming && <span className={styles['cursor-blink']}></span>}
        {showLoadingIndicator && <LoadingIndicator small />}
      </div>
      {message.timestamp && (
        <div className={styles['message-timestamp']}>{message.timestamp.toLocaleTimeString()}</div>
      )}
    </div>
  );
}
