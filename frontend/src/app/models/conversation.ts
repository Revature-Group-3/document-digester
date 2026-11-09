import { ChatMessage } from "./chat-message";

export interface Conversation {
    conversationId: string;
    title: string;
    messages: ChatMessage[];
}
