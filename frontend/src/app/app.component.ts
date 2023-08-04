import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { SharedDataService } from './shared-data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tim 6 cloud';

  ngOnInit() {
    this.sharedDataService.currentAlbumName$.subscribe(albumName => {
      this.currentAlbumName = albumName;
    });
  }

  showNavbar: boolean = false;
  currentAlbumName: string | null = null;

  constructor(private router: Router, private sharedDataService : SharedDataService) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        
        // Gledamo na kojoj smo putanji i prikazujemo navbar u skladu sa tim
        const navigationEndEvent = event as NavigationEnd;
        const url = navigationEndEvent.url;
        if (url.includes('main') || url.includes('explorer') || url.includes('details') || url.includes('upload') || url.includes("invite")
        || url.includes("permissions")) {
          this.showNavbar = true;
        } else {
          this.showNavbar = false;
        }
      }
    });
  }

}
