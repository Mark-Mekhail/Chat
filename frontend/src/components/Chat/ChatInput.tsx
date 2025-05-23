import { useState } from 'react';
import styles from './ChatInput.module.css';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onCancelStream?: () => void;
  isLoading: boolean;
  isStreaming?: boolean;
}

export function ChatInput({
  onSendMessage,
  onCancelStream,
  isLoading,
  isStreaming = false,
}: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    onSendMessage(input);
    setInput('');
  };

  const handleCancel = () => {
    if (onCancelStream) {
      onCancelStream();
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles['input-form']}>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Type your message here..."
        disabled={isLoading}
        className={styles.input}
      />
      {isStreaming && onCancelStream ? (
        <button
          type="button"
          onClick={handleCancel}
          className={`${styles.button} ${styles.cancel}`}
        >
          Stop
        </button>
      ) : (
        <button type="submit" disabled={isLoading || !input.trim()} className={styles.button}>
          Send
        </button>
      )}
    </form>
  );
}
