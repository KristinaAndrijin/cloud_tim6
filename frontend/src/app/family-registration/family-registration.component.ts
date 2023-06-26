import { Component, OnInit } from '@angular/core';
import { CognitoUserPool,CognitoUserAttribute, CognitoUser } from 'amazon-cognito-identity-js';
import { NgForm, FormGroup, FormControl, Validators, AbstractControl} from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-family-registration',
  templateUrl: './family-registration.component.html',
  styleUrls: ['./family-registration.component.css']
})
export class FamilyRegistrationComponent implements OnInit {

  isLoading:boolean = false;
  username:string = '';
  registerForm!: FormGroup;
  codeSent: boolean = false;
  codeForm!: FormGroup;
  userPool!: any;
  isDisabled: boolean = false;
  isDisabledU: boolean = true;
  codeSuccessful: boolean = false;
  inviter_username: string = ""

  constructor(private route: ActivatedRoute, private router: Router) {
    this.check = this.check.bind(this);
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.inviter_username = params['inviter'];
      // this.activate(token);
    });
    this.registerForm = new FormGroup({
      inviter_username: new FormControl(this.inviter_username),
      email: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
      username: new FormControl('', Validators.required),
      fname: new FormControl('', Validators.required),
      lname: new FormControl('', Validators.required),
      mobileNo: new FormControl('', Validators.required),
      birthdate: new FormControl('', Validators.required),
      btn: new FormControl("")},
      { validators: this.check },
    );
  }

  onSignup() {
    // console.log("hej");
    //   this.isLoading = true;
    //   var poolData = {
    //     UserPoolId: environment.cognitoUserPoolId, 
    //     ClientId: environment.cognitoAppClientId 
    //   };
    //   this.userPool = new CognitoUserPool(poolData); 
    //   var attributeList = [];
    //   let formData: formDataInterface = {
    //     "given_name": this.registerForm.get('fname')?.value,
    //     "family_name": this.registerForm.get('lname')?.value,
    //     "preferred_username": this.registerForm.get('username')?.value,
    //     "email": this.registerForm.get('email')?.value,
    //     "phone_number": this.registerForm.get('mobileNo')?.value,
    //     "birthdate": this.registerForm.get('birthdate')?.value,
    //   }
  
    //   for (let key in formData) {
    //     let attrData = {
    //       Name: key,
    //       Value: formData[key]
    //     }
    //     // console.log(key + " : " + formData[key]);
    //     let attribute = new CognitoUserAttribute(attrData); 
    //     attributeList.push(attribute)
    //   }
    //   this.username = this.registerForm.get('username')?.value
    //   this.userPool.signUp(this.username, this.registerForm.get('password')?.value, attributeList, [], (
    //     err: any,
    //     result: any
    //   ) => {
    //     this.isLoading = false;
    //     if (err) {
    //       alert(err.message || JSON.stringify(err));
    //       return;
    //     }
    //     console.log("jej");
    //     this.codeSent = true;
    //   });
  }

  check(control: AbstractControl) {
    // return 
    const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?=.*[^\s]).{8,}$/;
    const lettersOnlyRegex = /^[A-Za-z]+$/;
    const numbersOnlyRegex = /^\+?\d+$/;
    const letterAndNumbersRegex = /^[a-zA-Z0-9]+$/;
    const password = control.get('password');
    const isValidPassword = passwordRegex.test(password?.value);
    const cmail = control.get('email');
    const isValidEmail = emailRegex.test(cmail?.value);
    const name = control.get('fname');
    const isValidName = lettersOnlyRegex.test(name?.value);
    const surname = control.get('lname');
    const isValidSurname = lettersOnlyRegex.test(surname?.value);
    const phoneNumber = control.get('mobileNo');
    const isPhoneValid = numbersOnlyRegex.test(phoneNumber?.value);
    const username = control.get('username');
    const isUsernameValid = letterAndNumbersRegex.test(username?.value);
    const birthdate = control.get('birthdate');
    const isBirthdateValid = birthdate?.value != '';
    if (isValidEmail && isValidPassword && isValidName && isValidSurname && isPhoneValid && isUsernameValid) {
      this.isDisabled = false;
    } else {
      this.isDisabled = true;
    }
    const errors: { [key: string]: any } = {};
    if (!isValidEmail) {
      errors['validEmail'] = true;
    }
    if (!isValidPassword) {
      errors['validPassword'] = true;
    }
    if (!isValidName) {
      errors['validName'] = true;
    }
    if (!isValidSurname) {
      errors['validSurname'] = true;
    }
    if (!isPhoneValid) {
      errors['validPN'] = true;
    }
    if (!isUsernameValid) {
      errors['validUsername'] = true;
    }
    if (!isBirthdateValid) {
      errors['validB'] = true;
    }
   return Object.keys(errors).length > 0 ? errors : null;
  }

}

interface formDataInterface {
  "given_name": string;
  "family_name": string;
  "preferred_username": string;
  "email": string;
  "phone_number": string;
  "birthdate": string;
  [key: string]: string;
};