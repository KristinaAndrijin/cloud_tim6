import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProtectedDashboardTryComponent } from './protected-dashboard-try.component';

describe('ProtectedDashboardTryComponent', () => {
  let component: ProtectedDashboardTryComponent;
  let fixture: ComponentFixture<ProtectedDashboardTryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProtectedDashboardTryComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProtectedDashboardTryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
