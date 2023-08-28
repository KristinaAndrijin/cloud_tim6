import { TestBed } from '@angular/core/testing';

import { FamilyInvitationService } from './family-invitation.service';

describe('FamilyInvitationService', () => {
  let service: FamilyInvitationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FamilyInvitationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
