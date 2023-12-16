from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models.base import Base

if TYPE_CHECKING:
    from .city import City
    from .organization import Organization
    from .category import Category
    from .user import User


class Event(Base):
    __tablename__ = "event"

    title: Mapped[str | None]
    street: Mapped[str | None]
    maxPrice: Mapped[str | None]
    startDate: Mapped[datetime | None]
    endDate: Mapped[datetime | None]
    rating: Mapped[str | None]

    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))

    city: Mapped["City"] = relationship(back_populates="events")
    organization: Mapped["Organization"] = relationship(back_populates="events")
    category: Mapped["Category"] = relationship(back_populates="events")
    users: Mapped[list["User"]] = relationship(
        secondary="user_event", back_populates="events"
    )

    # users_details: Mapped[list["UserEvent"]] = relationship(back_populates="event")

    def __repr__(self):
        return f"Event(id={self.id}, title={self.title})"
