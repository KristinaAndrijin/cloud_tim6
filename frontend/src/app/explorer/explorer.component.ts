import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { ActivatedRoute } from '@angular/router';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { StringDialogComponent } from '../string-dialog/string-dialog.component';
import { AlbumService } from '../backend_services/album.service';
import { AlbumDialogComponent } from '../album-dialog/album-dialog.component';
import { JwtService } from '../jwt.service';




@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.css']
})
export class ExplorerComponent {
  albums!: any;
  files: any[] = [];
  albumName: string = "";
  dialogAlbumName: string ="";

  constructor(private filesService: FilesService, private router: Router, private route: ActivatedRoute, private dialog: MatDialog, private albumService:AlbumService, private jwtService: JwtService) { }

  ngOnInit(): void {
    // console.log(this.albums);
    // this.albums = this.filesService.getDummyAlbums();
    this.files = this.filesService.getFiles();
    this.route.queryParams.subscribe(params => {
      this.albumName = params['album'];
    });
    this.getAlbums();
  }

  navigateToExplorer(albumName: string) {
    this.router.navigate(['explorer'], { queryParams: { album: albumName } }).then(()=>{location.reload();});
  }

  navigateToDetails(fileName: string) {
    this.router.navigate(['details'], { queryParams: { file: fileName }} );
  }

  deleteAlbum(album: any) {
    const album_to_delete = album.owner+"/"+album.name
    console.log(album_to_delete)
    this.albumService.delete_album(album_to_delete).subscribe(
      {
        next: result => {
          alert("Album deleted!");
          console.log(result);
          this.getAlbums();
        },
        error: e =>
        {
          console.log(e)
          alert(e?.error?.message || JSON.stringify(e));
        }
      }
    )
  }
  
  editAlbumPermissions(album: any) {
    let album_key = album.owner + '/' + album.name
    console.log(album.name);
    if (album.owner.split('/')[0] != this.jwtService.getCurrentUser()) {
      alert('You cannot access permissions for this file');
    } else {
      this.router.navigate(['permissions'], { queryParams: { album_key: album_key } });
    }
  }
  
  editFile(file: any) {
    // Handle edit file functionality
  }
  
  moveFile(file: any) {
    // Handle move file functionality
  }
  
  downloadFile(file: any) {
    // Handle download file functionality
  }
  
  addToAlbum(file: any) {
    // Handle add file to album functionality
  }
  
  deleteFile(file: any) {
    // Handle delete file functionality
  }

  // izvuci ime iz file key ??
  editFilePermissions(file: any) {
    let file_key = "kris/slay.omg"
    this.router.navigate(['permissions'], { queryParams: { file_key: file_key } });
  }
  uploadFile(albumName: string) {
    this.router.navigate(['upload'], { queryParams: { album: albumName } });
  }

  create_album(){
    const dialogRef: MatDialogRef<StringDialogComponent> = this.dialog.open(StringDialogComponent, {
      width: '450px',
      data: this.dialogAlbumName
    });
    
    let path = this.albumName.split('/');
    let position = path.slice(1).join('/');
    console.log(position);
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log(result);
        this.albumService.create_album(position + "/" + result).subscribe({
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

  openAlbumDialog(file: any) {
    const dialogRef = this.dialog.open(AlbumDialogComponent, {
      width: '450px',
      data: this.albums
    });
  
    dialogRef.afterClosed().subscribe(album => {
      if (album) {
        console.log(album.name);
      }
    });
  }
  
  
  getAlbums() {
    let path = this.albumName.split('/');
    let position = path.slice(1).join('/') + '/';
    let back_albums = [{}];
    this.filesService.getAlbums().subscribe(
      {
        next: result => {
          console.log(result);
          let albums_back = result.albums;
          albums_back.forEach((element: string) => {
            if (element.startsWith(this.albumName + '/')) {
              let parts = element.split('/');
              let owner = parts[0];
              let album_name = parts.slice(1).join('/').replace(this.albumName, '');
              let fancy_album_name = parts.slice(1).join('/').replace(position, '');
              back_albums.push({ name: album_name, owner: owner, fancy_name: fancy_album_name });
            }
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
