import { Component, OnInit } from '@angular/core';
import { NgForm, FormGroup, FormControl, Validators, AbstractControl } from '@angular/forms';
import { Router } from '@angular/router';
import { FamilyInvitationService } from '../backend_services/family-invitation.service';

@Component({
  selector: 'app-invite-family-member',
  templateUrl: './invite-family-member.component.html',
  styleUrls: ['./invite-family-member.component.css']
})
export class InviteFamilyMemberComponent implements OnInit{
  inviteForm!: FormGroup;
  isDisabled: boolean = false;
  email: string = ""

  constructor(private router: Router, private invitationService: FamilyInvitationService) {
    this.check = this.check.bind(this);
   }
   
  ngOnInit(): void {
    this.inviteForm = new FormGroup({
      email: new FormControl('', Validators.required)},
      { validators: this.check },
    );
  }

  inviteUser() {
    this.email = this.inviteForm.get('email')?.value;
    this.invitationService.post_invitation(this.email).subscribe(
      {
        next: result => {
          console.log(result);
          alert("Invitation sent to: " + this.email);
        },
        error: err => {
          console.log(err);
          alert(err?.error?.message || JSON.stringify(err));
        }
      }
    )
    this.inviteForm.reset();
  }

  check(control: AbstractControl) {
    const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    const cmail = control.get('email');
    const isValidEmail = emailRegex.test(cmail?.value);
    if (isValidEmail) {
      this.isDisabled = false;
    } else {
      this.isDisabled = true;
    }
    const errors: { [key: string]: any } = {};
    if (!isValidEmail) {
      errors['validEmail'] = true;
    }
    return Object.keys(errors).length > 0 ? errors : null;
    
  }

}
