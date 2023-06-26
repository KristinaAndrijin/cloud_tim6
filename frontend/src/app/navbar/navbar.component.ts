import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';
import { JwtService } from '../jwt.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  @Input() currentAlbum: string = '';
  
  constructor(private router: Router, private jwtService: JwtService) {}

  ngOnInit(): void { }

  goToMainPage() {
    this.router.navigate(['main']);
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
}
