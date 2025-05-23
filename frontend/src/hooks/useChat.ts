import { useState, useRef, useCallback } from 'react';
import type { ChatMessage } from '../types/ChatMessage';
import { streamChatMessage } from '../services/chatService';

export function useChat(initialMessages: ChatMessage[] = []) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const streamControllerRef = useRef<{ abort: () => void } | null>(null);

  const appendMessage = useCallback((message: ChatMessage) => {
    setMessages(prev => [...prev, message]);
  }, []);

  const updateLastMessage = useCallback((content: string) => {
    setMessages(currentMessages => {
      const lastMessageIndex = currentMessages.length - 1;
      if (lastMessageIndex < 0) return currentMessages;

      const updatedMessages = [...currentMessages];
      updatedMessages[lastMessageIndex] = {
        ...updatedMessages[lastMessageIndex],
        content: updatedMessages[lastMessageIndex].content + content,
      };
      return updatedMessages;
    });
  }, []);

  const finalizeLastMessage = useCallback(() => {
    setMessages(currentMessages => {
      const lastMessageIndex = currentMessages.length - 1;
      if (lastMessageIndex < 0) return currentMessages;

      const updatedMessages = [...currentMessages];
      updatedMessages[lastMessageIndex] = {
        ...updatedMessages[lastMessageIndex],
        isStreaming: false,
      };
      return updatedMessages;
    });
  }, []);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date(),
    };

    appendMessage(userMessage);
    setIsLoading(true);

    const assistantMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true,
    };

    appendMessage(assistantMessage);

    streamControllerRef.current = streamChatMessage(
      [...messages, userMessage],
      updateLastMessage,
      () => {
        setIsLoading(false);
        finalizeLastMessage();
        streamControllerRef.current = null;
      },
      (error: Error) => {
        console.error('Streaming error:', error);
        setIsLoading(false);
        finalizeLastMessage();
        streamControllerRef.current = null;

        setMessages(currentMessages => {
          const lastMessageIndex = currentMessages.length - 1;
          const updatedMessages = [...currentMessages];
          updatedMessages[lastMessageIndex] = {
            ...updatedMessages[lastMessageIndex],
            content: 'Sorry, I encountered an error. Please try again later.',
          };
          return updatedMessages;
        });
      }
    );
  };

  const cancelStream = useCallback(() => {
    if (streamControllerRef.current) {
      streamControllerRef.current.abort();
      streamControllerRef.current = null;
      setIsLoading(false);
      finalizeLastMessage();
    }
  }, [finalizeLastMessage]);

  return {
    messages,
    isLoading,
    isStreaming: isLoading,
    sendMessage,
    cancelStream,
  };
}
