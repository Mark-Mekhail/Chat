import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useChat } from '../useChat';
import { streamChatMessage } from '../../services/chatService';
import { ChatMessage } from '../../types/ChatMessage';

// Mock the chatService
vi.mock('../../services/chatService', () => ({
  streamChatMessage: vi.fn(),
}));

describe('useChat Hook', () => {
  const mockStreamController = {
    abort: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(streamChatMessage).mockReturnValue(mockStreamController);
  });

  it('initializes with correct state', () => {
    const initialMessages = [
      { role: 'user', content: 'Hello', timestamp: new Date() } as ChatMessage,
    ];

    const { result } = renderHook(() => useChat(initialMessages));

    expect(result.current.messages).toEqual(initialMessages);
    expect(result.current.isLoading).toBe(false);
  });

  it('appends user message and creates assistant message when sending', () => {
    const { result } = renderHook(() => useChat([]));

    act(() => {
      result.current.sendMessage('Hello world');
    });

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[0].role).toBe('user');
    expect(result.current.messages[0].content).toBe('Hello world');
    expect(result.current.messages[1].role).toBe('assistant');
    expect(result.current.isLoading).toBe(true);
    expect(streamChatMessage).toHaveBeenCalled();
  });

  it('updates the last message when receiving streaming content', () => {
    const { result } = renderHook(() => useChat([]));

    // Simulate sending a message
    act(() => {
      result.current.sendMessage('Hello');
    });

    // Extract the updateLastMessage callback that was passed to streamChatMessage
    const updateCallback = vi.mocked(streamChatMessage).mock.calls[0][1];

    // Simulate receiving streaming content
    act(() => {
      updateCallback('This is ');
      updateCallback('a response');
    });

    expect(result.current.messages[1].content).toBe('This is a response');
  });

  it('finalizes the last message when streaming ends', () => {
    const { result } = renderHook(() => useChat([]));

    // Simulate sending a message
    act(() => {
      result.current.sendMessage('Hello');
    });

    // Extract the callbacks
    const updateCallback = vi.mocked(streamChatMessage).mock.calls[0][1];
    const doneCallback = vi.mocked(streamChatMessage).mock.calls[0][2];

    // Simulate streaming and completion
    act(() => {
      updateCallback('This is a response');
      doneCallback();
    });

    expect(result.current.messages[1].isStreaming).toBe(false);
    expect(result.current.isLoading).toBe(false);
  });

  it('cancels the stream when requested', () => {
    const { result } = renderHook(() => useChat([]));

    // Simulate sending a message
    act(() => {
      result.current.sendMessage('Hello');
    });

    // Cancel the stream
    act(() => {
      result.current.cancelStream();
    });

    expect(mockStreamController.abort).toHaveBeenCalled();
    expect(result.current.isLoading).toBe(false);
  });

  it('handles errors during streaming', () => {
    const { result } = renderHook(() => useChat([]));

    // Simulate sending a message
    act(() => {
      result.current.sendMessage('Hello');
    });

    // Extract the error callback
    const errorCallback = vi.mocked(streamChatMessage).mock.calls[0][3];

    // Simulate an error
    act(() => {
      errorCallback(new Error('Network error'));
    });

    expect(result.current.messages[1].content).toContain('Sorry');
    expect(result.current.isLoading).toBe(false);
  });
});
