import aio_pika
import json
from app.schemas.recommendation import Recommendation
from app.core.config import settings

class RecommendationPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = settings.rabbitmq_queue

    async def _ensure_connection(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(
                host=settings.rabbitmq_host,
                port=settings.rabbitmq_port,
                login=settings.rabbitmq_user,
                password=settings.rabbitmq_password
            )
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, recommendation: Recommendation):
        await self._ensure_connection()
        message = {
            "recommendation_id": recommendation.id,
            "recommendation": recommendation.recommendation_text,
            "timestamp": recommendation.timestamp.isoformat()
        }
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=self.queue_name
        )