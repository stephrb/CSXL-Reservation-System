import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
// import { Observable, throwError, map, OperatorFunction, Subscriber } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {

  constructor(private http: HttpClient) { }
}
