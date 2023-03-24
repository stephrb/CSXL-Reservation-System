from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Self
from sqlalchemy.types import DateTime
from .entity_base import EntityBase
from ..models import Reservation, Reservable, User

class ReservationEntity(EntityBase):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[DateTime] = mapped_column(DateTime, index=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime, index=True)
    reservable: Mapped[Reservable] = mapped_column(Reservable, index=True)
    user: Mapped[User] = mapped_column(User, index=True)

    @classmethod
    def from_model(cls, model: Reservable) -> Self:
        return cls(
            id=model.id,
            name=model.name,
            type=model.type,
            description=model.description,
        )

    def to_model(self) -> Reservable:
        return Reservable(
            id=self.id,
            name=self.name,
            type=self.type,
            description=self.description
        )