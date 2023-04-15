from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservable, ReservableForm, User
from ..entities import ReservableEntity
from .permission import PermissionService

class ReservableService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    def list_reservables(self) -> list[Reservable] | None:
        """Lists all reservables"""
        statement = select(ReservableEntity)
        entities = self._session.scalars(statement)
        return [entity.to_model() for entity in entities]
    
    def add(self, reservable_form: ReservableForm, subject: User):
        """Adds a reservable given that the User has proper permissions"""
        self._permission.enforce(subject, 'reservable.add', 'reservable/')
        new_entity: ReservableEntity = ReservableEntity.from_form_model(reservable_form)
        self._session.add(new_entity)
        self._session.commit()
        return new_entity.to_model()
    
    def delete(self, reservable_id: int, subject: User):
        """Deletes a reservable given that the User has proper permissions"""
        self._permission.enforce(subject, 'reservable.delete', f'reservable/{reservable_id}')
        statement = delete(ReservableEntity).where(ReservableEntity.id==reservable_id)
        self._session.execute(statement)
        self._session.commit()