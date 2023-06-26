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
    
    
  ];

  getAlbums() {
    return this.albums;
  }
}
