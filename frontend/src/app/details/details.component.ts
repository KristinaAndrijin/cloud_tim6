import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FilesService } from '../backend_services/files.service';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css']
})
export class DetailsComponent {
  fileName: string = "";
  albumName: string = "";
  fileDetails: any;
  constructor(private route: ActivatedRoute, private filesService: FilesService) { }


  formatBytes(bytes: number, decimals: number = 2): string {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }
  

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.fileName = params['file'];
      this.albumName = params['album'];

      this.filesService.getMetadata(this.fileName).subscribe(
        response => {
          console.log(response);
          this.fileDetails = response;
        },
        error => {
          console.error('Error fetching metadata:', error);
          // Handle error scenario
        }
      );
    });
  }


  download()
  {
    this.filesService.generatePresignedUrl(this.fileName).subscribe(
      response => {
        if (response.signedUrl) {
          const link = document.createElement('a');
          link.href = response.signedUrl; // Use the generated presigned URL
          link.target = '_blank'; // Open the URL in a new tab
          link.download = this.fileName; // Set the suggested filename for the download
          link.click(); // Trigger the click event on the link to start the download
        } else {
          console.error('No signed URL received for download.');
        }
      },
      error => {
        console.error('Error generating presigned URL:', error);
      }
    );
  }
}
