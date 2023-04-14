from fastapi import APIRouter, Depends
from ..services import ReservableService
from ..models import Reservable, ReservableForm

api = APIRouter(prefix="/api/reservable")

@api.get("", response_model=list[Reservable], tags=["Reservables"])
def get_reservables(res_svc: ReservableService = Depends()) -> list[Reservable]:
    return res_svc.list_reservables()

@api.post("", response_model=Reservable, tags=["Reservables"])
def create_reservable(reservable_form: ReservableForm, res_svc: ReservableService = Depends()):
    return res_svc.add_reservable(reservable_form)

@api.delete("/{reservable_id}", tags=["Reservables"])
def delete_reservable(reservable_id: int, res_svc: ReservableService = Depends()):
    res_svc.delete_reservable(reservable_id=reservable_id)

