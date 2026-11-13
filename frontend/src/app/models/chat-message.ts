import { SearchResult } from './search-result';

export interface ChatMessageRequest {
    content: string;
}

interface BaseChatMessage {
    id: string;
    createdAt: string;
    status: 'sent' | 'complete' | 'failed';
}

export interface UserMessage extends BaseChatMessage {
    role: 'user';
    type: 'text';
    content: string;
}

export interface AssistantMessage extends BaseChatMessage {
    role: 'assistant';
    type: 'search-results';
    results: SearchResult[];
}

export type ChatMessage = UserMessage | AssistantMessage;