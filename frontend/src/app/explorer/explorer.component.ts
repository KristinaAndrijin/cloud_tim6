import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { MatDialog } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { ActivatedRoute } from '@angular/router';



@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.css']
})
export class ExplorerComponent {
  albums: any[] = [];
  files: any[] = [];
  albumName: string = "";

  constructor(private filesService: FilesService, private router: Router, private route: ActivatedRoute) { }

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

  showAlbumOptions(event: MouseEvent) {
    event.stopPropagation();
  }
  
  showFileOptions(event: MouseEvent) {
    event.stopPropagation();
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
  
  

}
