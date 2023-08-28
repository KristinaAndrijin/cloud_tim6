import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InviteFamilyMemberComponent } from './invite-family-member.component';

describe('InviteFamilyMemberComponent', () => {
  let component: InviteFamilyMemberComponent;
  let fixture: ComponentFixture<InviteFamilyMemberComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InviteFamilyMemberComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InviteFamilyMemberComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
