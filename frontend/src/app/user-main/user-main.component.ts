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

  constructor(private filesService: FilesService, private router: Router, private jwtService: JwtService, private album:AlbumService, private dialog: MatDialog) {
  }
  albums: any[] = [];

  ngOnInit(): void {
    this.albums = this.filesService.getAlbums();
  }

  navigateToExplorer(albumName: string) {
    this.router.navigate(['explorer'], { queryParams: { album: albumName } });
  }

  create_album(){
    const dialogRef: MatDialogRef<StringDialogComponent> = this.dialog.open(StringDialogComponent, {
      width: '250px',
      data: this.dialogAlbumName
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // Handle the result (string) here
        console.log(result);
        this.album.create_album(result).subscribe({
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
