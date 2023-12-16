from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.database.models.base import Base

if TYPE_CHECKING:
    from .event import Event
    from .user import User


class Category(Base):
    __tablename__ = "category"

    name: Mapped[str | None]

    events: Mapped[list["Event"]] = relationship(back_populates="category")
    users: Mapped[list["User"]] = relationship(secondary="favorite_category", back_populates="categories")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"
