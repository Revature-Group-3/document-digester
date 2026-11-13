import { SearchResult } from './search-result';

export interface ChatTurn {
    role: 'user' | 'assistant';
    content: string;
}

export interface ChatRequest {
    query: string;
    top_k?: number;
    history?: ChatTurn[];
}

export interface ChatResponse {
    query: string;
    answer: string;
    sources: SearchResult[];
}
