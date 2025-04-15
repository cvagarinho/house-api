from app.messaging.consumer import RecommendationConsumer
import sys
import logging

logger = logging.getLogger(__name__)

def main():
    try:
        consumer = RecommendationConsumer()
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
        consumer.close()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()