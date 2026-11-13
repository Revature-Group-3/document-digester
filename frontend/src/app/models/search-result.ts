export interface SearchResult {
    content: string;
    score: number | null;
    source: string;
    section: string;
    url: string | null;
}