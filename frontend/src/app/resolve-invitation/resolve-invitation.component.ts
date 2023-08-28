import { Component, OnInit } from '@angular/core';
import { NgForm, FormGroup, FormControl, Validators, AbstractControl } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthenticationDetails, CognitoUser, CognitoUserPool } from 'amazon-cognito-identity-js';
import { environment } from 'src/environments/environment';
import { JwtService } from '../jwt.service';
import { FamilyInvitationService } from '../backend_services/family-invitation.service';
@Component({
  selector: 'app-resolve-invitation',
  templateUrl: './resolve-invitation.component.html',
  styleUrls: ['./resolve-invitation.component.css']
})
export class ResolveInvitationComponent implements OnInit {

  decided: boolean = false;
  isLoading: boolean = false;
  username: string = "";
  password: string = "";
  loginForm!: FormGroup;
  isDisabled: boolean = false;
  inviter_username: string = "";
  invitee_email: string ="";
  invitee_username: string = "";
  action: string = "";

  constructor(private router: Router, private jwtService: JwtService, private invitationService: FamilyInvitationService, private route: ActivatedRoute) {
    this.check = this.check.bind(this);
   }

   ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.inviter_username = params['inviter'];
      this.invitee_email = params['invitee_email'];
      this.invitee_username = params['invitee_username'];
      // this.activate(token);
    });
    this.loginForm = new FormGroup({
      password: new FormControl('', Validators.required),
      btn: new FormControl("")},
      { validators: this.check },
    );
  }

  onConfirm() {
    this.decided = true;
    console.log("confirmed");
    this.action = "confirm";
  }

  onDisprove() {
    this.decided = true;
    console.log("rejected");
    this.action = "disprove";
  }


  onLogin() {
    this.password = this.loginForm.get('password')?.value
    let authenticationDetails = new AuthenticationDetails({
      Username: this.inviter_username,
      Password: this.password,
  });
    let poolData = {
      UserPoolId: environment.cognitoUserPoolId,
      ClientId: environment.cognitoAppClientId
    };

    let userPool = new CognitoUserPool(poolData);
      let userData = { Username: this.inviter_username, Pool: userPool };
      var cognitoUser = new CognitoUser(userData);
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: (result) => {
          console.log("login uspesno");
          this.jwtService.setToken(result.getIdToken().getJwtToken());
          if (this.action == "confirm") {
              this.invitationService.confirm(this.invitee_email, this.invitee_username).subscribe({
                next: result => {
                  alert(result.message);
                  console.log(result.response);
                  this.jwtService.logout();
                },
                error: e =>{
                  alert(e?.error?.message);
                  console.log(e);
                }
              })
          } else {
            this.invitationService.disprove(this.invitee_email, this.invitee_username).subscribe({
              next: result => {
                alert(result.message);
                console.log(result.response);
                this.jwtService.logout();
              },
              error: e =>{
                alert(e?.error?.message);
                console.log(e);
              }
            })
          }
        },
        onFailure: (err) => {
          console.log("login neuspesna");
          console.log(authenticationDetails);
          alert(err.message || JSON.stringify(err));
          this.isLoading = false;
        },
      });
  }

  check(control: AbstractControl) {
    // const usernameRegex = /^[a-zA-Z0-9]+$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?=.*[^\s]).{8,}$/;
    const password = control.get('password');
    const isValidPassword = passwordRegex.test(password?.value);
    const cmail = control.get('username');
    // const isValidUsername = usernameRegex.test(cmail?.value);
    if (/*isValidUsername*/ /*&& isValidPassword*/ true) {
      this.isDisabled = false;
    } else {
      this.isDisabled = true;
    }
    const errors: { [key: string]: any } = {};
    // if (!isValidUsername) {
    //   errors['validUsername'] = true;
    // }
    if (!isValidPassword) {
      errors['validPassword'] = true;
    }
    return Object.keys(errors).length > 0 ? errors : null;
    
  }
}

