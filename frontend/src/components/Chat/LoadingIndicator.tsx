import styles from './LoadingIndicator.module.css';

export function LoadingIndicator() {
  return (
    <div className={styles.loading}>
      <div className={styles['dot-flashing']}></div>
    </div>
  );
}
