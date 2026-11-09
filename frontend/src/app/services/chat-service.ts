import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Conversation } from '../models/conversation';


@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private http = inject(HttpClient);
    private apiUrl = '/mock-conversations.json'

    getConversations(): Observable<Conversation[]> {
        return this.http.get<Conversation[]>(this.apiUrl);
    }
}