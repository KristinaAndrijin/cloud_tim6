import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.css']
})
export class ExplorerComponent {

  albums: any[] = [];

  constructor(private filesService: FilesService, private router: Router) { }

  ngOnInit(): void {
    this.albums = this.filesService.getAlbums();
  }

  logClickedItem(albumName: string) {
    console.log("Clicked item: " + albumName);
    this.router.navigate(["explorer"]);
  }

}
