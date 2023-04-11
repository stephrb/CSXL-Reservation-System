from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservable
from ..entities import ReservableEntity
from .permission import PermissionService

class ReservableService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    def list_reservables(self) -> list[Reservable] | None:
        statement = select(ReservableEntity)
        entities = self._session.scalars(statement)
        return [entity.to_model() for entity in entities]