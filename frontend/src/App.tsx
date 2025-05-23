import './styles/global.css';
import { Chat } from './components/Chat/Chat';
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary';
import styles from './App.module.css';

function App() {
  return (
    <div className={styles['app-container']}>
      <header className={styles.header}>
        <h1>AI Chat Assistant</h1>
      </header>
      <main className={styles.main}>
        <ErrorBoundary>
          <Chat />
        </ErrorBoundary>
      </main>
      <footer className={styles.footer}>
        <p>Powered by Open-Source LLM</p>
      </footer>
    </div>
  );
}

export default App;
