"""Import all models here to ensure they are registered with SQLAlchemy"""

from app.db.base import Base
from app.models.recommendation import RecommendationModel
from app.models.user import User

__all__ = ["Base", "User", "RecommendationModel"]
