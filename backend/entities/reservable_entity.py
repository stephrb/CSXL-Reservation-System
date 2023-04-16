from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Self
from .entity_base import EntityBase
from ..models import Reservable, ReservableForm

class ReservableEntity(EntityBase):
    __tablename__ = "reservable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    description: Mapped[str] = mapped_column(String(100))

    @classmethod
    def from_model(cls, model: Reservable) -> Self:
        return cls(
            id=model.id,
            name=model.name,
            type=model.type,
            description=model.description,
        )
    
    @classmethod
    def from_form_model(cls, model: ReservableForm) -> Self:
        return cls(
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

