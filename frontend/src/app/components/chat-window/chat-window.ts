import { Component, computed, effect, inject, input, output, signal, afterRenderEffect, viewChild } from '@angular/core';
import { finalize } from 'rxjs';

import { ChatService } from '../../services/chat-service';
import { ChatInput } from '../chat-input/chat-input';
import { Conversation } from '../../models/conversation';
import { ChatMessage } from '../../models/chat-message';
import { MessageList } from '../message-list/message-list';
import { SearchBar } from '../search-bar/search-bar';

@Component({
  imports: [ChatInput, MessageList, SearchBar],
  selector: 'app-chat-window',
  styleUrl: './chat-window.scss',
  templateUrl: './chat-window.html',
})

export class ChatWindow {
  private chatService = inject(ChatService);
  conversation = input<Conversation | null>(null);
  conversationCreated = output<Conversation>();
  messages = signal<ChatMessage[]>([]);
  messageSearch = signal('');
  searching = signal(false);
  searchError = signal<string | null>(null);
  chatInput = viewChild(ChatInput);

  constructor() {
    effect(() => {
      this.messages.set([...(this.conversation()?.messages ?? [])]);
      this.messageSearch.set('');
    });

    afterRenderEffect(() => {
      this.conversation();
      this.chatInput()?.focusInput();
    });
  }

  filteredMessages = computed(() => {
    const search = this.messageSearch().toLowerCase();

    return this.messages().filter(message => {
      if (message.type === 'text') {
        return message.content.toLowerCase().includes(search);
      }

      if (message.type === 'search-results') {
        return message.results.some(result =>
          [
            result.content,
            result.source,
            result.section,
            result.url
          ].some(value => (value ?? '').toLowerCase().includes(search))
        );
      }

      return false;
    });
  });

  sendMessage(contentInput: string) {
    const content = contentInput.trim();
    if (!content) return;

    const isNew = !this.conversation();
    const conversation = this.conversation() ?? this.chatService.createConversation(content);

    const message: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      type: 'text',
      content: content,
      createdAt: Date.now().toString(),
      status: 'sent',
    };

    this.chatService.addMessage(conversation.conversationId, message);
    this.messages.set([...conversation.messages]);
    if (isNew) this.conversationCreated.emit(conversation);

    this.searching.set(true);
    this.searchError.set(null);
    this.chatService.searchDocuments(content).pipe(
      finalize(() => this.searching.set(false))
    ).subscribe({
      next: response => {
        const assistantMessage: ChatMessage = {
          id: crypto.randomUUID(),
          role: 'assistant',
          type: 'search-results',
          results: response.results,
          createdAt: Date.now().toString(),
          status: 'complete',
        };

        this.chatService.addMessage(conversation.conversationId, assistantMessage);
        if (this.conversation()?.conversationId === conversation.conversationId) {
          this.messages.set([...conversation.messages]);
        }
      },
      error: error => {
        console.error('Failed to search documentation', error);
        this.searchError.set('Could not search documentation. Please try again.');
      },
    });
  }
}
