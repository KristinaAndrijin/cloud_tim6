import { Component, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';


@Component({
  selector: 'app-string-dialog',
  templateUrl: './string-dialog.component.html',
  styleUrls: ['./string-dialog.component.css']
})
export class StringDialogComponent {

  inputString: string = '';
  @Inject(MAT_DIALOG_DATA) public data: any
  constructor(
    public dialogRef: MatDialogRef<StringDialogComponent>,
    

  ) {
    this.inputString = '';
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }
}
