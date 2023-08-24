import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, concat, forkJoin } from 'rxjs';
import { map, mergeMap } from 'rxjs/operators';
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
  replaces: string | null
}

export interface AlbumObjectData

{
  album_key: string,
  file_name : string,
  upload_date : string,
}

@Injectable({
  providedIn: 'root'
})
export class FilesService {
  
  delete_item(fileName: string) {
    return this.http.post(`${environment.baseUrl}delete_item`, {'object_key': fileName})
  }

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

  getAlbums(albumName: string):Observable<any> {
    return this.http.post(`${environment.baseUrl}get_albums_by_user`,
    {"album_name": albumName},
    {headers: new HttpHeaders().set("content-type", "application/json")});
  }

  getFilesDummy() {
    return this.files;
  }


  getFiles(albumName: string):Observable<any> {
    console.log(albumName);
    // const currentDate: Date = new Date();

    // const year: number = currentDate.getFullYear();
    // const month: number = currentDate.getMonth();
    // console.log(month+1);
    // const day: number = currentDate.getDate();

    // const hours: number = currentDate.getHours();
    // const minutes: number = currentDate.getMinutes();
    // const seconds: number = currentDate.getSeconds();

    // // const date: number = currentDate.getDate();

    // const formattedTime: string = `${day}.${month+1}.${year}. ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    // console.log(`Current time: ${formattedTime}`);
    return this.http.post(`${environment.baseUrl}get_files_by_album`,
      {"album_name": albumName},
      {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }

  create_album(album_name: string){
    return this.http.post(`${environment.baseUrl}create_album`,
    {"album_name": album_name},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }


  getMetadata(fileName: string): Observable<any> {
    const url = `${environment.baseUrl}obtain_metadata`;
    const body = {
      obj_key: fileName
    };

    return this.http.post(url, body);
  }

  changeMetadata(object_key:string, description:string, tags:string): Observable<any> {
    const url = `${environment.baseUrl}change_metadata`;
    const body = {
      obj_key: object_key,
      description: description,
      tags: tags,
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

  const currentDate: Date = new Date();

  const year: number = currentDate.getFullYear();
  const month: number = currentDate.getMonth();
  console.log(month+1);
  const day: number = currentDate.getDate();

  const hours: number = currentDate.getHours();
  const minutes: number = currentDate.getMinutes();
  const seconds: number = currentDate.getSeconds();

  // const date: number = currentDate.getDate();

  const now: string = `${day}.${month+1}.${year}. ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;


  return this.http.post(url, { fileName, contentType }).pipe(
    switchMap((response: any) => {
      const { signedUrl, key } = response;

      // Create observables for metadata and album uploads
      const uploadMetadata$ = this.uploadFileMetadata(file, fileDescription, fileTags, now, null);
      const uploadAlbum$ = this.uploadAlbumObject(file, fileDescription, fileTags, address, now);

      // Use concatMap to execute metadata and album uploads sequentially
      return concat(uploadMetadata$, uploadAlbum$).pipe(
        switchMap(() => {
          // After metadata and album uploads are finished, start upload to S3
          return this.uploadToS3(signedUrl, file, key).pipe(
            catchError(error => {
              console.error('File upload to S3 failed:', error);
              return EMPTY;
            })
          );
        })
      );
    })
  );
}


editFile(file: File, fileDescription: string, fileTags: string, obj_key:string): Observable<any> {
  const url = `${environment.baseUrl}generate_presigned_url_edit`;
  const fileName = file.name;
  const contentType = file.type;

  const currentDate: Date = new Date();

  const year: number = currentDate.getFullYear();
  const month: number = currentDate.getMonth();
  console.log(month+1);
  const day: number = currentDate.getDate();

  const hours: number = currentDate.getHours();
  const minutes: number = currentDate.getMinutes();
  const seconds: number = currentDate.getSeconds();

  // const date: number = currentDate.getDate();

  const now: string = `${day}.${month+1}.${year}. ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;


  return this.http.post(url, { obj_key, fileName ,contentType }).pipe(
    switchMap((response: any) => {
      const { signedUrl, key } = response;

      // Create observables for metadata and album uploads
      const uploadMetadata$ = this.uploadFileMetadata(file, fileDescription, fileTags, now, obj_key);

      // Use concatMap to execute metadata and album uploads sequentially
      return concat(uploadMetadata$).pipe(
        switchMap(() => {
          // After metadata and album uploads are finished, start upload to S3
          return this.uploadToS3(signedUrl, file, key).pipe(
            catchError(error => {
              console.error('File upload to S3 failed:', error);
              return EMPTY;
            })
          );
        })
      );
    })
  );
}




  
  uploadToS3(signedUrl: string, file: File, key: string): Observable<any> {
    const headers = { 'Content-Type': file.type };

    return this.http.put(signedUrl, file, { headers });
  }

  //ako postoji replaces onda ova poruka zapravo započinje edit koji menja i metadatu i album object i gdegod da se pojavi obj_key
  uploadFileMetadata(file: File, fileDescription: string, fileTags: string, now: string, replaces: string|null): Observable<any> {
    const url = `${environment.baseUrl}upload_write_metadata_to_queue`;
    const fileName = file.name;
    // const now = new Date();

    const meta : FileMetadata = 
    {
      name : file.name,
      size : file.size,
      type : file.type,
      upload_date : now,
      description: fileDescription,
      tags : fileTags,
      replaces: replaces
    }

    return this.http.post(url, meta);
  }

  uploadAlbumObject(file: File, fileDescription: string, fileTags: string, address: string, now: string): Observable<any> {
    //todo: implement
    const url = `${environment.baseUrl}write_album_object_to_queue`;
    const fileName = file.name;
    // const now = new Date();

    const aoData :  AlbumObjectData =
    {
      album_key: address,
      file_name : file.name,
      upload_date : now,
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

  getUsersPermissions(album_name: string, file_key: string):Observable<any> {
    return this.http.post(`${environment.baseUrl}get_access_by_user_file`,
      {"album_name": album_name,
        "file_key": file_key
      },
      {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }

  removeAccessPermissions(file_key: string, username: string):Observable<any> {
    return this.http.put(`${environment.baseUrl}remove_access_to_file_from_user`,
      {"file_key": file_key,
      "username": username},
      {headers: new HttpHeaders().set("content-type", "application/json")}
      );
   }
  
   giveAccessPermissions(file_key: string, username: string):Observable<any> {
    return this.http.put(`${environment.baseUrl}give_access_to_file_to_user`,
      {"file_key": file_key,
      "username": username},
      {headers: new HttpHeaders().set("content-type", "application/json")}
      );
   }

}
