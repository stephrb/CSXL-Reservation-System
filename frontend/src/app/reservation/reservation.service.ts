import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, switchMap, forkJoin} from 'rxjs';
import { Paginated } from '../pagination';

export interface Reservation {
  id: number
  start_time: Date
  end_time:  Date
  reservable: Reservable
}

export interface Reservable {
    id: number
    name: string
    type: string
    description: string
}

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  constructor(private http: HttpClient) { }


  getUserReservations(): Observable<Reservation[]> {
    return this.http.get<Paginated<Reservation>>("/api/reservation").pipe(
      // Converts the nested observables into a single observable
      switchMap((reservations: Paginated<Reservation>) => 
        // Waits until last observable has emitted and combines the reservation observables to emit as an array
        forkJoin(
          reservations.items.map(reservation => this.getReservable(reservation.id).pipe(map(reservable => {
                return {
                  id: reservation.id,
                  start_time: new Date(reservation.start_time),
                  end_time: new Date(reservation.end_time),
                  reservable: reservable
                };})))
        )
      )
    );
  }
 

  getReservable(reservation_id: number): Observable<Reservable> {
    return this.http.get<Reservable>("/api/reservation/" +  reservation_id);
  }

  getListReservables(): Observable<Reservable[]> {
    return this.http.get<Reservable[]>("/api/reservable")
  }

  hasReservation(reservable: Reservable): Observable<boolean> {
    return this.getUserReservations().pipe(
      map((reservations: Reservation[]) =>
        reservations.some((r: Reservation) => r.reservable.name === reservable.name)
      )
    );
  }

  isReserved(reservation: Reservation, hour: string): boolean{
    const reservationStartTime = new Date(reservation.start_time);
    const reservationEndTime = new Date(reservation.end_time);
  
    const hourStartTime = new Date(reservationStartTime);
    const hourString = hour.slice(-2).toUpperCase();
    const hourValue = parseInt(hour.slice(0, 2), 10);
    if (hourString === "PM" && hourValue !== 12) {
      hourStartTime.setHours(hourValue + 12, 0, 0, 0);
    } else if (hourString === "AM" && hourValue === 12) {
      hourStartTime.setHours(0, 0, 0, 0);
    } else {
      hourStartTime.setHours(hourValue, 0, 0, 0);
    }
  
    const hourEndTime = new Date(hourStartTime);
    hourEndTime.setHours(hourEndTime.getHours() + 1);
  
    return (reservationStartTime < hourEndTime) && (reservationEndTime > hourStartTime);
  }
  
}