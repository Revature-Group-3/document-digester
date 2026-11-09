import { Component } from '@angular/core';
import { ChatInput } from '../chat-input/chat-input';
import { ChatBubble } from '../chat-bubble/chat-bubble';

@Component({
  imports: [ChatInput, ChatBubble],
  selector: 'app-chat-window',
  styleUrl: './chat-window.scss',
  templateUrl: './chat-window.html',
})
export class ChatWindow { }
