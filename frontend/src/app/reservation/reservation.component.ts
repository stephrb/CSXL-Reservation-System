import { Component } from '@angular/core';
import { Route } from '@angular/router'
import { Observable } from 'rxjs';
import { Profile, ProfileService } from '../profile/profile.service';
import { Reservation, ReservationService, Reservable } from './reservation.service';
import { PermissionService } from '../permission.service';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})

export class ReservationComponent {

  public hours: string[] = [];
  public profile$: Observable<Profile | undefined>;
  public checkinPermission$: Observable<boolean>;
  public adminPermission$: Observable<boolean>;
  public userReservations$: Observable<Reservation[]>;
  public reservables$: Observable<Reservable[]>;

  constructor( public profileService: ProfileService, public reservationService: ReservationService, private permission: PermissionService
  ){{
    this.hours = this.getHours(new Date());  
    this.profile$ = profileService.profile$;
    this.checkinPermission$ = this.permission.check('checkin.create', 'checkin/');
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    this.userReservations$ = this.reservationService.getUserReservations();
    this.reservables$ = this.reservationService.getListReservables();
  }


  }
  public static Route: Route = {
    path: 'reservation',
    component: ReservationComponent, 
    title: 'Reservation', 
  };

  getHours(date: Date): string[] {
    const hours = [];
    for (let i = 0; i < 24; i++) {
      let hour = i % 12 || 12;
      let suffix = i >= 12 ? 'pm' : 'am';
      const hourString = hour + ':00' + suffix;
      hours.push(hourString);
    }
    return hours;
}


  hasReservation(reservable: any): Observable<boolean> {
    return this.reservationService.hasReservation(reservable);
  }
  

  isReserved(reservation: Reservation, hour: string): boolean {
    return this.reservationService.isReserved(reservation, hour);
  }
  
}
