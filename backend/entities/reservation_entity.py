from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from ..models import Reservation, ReservationForm
from .user_entity import UserEntity
from .reservable_entity import ReservableEntity

class ReservationEntity(EntityBase):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    start_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    reservable_id: Mapped[int] = mapped_column(ForeignKey('reservable.id', ondelete="CASCADE"), index=True)
    reservable: Mapped[ReservableEntity] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    user: Mapped["UserEntity"] = relationship("UserEntity")

    @classmethod
    def from_model(cls, model: Reservation) -> Self:
        return cls(
            id=model.id,
            start_time=model.start_time,
            end_time=model.end_time
        )
    @classmethod
    def from_form_model(cls, model: ReservationForm) -> Self:
        return cls(start_time=model.start_time, end_time=model.end_time, reservable_id=model.reservable_id)

    def to_model(self) -> Reservation:
        return Reservation(
            id=self.id,
            start_time=self.start_time,
            end_time=self.end_time
        )