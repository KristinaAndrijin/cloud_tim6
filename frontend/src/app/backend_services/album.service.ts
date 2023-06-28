import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AlbumService {

  constructor(private http: HttpClient) {
   }
   create_album(album_name: string){
      return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/create_album",
      {"album_name": album_name},
      {headers: new HttpHeaders().set("content-type", "application/json")}
      );
   }
   delete_album(album_name: string){
    return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/delete_album",
    {"album_name": album_name},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }
}
