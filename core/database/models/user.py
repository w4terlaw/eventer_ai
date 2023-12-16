from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.database.models.base import Base

if TYPE_CHECKING:
    from .event import Event
    from .category import Category


class User(Base):
    __tablename__ = "user"

    last_name: Mapped[str | None]
    first_name: Mapped[str | None]
    middle_name: Mapped[str | None]

    categories: Mapped[list["Category"]] = relationship(
        secondary="favorite_category", back_populates="users"
    )
    # categories_details: Mapped[list["FavoriteCategory"]] = relationship(back_populates="user")

    events: Mapped[list["Event"]] = relationship(
        secondary="user_event", back_populates="users"
    )
    # events_details: Mapped[list["UserEvent"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.last_name} {self.first_name} {self.middle_name})"
