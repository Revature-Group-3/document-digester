import { Component, output, signal, viewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
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
  private input = viewChild<ElementRef<HTMLInputElement>>('input');
  messageSubmitted = output<string>();
  value = signal('');

  submitMessage() {
    const message = this.value().trim();
    if (message) {
      this.messageSubmitted.emit(message);
      this.value.set('');
    }
  }

  focusInput() {
    this.input()?.nativeElement.focus();
  }
}
