import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { Conversation } from '../../models/conversation';
import { ConversationActionDialog, ConversationActionDialogData } from '../conversation-action-dialog/conversation-action-dialog';
import { ConversationList } from './conversation-list';

describe('ConversationList', () => {
  let component: ConversationList;
  let fixture: ComponentFixture<ConversationList>;
  let dialogData: ConversationActionDialogData | undefined;
  let dialogResult: string | true | undefined;

  beforeEach(async () => {
    dialogData = undefined;
    dialogResult = undefined;

    const dialogStub = {
      open: (
        _component: typeof ConversationActionDialog,
        config: MatDialogConfig<ConversationActionDialogData>
      ) => {
        dialogData = config.data ?? undefined;
        return { afterClosed: () => of(dialogResult) };
      },
    };

    await TestBed.configureTestingModule({
      imports: [ConversationList],
    })
      .overrideComponent(ConversationList, {
        add: { providers: [{ provide: MatDialog, useValue: dialogStub }] },
      })
      .compileComponents();

    fixture = TestBed.createComponent(ConversationList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should emit the selected conversation id', () => {
    let selectedId: string | undefined;
    component.conversationSelected.subscribe(id => selectedId = id);

    component.selectConversation('conversation-1');

    expect(selectedId).toBe('conversation-1');
  });

  it('should open a rename dialog and emit the confirmed title', () => {
    const conversation: Conversation = {
      conversationId: 'conversation-1',
      title: 'Original title',
      messages: [],
    };
    let renamed: { conversationId: string; title: string } | undefined;
    dialogResult = 'Updated title';
    component.conversationRenamed.subscribe(value => renamed = value);

    component.renameConversation(conversation);

    expect(dialogData).toEqual({ action: 'rename', title: 'Original title' });
    expect(renamed).toEqual({ conversationId: 'conversation-1', title: 'Updated title' });
  });

  it('should emit deletion only when the delete dialog is confirmed', () => {
    const conversation: Conversation = {
      conversationId: 'conversation-1',
      title: 'Conversation to delete',
      messages: [],
    };
    let deletedId: string | undefined;
    component.conversationDeleted.subscribe(id => deletedId = id);

    component.deleteConversation(conversation);
    expect(dialogData).toEqual({ action: 'delete', title: 'Conversation to delete' });
    expect(deletedId).toBeUndefined();

    dialogResult = true;
    component.deleteConversation(conversation);
    expect(deletedId).toBe('conversation-1');
  });
});
