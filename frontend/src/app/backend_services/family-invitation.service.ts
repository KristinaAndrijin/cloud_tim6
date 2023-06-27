import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FamilyInvitationService {

  constructor(private http: HttpClient) { }

  post_invitation(email:string):Observable<any> {
    return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/post_invitation",
    {"email": email},
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }


  accept_invitation(inviter:string, inviter_email:string, invitee: string, invitee_username:string):Observable<any> {
    return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/accept_invitation",
    {"inviter": inviter,
      "inviter_email": inviter_email,
      "invitee": invitee,
      "invitee_username": invitee_username
    },
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }

  confirm(invitee_email: string, invitee_username: string):Observable<any> {
    return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/confirm_invite",
    {"invitee_email": invitee_email,
      "invitee_username": invitee_username
    },
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }

  disprove(invitee_email: string, invitee_username: string):Observable<any> {
    return this.http.post("https://yccc05r7mh.execute-api.eu-central-1.amazonaws.com/dev/disprove_invite",
    {"invitee_email": invitee_email,
      "invitee_username": invitee_username
    },
    {headers: new HttpHeaders().set("content-type", "application/json")}
    );
  }



}