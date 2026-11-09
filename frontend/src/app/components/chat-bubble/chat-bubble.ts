import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

@Component({
  imports: [MatCardModule],
  selector: 'app-chat-bubble',
  styleUrl: './chat-bubble.scss',
  templateUrl: './chat-bubble.html',
})
export class ChatBubble { }
