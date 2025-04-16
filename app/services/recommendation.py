from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.redis_manager import redis_manager
from app.messaging.publisher import RecommendationPublisher
from app.models.recommendation import RecommendationModel
from app.schemas.recommendation import PatientData, Recommendation
from app.services.base import BaseService


class RecommendationService(BaseService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self._publisher = RecommendationPublisher()

    async def generate(self, patient_data: PatientData) -> Recommendation:
        recommendations = self._apply_rules(patient_data)
        db_recommendation = await self._save_recommendation(recommendations)
        recommendation = Recommendation(
            id=str(db_recommendation.id),
            timestamp=db_recommendation.timestamp.isoformat(),
            recommendation_text=db_recommendation.recommendation_text,
        )
        await self._publish_recommendation(recommendation)
        return recommendation

    async def get_by_id(self, recommendation_id: str) -> Recommendation | None:
        cached = await redis_manager.get(f"recommendation:{recommendation_id}")
        if cached:
            return Recommendation(**cached)

        result = await self._db.get(RecommendationModel, recommendation_id)
        if not result:
            return None

        recommendation = Recommendation(
            id=str(result.id),
            timestamp=result.timestamp.isoformat(),
            recommendation_text=result.recommendation_text,
        )

        await redis_manager.set(
            f"recommendation:{recommendation_id}", recommendation.model_dump()
        )

        return recommendation

    def _apply_rules(self, patient_data: PatientData) -> list[str]:
        recommendations = []
        if patient_data.age > 65 and patient_data.has_chronic_pain:
            recommendations.append("Physical Therapy")
        if patient_data.bmi > 30:
            recommendations.append("Weight Management Program")
        if patient_data.recent_surgery:
            recommendations.append("Post-Surgery Recovery Plan")
        return recommendations

    async def _save_recommendation(
        self, recommendations: list[str]
    ) -> RecommendationModel:
        db_recommendation = RecommendationModel(
            timestamp=datetime.now(), recommendation_text=", ".join(recommendations)
        )
        self._db.add(db_recommendation)
        await self._db.commit()
        await self._db.refresh(db_recommendation)
        return db_recommendation

    async def _publish_recommendation(self, recommendation: Recommendation) -> None:
        try:
            await self._publisher.publish(recommendation.model_dump())
        except Exception as e:
            print(f"Failed to publish recommendation: {e}")
