import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-album-dialog',
  templateUrl: './album-dialog.component.html',
  styleUrls: ['./album-dialog.component.css']
})
export class AlbumDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<AlbumDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public albums: any[]
  ) {}

  selectAlbum(album: any) {
    this.dialogRef.close(album);
  }
}
