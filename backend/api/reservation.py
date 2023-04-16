from fastapi import APIRouter, Depends, HTTPException
from ..services import ReservationService
from ..models import Reservation, User, Paginated, PaginationParams, Reservable, ReservationForm
from .authentication import registered_user
from datetime import datetime

api = APIRouter(prefix="/api/reservation")

@api.get("", response_model=Paginated[Reservation], tags=['Reservations'])
def list_user_reservations(
    subject: User = Depends(registered_user), 
    res_svc: ReservationService = Depends(),
    page: int = 0,
    page_size: int = 10,
    order_by: str = "start_time",
    upcoming: bool = True
) -> Paginated[Reservation]:
     """Lists all of the reservations for a given User."""
     pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter="")
     
     return res_svc.list_user_reservations(subject, pagination_params, upcoming)

@api.get("/{reservation_id}", response_model=Reservable | None, tags=['Reservations'])
def get_reservable(reservation_id: int, res_svc: ReservationService = Depends()):
     """Gets a reservable given the associated Reservation."""
     return res_svc.get_reservable(reservation_id)

@api.delete("/{reservation_id}", tags=['Reservations'])
def delete_reservation(reservation_id: int, res_svc: ReservationService = Depends()):
     """Deletes a reservation using the given reservation id number."""
     res_svc.delete_reservation(reservation_id)

@api.get("/availability/{reservable_id}", response_model=list[Reservation], tags=["Reservations"])
def get_availability(reservable_id: int, date:datetime, res_svc: ReservationService = Depends()):
     """Lists all of the reservations associated with a reservable using the given reservable id number."""
     return res_svc.get_reservations_by_reservable(reservable_id, date)

@api.post("", response_model=Reservation, tags=['Reservations'])
def create_reservation(
     reservationForm: ReservationForm,
     subject: User = Depends(registered_user), 
     res_svc: ReservationService = Depends()):
     """Creates a reservation using the associated ReservationForm for the User."""
     try:
          reservation = res_svc.create_reservation(reservationForm, subject.id)
          return reservation
     except ValueError:
          raise HTTPException(409, detial='Reservation could not be created due to an overlapping reservation')

@api.get("/end_time/{reservable_id}", response_model=list[datetime], tags=['Reservations'])
def get_available_end_times(reservable_id: int, start_time: datetime, res_svc: ReservationService = Depends()):
     """Gets the available end times for a start_time to allow the user to create a reservation."""
     try:
          return res_svc.get_available_end_times(reservable_id, start_time)
     except ValueError:
          raise HTTPException(422, detail=f'start_time: {start_time} is not a valid time slot like XX:00:00.00 or XX:30:00.00')
          

