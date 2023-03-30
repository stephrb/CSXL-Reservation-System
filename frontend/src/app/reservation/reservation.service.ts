import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Paginated } from '../pagination';

export interface Reservation {
  id: number
  start_time: Date
  end_time:  Date
}

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  constructor(private http: HttpClient) { }

  getUserReservations(): Observable<Reservation[]> {
    return this.http.get<Paginated<Reservation>>("/api/reservation").pipe(map((paginatedReservations: Paginated<Reservation>) => paginatedReservations.items.map(reservation => {
      return {  id: reservation.id,
                start_time: new Date(reservation.start_time),
                end_time:  new Date(reservation.end_time)}
    })
    ))
  }
}
