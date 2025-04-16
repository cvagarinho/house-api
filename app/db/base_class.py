"""Import all models here to ensure they are registered with SQLAlchemy"""

from app.db.base import Base
from app.models.user import User
from app.models.recommendation import RecommendationModel

__all__ = ["Base", "User", "RecommendationModel"]