import { Component, inject } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { ChatWindow } from '../chat-window/chat-window';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.scss',
  imports: [
    MatSidenavModule,
    MatListModule,
    ChatWindow,
  ],
})
export class Sidebar {
}
