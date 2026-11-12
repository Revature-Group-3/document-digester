import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { By } from '@angular/platform-browser';
import { Sidebar } from './sidebar';
import { ChatWindow } from '../chat-window/chat-window';

describe('New conversation flow', () => {
  let fixture: ComponentFixture<Sidebar>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Sidebar],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    fixture = TestBed.createComponent(Sidebar);
    http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => http.verify());

  function loadHistory() {
    http.expectOne('/mock-conversations.json').flush({ conversations: [{
      conversationId: 'saved', title: 'Saved conversation', messages: [{
        id: 'old', role: 'user', content: 'Saved question', createdAt: '1', status: 'sent',
      }],
    }] });
    fixture.detectChanges();
  }

  function windowComponent(): ChatWindow {
    return fixture.debugElement.query(By.directive(ChatWindow)).componentInstance;
  }

  it('opens on the welcome screen even when history exists', () => {
    loadHistory();
    expect(fixture.componentInstance.selectedConversation()).toBeNull();
    expect(fixture.nativeElement.querySelector('h1').textContent).toContain('Welcome!');
  });

  it('creates a conversation on first submit and stores each message once', () => {
    loadHistory();
    windowComponent().sendMessage('How do signals work?');
    fixture.detectChanges();
    expect(fixture.componentInstance.conversations().length).toBe(2);
    expect(fixture.componentInstance.selectedConversation()?.title).toBe('How do signals work?');
    expect(fixture.componentInstance.selectedConversation()?.messages.length).toBe(1);
    expect(fixture.nativeElement.querySelector('h1')).toBeNull();
    windowComponent().sendMessage('Another question');
    fixture.detectChanges();
    expect(windowComponent().messages().length).toBe(2);
    expect(fixture.componentInstance.selectedConversation()?.messages.length).toBe(2);
  });

  it('starts fresh via the button and lets users reopen saved conversations', () => {
    loadHistory();
    fixture.componentInstance.selectConversation('saved');
    fixture.detectChanges();
    windowComponent().messageSearch.set('no match');
    fixture.nativeElement.querySelector('.new-conversation').click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('h1')).toBeTruthy();
    expect(windowComponent().messageSearch()).toBe('');
    fixture.componentInstance.selectConversation('saved');
    fixture.detectChanges();
    expect(windowComponent().messages()[0].content).toBe('Saved question');
  });

  it('preserves a new conversation if history finishes loading afterwards', () => {
    windowComponent().sendMessage('First question');
    fixture.detectChanges();
    loadHistory();
    expect(fixture.componentInstance.conversations().length).toBe(2);
    expect(fixture.componentInstance.selectedConversation()?.messages.length).toBe(1);
  });

  it('does not create a conversation for whitespace', () => {
    loadHistory();
    windowComponent().sendMessage('   ');
    fixture.detectChanges();
    expect(fixture.componentInstance.conversations().length).toBe(1);
    expect(fixture.componentInstance.selectedConversation()).toBeNull();
  });
});
