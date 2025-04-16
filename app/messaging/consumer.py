import json
import logging

import pika

from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="recommendations.log",
)

logger = logging.getLogger(__name__)


class RecommendationConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.rabbitmq_host,
                port=settings.rabbitmq_port,
                credentials=pika.PlainCredentials(
                    settings.rabbitmq_user, settings.rabbitmq_password
                ),
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=settings.rabbitmq_queue)

    def process_message(self, ch, method, properties, body):
        try:
            message = json.loads(body)

            logger.info(f"Received recommendation: {message}")

            self._send_notification(message)

            self._store_analytics(message)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def _send_notification(self, message):
        logger.info(
            f"SIMULATION: Sending notification for recommendation {message['recommendation_id']}"
            f"\nTo: patient@example.com"
            f"\nSubject: New Clinical Recommendation"
            f"\nBody: {message['recommendation']}"
        )

    def _store_analytics(self, message):
        logger.info(
            f"ANALYTICS: Storing recommendation data"
            f"\nTimestamp: {message['timestamp']}"
            f"\nRecommendation ID: {message['recommendation_id']}"
            f"\nType: {message['recommendation']}"
        )

    def start_consuming(self):
        self.channel.basic_consume(
            queue=settings.rabbitmq_queue, on_message_callback=self.process_message
        )
        logger.info("Consumer started. Waiting for messages...")
        self.channel.start_consuming()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
