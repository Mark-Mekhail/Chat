import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';

// Mock the Chat component since we test it separately
vi.mock('./components/Chat/Chat', () => ({
  Chat: () => <div data-testid="mock-chat">Mock Chat Component</div>,
}));

// Mock the ErrorBoundary component for cleaner testing
vi.mock('./components/ErrorBoundary/ErrorBoundary', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="mock-error-boundary">{children}</div>
  ),
}));

describe('App Component', () => {
  it('renders header with title', () => {
    render(<App />);
    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
  });

  it('renders footer text', () => {
    render(<App />);
    expect(screen.getByText('Powered by Open-Source LLM')).toBeInTheDocument();
  });

  it('renders ErrorBoundary', () => {
    render(<App />);
    expect(screen.getByTestId('mock-error-boundary')).toBeInTheDocument();
  });

  it('renders Chat component inside ErrorBoundary', () => {
    render(<App />);
    expect(screen.getByTestId('mock-chat')).toBeInTheDocument();
  });
});
