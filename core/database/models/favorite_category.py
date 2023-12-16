from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base

if TYPE_CHECKING:
    pass


class FavoriteCategory(Base):
    __tablename__ = "favorite_category"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    # user: Mapped["User"] = relationship(back_populates="categories_details")
    # category: Mapped["Category"] = relationship(back_populates="users_details")

    def __repr__(self):
        return f"FavoriteCategory(id={self.id}, user_id={self.user_id}, category_id={self.category_id})"
