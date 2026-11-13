import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

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
