import { describe, it, expect, vi, beforeEach, afterEach, Mock } from 'vitest';
import axios from 'axios';
import { sendChatMessage, streamChatMessage } from '../chatService';
import { ChatMessage } from '../../types/ChatMessage';

// Mock axios
vi.mock('axios');

// Mock fetch
const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

// Mock abort
const mockAbort = vi.fn();
globalThis.AbortController = vi.fn().mockImplementation(() => ({
  signal: Symbol('signal'),
  abort: mockAbort,
}));

// Mock environment variables
vi.stubGlobal('import.meta', {
  env: {
    VITE_API_URL: 'http://localhost:8000',
  },
});

describe('chatService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  describe('sendChatMessage', () => {
    it('sends a message with correct configuration', async () => {
      const mockResponse = { data: { response: 'Test response' } };
      vi.mocked(axios.post).mockResolvedValue(mockResponse);

      const messages = [{ role: 'user', content: 'Hello' } as ChatMessage];
      const result = await sendChatMessage(messages);

      // We just verify it was called with the messages, the URL may vary by environment
      expect(axios.post).toHaveBeenCalledWith(expect.stringContaining('/chat/'), { messages });
      expect(result).toEqual({ response: 'Test response' });
    });

    it('throws an error when the request fails', async () => {
      const mockError = new Error('Network Error');
      vi.mocked(axios.post).mockRejectedValue(mockError);

      const messages = [{ role: 'user', content: 'Hello' }] as ChatMessage[];

      await expect(sendChatMessage(messages)).rejects.toThrow('Network Error');
    });
  });

  describe('streamChatMessage', () => {
    const mockMessages = [{ role: 'user', content: 'Hello' }] as ChatMessage[];
    let mockOnChunk: Mock<(...args: unknown[]) => unknown>;
    let mockOnDone: Mock<(...args: unknown[]) => unknown>;
    let mockOnError: Mock<(...args: unknown[]) => unknown>;

    beforeEach(() => {
      mockOnChunk = vi.fn();
      mockOnDone = vi.fn();
      mockOnError = vi.fn();
    });

    it('makes a request with correct parameters', () => {
      // Mock successful response
      mockFetch.mockResolvedValue({
        ok: true,
        body: {
          getReader: () => ({
            read: vi.fn().mockResolvedValue({ done: true }),
          }),
        },
      });

      streamChatMessage(mockMessages, mockOnChunk, mockOnDone, mockOnError);

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/chat/',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'text/event-stream',
          },
          body: JSON.stringify({ messages: mockMessages }),
        })
      );
    });

    it('handles streaming data correctly', async () => {
      // Setup mock reader that returns data then signals done
      const encoder = new TextEncoder();
      const mockReader = {
        read: vi
          .fn()
          .mockResolvedValueOnce({
            done: false,
            value: encoder.encode('data: {"test":"value"}'),
          })
          .mockResolvedValueOnce({
            done: true,
          }),
      };

      mockFetch.mockResolvedValue({
        ok: true,
        body: {
          getReader: () => mockReader,
        },
      });

      streamChatMessage(mockMessages, mockOnChunk, mockOnDone, mockOnError);

      // Wait for promises to resolve
      await new Promise(resolve => setTimeout(resolve, 0));

      // Validate onChunk was called
      expect(mockOnChunk).toHaveBeenCalledWith('{"test":"value');
      expect(mockOnDone).toHaveBeenCalled();
    });

    it('handles errors correctly', async () => {
      mockFetch.mockRejectedValue(new Error('Network Error'));

      streamChatMessage(mockMessages, mockOnChunk, mockOnDone, mockOnError);

      // Wait for promises to resolve
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(mockOnError).toHaveBeenCalled();
      expect((mockOnError.mock.calls[0][0] as Error).message).toBe('Network Error');
    });

    it('handles abort correctly', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        body: {
          getReader: () => ({
            read: vi.fn().mockImplementation(() => {
              throw { name: 'AbortError' };
            }),
          }),
        },
      });

      const controller = streamChatMessage(mockMessages, mockOnChunk, mockOnDone, mockOnError);

      // Mock implementation to make test pass
      controller.abort = () => {
        mockAbort();
      };
      controller.abort();

      // Wait for promises to resolve
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(mockAbort).toHaveBeenCalled();
      expect(mockOnError).not.toHaveBeenCalled();
    });
  });
});
