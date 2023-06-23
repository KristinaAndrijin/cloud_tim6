import { Component, OnInit } from '@angular/core';
import { NgForm, FormGroup, FormControl, Validators, AbstractControl } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationDetails, CognitoUser, CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  isLoading: boolean = false;
  email_address: string = "";
  password: string = "";
  loginForm!: FormGroup;
  isDisabled: boolean = false;

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      email: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
      btn: new FormControl("")},
      // { validators: this.check },
    );
  }

  onLogin() {
    
  }

}
