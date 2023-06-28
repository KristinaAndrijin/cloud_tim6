import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class FilesService {

  constructor(private http: HttpClient) { }

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

  getAlbums():Observable<any> {
    return this.http.get("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/get_albums_by_user");
  }

  getFiles() {
    return this.files;
  }

  getFileDetails() {
    return this.fileDetails;
  }

  getDummyAlbums() {
    return this.albums;
  }

  uploadFile(file: File, fileDescription: string, fileTags: string, address: string): Observable<any> {
    const url = 'https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/get_signed_url';
    const fileName = file.name;

    return this.http.post(url, { fileName }).pipe(
      map((response: any) => {
        console.log(response.signedUrl);
        const { signedUrl, key } = response;
        return this.uploadToS3(signedUrl, file, key);
      })
    );
  }

  private uploadToS3(signedUrl: string, file: File, key: string): Observable<any> {
    const headers = { 'Content-Type': file.type };

    return this.http.post(signedUrl, file, { headers });
  }

}
