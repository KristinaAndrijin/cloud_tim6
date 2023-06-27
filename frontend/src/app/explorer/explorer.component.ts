import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { ActivatedRoute } from '@angular/router';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { StringDialogComponent } from '../string-dialog/string-dialog.component';
import { AlbumService } from '../backend_services/album.service';



@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.css']
})
export class ExplorerComponent {
  albums: any[] = [];
  files: any[] = [];
  albumName: string = "";
  dialogAlbumName: string ="";

  constructor(private filesService: FilesService, private router: Router, private route: ActivatedRoute, private dialog: MatDialog, private albumService:AlbumService) { }

  ngOnInit(): void {
    this.albums = this.filesService.getAlbums();
    this.files = this.filesService.getFiles();
    this.route.queryParams.subscribe(params => {
      this.albumName = params['album'];
    });
  }

  navigateToExplorer(albumName: string) {
    this.router.navigate(['explorer'], { queryParams: { album: albumName } });
  }

  navigateToDetails(fileName: string) {
    this.router.navigate(['details'], { queryParams: { file: fileName }} );
  }

  deleteAlbum(album: any) {
    // Handle delete album functionality
  }
  
  editAlbumPermissions(album: any) {
    let album_key = "kris/slay"
    this.router.navigate(['permissions'], { queryParams: { album_key: album_key } });
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
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log(result);
        this.albumService.create_album(result).subscribe({
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
