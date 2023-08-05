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

  

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.fileName = params['file'];
      this.albumName = params['album'];

      this.fileDetails = this.filesService.getFileDetails();
    });

    
  }
}
