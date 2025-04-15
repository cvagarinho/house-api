import pika
import json
from app.schemas.recommendation import Recommendation
from app.core.config import settings

class RecommendationPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.rabbitmq_host,
                port=settings.rabbitmq_port,
                credentials=pika.PlainCredentials(
                    settings.rabbitmq_user,
                    settings.rabbitmq_password
                )
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=settings.rabbitmq_queue)

    def publish_recommendation(self, recommendation: Recommendation):
        message = {
            "recommendation_id": recommendation.id,
            "recommendation": recommendation.recommendation_text,
            "timestamp": recommendation.timestamp.isoformat()
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key=settings.rabbitmq_queue,
            body=json.dumps(message)
        )

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()