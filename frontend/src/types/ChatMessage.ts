export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
  isStreaming?: boolean;
}

export interface ChatRequest {
  messages: ChatMessage[];
}

export interface ChatResponse {
  response: string;
}

export interface StreamingController {
  abort: () => void;
}
