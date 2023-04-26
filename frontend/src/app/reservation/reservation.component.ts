import { Component, ChangeDetectorRef } from '@angular/core';
import { Route } from '@angular/router'
import { Observable, of } from 'rxjs';
import { Profile, ProfileService } from '../profile/profile.service';
import { Reservation, ReservationService, Reservable, reservableForm } from './reservation.service';
import { PermissionService } from '../permission.service';


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
  public reservable_form: reservableForm = {
      name: '',
      type: '',
      description: null
    };
  public profile$: Observable<Profile | undefined>;
  public checkinPermission$: Observable<boolean>;
  public adminPermission$: Observable<boolean>;
  public userReservations$: Observable<readonly Reservation[]>;
  public listReservables$: Observable<readonly Reservable[]>;
  public reservablesWithAvailability$: Observable<{ reservable: Reservable, reservations: Reservation[] }[]>
  public displayedColumns: string[] = ['name', 'type', 'description', 'delete', 'edit'];
  public reservationColumns: string[] = ['date', 'time', 'reservation', 'type', 'description', 'delete'];
  public editRow: number = -1;

  constructor( public profileService: ProfileService, public reservationService: ReservationService, private permission: PermissionService, private cd: ChangeDetectorRef
  ){
    this.hours = this.getHours(new Date());  
    this.profile$ = profileService.profile$;
    this.checkinPermission$ = this.permission.check('checkin.create', 'checkin/');
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    this.userReservations$ = this.reservationService.getUserReservations();
    this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate);
    this.possibleEndTimes$ = of();
    this.listReservables$ = this.reservationService.getListReservables();
    this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate)
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
            this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate)
            this.cd.detectChanges(); 
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
    const start = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 9, 0);
  const end = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 19, 0);
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
  
  onDeleteReservable(reservable: Reservable) {
    if (window.confirm("You are about to delete " + reservable.name)) {
      this.reservationService
        .deleteReservable(reservable.id)
        .subscribe({
          next: () => {
            this.listReservables$ = this.reservationService.getListReservables();
            this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate)
            this.cd.detectChanges();
          },
          error: (err) => this.onError(err)
        });
    }
  }

  onCreateReservable(reservable_form: reservableForm) {
    if (window.confirm("You are about to add " + reservable_form.name)) {
      this.reservationService
        .createReservable(reservable_form)
        .subscribe({
          next: () => {
            this.listReservables$ = this.reservationService.getListReservables();
            this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate)
            this.cd.detectChanges();
            reservable_form.name = '';
            reservable_form.type = '';
            reservable_form.description = null;
          },
          error: (err) => this.onError(err)
        });
    }
  }

  onCellClick(date: Date, reservable: Reservable) {
    this.selectedStartTime = date;
    this.selectedReservable = reservable;
    this.possibleEndTimes$ = this.reservationService.getAvailableEndTimes(this.selectedReservable.id, this.selectedStartTime);
  }

  onCreateReservation() {
    if(this.selectedReservable && this.selectedStartTime && this.selectedEndTime) {
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

  isEdit(reservable_id: number) {
    return reservable_id == this.editRow;
  }

  onEditClick(reservable_id: number) {
    this.editRow = reservable_id; 
  }

  onSaveEdits(id: number, name: string, type: string, description: string) {
    const reservable: Reservable = { id, name, type, description };
    if (window.confirm("Update " + reservable.name + "?")) {
          this.reservationService
          .updateReservable(reservable)
          .subscribe({
            next: () => {
              this.listReservables$ = this.reservationService.getListReservables();
              this.reservablesWithAvailability$ = this.reservationService.getReservablesWithAvailability(this.selectedDate);
              this.cd.detectChanges(); 
            },
            error: (err) => this.onError(err)
          });
    }
    this.editRow = -1;
  }
    
}
