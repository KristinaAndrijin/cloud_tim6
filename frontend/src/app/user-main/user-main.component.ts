import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';
import { CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';
import { JwtService } from '../jwt.service';
import { AlbumService } from '../backend_services/album.service';
import { SharedDataService } from '../shared-data.service';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { StringDialogComponent } from '../string-dialog/string-dialog.component';


@Component({
  selector: 'app-user-main',
  templateUrl: './user-main.component.html',
  styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit {
  dialogAlbumName: string ="";
  currentAlbum: string = "";

  constructor(private filesService: FilesService, private router: Router, private jwtService: JwtService) {
  }
  albums: any[] = [];

  ngOnInit(): void {
    this.getAlbums();
  }

  navigateToExplorer(albumName: string) {
    this.router.navigate(['explorer'], { queryParams: { album: albumName } });
  }

  getAlbums() {
    let back_albums = [{}];
    this.filesService.getAlbums().subscribe(
      {
        next: result => {
          console.log(result);
          let albums_back = result.albums;
          albums_back.forEach((element: string) => {
            let parts = element.split('/');
            let owner = parts[0];
            let album_name = parts.slice(1).join('/');
            back_albums.push({ name: album_name, owner: owner });
          });
          // alert("Albums received!");
          this.albums = back_albums;
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    )
    return [];
  }

}
