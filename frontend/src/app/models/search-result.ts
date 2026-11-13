export interface SearchResult {
    content: string;
    score: number;
    source: string;
    section: string;
    url?: string;
}