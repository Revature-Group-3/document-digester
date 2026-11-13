import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatBubble } from './chat-bubble';

describe('ChatBubble', () => {
  let component: ChatBubble;
  let fixture: ComponentFixture<ChatBubble>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChatBubble],
    }).compileComponents();

    fixture = TestBed.createComponent(ChatBubble);
    component = fixture.componentInstance;
    // `data` is a required input, so it must be set before the first render.
    fixture.componentRef.setInput('data', {
      id: '1',
      role: 'assistant',
      type: 'answer',
      content: 'Signals let nodes communicate [1].',
      sources: [{
        content: 'Signals allow nodes to communicate.',
        score: 0.03,
        source: 'Using signals',
        section: 'Overview',
        url: 'https://docs.godotengine.org/',
      }],
      createdAt: new Date().toISOString(),
      status: 'complete',
    });
    await fixture.whenStable();
  });

  it('should render the answer and its sources', () => {
    expect(component).toBeTruthy();
    const text = fixture.nativeElement.textContent;
    expect(text).toContain('Signals let nodes communicate [1].');
    expect(text).toContain('Sources (1)');
    expect(fixture.nativeElement.querySelector('.sources a').getAttribute('href')).toBe('https://docs.godotengine.org/');
  });
});
