import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Chat } from '../Chat/Chat';
import { useChat } from '../../hooks/useChat';

// Mock the useChat hook
vi.mock('../../hooks/useChat', () => ({
  useChat: vi.fn(),
}));

// Mock scrollIntoView which isn't implemented in jsdom
Element.prototype.scrollIntoView = vi.fn();

describe('Chat Component', () => {
  beforeEach(() => {
    // Set up default mock implementation
    vi.mocked(useChat).mockReturnValue({
      messages: [
        {
          role: 'assistant',
          content: "Hello! I'm an AI assistant. How can I help you today?",
          timestamp: new Date('2025-05-22T10:00:00'),
        },
      ],
      isLoading: false,
      isStreaming: false,
      sendMessage: vi.fn(),
      cancelStream: vi.fn(),
    });
  });

  it('renders the initial assistant message', () => {
    render(<Chat />);

    expect(
      screen.getByText("Hello! I'm an AI assistant. How can I help you today?")
    ).toBeInTheDocument();
  });

  it('renders chat input component', () => {
    render(<Chat />);

    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
  });

  it('renders multiple messages correctly', () => {
    vi.mocked(useChat).mockReturnValue({
      messages: [
        {
          role: 'assistant',
          content: "Hello! I'm an AI assistant. How can I help you today?",
          timestamp: new Date('2025-05-22T10:00:00'),
        },
        {
          role: 'user',
          content: 'What can you do?',
          timestamp: new Date('2025-05-22T10:01:00'),
        },
        {
          role: 'assistant',
          content: 'I can help with answering questions.',
          timestamp: new Date('2025-05-22T10:02:00'),
        },
      ],
      isLoading: false,
      isStreaming: false,
      sendMessage: vi.fn(),
      cancelStream: vi.fn(),
    });

    render(<Chat />);

    expect(
      screen.getByText("Hello! I'm an AI assistant. How can I help you today?")
    ).toBeInTheDocument();
    expect(screen.getByText('What can you do?')).toBeInTheDocument();
    expect(screen.getByText('I can help with answering questions.')).toBeInTheDocument();
  });

  it('passes correct props to ChatInput', () => {
    const mockSendMessage = vi.fn();
    const mockCancelStream = vi.fn();

    vi.mocked(useChat).mockReturnValue({
      messages: [
        {
          role: 'assistant',
          content: "Hello! I'm an AI assistant. How can I help you today?",
          timestamp: new Date('2025-05-22T10:00:00'),
        },
      ],
      isLoading: true,
      isStreaming: true,
      sendMessage: mockSendMessage,
      cancelStream: mockCancelStream,
    });

    render(<Chat />);

    // When streaming is true, we should see a Stop button
    expect(screen.getByRole('button', { name: 'Stop' })).toBeInTheDocument();
  });
});
