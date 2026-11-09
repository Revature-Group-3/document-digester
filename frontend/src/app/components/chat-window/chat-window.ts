import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatInput } from '../chat-input/chat-input';

@Component({
  imports: [RouterOutlet, ChatInput],
  selector: 'app-chat-window',
  styleUrl: './chat-window.scss',
  templateUrl: './chat-window.html',
})
export class ChatWindow { }
