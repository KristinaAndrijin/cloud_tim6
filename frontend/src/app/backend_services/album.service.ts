import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

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

 getUsersPermissions(album_name: string):Observable<any> {
  return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/get_access_by_user_album",
    {"album_name": album_name},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }

 removeAccessPermissions(album_name: string, username: string):Observable<any> {
  return this.http.put("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/remove_access_to_album_from_user",
    {"album_name": album_name,
    "username": username},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }

 giveAccessPermissions(album_name: string, username: string):Observable<any> {
  return this.http.put("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/give_access_to_album_to_user",
    {"album_name": album_name,
    "username": username},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }
}
