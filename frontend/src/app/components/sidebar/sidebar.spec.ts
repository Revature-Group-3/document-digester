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

  function sendMessage(content: string) {
    windowComponent().sendMessage(content);
    http.expectOne('/api/chat').flush({ query: content, answer: 'Answer', sources: [] });
    fixture.detectChanges();
  }

  function windowComponent(): ChatWindow {
    return fixture.debugElement.query(By.directive(ChatWindow)).componentInstance;
  }

  it('opens on the welcome screen without seeded conversations', () => {
    expect(fixture.componentInstance.selectedConversation()).toBeNull();
    expect(fixture.componentInstance.conversations()).toEqual([]);
    expect(fixture.nativeElement.textContent).toContain('No conversations yet.');
    expect(fixture.nativeElement.querySelector('h1').textContent).toContain('Welcome!');
  });

  it('creates a conversation on first submit and stores each message once', () => {
    sendMessage('How do signals work?');
    expect(fixture.componentInstance.conversations().length).toBe(1);
    expect(fixture.componentInstance.selectedConversation()?.title).toBe('How do signals work?');
    expect(fixture.componentInstance.selectedConversation()?.messages.filter(message => message.role === 'user')).toHaveLength(1);
    expect(fixture.nativeElement.querySelector('h1')).toBeNull();
    sendMessage('Another question');
    expect(windowComponent().messages().filter(message => message.role === 'user')).toHaveLength(2);
    expect(fixture.componentInstance.selectedConversation()?.messages.filter(message => message.role === 'user')).toHaveLength(2);
  });

  it('starts fresh via the button and lets users reopen in-memory conversations', () => {
    sendMessage('Saved question');
    const conversationId = fixture.componentInstance.selectedConversation()!.conversationId;
    windowComponent().messageSearch.set('no match');
    fixture.nativeElement.querySelector('.new-conversation').click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('h1')).toBeTruthy();
    expect(windowComponent().messageSearch()).toBe('');
    fixture.componentInstance.selectConversation(conversationId);
    fixture.detectChanges();
    expect(windowComponent().messages()[0]).toMatchObject({ role: 'user', content: 'Saved question' });
  });

  it('does not create a conversation for whitespace', () => {
    windowComponent().sendMessage('   ');
    fixture.detectChanges();
    expect(fixture.componentInstance.conversations().length).toBe(0);
    expect(fixture.componentInstance.selectedConversation()).toBeNull();
  });
});
