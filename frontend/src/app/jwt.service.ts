import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class JwtService {

  getToken() {
    return sessionStorage.getItem('accessToken');
  }

  setToken(accessToken: string) {
    sessionStorage.setItem('accessToken',accessToken);
  }

  logout(){
    sessionStorage.clear();
  }

  getCurrentUser() {
    return sessionStorage.getItem('username');
  }

  setCurrentUser(user: string) {
    sessionStorage.setItem('username', user);
  }

  constructor() { }
}
