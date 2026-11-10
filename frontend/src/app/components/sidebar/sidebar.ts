import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatButtonModule } from '@angular/material/button';

import { MatListModule } from '@angular/material/list';
import { ChatWindow } from '../chat-window/chat-window';
import { SearchBar } from '../search-bar/search-bar';
import { ConversationList } from '../conversation-list/conversation-list';
import { Conversation } from '../../models/conversation';
import { ChatService } from '../../services/chat-service';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.scss',
  imports: [
    MatSidenavModule,
    MatButtonModule,
    MatListModule,
    ChatWindow,
    SearchBar,
    ConversationList,
  ],
})
export class Sidebar implements OnInit {
  private chatService = inject(ChatService);
  conversations = signal<Conversation[]>([]);
  selectedConversation = signal<Conversation | null>(null);
  conversationSearch = signal('');

  filteredConversations = computed(() => {
    const search = this.conversationSearch().toLowerCase();
    return this.conversations().filter(conversation => conversation.title.toLowerCase().includes(search));
  });

  ngOnInit(): void {
    this.chatService.loadConversations().subscribe({
      next: conversations => {
        this.conversations.set(conversations);
        if (conversations.length > 0) {
          this.selectConversation(conversations[0].conversationId);
        }
      },
      error: error => console.error('Failed to load conversations', error),
    });
  }

  selectConversation(conversationId: string): void {
    const conversation = this.conversations().find(
      item => item.conversationId === conversationId
    ) ?? null;
    this.selectedConversation.set(conversation);
  }
}
