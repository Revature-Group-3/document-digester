import { Component } from '@angular/core';
import { ChatWindow } from '../../components/chat-window/chat-window';


@Component({
  imports: [ChatWindow],
  selector: 'app-home-page',
  styleUrl: './home-page.scss',
  templateUrl: './home-page.html',
})
export class HomePage { }
