import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { LoadingIndicator } from '../../components/Chat/LoadingIndicator';

describe('LoadingIndicator Component', () => {
  it('renders with default size', () => {
    const { container } = render(<LoadingIndicator />);

    // Check that the loading div exists
    const loadingDiv = container.querySelector('[class*="loading"]');
    expect(loadingDiv).not.toBeNull();

    // Check that it doesn't have the small class
    expect(loadingDiv?.className.includes('small')).toBe(false);

    // Check that the dot-flashing element exists
    expect(container.querySelector('[class*="dot-flashing"]')).not.toBeNull();
  });

  it('renders with small size when small prop is true', () => {
    const { container } = render(<LoadingIndicator small={true} />);

    // Check that the loading div has the small class
    const loadingDiv = container.querySelector('[class*="loading"]');
    expect(loadingDiv?.className.includes('small')).toBe(true);
  });
});
