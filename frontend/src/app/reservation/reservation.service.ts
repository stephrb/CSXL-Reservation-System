import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Reservation {
  id: number
  start_time: Date
  end_time:  Date
  reservable_id: number
  reservable: Reservable
  user_id: number
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
    return this.http.get<Reservation[]>("/api/reservation").pipe(map((reservations: Reservation[]) => reservations.map(reservation => {
      return {  id: reservation.id,
                start_time: new Date(reservation.start_time),
                end_time:  new Date(reservation.end_time), 
                reservable_id: reservation.reservable_id, 
                reservable: {id: reservation.reservable.id, name: reservation.reservable.name, type: reservation.reservable.type, 
                  description: reservation.reservable.description}, 
                user_id: reservation.user_id}
    })
    ))
  }
}
