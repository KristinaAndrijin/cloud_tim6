import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { switchMap, catchError } from 'rxjs/operators';
import { EMPTY } from 'rxjs';
import { environment } from '../../environments/environment';



export interface FileMetadata 
{
  name : string,
  size : number,
  type : string,
  upload_date : string,
  description: string,
  tags : string,
}

export interface AlbumObjectData

{
  album_key: string
  file_name : string
}

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


  private files = [
    { name: 'kreizi.gif', owner: 'vlada', dateUploaded: '1944-06-24' },
    { name: 'documentbralenale.xml', owner: 'Aleksandar Aleksandrovic', dateUploaded: '2022-06-28' },
    // Add more dummy file objects as needed
  ];

  getAlbums():Observable<any> {
    return this.http.get(`${environment.baseUrl}get_albums_by_user`);
  }

  getFiles() {
    return this.files;
  }

  getMetadata(fileName: string): Observable<any> {
    const url = `${environment.baseUrl}obtain_metadata`;
    const body = {
      obj_key: fileName
    };

    return this.http.post(url, body);
  }

  getDummyAlbums() {
    return this.albums;
  }

  /*uploadFile(file: File, fileDescription: string, fileTags: string, address: string): Observable<any> {
    const url = 'https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/get_signed_url';
    const fileName = file.name;

    return this.http.post(url, { fileName }).pipe(
      map((response: any) => {
        console.log(response.signedUrl);
        const { signedUrl, key } = response;
        return this.uploadToS3(signedUrl, file, key).subscribe();
      })
    );
  }
*/

// uploadFile(file: File, fileDescription: string, fileTags: string, address: string): Observable<any>{
//     const url = `${environment.baseUrl}get_signed_url`;
//   const fileName = file.name;
//   return this.http.post(url, {fileName});
// }
  

  uploadFile(file: File, fileDescription: string, fileTags: string, address: string): Observable<any> {
    const url = `${environment.baseUrl}get_signed_url`;
    const fileName = file.name;
    const contentType = file.type;

    return this.http.post(url, { fileName, contentType }).pipe(
      switchMap((response: any) => {
        const { signedUrl, key } = response;
        console.log(signedUrl)
        return this.uploadToS3(signedUrl, file, key).pipe(
          catchError(error => {
            console.error('File upload to S3 failed:', error);
            return EMPTY;
          }),
          switchMap(() => {
            return this.uploadFileMetadata(file, fileDescription, fileTags, address);
          }),
          switchMap(() => {
            return this.uploadAlbumObject(file, fileDescription, fileTags, address);
          }),
        );
      })
    );
  }

  
  uploadToS3(signedUrl: string, file: File, key: string): Observable<any> {
    const headers = { 'Content-Type': file.type };

    return this.http.put(signedUrl, file, { headers });
  }

  uploadFileMetadata(file: File, fileDescription: string, fileTags: string, address: string): Observable<any> {
    const url = `${environment.baseUrl}upload_write_metadata_to_queue`;
    const fileName = file.name;
    const now = new Date();

    const meta : FileMetadata = 
    {
      name : file.name,
      size : file.size,
      type : file.type,
      upload_date : now.toDateString(),
      description: fileDescription,
      tags : fileTags,
    }

    return this.http.post(url, meta);
  }

  uploadAlbumObject(file: File, fileDescription: string, fileTags: string, address: string): Observable<any> {
    //todo: implement
    const url = `${environment.baseUrl}write_album_object_to_queue`;
    const fileName = file.name;
    const now = new Date();

    const aoData :  AlbumObjectData =
    {
      album_key: address,
      file_name : file.name
    }

    return this.http.post(url, aoData);
  }


  generatePresignedUrl(fileName: string): Observable<{ signedUrl: string }> {
    const url = `${environment.baseUrl}/generate_presigned_url_download`; 

    const payload = {
      fileName: fileName
    };

    return this.http.post<{ signedUrl: string }>(url, payload);
  }

}
