import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatMessage } from '../../models/chat-message';
import { Conversation } from '../../models/conversation';
import { ChatService } from '../../services/chat-service';
import { ChatWindow } from './chat-window';

describe('ChatWindow', () => {
  let component: ChatWindow;
  let fixture: ComponentFixture<ChatWindow>;
  let conversation: Conversation;

  beforeEach(async () => {
    conversation = {
      conversationId: 'conversation-1',
      title: 'Test conversation',
      messages: [],
    };

    await TestBed.configureTestingModule({
      imports: [ChatWindow],
      providers: [{
        provide: ChatService,
        useValue: {
          addMessage: (_conversationId: string, message: ChatMessage) => {
            conversation.messages.push(message);
          },
        },
      }],
    }).compileComponents();

    fixture = TestBed.createComponent(ChatWindow);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should add the first message only once', () => {
    fixture.componentRef.setInput('conversation', conversation);
    fixture.detectChanges();

    component.sendMessage('Hello');

    expect(conversation.messages).toHaveLength(1);
    expect(component.messages()).toHaveLength(1);
  });
});
