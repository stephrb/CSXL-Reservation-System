"""Reservables can be reserved by a registered user"""

from pydantic import BaseModel
class Reservable(BaseModel):
    """Reservable base model."""
    id: int | None = None
    name: str
    type: str
    description: str | None = None

class ReservableForm(BaseModel):
    """ReservableForm base model."""
    name: str
    type: str
    description: str | None