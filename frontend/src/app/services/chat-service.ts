import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Conversation } from '../models/conversation';
import { ChatMessage } from '../models/chat-message';
import { ChatResponse, ChatTurn } from '../models/chat-response';

/** How many earlier messages are sent to the LLM as conversation history. */
const MAX_HISTORY_MESSAGES = 10;

@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private http = inject(HttpClient);
    private chatUrl = '/api/chat';
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

    renameConversation(conversationId: string, title: string): void {
        const conversation = this.conversations.find(c => c.conversationId === conversationId);
        if (conversation) {
            conversation.title = title;
        }
    }

    deleteConversation(conversationId: string): void {
        this.conversations = this.conversations.filter(c => c.conversationId !== conversationId);
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

    /** Ask the backend RAG pipeline (retrieval + local Ollama LLM) a question. */
    askQuestion(query: string, previousMessages: ChatMessage[] = []): Observable<ChatResponse> {
        const history: ChatTurn[] = previousMessages
            .filter(message => message.status !== 'failed')
            .slice(-MAX_HISTORY_MESSAGES)
            .map(message => ({ role: message.role, content: message.content }));

        return this.http.post<ChatResponse>(this.chatUrl, { query, history });
    }
}
