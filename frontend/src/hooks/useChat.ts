import { useState, useRef, useCallback } from 'react';
import type { ChatMessage } from '../types/ChatMessage';
import { streamChatMessage } from '../services/chatService';

export function useChat(initialMessages: ChatMessage[] = []) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<(() => void) | null>(null);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;
    
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setIsStreaming(true);
    
    // Create an initial empty assistant message
    const assistantMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date()
    };
    
    // Add the empty message that will be updated with streaming content
    setMessages(prev => [...prev, assistantMessage]);
    
    // Start streaming
    abortControllerRef.current = await streamChatMessage(
      [...messages, userMessage],
      (chunk: string) => {
        setMessages(currentMessages => {
          const lastMessageIndex = currentMessages.length - 1;
          const updatedMessages = [...currentMessages];
          updatedMessages[lastMessageIndex] = {
            ...updatedMessages[lastMessageIndex],
            content: updatedMessages[lastMessageIndex].content + chunk
          };
          return updatedMessages;
        });
      },
      () => {
        setIsLoading(false);
        setIsStreaming(false);
        abortControllerRef.current = null;
      },
      (error: Error) => {
        console.error('Streaming error:', error);
        setIsLoading(false);
        setIsStreaming(false);
        abortControllerRef.current = null;
        
        // Update the last message with an error message
        setMessages(currentMessages => {
          const lastMessageIndex = currentMessages.length - 1;
          const updatedMessages = [...currentMessages];
          updatedMessages[lastMessageIndex] = {
            ...updatedMessages[lastMessageIndex],
            content: 'Sorry, I encountered an error. Please try again later.'
          };
          return updatedMessages;
        });
      }
    );
  };

  const cancelStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current();
      abortControllerRef.current = null;
      setIsLoading(false);
      setIsStreaming(false);
    }
  }, []);

  return {
    messages,
    isLoading,
    isStreaming,
    sendMessage,
    cancelStream
  };
}
