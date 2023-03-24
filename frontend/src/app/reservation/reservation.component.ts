import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router'

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.css']
})

export class ReservationComponent {
  public static Route: Route = {
    path: 'reservation',
    component: ReservationComponent, 
    title: 'Reservation', 
  };
}
