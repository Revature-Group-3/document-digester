import { Component } from '@angular/core';
import { ChatWindow } from '../../components/chat-window/chat-window';
import { Sidebar } from '../../components/sidebar/sidebar';


@Component({
  imports: [ChatWindow, Sidebar],
  selector: 'app-home-page',
  styleUrl: './home-page.scss',
  templateUrl: './home-page.html',
})
export class HomePage { }
