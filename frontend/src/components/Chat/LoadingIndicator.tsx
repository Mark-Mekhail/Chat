import styles from './LoadingIndicator.module.css';

interface LoadingIndicatorProps {
  small?: boolean;
}

export function LoadingIndicator({ small = false }: LoadingIndicatorProps) {
  return (
    <div className={`${styles.loading} ${small ? styles.small : ''}`}>
      <div className={styles['dot-flashing']}></div>
    </div>
  );
}
