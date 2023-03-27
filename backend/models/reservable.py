"""Reservables can be reserved by a registered user"""

from pydantic import BaseModel
class Reservable(BaseModel):
    id: int | None = None
    name: str
    type: str
    description: str | None = None