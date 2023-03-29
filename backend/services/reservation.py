from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Reservation, User, PaginationParams, Paginated
from ..entities import ReservationEntity
from .permission import PermissionService
from datetime import datetime
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