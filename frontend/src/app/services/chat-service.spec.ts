import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { Conversation } from '../models/conversation';
import { SearchResponse } from '../models/search-response';
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

  it('should send a search query and return the backend response', () => {
    const response = {
      query: 'signals',
      results: [{
        content: 'Signals allow nodes to communicate.',
        score: 0.95,
        source: 'Godot Documentation',
        section: 'Using Signals',
        url: 'https://docs.godotengine.org/',
      }],
    };
    let receivedResponse: SearchResponse | undefined;

    service.searchDocuments('signals').subscribe(result => {
      receivedResponse = result;
    });

    const request = httpTestingController.expectOne('/api/search');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({ query: 'signals' });
    request.flush(response);

    expect(receivedResponse).toEqual(response);
  });
});
