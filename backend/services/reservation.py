from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservation, User
from ..entities import ReservationEntity
from .permission import PermissionService

class ReservationService:
    
    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    def list(self, user: User) -> list[Reservation] | None:
        query = select(ReservationEntity).where(ReservationEntity.user_id == user.id)
        reservation_list = self._session.scalars(query)
        if reservation_list is None:
            return None
        else:
            model = [reservation.to_model() for reservation in reservation_list]
            return model