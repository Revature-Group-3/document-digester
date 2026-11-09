import { Component, inject, OnInit, signal } from '@angular/core';

import { ChatInput } from '../chat-input/chat-input';
import { ChatService } from '../../services/chat-service';
import { Conversation } from '../../models/conversation';
import { ChatMessage } from '../../models/chat-message';
import { MessageList } from '../message-list/message-list';
import { SearchBar } from '../search-bar/search-bar';
import { ChatBubble } from '../chat-bubble/chat-bubble';

@Component({
  imports: [ChatInput, MessageList, SearchBar, ChatBubble],
  selector: 'app-chat-window',
  styleUrl: './chat-window.scss',
  templateUrl: './chat-window.html',
})

export class ChatWindow implements OnInit {
  private chatService = inject(ChatService);

  conversations = signal<Conversation[]>([]);
  selectedConversation = signal<Conversation | null>(null);
  messages = signal<ChatMessage[]>([]);

  /* ngOnInit(): void {
    this.chatService.loadConversations().subscribe(conversations => this.conversations.set(conversations));
  }
  */

  // TODO: get rid of placeholder
  ngOnInit() {
    this.chatService.loadConversations().subscribe(conversations => {
      this.conversations.set(conversations);

      if (conversations.length > 0) {
        this.selectConversation(conversations[0].conversationId);
      }
    });
  }

  selectConversation(conversationId: string): void {
    const conversation = this.conversations().find(conversation => conversation.conversationId === conversationId) ?? null;
    this.selectedConversation.set(conversation);
    this.messages.set(this.chatService.getMessages(conversationId));
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
