from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import logging
from ..kafka_producer import get_kafka_producer
import psycopg2
from psycopg2.extras import RealDictCursor
import os

router = APIRouter()
logger = logging.getLogger(__name__)

class QuizSubmission(BaseModel):
    display_name: str
    tags: Dict[str, Any]
    city: str = "Santa Barbara"
    state: str = "CA"

@router.post("/submit")
async def submit_quiz(submission: QuizSubmission):
    """Submit quiz responses"""
    try:
        quiz_message = {
            "display_name": submission.display_name,
            "tags": submission.tags,  # Changed from quiz_tags to tags
            "city": submission.city,
            "state": submission.state,
            "submitted_at": datetime.utcnow().isoformat()
        }
        
        producer = get_kafka_producer()
        success = producer.publish_quiz_submission(quiz_message)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to process quiz")
        
        return {"status": "success", "message": "Quiz submitted!"}
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def quiz_health():
    return {"status": "healthy", "service": "quiz"}

@router.get("/results/latest")
async def get_latest_results():
    """Get the most recent quiz results"""
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        conn = psycopg2.connect(
            host=db_host,
            port=5432,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                submission_id,
                display_name,
                top_twin_name,
                match_score,
                
                created_at
            FROM quiz_submissions
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="No results found")
        
        return dict(result)
        
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        raise HTTPException(status_code=500, detail=str(e))
