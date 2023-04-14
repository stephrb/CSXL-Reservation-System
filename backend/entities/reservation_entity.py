from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from ..models import Reservation
from .user_entity import UserEntity
from .reservable_entity import ReservableEntity

class ReservationEntity(EntityBase):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    start_time: Mapped[DateTime] = mapped_column(DateTime, index=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime)

    reservable_id: Mapped[int] = mapped_column(ForeignKey('reservable.id', ondelete="CASCADE"), index=True)
    reservable: Mapped[ReservableEntity] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    user: Mapped[UserEntity] = relationship()

    @classmethod
    def from_model(cls, model: Reservation) -> Self:
        return cls(
            id=model.id,
            start_time=model.start_time,
            end_time=model.end_time
        )

    def to_model(self) -> Reservation:
        return Reservation(
            id=self.id,
            start_time=self.start_time,
            end_time=self.end_time
        )