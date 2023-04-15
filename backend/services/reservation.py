from fastapi import Depends
from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservation, User, PaginationParams, Paginated, Reservable
from ..entities import ReservationEntity, ReservableEntity
from .permission import PermissionService
from datetime import datetime, timedelta
from operator import ge, lt
import operator

class ReservationService:
    
    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    
    def list_user_reservations_private(self, user: User, pagination_params: PaginationParams, op: operator) -> Paginated[Reservation] | None:
        """Lists reservations associated with the given User"""

        statement = select(ReservationEntity).where(ReservationEntity.user_id == user.id).where(op(ReservationEntity.start_time, datetime.now()))
        length_statement = select(func.count()).select_from(ReservationEntity).where(ReservationEntity.user_id == user.id).where(op(ReservationEntity.start_time, datetime.now()))
        
        offset = pagination_params.page * pagination_params.page_size
        limit = pagination_params.page_size

        if pagination_params.order_by != '':
            statement = statement.order_by(
                getattr(ReservationEntity, pagination_params.order_by))

        statement = statement.offset(offset).limit(limit)

        length = self._session.execute(length_statement).scalar()
        entities = self._session.execute(statement).scalars()

        return Paginated(items=[entity.to_model() for entity in entities], length=length, params=pagination_params)
    

    def list_user_reservations(self, user: User, pagination_params: PaginationParams, upcoming: bool) -> Paginated[Reservation] | None:
        """Gets a list of reservations for a user based on if they are upcoming or past reservations"""
        if upcoming:
            return self.list_user_reservations_private(user, pagination_params, ge)
        else:
            return self.list_user_reservations_private(user, pagination_params, lt)
        
    def get_reservable(self, reservation_id: int) -> Reservable | None:
        """Gets a reservable for a specific reservation"""
        statement = select(ReservableEntity).join(ReservationEntity).where(ReservationEntity.id==reservation_id)
        entity = self._session.scalar(statement)
        if entity:
            return entity.to_model()
    
    def get_reservation(self, reservation_id: int) -> Reservation | None:
        """Gets a reservation given the reservation id number"""
        statement = select(ReservationEntity).where(ReservationEntity.id==reservation_id)
        entity = self._session.scalar(statement)
        if entity:
            return entity.to_model()

    def delete_reservation(self, reservation_id: int) -> None:
        """Deletes a reservation given a reservation id number"""
        statement = delete(ReservationEntity).where(ReservationEntity.id==reservation_id)
        self._session.execute(statement)
        self._session.commit()

    def get_reservations_by_reservable(self, reservable_id: int, date: datetime) -> list[Reservation] | None:
        """Gets a list of reservations given a reservable id number"""
        statement = select(ReservationEntity).where(ReservationEntity.reservable_id == reservable_id)\
        .filter(ReservationEntity.start_time >= date, ReservationEntity.start_time < date + timedelta(days=1))
        entities = self._session.scalars(statement)
        return [entity.to_model() for entity in entities]