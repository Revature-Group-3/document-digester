import { Component, input, output } from '@angular/core';

import { Conversation } from '../../models/conversation';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatIcon } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';

@Component({
  imports: [MatListModule, MatButtonModule, MatIcon, MatMenuModule],
  selector: 'app-conversation-list',
  styleUrl: './conversation-list.scss',
  templateUrl: './conversation-list.html',
})
export class ConversationList {
  conversations = input<Conversation[]>([]);
  selectedConversationId = input<string | null>(null);
  conversationSelected = output<string>();
  conversationRenamed = output<{ conversationId: string; title: string }>();
  conversationDeleted = output<string>();

  selectConversation(conversationId: string): void {
    this.conversationSelected.emit(conversationId);
  }

  renameConversation(conversation: Conversation): void {
    const title = window.prompt('Rename conversation', conversation.title)?.trim();
    if (title && title !== conversation.title) {
      this.conversationRenamed.emit({ conversationId: conversation.conversationId, title });
    }
  }

   deleteConversation(conversation: Conversation): void {
    if (window.confirm(`Delete "${conversation.title}"?`)) {
      this.conversationDeleted.emit(conversation.conversationId);
    }
  }
}
