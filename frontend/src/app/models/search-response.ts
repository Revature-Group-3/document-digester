import { SearchResult } from './search-result';

export interface SearchResponse {
    query: string;
    results: SearchResult[];
}