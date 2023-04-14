from fastapi import Depends
from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservation, User, PaginationParams, Paginated, Reservable, ReservationForm
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
        if upcoming:
            return self.list_user_reservations_private(user, pagination_params, ge)
        else:
            return self.list_user_reservations_private(user, pagination_params, lt)
        
    def get_reservable(self, reservation_id: int) -> Reservable | None:
        statement = select(ReservableEntity).join(ReservationEntity).where(ReservationEntity.id==reservation_id)
        entity = self._session.scalar(statement)
        if entity:
            return entity.to_model()
    
    def get_reservation(self, reservation_id: int) -> Reservation | None:
        statement = select(ReservationEntity).where(ReservationEntity.id==reservation_id)
        entity = self._session.scalar(statement)
        if entity:
            return entity.to_model()

    def delete_reservation(self, reservation_id: int) -> None:
        statement = delete(ReservationEntity).where(ReservationEntity.id==reservation_id)
        self._session.execute(statement)
        self._session.commit()

    def get_reservations_by_reservable(self, reservable_id: int, date: datetime) -> list[Reservation]:
        date = datetime(date.year, date.month, date.day)
        statement = select(ReservationEntity).where(ReservationEntity.reservable_id == reservable_id)\
        .filter(ReservationEntity.start_time >= date, ReservationEntity.start_time < date + timedelta(days=1))
        entities = self._session.scalars(statement)
        return [entity.to_model() for entity in entities]
    
    def create_reservation(self, reservation_form: ReservationForm, user_id: int) -> Reservation:        
        reservation_entity = ReservationEntity.from_form_model(reservation_form)
        reservations_on_day = self.get_reservations_by_reservable(reservation_form.reservable_id, reservation_form.start_time)
        for reservation in reservations_on_day:
            if reservation.start_time < reservation_form.end_time and reservation_form.start_time < reservation.end_time:
                raise ValueError(f'New reservation with start_time: {reservation_form.start_time} and end_time: {reservation_form.end_time} overlaps with existing reservation from {reservation.start_time} to {reservation.end_time}')
        reservation_entity.user_id = user_id
        self._session.add(reservation_entity)
        self._session.commit()

        return reservation_entity.to_model()

    
    def get_available_end_times(self, reservable_id: int, start_time: datetime) -> list[datetime]:
        if start_time < datetime.now(start_time.tzinfo) or start_time.minute not in [0, 30] or start_time.second != 0 or start_time.microsecond != 0:
            raise ValueError(f'Start_time: {start_time} is not a valid time slot')
        
        max_end_time = min(datetime(year=start_time.year, month=start_time.month, day=start_time.day, tzinfo=start_time.tzinfo) + timedelta(days=1), start_time + timedelta(hours=3))
        statement = select(ReservationEntity).filter(ReservationEntity.reservable_id == reservable_id,
                                                    ReservationEntity.start_time >= start_time,
                                                    ReservationEntity.start_time < max_end_time)
        
        closest_reservation = self._session.scalars(statement).first()
        
        closest_time = closest_reservation.to_model().start_time if closest_reservation and closest_reservation.to_model().start_time < max_end_time else max_end_time

        available_reservations = [start_time + timedelta(minutes=30) * i for i in range(1, (closest_time - start_time) // timedelta(minutes=30) + 1)]

        return available_reservations