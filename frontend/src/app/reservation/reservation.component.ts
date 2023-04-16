import { Component, ChangeDetectorRef } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { Route } from '@angular/router'
import { Observable, of } from 'rxjs';
import { Profile, ProfileService } from '../profile/profile.service';
import { Reservation, ReservationService, Reservable } from './reservation.service';
import { PermissionService } from '../permission.service';
import { FormBuilder } from '@angular/forms';


@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})

export class ReservationComponent {

  public selectedDate: Date = new Date();
  public hours: Date[] = [];
  public selectedStartTime: Date | undefined;
  public selectedReservable: Reservable | undefined;
  public selectedEndTime: Date | undefined;
  public possibleEndTimes$: Observable<Date[]>;
  public profile$: Observable<Profile | undefined>;
  public checkinPermission$: Observable<boolean>;
  public adminPermission$: Observable<boolean>;
  public userReservations$: Observable<Reservation[]>;
  public reservablesWithAvailability$: Observable<{ reservable: Reservable, reservations: Reservation[] }[]>

  constructor( public profileService: ProfileService, public reservationService: ReservationService, private permission: PermissionService, private cd: ChangeDetectorRef, private formBuilder: FormBuilder){
    this.hours = this.getHours(new Date());  
    this.profile$ = profileService.profile$;
    this.checkinPermission$ = this.permission.check('checkin.create', 'checkin/');
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    this.userReservations$ = this.reservationService.getUserReservations();
    this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate);
    this.possibleEndTimes$ = of();
  }

  public static Route: Route = {
    path: 'reservation',
    component: ReservationComponent, 
    title: 'Reservation', 
  };

  onDeleteReservation(reservation: Reservation) {
    if (window.confirm("You are about to delete your reservation for " + reservation.reservable.name + " on " 
      + reservation.start_time.toLocaleString() + " - " + reservation.end_time.toLocaleTimeString())) {
      this.reservationService
        .deleteReservation(reservation.id)
        .subscribe({
          next: () => {
            this.userReservations$ = this.reservationService.getUserReservations();
            this.cd.detectChanges(); // Trigger change detection manually
          },
          error: (err) => this.onError(err)
        });
    }
  }

  private onError(err: Error) {
    if (err.message) {
      window.alert(err.message);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
  }

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

  isAvailable(reservations: Reservation[], hour: Date): boolean {
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
    this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate);
  }

  isValidDate(date: Date): boolean {
    return date.getTime() > Date.now(); 
  }

  onCellClick(date: Date, reservable: Reservable){
    this.selectedStartTime = date;
    this.selectedReservable = reservable;
    this.possibleEndTimes$ = this.reservationService.getAvailableEndTimes(this.selectedReservable.id, this.selectedStartTime);
  }

  onCreateReservation() {
    if(this.selectedReservable && this.selectedStartTime && this.selectedEndTime){
       if (window.confirm("Create a reservation for " + this.selectedReservable.name + " on " 
        + this.selectedStartTime.toLocaleString() + " - " + this.selectedEndTime.toLocaleTimeString() +"?")) {
          this.reservationService
          .createReservation(this.selectedStartTime, this.selectedEndTime, this.selectedReservable.id)
          .subscribe({
            next: () => {
              this.userReservations$ = this.reservationService.getUserReservations();
              this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate);
              this.selectedReservable = undefined;
              this.selectedStartTime = undefined; 
              this.selectedEndTime = undefined;
              this.cd.detectChanges(); 
            },
            error: (err) => this.onError(err)
          });
      }
    }
  }
    
}
