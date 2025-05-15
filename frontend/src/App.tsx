import './App.css'
import { Chat } from './components/Chat'
import ErrorBoundary from './components/ErrorBoundary'

function App() {
  return (
    <div className="app-container">
      <header>
        <h1>AI Chat Assistant</h1>
      </header>
      <main>
        <ErrorBoundary>
          <Chat />
        </ErrorBoundary>
      </main>
      <footer>
        <p>Powered by Open-Source LLM</p>
      </footer>
    </div>
  )
}

export default App
