import { Component, inject, input, output } from '@angular/core';

import { Conversation } from '../../models/conversation';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatIcon } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import {
  ConversationActionDialog,
  ConversationActionDialogData,
} from '../conversation-action-dialog/conversation-action-dialog';

@Component({
  imports: [MatListModule, MatButtonModule, MatIcon, MatMenuModule, MatDialogModule],
  selector: 'app-conversation-list',
  styleUrl: './conversation-list.scss',
  templateUrl: './conversation-list.html',
})
export class ConversationList {
  private dialog = inject(MatDialog);
  conversations = input<Conversation[]>([]);
  selectedConversationId = input<string | null>(null);
  conversationSelected = output<string>();
  conversationRenamed = output<{ conversationId: string; title: string }>();
  conversationDeleted = output<string>();

  selectConversation(conversationId: string): void {
    this.conversationSelected.emit(conversationId);
  }

  renameConversation(conversation: Conversation): void {
    this.dialog
      .open<ConversationActionDialog, ConversationActionDialogData, string | true>(
        ConversationActionDialog,
        {
          width: '400px',
          data: { action: 'rename', title: conversation.title },
        }
      )
      .afterClosed()
      .subscribe(title => {
        if (typeof title === 'string' && title !== conversation.title) {
          this.conversationRenamed.emit({ conversationId: conversation.conversationId, title });
        }
      });
  }

  deleteConversation(conversation: Conversation): void {
    this.dialog
      .open<ConversationActionDialog, ConversationActionDialogData, string | true>(
        ConversationActionDialog,
        {
          width: '400px',
          data: { action: 'delete', title: conversation.title },
        }
      )
      .afterClosed()
      .subscribe(confirmed => {
        if (confirmed === true) {
          this.conversationDeleted.emit(conversation.conversationId);
        }
      });
  }
}
