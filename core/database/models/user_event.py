from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base

if TYPE_CHECKING:
    pass


class UserEvent(Base):
    __tablename__ = "user_event"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))

    def __repr__(self):
        return f"UserEvent(id={self.id}, user_id={self.user_id}, event_id={self.event_id})"
