import { TestBed } from '@angular/core/testing';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

import {
  ConversationActionDialog,
  ConversationActionDialogData,
} from './conversation-action-dialog';

describe('ConversationActionDialog', () => {
  let component: ConversationActionDialog;
  let closedWith: string | true | undefined;

  function createDialog(data: ConversationActionDialogData): void {
    closedWith = undefined;
    TestBed.configureTestingModule({
      imports: [ConversationActionDialog],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: data },
        {
          provide: MatDialogRef,
          useValue: { close: (result?: string | true) => closedWith = result },
        },
      ],
    });

    component = TestBed.createComponent(ConversationActionDialog).componentInstance;
  }

  it('should return the trimmed title when renaming', () => {
    createDialog({ action: 'rename', title: 'Original' });
    component.title.set('  Updated  ');

    component.confirm();

    expect(closedWith).toBe('Updated');
  });

  it('should close without a rename result when the title is unchanged', () => {
    createDialog({ action: 'rename', title: 'Original' });

    component.confirm();

    expect(closedWith).toBeUndefined();
  });

  it('should return confirmation for deletion', () => {
    createDialog({ action: 'delete', title: 'Original' });

    component.confirm();

    expect(closedWith).toBe(true);
  });
});
