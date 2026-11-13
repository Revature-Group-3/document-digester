import { Component, inject, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialogModule,
  MatDialogRef,
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

export interface ConversationActionDialogData {
  action: 'rename' | 'delete';
  title: string;
}

@Component({
  imports: [MatButtonModule, MatDialogModule, MatFormFieldModule, MatInputModule],
  selector: 'app-conversation-action-dialog',
  styleUrl: './conversation-action-dialog.scss',
  templateUrl: './conversation-action-dialog.html',
})
export class ConversationActionDialog {
  readonly data = inject<ConversationActionDialogData>(MAT_DIALOG_DATA);
  private dialogRef = inject<MatDialogRef<ConversationActionDialog, string | true>>(MatDialogRef);
  title = signal(this.data.title);

  setTitle(event: Event): void {
    if (event.target instanceof HTMLInputElement) {
      this.title.set(event.target.value);
    }
  }

  confirm(): void {
    if (this.data.action === 'rename') {
      const title = this.title().trim();
      if (title) {
        this.dialogRef.close(title === this.data.title ? undefined : title);
      }
      return;
    }

    this.dialogRef.close(true);
  }

  cancel(): void {
    this.dialogRef.close();
  }
}
