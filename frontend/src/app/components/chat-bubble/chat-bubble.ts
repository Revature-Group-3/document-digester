import { Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { DatePipe } from '@angular/common';

import { ChatMessage } from '../../models/chat-message';
import { SearchResults } from '../search-results/search-results';

@Component({
  imports: [MatCardModule, DatePipe, SearchResults],
  selector: 'app-chat-bubble',
  styleUrl: './chat-bubble.scss',
  templateUrl: './chat-bubble.html',
})
export class ChatBubble {
  data = input.required<ChatMessage>();
}
