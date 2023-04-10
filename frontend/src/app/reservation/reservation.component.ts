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

  public selectedDate: Date = new Date();
  public hours: Date[] = [];
  public profile$: Observable<Profile | undefined>;
  public checkinPermission$: Observable<boolean>;
  public adminPermission$: Observable<boolean>;
  public userReservations$: Observable<Reservation[]>;
  public reservablesWithAvailability$: Observable<{ reservable: Reservable, reservations: Reservation[] }[]>

  constructor( public profileService: ProfileService, public reservationService: ReservationService, private permission: PermissionService
  ){
    this.hours = this.getHours(new Date());  
    this.profile$ = profileService.profile$;
    this.checkinPermission$ = this.permission.check('checkin.create', 'checkin/');
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    this.userReservations$ = this.reservationService.getUserReservations();
    this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate.getFullYear(), this.selectedDate.getMonth(), this.selectedDate.getDate())
  }
  public static Route: Route = {
    path: 'reservation',
    component: ReservationComponent, 
    title: 'Reservation', 
  };

  getHours(date: Date): Date[] {
    const start = new Date(date.getFullYear(), date.getMonth(), date.getDate()); 
    const end = new Date(start.getTime() + 24 * 60 * 60 * 1000 - 1); 
    const timeIncrement = 30 * 60 * 1000; 
    const result: Date[] = [];
    let current = start; 
    while (current <= end) {
      result.push(new Date(current.getTime())); 
      current = new Date(current.getTime() + timeIncrement); 
    }
    return result;
  }

  isAvailable(reservations: Reservation[], hour: Date, test:any): boolean {
    const reservation = reservations.some(reservation => {
      const startHour: Date = new Date(reservation.start_time);
      const endHour: Date = new Date(reservation.end_time);
      return hour >= startHour && hour < endHour;
    });

    return !reservation;
  }
  


  onDateChange(event: any) {
    this.selectedDate = event.value;
    this.hours = this.getHours(this.selectedDate);
    this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(
      this.selectedDate.getFullYear(), 
      this.selectedDate.getMonth(), 
      this.selectedDate.getDate())
  }

}
