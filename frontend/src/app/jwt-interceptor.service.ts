import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JwtInterceptorService implements HttpInterceptor {

  constructor() { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>>{
    const jwt = sessionStorage.getItem('accessToken');
    if (jwt){

      //moguće da će nam trebati specifičniji url filter
      if( request.url.startsWith('https://projekat6.s3.amazonaws.com')){
        return next.handle(request);
      }

      const cloned = request.clone({
        setHeaders:{
          Authorization: `${jwt}`
        }
      });
      return next.handle(cloned);
    }
    else{
      return next.handle(request);
    }
  } 
}
