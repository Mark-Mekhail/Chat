import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Message } from '../../components/Chat/Message';

describe('Message Component', () => {
  it('renders user message correctly', () => {
    const mockMessage = {
      role: 'user' as const,
      content: 'Hello, how are you?',
      timestamp: new Date('2025-05-22T10:30:00'),
    };

    render(<Message message={mockMessage} />);

    expect(screen.getByText('Hello, how are you?')).toBeInTheDocument();
    expect(screen.getByText('10:30:00 AM')).toBeInTheDocument();
  });

  it('renders assistant message correctly', () => {
    const mockMessage = {
      role: 'assistant' as const,
      content: 'I am an AI assistant.',
      timestamp: new Date('2025-05-22T10:31:00'),
    };

    render(<Message message={mockMessage} />);

    expect(screen.getByText('I am an AI assistant.')).toBeInTheDocument();
    expect(screen.getByText('10:31:00 AM')).toBeInTheDocument();
  });

  it('shows loading indicator when streaming with empty content', () => {
    const mockMessage = {
      role: 'assistant' as const,
      content: '',
      timestamp: new Date('2025-05-22T10:32:00'),
    };

    const { container } = render(<Message message={mockMessage} isStreaming={true} />);

    // The LoadingIndicator is rendered inside the message
    const loadingContainer = container.querySelector('[class*="message-content"]');
    expect(loadingContainer?.innerHTML).toContain('small');
  });

  it('shows cursor when streaming with content', () => {
    const mockMessage = {
      role: 'assistant' as const,
      content: 'Typing...',
      timestamp: new Date('2025-05-22T10:33:00'),
    };

    const { container } = render(<Message message={mockMessage} isStreaming={true} />);

    expect(screen.getByText('Typing...')).toBeInTheDocument();

    // Look for the cursor element
    const messageContent = container.querySelector('[class*="message-content"]');
    expect(messageContent?.innerHTML).toContain('cursor-blink');
  });
});
