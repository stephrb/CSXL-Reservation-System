from fastapi import APIRouter, Depends
from ..services import ReservationService
from ..models import Reservation, User
from .authentication import registered_user

api = APIRouter(prefix="/api/reservation")

@api.get("", response_model=list[Reservation], tags=['Reservation'])
def list_reservations(subject: User = Depends(registered_user), res_svc: ReservationService = Depends()):
    return res_svc.list(subject)
