import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FilesService {

  constructor() { }

  private albums = [
    { name: 'default', owner: 'Mirko' },
    { name: 'smesno', owner: 'Mirko' },
    { name: 'Abkhaz', owner: 'Stevan' },
    { name: 'default', owner: 'Mirko' },
    { name: 'smesno', owner: 'Mirko' },
    { name: 'default', owner: 'Mirko' },
    { name: 'smesno', owner: 'Mirko' },
    { name: 'default', owner: 'Mirko' },
    { name: 'smesno', owner: 'Mirko' },
    { name: 'default', owner: 'Mirko' },
    { name: 'smesno', owner: 'Mirko' },
    { name: 'default', owner: 'Mirko' },
  ];

  private files = [
    { name: 'snake.png', owner: 'Mirko', dateUploaded: '2022-07-12' },
    { name: 'documentbralenale.xml', owner: 'Aleksandar Aleksandrovic', dateUploaded: '2022-06-28' },
    // Add more dummy file objects as needed
  ];

  getAlbums() {
    return this.albums;
  }

  getFiles() {
    return this.files;
  }
}
