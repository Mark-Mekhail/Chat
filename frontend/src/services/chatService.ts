import axios from 'axios';
import type { ChatMessage, ChatResponse } from '../types/ChatMessage';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export async function sendChatMessage(messages: ChatMessage[]): Promise<ChatResponse> {
  const response = await axios.post(`${API_URL}/chat/`, { messages });
  return response.data;
}
