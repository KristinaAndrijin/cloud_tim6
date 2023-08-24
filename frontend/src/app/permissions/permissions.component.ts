import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import {MatPaginator, PageEvent} from "@angular/material/paginator";
import { MatSort } from '@angular/material/sort';
import { MatDialog } from '@angular/material/dialog';
import {MatTableDataSource} from "@angular/material/table";
import { AlbumService } from '../backend_services/album.service';
import { FilesService } from '../backend_services/files.service';

@Component({
  selector: 'app-permissions',
  templateUrl: './permissions.component.html',
  styleUrls: ['./permissions.component.css']
})
export class PermissionsComponent implements OnInit {

  album: boolean = false;
  album_key: string = "";
  file_key: string="";
  album_name: string="";
  displayedColumns: string[] = ['username', 'actions'];
  dataSource = new MatTableDataSource<UserAccess>(ELEMENT_DATA);

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  constructor(private router: Router, private route: ActivatedRoute, private albumService: AlbumService, private filesService: FilesService) {}
  
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['album_key']) {
        this.album = true;
        this.album_key = params['album_key'];
        this.initAlbums();
      } else {
        this.album = false;
        // this.album = true
        this.file_key = params['file_key'];
        this.album_name = params['album_name'];
        this.initFiles();
      }

      // console.log(this.album);
      // console.log(this.album_key);
      // console.log(this.file_key);

      // this.albumService.getUsersPermissions(this.album_key);
      
      // this.activate(token);
    });
  }

initFiles() {
  console.log(this.file_key);
  console.log(this.album_name);
  this.filesService.getUsersPermissions(this.album_name, this.file_key).subscribe(
    {
      next: result => {
        let accesses = result.permissions;
        this.dataSource.data = accesses;
        console.log(result);
      },
      error: err => {
        console.log(err);
        alert(err?.error?.message || JSON.stringify(err));
      }
    }
  );
}

initAlbums() {
  this.albumService.getUsersPermissions(this.album_key).subscribe(
    {
      next: result => {
        let accesses = result.permissions;
        this.dataSource.data = accesses;
        console.log(result);
      },
      error: err => {
        console.log(err);
        alert(err?.error?.message || JSON.stringify(err));
      }
    }
  );

  // const dummy: UserAccess[] = [
  //   { username: 'user1', hasAccess: true },
  //   { username: 'user2', hasAccess: false },
  //   { username: 'user3', hasAccess: true },
  //   { username: 'user4', hasAccess: true },
  //   { username: 'user5', hasAccess: false },
  //   { username: 'user6', hasAccess: true },
  //   { username: 'user1', hasAccess: true },
  //   { username: 'user2', hasAccess: false },
  //   { username: 'user3', hasAccess: true },
  //   { username: 'user4', hasAccess: true },
  //   { username: 'user5', hasAccess: false },
  //   { username: 'user6', hasAccess: true }
  // ];
  // this.dataSource.data = dummy;
}

give_access(userAccess: UserAccess) {
  if (this.album) {
    let album_name = this.album_key.split('/').slice(1).join('/')
    // console.log(album_name);
    // console.log(userAccess.username);
    this.albumService.giveAccessPermissions(album_name, userAccess.username).subscribe(
      {
        next: result => {
          // alert('slay');
          this.initAlbums();
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    );
  } else {
    alert('slay');
    console.log(userAccess);
    console.log(this.file_key);
    this.filesService.giveAccessPermissions(this.file_key, userAccess.username).subscribe(
      {
        next: result => {
          // alert('slay');
          this.initFiles();
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    );
  }
}

remove_access(userAccess: UserAccess) {
  if (this.album) {
    let album_name = this.album_key.split('/').slice(1).join('/')
    // console.log(album_name);
    // console.log(userAccess.username);
    this.albumService.removeAccessPermissions(album_name, userAccess.username).subscribe(
      {
        next: result => {
          // alert('slay');
          this.initAlbums();
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    );
  } else {
    alert('slay');
    console.log(userAccess);
    console.log(this.file_key);
    this.filesService.removeAccessPermissions(this.file_key, userAccess.username).subscribe(
      {
        next: result => {
          // alert('slay');
          this.initFiles();
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    );
  }
}

}

const ELEMENT_DATA: UserAccess[] = [];

interface UserAccess {
  username: string;
  access: boolean;
  hasAccess: boolean;
}
