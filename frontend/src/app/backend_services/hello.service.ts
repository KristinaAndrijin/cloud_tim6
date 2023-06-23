import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class HelloService {

  constructor(private http: HttpClient) { }

  sendHello():Observable<any>{
    return this.http.get("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/hello");
  }
  
}
