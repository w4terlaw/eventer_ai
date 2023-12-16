from sqlalchemy.orm import Mapped, mapped_column

from core import database
from core.database import SessionLocal


class Base(database.Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    def save(self, session: SessionLocal, commit: bool = True):
        session.add(self)
        if commit:
            session.commit()
        return self
