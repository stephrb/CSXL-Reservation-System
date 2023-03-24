"""Reservations are the data object to keep track of user reservations"""

from pydantic import BaseModel
from datetime import datetime
from . import User, Reservable

class Reservation(BaseModel):
    id: int | None = None
    start_time: datetime
    end_time: datetime
