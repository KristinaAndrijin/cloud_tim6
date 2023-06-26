import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';

@Component({
  selector: 'app-user-main',
  templateUrl: './user-main.component.html',
  styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit {

  albums: any[] = [];

  constructor(private filesService: FilesService) { }

  ngOnInit(): void {
    this.albums = this.filesService.getAlbums();
  }

  logClickedItem(albumName: string) {
    console.log("Clicked item: " + albumName);
  }

}
