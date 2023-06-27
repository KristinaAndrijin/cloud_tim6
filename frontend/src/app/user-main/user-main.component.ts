import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';
import { JwtService } from '../jwt.service';
import { AlbumService } from '../backend_services/album.service';

@Component({
  selector: 'app-user-main',
  templateUrl: './user-main.component.html',
  styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit {

  constructor(private router: Router, private jwtService: JwtService, private album:AlbumService) {
  }

  ngOnInit(): void {
  }

  logout() {
    let poolData = {
      UserPoolId: environment.cognitoUserPoolId,
      ClientId: environment.cognitoAppClientId
    };
    let userPool = new CognitoUserPool(poolData);
    let cognitoUser = userPool.getCurrentUser();
    cognitoUser?.signOut();
    this.jwtService.logout();
    this.router.navigate(['']).then(()=>{location.reload();});
  }

  create_album(){
    this.album.create_album("test123").subscribe();
  }

}
