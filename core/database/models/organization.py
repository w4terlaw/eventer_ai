from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.database.models.base import Base

if TYPE_CHECKING:
    from .event import Event


class Organization(Base):
    __tablename__ = "organization"

    name: Mapped[str | None]
    logo: Mapped[str | None]
    phone: Mapped[str | None]

    events: Mapped[list["Event"]] = relationship(back_populates="organization")

    def __repr__(self):
        return f"Organization(id={self.id}, name={self.name})"
