from fastapi import APIRouter, Depends
from ..services import ReservationService
from ..models import Reservation, User, Paginated, PaginationParams, Reservable
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
     """Lists all of the reservations for a given User"""
     pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter="")
     
     return res_svc.list_user_reservations(subject, pagination_params, upcoming)

@api.get("/{reservation_id}", response_model=Reservable | None, tags=['Reservations'])
def get_reservable(reservation_id: int, res_svc: ReservationService = Depends()):
     """Gets a reservable given the associated Reservation"""
     return res_svc.get_reservable(reservation_id)

@api.delete("/{reservation_id}", tags=['Reservations'])
def delete_reservation(reservation_id: int, res_svc: ReservationService = Depends()):
     """Deletes a reservation using the given reservation id number"""
     res_svc.delete_reservation(reservation_id)

@api.get("/availability/{reservable_id}", tags=["Reservations"])
def get_availability(reservable_id: int, date:datetime, res_svc: ReservationService = Depends()):
     """Lists all of the reservations associated with a reservable using the given reservable id number"""
     return res_svc.get_reservations_by_reservable(reservable_id, datetime(date.year, date.month, date.day))
