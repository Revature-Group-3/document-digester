import { Component, output, signal } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

@Component({
  imports: [MatFormFieldModule, MatInputModule, MatIconModule, MatButtonModule],
  selector: 'app-chat-input',
  styleUrl: './chat-input.scss',
  templateUrl: './chat-input.html',
})
export class ChatInput {
  messageSubmitted = output<string>();
  value = signal('');

  submitMessage() {
    const message = this.value().trim();
    if (message) {
      this.messageSubmitted.emit(message);
      this.value.set('');
    }
  }
}
