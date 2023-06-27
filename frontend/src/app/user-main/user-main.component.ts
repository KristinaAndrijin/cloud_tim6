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

  constructor(private filesService: FilesService, private router: Router, private jwtService: JwtService, private album:AlbumService, private dialog: MatDialog) {
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
    const dialogRef: MatDialogRef<StringDialogComponent> = this.dialog.open(StringDialogComponent, {
      width: '300px',
      data: this.dialogAlbumName
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // Handle the result (string) here
        console.log(result);
        this.dialogAlbumName = result;
        const albumName = this.currentAlbum + this.dialogAlbumName;
        this.album.create_album(albumName).subscribe({
          next: result => {
            alert("Album kreiran!");
            console.log(result);
          },
          error: e =>
          {console.log(e)}
        });
      }
    });
    
  } 

}
