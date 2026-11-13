import { Component, input } from '@angular/core';
import { SearchResult } from '../../models/search-result';
import { MatCard, MatCardContent } from '@angular/material/card';

@Component({
  imports: [MatCard, MatCardContent],
  selector: 'app-search-results',
  styleUrl: './search-results.scss',
  templateUrl: './search-results.html',
})
export class SearchResults {
  results = input.required<SearchResult[]>();
}
