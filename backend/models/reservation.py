"""Reservations are the data object to keep track of user reservations"""

from pydantic import BaseModel
from sqlalchemy.types import DateTime
from . import User, Reservable

class Reservation(BaseModel):
    id: int | None = None
    start_time: DateTime
    end_time: DateTime
    reservable: Reservable
    user: User
