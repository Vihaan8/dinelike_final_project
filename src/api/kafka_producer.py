"""
Kafka producer for publishing quiz submissions and user activity events
"""
from kafka import KafkaProducer
import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DineLikeKafkaProducer:
    def __init__(self, bootstrap_servers: str = None):
        """Initialize Kafka producer"""
        if bootstrap_servers is None:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        
        logger.info(f"Initializing Kafka producer with servers: {bootstrap_servers}")
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',  # Wait for all replicas
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            raise

    def publish_quiz_submission(self, quiz_data: Dict[str, Any]) -> bool:
        """
        Publish quiz submission to Kafka
        
        Args:
            quiz_data: Dictionary containing quiz submission data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            future = self.producer.send('quiz-submissions', value=quiz_data)
            record_metadata = future.get(timeout=10)
            logger.info(f"Quiz submission published to topic {record_metadata.topic} partition {record_metadata.partition}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish quiz submission: {e}")
            return False

    def close(self):
        """Close producer connection"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")


def get_kafka_producer() -> DineLikeKafkaProducer:
    """Get or create Kafka producer instance"""
    return DineLikeKafkaProducer()
