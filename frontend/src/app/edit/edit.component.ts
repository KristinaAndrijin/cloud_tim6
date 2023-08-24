import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FilesService } from '../backend_services/files.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent {

  object_key: string = "";
  description: string = "";
  tags: string = "";
  file: File | null = null;

  constructor(
    private route: ActivatedRoute,
    private filesService: FilesService,
    private snackBar: MatSnackBar
  ) {}
  

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.object_key = params['object_key'];
    });

    this.filesService.getMetadata(this.object_key).subscribe(
      {next: result => {
        this.description = result.description
        this.tags = result.tags
      },
      error: e => {
        console.log(e);
        alert(e?.error?.message || JSON.stringify(e));
        console.log(e?.error?.message || JSON.stringify(e));
      }}
    )
  }

  onFileSelected(event: any): void {
    const fileList: FileList | null = event.target.files;
    if (fileList && fileList.length > 0) {
      this.file = fileList[0];
    }
  }

  editFile(): void {
    if (!this.file) {
      
      this.filesService.changeMetadata(this.object_key,this.description,this.tags).subscribe(
        {next: result => {
          this.snackBar.open('File metadata changed', 'Dismiss', {
            duration: 3000, 
            horizontalPosition: 'center', 
            verticalPosition: 'bottom' 
          });
          console.log(result);
        },
        error: e => {
          console.log(e);
          alert(e?.error?.message || JSON.stringify(e));
          console.log(e?.error?.message || JSON.stringify(e));
        }}
      )

    }
  
    const fileDescription: string = this.description;
    const fileTags: string = this.tags;
  
    /*this.filesService.uploadFile(this.file, fileDescription, fileTags, this.albumName).subscribe(
      {
        next: result => {
          console.log(this.albumName);
          this.snackBar.open('File upload started', 'Dismiss', {
            duration: 3000, 
            horizontalPosition: 'center', 
            verticalPosition: 'bottom' 
          });
          console.log(result);
        },
        error: e => {
          console.log(e);
          alert(e?.error?.message || JSON.stringify(e));
          console.log(e?.error?.message || JSON.stringify(e));
        }
      }
    );*/
  }

}
