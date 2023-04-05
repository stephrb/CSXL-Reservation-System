from fastapi import APIRouter, Depends
from ..services import ReservationService
from ..models import Reservation, User, Paginated, PaginationParams, Reservable
from .authentication import registered_user
from operator import lt, ge

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
     pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter="")
     
     return res_svc.list_user_reservations(subject, pagination_params, upcoming)

@api.get("/{reservation_id}", response_model=Reservable | None, tags=['Reservations'])
def get_reservable(reservation_id: int, res_svc: ReservationService = Depends()):
     return res_svc.get_reservable(reservation_id)

@api.delete("/{reservation_id}", tags=['Reservations'])
def delete_reservation(reservation_id: int, res_svc: ReservationService = Depends()):
     res_svc.delete_reservation(reservation_id)
