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

  constructor(private filesService: FilesService, private router: Router, private jwtService: JwtService, private dialog: MatDialog, private albumService:AlbumService) {
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
          // console.log(result);
          let albums_back = result.albums;
          albums_back.forEach((element: string) => {
            // console.log(element);
            let parts = element.split('/');
            let owner = parts[0];
            let album_name = parts.slice(1).join('/');
            back_albums.push({ name: album_name, owner: owner });
            // console.log(back_albums);
          });
          // alert("Albums received!");
          this.albums = back_albums;
          this.albums[0] = { name: 'default', owner: this.jwtService.getCurrentUser() }
          // console.log(this.albums);
          // console.log(this.albums[0]);
          // console.log(this.albums[1]);
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    )
    return [];
  }

  uploadFile(albumName: string) {
    if (albumName == '') {
      albumName = this.jwtService.getCurrentUser() + '';
    }
    this.router.navigate(['upload'], { queryParams: { album: albumName } });
  }

  create_album(){
    const dialogRef: MatDialogRef<StringDialogComponent> = this.dialog.open(StringDialogComponent, {
      width: '450px',
      data: this.dialogAlbumName
    });
    
    let path = this.jwtService.getCurrentUser() + '/';
    // let position = path.split('/').slice(1).join('/');
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        let address = result;
        address.replace('default', '');
        // if (position === "undefined") {
        //   address = result;
        // }
        // else{
        //   address = position + "/" + result
        // }
        this.albumService.create_album(address).subscribe({
          next: result => {
            alert("Album created!");
            console.log(result);
            this.getAlbums();
          },
          error: e =>
          {
            console.log(e)
            alert(e?.error?.message || JSON.stringify(e));
          }
        });
      }
    });
    
  }

}
