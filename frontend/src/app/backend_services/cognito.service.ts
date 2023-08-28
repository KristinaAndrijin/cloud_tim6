import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CognitoService {

  constructor(private http: HttpClient) { }

  login(username: string, password:string) {
    return this.http.post(`${environment.baseUrl}login`,
    {"username": username,
    "password": password},
    {headers: new HttpHeaders().set("content-type", "application/json")})
  }
}
