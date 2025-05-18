import { useRef, useEffect } from 'react';
import { useChat } from '../../hooks/useChat';
import { ChatInput } from './ChatInput';
import { Message } from './Message';
import { LoadingIndicator } from './LoadingIndicator';
import styles from './Chat.module.css';

export function Chat() {
  const initialMessage = {
    role: 'assistant' as const,
    content: 'Hello! I\'m an AI assistant. How can I help you today?',
    timestamp: new Date()
  };
  
  const { messages, isLoading, sendMessage } = useChat([initialMessage]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  return (
    <div className={styles['chat-container']}>
      <div className={styles['messages-container']}>
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <LoadingIndicator />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
    </div>
  );
}
