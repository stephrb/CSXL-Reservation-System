from fastapi import APIRouter, Depends
from ..services import ReservableService
from ..models import Reservable

api = APIRouter(prefix="/api/reservable")

@api.get("", response_model=list[Reservable], tags=["Reservables"])
def get_reservables(res_svc: ReservableService = Depends()) -> list[Reservable]:
    return res_svc.list_reservables()
