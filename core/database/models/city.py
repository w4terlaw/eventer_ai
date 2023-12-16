from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.database.models.base import Base

if TYPE_CHECKING:
    from .event import Event


class City(Base):
    __tablename__ = "city"

    name: Mapped[str | None]

    events: Mapped[list["Event"]] = relationship(back_populates="city")

    def __repr__(self):
        return f"City(id={self.id}, name={self.name})"
