import { Component, OnInit } from '@angular/core';
import { CognitoUserPool,CognitoUserAttribute, CognitoUser  } from 'amazon-cognito-identity-js';
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
  username:string = '';
  registerForm!: FormGroup;
  codeSent: boolean = false;
  codeForm!: FormGroup;
  userPool!: any;

  constructor(private router: Router) { }

  ngOnInit(): void {
    // if (!this.codeSent) {
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
    // } else {
      this.codeForm = new FormGroup({
        code: new FormControl('', Validators.required),
        btn: new FormControl("")},
      );
    // }
  }

  // onSignup() {}

  onSignup() {
    console.log("hej");
      this.isLoading = true;
      var poolData = {
        UserPoolId: environment.cognitoUserPoolId, 
        ClientId: environment.cognitoAppClientId 
      };
      this.userPool = new CognitoUserPool(poolData); 
      var attributeList = [];
      let formData: formDataInterface = {
        "given_name": this.registerForm.get('fname')?.value,
        "family_name": this.registerForm.get('lname')?.value,
        "custom:username": this.registerForm.get('username')?.value,
        "email": this.registerForm.get('email')?.value,
        "phone_number": this.registerForm.get('mobileNo')?.value,
        "birthdate": this.registerForm.get('birthdate')?.value,
      }
  
      for (let key in formData) {
        let attrData = {
          Name: key,
          Value: formData[key]
        }
        // console.log(key + " : " + formData[key]);
        let attribute = new CognitoUserAttribute(attrData); 
        attributeList.push(attribute)
      }
      this.username = this.registerForm.get('username')?.value
      this.userPool.signUp(this.username, this.registerForm.get('password')?.value, attributeList, [], (
        err: any,
        result: any
      ) => {
        this.isLoading = false;
        if (err) {
          alert(err.message || JSON.stringify(err));
          return;
        }
        console.log("jej");
        this.codeSent = true;
      //   const username = this.registerForm.get('username')?.value;
      // const userData = {
      //   Username: username,
      //   Pool: userPool
      // };
      // const cognitoUser = new CognitoUser(userData);
      // console.log(cognitoUser);
      // cognitoUser.confirmRegistration()
        // this.router.navigate(['/login']);
      });

      // const username = this.registerForm.get('username')?.value;
      // const userData = {
      //   Username: username,
      //   Pool: userPool
      // };
      // const cognitoUser = new CognitoUser(userData);
      // console.log(cognitoUser);
  }

  checkCode() {
    const username = this.username;
      const userData = {
        Username: username,
        Pool: this.userPool
      };
      const cognitoUser = new CognitoUser(userData);
      console.log(cognitoUser);
      let codeSuccess: boolean = false;
      cognitoUser.confirmRegistration(this.codeForm.get('code')?.value, true, function(err, result) {
        if (err) {
          console.log(err);
          alert(err.message || JSON.stringify(err));
          // Handle the error, e.g., display an error message to the user
        } else {
          console.log(result);
          alert("Slay!");
          codeSuccess = true;
          // this.router.navigate(['/login']);
          // The user has been successfully confirmed
          // You can now allow the user to sign in or perform other actions
        }
      })
    if (codeSuccess) {
      this.router.navigate(['/login']);
    }
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