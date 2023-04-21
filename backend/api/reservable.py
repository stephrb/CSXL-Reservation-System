from fastapi import APIRouter, Depends, HTTPException, Query
from ..services import ReservableService, UserPermissionError
from ..models import Reservable, ReservableForm, User
from .authentication import registered_user

api = APIRouter(prefix="/api/reservable")

@api.get("", response_model=list[Reservable], tags=["Reservables"])
def get_reservables(res_svc: ReservableService = Depends()) -> list[Reservable]:
    """Gets a list of all reservables in the reservable database."""
    return res_svc.list_reservables()

@api.post("", response_model=Reservable, tags=["Reservables"])
def create_reservable(reservable_form: ReservableForm, subject: User = Depends(registered_user), res_svc: ReservableService = Depends()):
    """Creates a reservable using the given ReservableForm."""
    try:
        return res_svc.add(reservable_form, subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@api.delete("/{reservable_id}", tags=["Reservables"])
def delete(reservable_id: int, subject: User = Depends(registered_user), res_svc: ReservableService = Depends()):
    """Deletes the specified reservable using the given id number."""
    try:
        res_svc.delete(reservable_id=reservable_id, subject=subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
@api.get("/filter", response_model=list[Reservable], tags=["Reservables"])
def get_reservables_by_types(types: list[str] | None = Query(None), res_svc: ReservableService = Depends()) -> list[Reservable]:
    """Gets a list of reservables that have the specified types."""
    return res_svc.filter_by_type(types)