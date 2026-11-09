import { Component, input } from '@angular/core';

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
}
