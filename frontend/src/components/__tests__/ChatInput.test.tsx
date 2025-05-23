import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ChatInput } from '../Chat/ChatInput';

describe('ChatInput Component', () => {
  it('renders correctly', () => {
    const mockSendMessage = vi.fn();

    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);

    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
  });

  it('disables input when loading', () => {
    const mockSendMessage = vi.fn();

    render(<ChatInput onSendMessage={mockSendMessage} isLoading={true} />);

    expect(screen.getByPlaceholderText('Type your message here...')).toBeDisabled();
  });

  it('shows stop button when streaming', () => {
    const mockSendMessage = vi.fn();
    const mockCancelStream = vi.fn();

    render(
      <ChatInput
        onSendMessage={mockSendMessage}
        isLoading={true}
        isStreaming={true}
        onCancelStream={mockCancelStream}
      />
    );

    expect(screen.getByRole('button', { name: 'Stop' })).toBeInTheDocument();
  });

  it('calls onSendMessage when submitting input', () => {
    const mockSendMessage = vi.fn();

    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);

    const input = screen.getByPlaceholderText('Type your message here...');
    fireEvent.change(input, { target: { value: 'Hello' } });

    const sendButton = screen.getByRole('button', { name: 'Send' });
    fireEvent.click(sendButton);

    expect(mockSendMessage).toHaveBeenCalledWith('Hello');
  });

  it('calls onCancelStream when clicking Stop button', () => {
    const mockSendMessage = vi.fn();
    const mockCancelStream = vi.fn();

    render(
      <ChatInput
        onSendMessage={mockSendMessage}
        isLoading={true}
        isStreaming={true}
        onCancelStream={mockCancelStream}
      />
    );

    const stopButton = screen.getByRole('button', { name: 'Stop' });
    fireEvent.click(stopButton);

    expect(mockCancelStream).toHaveBeenCalled();
  });

  it('should not call onSendMessage with empty input', () => {
    const mockSendMessage = vi.fn();

    render(<ChatInput onSendMessage={mockSendMessage} isLoading={false} />);

    const sendButton = screen.getByRole('button', { name: 'Send' });
    fireEvent.click(sendButton);

    expect(mockSendMessage).not.toHaveBeenCalled();
  });
});
