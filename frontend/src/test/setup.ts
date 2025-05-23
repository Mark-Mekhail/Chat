import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock the IntersectionObserver
const mockIntersectionObserver = vi.fn();
mockIntersectionObserver.mockReturnValue({
  observe: () => null,
  unobserve: () => null,
  disconnect: () => null,
});
window.IntersectionObserver = mockIntersectionObserver;

// Mock scrollIntoView which isn't implemented in jsdom
Element.prototype.scrollIntoView = vi.fn();
