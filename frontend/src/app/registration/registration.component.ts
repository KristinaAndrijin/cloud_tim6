import { Component, OnInit } from '@angular/core';
import { CognitoUserPool,CognitoUserAttribute  } from 'amazon-cognito-identity-js';
import { NgForm, FormGroup, FormControl, Validators, AbstractControl} from '@angular/forms';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';


@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent {
  isLoading:boolean = false;
  fname:string = '';
  lname:string = '';
  username:string = '';
  email:string = '';
  mobileNo:string = '';
  password:string = '';
  birthdate:string='';
  registerForm!: FormGroup;


  constructor(private router: Router) { }

  ngOnInit(): void {
    this.registerForm = new FormGroup({
      email: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
      username: new FormControl('', Validators.required),
      fname: new FormControl('', Validators.required),
      lname: new FormControl('', Validators.required),
      mobileNo: new FormControl('', Validators.required),
      birthdate: new FormControl('', Validators.required),
      btn: new FormControl("")},
      // { validators: this.check },
    );
  }

  // onSignup() {}

  onSignup() {
    console.log("hej");
      this.isLoading = true;
      var poolData = {
        UserPoolId: environment.cognitoUserPoolId, 
        ClientId: environment.cognitoAppClientId 
      };
      var userPool = new CognitoUserPool(poolData); 
      var attributeList = [];
      let formData: formDataInterface = {
        "given_name": this.fname,
        "family_name": this.lname,
        "custom:username": this.username,
        "email": this.email,
        "phone_number": this.mobileNo,
        "birthdate": this.birthdate,
      }
  
      for (let key in formData) {
        let attrData = {
          Name: key,
          Value: formData[key]
        }
        let attribute = new CognitoUserAttribute(attrData); 
        attributeList.push(attribute)
      }
      userPool.signUp(this.email, this.password, attributeList, [], (
        err: any,
        result: any
      ) => {
        this.isLoading = false;
        if (err) {
          alert(err.message || JSON.stringify(err));
          return;
        }
        console.log("jej");
        this.router.navigate(['/login']);
      });
  }
  

}


interface formDataInterface {
  "given_name": string;
  "family_name": string;
  "custom:username": string;
  "email": string;
  "phone_number": string;
  "birthdate": string;
  [key: string]: string;
};