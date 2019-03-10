import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StartFundraiserComponent } from './start-fundraiser.component';

describe('StartFundraiserComponent', () => {
  let component: StartFundraiserComponent;
  let fixture: ComponentFixture<StartFundraiserComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StartFundraiserComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StartFundraiserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
