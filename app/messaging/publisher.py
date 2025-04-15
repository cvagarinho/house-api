import pika
import json
from app.schemas.recommendation import Recommendation

class RecommendationPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',  # service name from docker-compose
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='recommendations')

    def publish_recommendation(self, recommendation: Recommendation):
        message = {
            "recommendation_id": recommendation.id,
            "recommendation": recommendation.recommendation_text,
            "timestamp": recommendation.timestamp.isoformat()
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key='recommendations',
            body=json.dumps(message)
        )

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()