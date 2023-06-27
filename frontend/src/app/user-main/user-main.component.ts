import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';
import { CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';
import { JwtService } from '../jwt.service';
import { AlbumService } from '../backend_services/album.service';
import { SharedDataService } from '../shared-data.service';

@Component({
  selector: 'app-user-main',
  templateUrl: './user-main.component.html',
  styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit {

  constructor(private filesService: FilesService, private router: Router, private jwtService: JwtService, private album:AlbumService) {
  }
  albums: any[] = [];

  ngOnInit(): void {
    this.albums = this.filesService.getAlbums();
  }

  logClickedItem(albumName: string) {
    console.log("Clicked item: " + albumName);
    this.router.navigate(["explorer"]);
  }

  create_album(){
    this.album.create_album("test123").subscribe();
  }

}
