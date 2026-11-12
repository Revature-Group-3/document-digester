export interface ChatMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    createdAt: string;
    status: 'sent' | 'complete' | 'failed';
}

export interface ChatMessageRequest {
    content: string;
}