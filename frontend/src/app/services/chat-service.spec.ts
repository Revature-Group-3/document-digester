import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { Conversation } from '../models/conversation';
import { ChatMessage } from '../models/chat-message';
import { ChatResponse } from '../models/chat-response';
import { ChatService } from './chat-service';

describe('ChatService', () => {
  let service: ChatService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ChatService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should load only conversations created in memory', () => {
    let loadedConversations: Conversation[] = [];
    service.loadConversations().subscribe(conversations => {
      loadedConversations = conversations;
    });
    expect(loadedConversations).toEqual([]);

    const conversation = service.createConversation('First question');
    service.loadConversations().subscribe(conversations => {
      loadedConversations = conversations;
    });

    expect(loadedConversations).toEqual([conversation]);
  });

  it('should post the question with prior history and return the backend answer', () => {
    const response: ChatResponse = {
      query: 'signals',
      answer: 'Signals allow nodes to communicate [1].',
      sources: [{
        content: 'Signals allow nodes to communicate.',
        score: 0.95,
        source: 'Godot Documentation',
        section: 'Using Signals',
        url: 'https://docs.godotengine.org/',
      }],
    };
    const previous: ChatMessage[] = [
      { id: '1', role: 'user', type: 'text', content: 'Hi', createdAt: '', status: 'sent' },
      { id: '2', role: 'user', type: 'text', content: 'Broken', createdAt: '', status: 'failed' },
    ];
    let receivedResponse: ChatResponse | undefined;

    service.askQuestion('signals', previous).subscribe(result => {
      receivedResponse = result;
    });

    const request = httpTestingController.expectOne('/api/chat');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      query: 'signals',
      history: [{ role: 'user', content: 'Hi' }],
    });
    request.flush(response);

    expect(receivedResponse).toEqual(response);
  });
});
