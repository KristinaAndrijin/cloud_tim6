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
    //console.log("INTERCEPTED! Adding JWT: ", jwt);
    // if(request.url.includes('/user/refreshToken')){
    //   return next.handle(request);
    // }
    if (jwt){
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
