"""
Kafka consumer for processing quiz submissions
"""
from kafka import KafkaConsumer
import json
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matching.matcher import TasteTwinMatcher
import psycopg2
from psycopg2.extras import Json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuizConsumer:
    def __init__(self):
        # Get Kafka bootstrap servers from environment variable
        kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        logger.info(f"Connecting to Kafka at: {kafka_servers}")
        
        self.consumer = KafkaConsumer(
            'quiz-submissions',
            bootstrap_servers=kafka_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='quiz-processing-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        # Database connection
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.matcher = TasteTwinMatcher()
        
    def get_db_connection(self):
        """Create database connection"""
        return psycopg2.connect(
            host=self.db_host,
            database="dinelike",
            user="dinelike",
            password="dinelike123"
        )
    
    def process_submission(self, submission_data):
        """Process a quiz submission"""
        try:
            logger.info(f"Processing submission for: {submission_data.get('display_name')}")
            
            # Find taste twin
            result = self.matcher.find_taste_twin(
                city=submission_data['city'],
                state=submission_data.get('state', 'NC'),
                tags=submission_data['tags']
            )
            
            if not result:
                logger.warning("No taste twin found")
                return
            
            # Store in database
            conn = self.get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO quiz_submissions 
                (display_name, city, state, tags, top_twin_user_id, top_twin_name, match_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                submission_data['display_name'],
                submission_data['city'],
                submission_data.get('state', 'NC'),
                Json(submission_data['tags']),
                result['user_id'],
                result['name'],
                result['match_score']
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"Successfully processed submission. Twin: {result['name']} ({result['match_score']:.2f})")
            
        except Exception as e:
            logger.error(f"Error processing submission: {e}", exc_info=True)
    
    def start_consuming(self):
        """Start consuming messages"""
        logger.info("Starting Kafka consumer...")
        try:
            for message in self.consumer:
                self.process_submission(message.value)
        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    consumer = QuizConsumer()
    consumer.start_consuming()
