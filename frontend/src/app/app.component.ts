import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tim 6 cloud';

  showNavbar: boolean = false;
  currentAlbumName: string = '';

  constructor(private router: Router) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        
        // Gledamo na kojoj smo putanji i prikazujemo navbar u skladu sa tim
        const navigationEndEvent = event as NavigationEnd;
        const url = navigationEndEvent.url;
        if (url.includes('main') || url.includes('explorer') || url.includes('details') || url.includes('upload')) {
          this.showNavbar = true;
        } else {
          this.showNavbar = false;
        }
      }
    });
  }

}
