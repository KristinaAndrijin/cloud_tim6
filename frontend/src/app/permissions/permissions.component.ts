import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-permissions',
  templateUrl: './permissions.component.html',
  styleUrls: ['./permissions.component.css']
})
export class PermissionsComponent implements OnInit {

  album: boolean = false;
  album_key: string = "";
  file_key: string="";

  constructor(private router: Router, private route: ActivatedRoute) {}
  
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['album_key']) {
        this.album = true;
        this.album_key = params['album_key'];
      } else {
        this.album = false;
        this.file_key = params['file_key'];
      }

      console.log(this.album);
      console.log(this.album_key);
      console.log(this.file_key);
      
      // this.activate(token);
    });
  }
}
