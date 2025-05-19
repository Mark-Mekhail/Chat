import axios from 'axios';
import type { ChatMessage, ChatResponse } from '../types/ChatMessage';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export async function sendChatMessage(messages: ChatMessage[]): Promise<ChatResponse> {
  const response = await axios.post(`${API_URL}/chat/`, { messages });
  return response.data;
}

export async function streamChatMessage(
  messages: ChatMessage[],
  onChunk: (chunk: string) => void,
  onDone: () => void,
  onError: (error: Error) => void
): Promise<() => void> {
  const controller = new AbortController();
    
  fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream'
    },
    body: JSON.stringify({ messages }),
    signal: controller.signal
  }).then(async (response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    if (!response.body) {
      throw new Error('No response body.');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        throw new Error('Stream ended unexpectedly');
      }

      const data = decoder.decode(value, { stream: true });
      const text = data.substring(6, data.length - 2);
      if (text === '[DONE]') {
        onDone();
        break;
      }

      onChunk(text);
    }
  }).catch(error => {
    if (error.name === 'AbortError') {
      onDone();
    }
    else {
      onError(error);
    }
  });

  return () => controller.abort();
}
