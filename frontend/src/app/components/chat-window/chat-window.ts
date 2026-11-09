import { Component, effect, input, signal } from '@angular/core';

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
  conversation = input<Conversation | null>(null);
  messages = signal<ChatMessage[]>([]);
  messageSearch = signal('');



  constructor() {
    effect(() => {
      this.messages.set(this.conversation()?.messages ?? []);
    });
  }

  sendMessage(contentInput: string) {
    const message: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: contentInput,
      createdAt: Date.now().toString(),
      status: 'sent',
    };
    this.messages.update(messages => [...messages, message]);
  }
}
