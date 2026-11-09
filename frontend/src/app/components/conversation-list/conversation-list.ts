import { Component, input, output } from '@angular/core';

import { Conversation } from '../../models/conversation';
import { MatListModule } from '@angular/material/list';

@Component({
  imports: [MatListModule],
  selector: 'app-conversation-list',
  styleUrl: './conversation-list.scss',
  templateUrl: './conversation-list.html',
})
export class ConversationList {
  conversations = input<Conversation[]>();
  conversationSelected = output<string>();

  selectConversation(conversationId: string): void {
    this.conversationSelected.emit(conversationId);
  }
}
