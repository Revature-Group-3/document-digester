import { afterNextRender, afterRenderEffect, Component, effect, ElementRef, input, viewChild } from '@angular/core';

import { ChatMessage } from '../../models/chat-message';
import { ChatBubble } from '../chat-bubble/chat-bubble';

@Component({
  imports: [ChatBubble],
  selector: 'app-message-list',
  styleUrl: './message-list.scss',
  templateUrl: './message-list.html',
})
export class MessageList {
  messages = input<ChatMessage[]>();

  messageContainer = viewChild<ElementRef<HTMLElement>>('messageList');

  constructor() {
    afterRenderEffect(() => {
      this.messages();
      const container = this.messageContainer()?.nativeElement;

      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    });
  }
}
