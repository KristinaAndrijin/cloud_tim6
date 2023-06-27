import { Component, OnInit } from '@angular/core';
import { FilesService } from '../backend_services/files.service';
import { Router } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { MatDialog } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';



@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.css']
})
export class ExplorerComponent {
  albums: any[] = [];
  files: any[] = [];

  constructor(private filesService: FilesService, private router: Router) { }

  ngOnInit(): void {
    this.albums = this.filesService.getAlbums();
    this.files = this.filesService.getFiles();
  }

  logClickedItem(albumName: string) {
    console.log("Clicked item: " + albumName);
    this.router.navigate(["details"]);
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
    // Handle edit album permissions functionality
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
  
  

}
