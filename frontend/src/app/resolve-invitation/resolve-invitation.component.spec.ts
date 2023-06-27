import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResolveInvitationComponent } from './resolve-invitation.component';

describe('ResolveInvitationComponent', () => {
  let component: ResolveInvitationComponent;
  let fixture: ComponentFixture<ResolveInvitationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ResolveInvitationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResolveInvitationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
