import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import { UserMainComponent } from './user-main/user-main.component';
import { InviteFamilyMemberComponent } from './invite-family-member/invite-family-member.component';
import { FamilyRegistrationComponent } from './family-registration/family-registration.component'; 
import { ExplorerComponent } from './explorer/explorer.component';
import { DetailsComponent } from './details/details.component';
import {UploadComponent} from './upload/upload.component'

const routes: Routes = [
  {path: "", component: LoginComponent},
  {path: "login", component: LoginComponent},
  {path: "registration", component: RegistrationComponent},
  {path: "main", component: UserMainComponent},
  {path: "invite", component: InviteFamilyMemberComponent},
  {path: "family-registration", component: FamilyRegistrationComponent},
  {path: "explorer", component: ExplorerComponent},
  {path: "details", component: DetailsComponent},
  {path: "upload", component:UploadComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
