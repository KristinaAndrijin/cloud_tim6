import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FamilyInvitationService {

  constructor(private http: HttpClient) { }

  post_invitation(email:string):Observable<any> {
    return this.http.post(`${environment.baseUrl}post_invitation`,
    {"email": email},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }


  accept_invitation(inviter:string, inviter_email:string, invitee: string, invitee_username:string):Observable<any> {
    return this.http.put(`${environment.baseUrl}accept_invitation`,
    {"inviter": inviter,
      "inviter_email": inviter_email,
      "invitee": invitee,
      "invitee_username": invitee_username
    },
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }

  confirm(invitee_email: string, invitee_username: string):Observable<any> {
    return this.http.post(`${environment.baseUrl}start_handler`,
    {"invitee_email": invitee_email,
      "invitee_username": invitee_username,
      "action": "CONFIRM"
    },
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }

  disprove(invitee_email: string, invitee_username: string):Observable<any> {
    return this.http.post(`${environment.baseUrl}start_handler`,
    {"invitee_email": invitee_email,
      "invitee_username": invitee_username,
      "action": "DISPROVE"
    },
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }



}