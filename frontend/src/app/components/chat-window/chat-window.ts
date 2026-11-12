import { Component, computed, effect, inject, input, output, signal } from '@angular/core';

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

  constructor() {
    effect(() => {
      this.messages.set([...(this.conversation()?.messages ?? [])]);
      this.messageSearch.set('');
    });
  }

  filteredMessages = computed(() => {
    const search = this.messageSearch().toLowerCase();
    return this.messages().filter(message => message.content.toLowerCase().includes(search));
  });

  sendMessage(contentInput: string) {
    const content = contentInput.trim();
    if (!content) return;

    const isNew = !this.conversation();
    const conversation = this.conversation() ?? this.chatService.createConversation(content);

    const message: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      createdAt: Date.now().toString(),
      status: 'sent',
    };

    this.chatService.addMessage(conversation.conversationId, message);
    this.messages.set([...conversation.messages]);
    if (isNew) this.conversationCreated.emit(conversation);
  }
}
