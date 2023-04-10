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

    getAvailability(reservable_id: number, year: number, month: number, day: number): Observable<Reservation[]> {
      return this.http.get<Reservation[]>("/api/reservation/" + reservable_id + year + month + day)
    }
  
}