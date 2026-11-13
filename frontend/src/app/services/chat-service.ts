import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

import { Conversation } from '../models/conversation';
import { ChatMessage } from '../models/chat-message';
import { SearchResult } from '../models/search-result';


@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private http = inject(HttpClient);
    private apiUrl = '/mock-conversations.json'
    private conversations: Conversation[] = [];

    loadConversations(): Observable<Conversation[]> {
        return this.http.get<{ conversations: Conversation[] }>(this.apiUrl).pipe(
            map(data => {
                const existingIds = new Set(this.conversations.map(item => item.conversationId));
                this.conversations = [...this.conversations, ...data.conversations.filter(item => !existingIds.has(item.conversationId))];
                return this.conversations;
            })
        );
    }

    createConversation(firstMessage: string): Conversation {
        const conversation: Conversation = {
            conversationId: crypto.randomUUID(),
            title: firstMessage.length > 48 ? firstMessage.slice(0, 48) + '…' : firstMessage,
            messages: [],
        };
        this.conversations = [conversation, ...this.conversations];
        return conversation;
    }

    // Careful not to call this before loadConversations()
    getMessages(conversationId: string): ChatMessage[] {
        const conversation = this.conversations.find(
            c => c.conversationId === conversationId
        );

        return conversation?.messages ?? [];
    }

    addMessage(conversationId: string, message: ChatMessage): void {
        const conversation = this.conversations.find(
            c => c.conversationId === conversationId
        );

        if (conversation) {
            conversation.messages.push(message);
        }
    }

    searchDocuments(query: string): Observable<SearchResult[]> {
        return this.http.post<SearchResult[]>(
            'http://localhost:8000/search',
            { content: query }
        );
    }
}