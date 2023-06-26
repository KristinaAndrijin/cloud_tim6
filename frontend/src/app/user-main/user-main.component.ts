import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-main',
  templateUrl: './user-main.component.html',
  styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit {

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
