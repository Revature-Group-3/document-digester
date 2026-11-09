import { Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { ChatMessage } from '../../models/chat-message';

@Component({
  imports: [MatCardModule],
  selector: 'app-chat-bubble',
  styleUrl: './chat-bubble.scss',
  templateUrl: './chat-bubble.html',
})
export class ChatBubble {
  data = input<ChatMessage>();
}
