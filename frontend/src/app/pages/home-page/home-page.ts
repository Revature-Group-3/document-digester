import { Component } from '@angular/core';
import { Sidebar } from '../../components/sidebar/sidebar';


@Component({
  imports: [Sidebar],
  selector: 'app-home-page',
  styleUrl: './home-page.scss',
  templateUrl: './home-page.html',
})
export class HomePage { }
