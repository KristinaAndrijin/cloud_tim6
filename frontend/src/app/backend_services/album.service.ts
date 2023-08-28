import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AlbumService {

  constructor(private http: HttpClient) {
   }
   create_album(album_name: string){
      return this.http.post(`${environment.baseUrl}create_album`,
      {"album_name": album_name},
      {headers: new HttpHeaders().set("content-type", "application/json")}
      );
   }
   delete_album(album_name: string){
    return this.http.post(`${environment.baseUrl}delete_album`,
    {"album_name": album_name},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }
 remove_file_from_album(filename:string, albumname:string, upload_date: string){
  return this.http.post(`${environment.baseUrl}remove_file_album`,{
    "album_name":albumname,
    "file_name":filename,
    "upload_date":upload_date
  })
 }

 getUsersPermissions(album_name: string):Observable<any> {
  return this.http.post(`${environment.baseUrl}get_access_by_user_album`,
    {"album_name": album_name},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }

 removeAccessPermissions(album_name: string, username: string):Observable<any> {
  return this.http.put(`${environment.baseUrl}remove_access_to_album_from_user`,
    {"album_name": album_name,
    "username": username},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }

 giveAccessPermissions(album_name: string, username: string):Observable<any> {
  return this.http.put(`${environment.baseUrl}give_access_to_album_to_user`,
    {"album_name": album_name,
    "username": username},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
 }
}
