import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Conversation } from '../models/conversation';
import { ChatMessage } from '../models/chat-message';
import { SearchResponse } from '../models/search-response';


@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private http = inject(HttpClient);
    private searchUrl = '/api/search';
    private conversations: Conversation[] = [];

    loadConversations(): Observable<Conversation[]> {
        return of(this.conversations);
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

    searchDocuments(query: string): Observable<SearchResponse> {
        return this.http.post<SearchResponse>(
            this.searchUrl,
            { query }
        );
    }
}