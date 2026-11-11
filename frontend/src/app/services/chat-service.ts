import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

import { Conversation } from '../models/conversation';
import { ChatMessage } from '../models/chat-message';


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
                this.conversations = data.conversations;
                return this.conversations;
            })
        );
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
}