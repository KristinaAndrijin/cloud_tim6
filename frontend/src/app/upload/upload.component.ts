// upload.component.ts
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FilesService } from '../backend_services/files.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {
  albumName: string = "";
  description: string = "";
  tags: string = "";
  file: File | null = null;

  constructor(private route: ActivatedRoute, private filesService: FilesService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.albumName = params['album'];
    });
  }

  onFileSelected(event: any): void {
    const fileList: FileList | null = event.target.files;
    if (fileList && fileList.length > 0) {
      this.file = fileList[0];
    }
  }

  uploadFile(): void {
    if (!this.file) {
      alert('Please select a file.'); 
      return; 
    }

    const fileDescription: string = this.description;
    const fileTags: string = this.tags;


    this.filesService.uploadFile(this.file, fileDescription, fileTags, this.albumName).subscribe(
      {
        next: result => {
          alert("File upload started");
          console.log(result);
        },
        error: e =>
        {
          console.log(e)
          alert(e?.error?.message || JSON.stringify(e));
        }
      }
    );

  }
}
