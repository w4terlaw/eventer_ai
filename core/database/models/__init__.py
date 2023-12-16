from core.database import Base, engine
from .category import Category
from .city import City
from .event import Event
from .favorite_category import FavoriteCategory
from .organization import Organization
from .user import User
from .user_event import UserEvent

Base.metadata.create_all(bind=engine)

__all__ = (
    "City",
    "Category",
    "Event",
    "Organization",
    "User",
    "UserEvent",
    "FavoriteCategory",
)
