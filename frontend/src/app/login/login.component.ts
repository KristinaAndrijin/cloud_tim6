import { Component, OnInit } from '@angular/core';
import { NgForm, FormGroup, FormControl, Validators, AbstractControl } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationDetails, CognitoUser, CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';
import { JwtService } from '../jwt.service';
import { HelloService } from '../backend_services/hello.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  isLoading: boolean = false;
  username: string = "";
  password: string = "";
  loginForm!: FormGroup;
  isDisabled: boolean = false;

  constructor(private router: Router, private jwtService: JwtService, private helloService: HelloService) {
    this.check = this.check.bind(this);
   }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      username: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
      btn: new FormControl("")},
      { validators: this.check },
    );
  }

  onLogin() {
    this.username = this.loginForm.get('username')?.value;
    this.password = this.loginForm.get('password')?.value
    let authenticationDetails = new AuthenticationDetails({
      Username: this.username,
      Password: this.password,
  });
    let poolData = {
      UserPoolId: environment.cognitoUserPoolId,
      ClientId: environment.cognitoAppClientId
    };

    let userPool = new CognitoUserPool(poolData);
      let userData = { Username: this.username, Pool: userPool };
      var cognitoUser = new CognitoUser(userData);
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: (result) => {
          console.log("login uspesno");
          const accessToken = result.getAccessToken().getJwtToken();
          console.log(result.getIdToken().getJwtToken());
          this.jwtService.setToken(result.getIdToken().getJwtToken());
          // this.helloService.sendHello().subscribe({
          //   next: result => {
          //     // console.log("hello stigao")
          //     // alert(result.message);
          //     // console.log(result.event);
          //     // console.log(result);
          //   },
          //   error: e =>
          //   {console.log("no")}
          // })
          console.log('Access Token:', accessToken);
          // alert("slay")
          this.router.navigate(["main"]);
        },
        onFailure: (err) => {
          console.log("login neuspesna");
          alert(err.message || JSON.stringify(err));
          this.isLoading = false;
        },
      });
  }

  check(control: AbstractControl) {
    const usernameRegex = /^[a-zA-Z0-9]+$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?=.*[^\s]).{8,}$/;
    const password = control.get('password');
    const isValidPassword = passwordRegex.test(password?.value);
    const cmail = control.get('username');
    const isValidUsername = usernameRegex.test(cmail?.value);
    if (isValidUsername && isValidPassword) {
      this.isDisabled = false;
    } else {
      this.isDisabled = true;
    }
    const errors: { [key: string]: any } = {};
    if (!isValidUsername) {
      errors['validUsername'] = true;
    }
    if (!isValidPassword) {
      errors['validPassword'] = true;
    }
    return Object.keys(errors).length > 0 ? errors : null;
    
  }



}
