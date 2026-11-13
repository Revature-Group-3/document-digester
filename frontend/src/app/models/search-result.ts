export interface SearchResult {
    content: string;
    score: number;
    source: string;
    section: string;
<<<<<<< HEAD
    url?: string;
=======
    url: string | null;
>>>>>>> origin/main
}