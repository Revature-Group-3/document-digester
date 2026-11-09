import { Component, inject } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { ChatWindow } from '../chat-window/chat-window';
import { SearchBar } from '../search-bar/search-bar';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.scss',
  imports: [
    MatSidenavModule,
    MatListModule,
    ChatWindow,
    SearchBar,
  ],
})
export class Sidebar {
}
