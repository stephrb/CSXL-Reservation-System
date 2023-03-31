import { Component } from '@angular/core';
import { Route } from '@angular/router'
import { Observable } from 'rxjs';
import { Profile, ProfileService } from '../profile/profile.service';
import { Reservation, ReservationService } from './reservation.service';
import { PermissionService } from '../permission.service';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})

export class ReservationComponent {

  public profile$: Observable<Profile | undefined>;
  public checkinPermission$: Observable<boolean>;
  public adminPermission$: Observable<boolean>;
  public userReservations$: Observable<Reservation[]>;

  constructor( public profileService: ProfileService, public reservationService: ReservationService, private permission: PermissionService
  ){{
    this.profile$ = profileService.profile$;
    this.checkinPermission$ = this.permission.check('checkin.create', 'checkin/');
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    this.userReservations$ = this.reservationService.getUserReservations();
  }


  }
  public static Route: Route = {
    path: 'reservation',
    component: ReservationComponent, 
    title: 'Reservation', 
  };
}
