import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from app.db.base import Base


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.now)
    recommendation_text = Column(String)
