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
    { name: 'smesno', owner: 'Mirko' },
    { name: 'default', owner: 'Mirko' },
    { name: 'smesno', owner: 'Mirko' },
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

  private fileDetails = {
    name: "Dummy File",
    format: "PDF",
    size: "2.5 MB",
    uploadDate: "2023-06-26",
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    tags: ["tag1", "tag2", "tag3"]
  };

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

  getFileDetails() {
    return this.fileDetails;
  }

  uploadFile(file: File | null, fileDescription: string, fileTags: string): void {
    console.log("File:", file);
    console.log("Description:", fileDescription);
    console.log("Tags:", fileTags);
  }
}
