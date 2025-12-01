"""
Community feed endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
import os
from pydantic import BaseModel

router = APIRouter(tags=["community"])

class QuizSubmissionResponse(BaseModel):
    submission_id: int
    display_name: str
    top_twin_name: str
    match_score: float
    city: str
    state: str
    created_at: str

@router.get("/feed", response_model=List[QuizSubmissionResponse])
async def get_community_feed(limit: int = 20):
    """Get recent quiz submissions"""
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        conn = psycopg2.connect(
            host=db_host,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT submission_id, display_name, top_twin_name,
                       match_score, city, state, created_at
                FROM quiz_submissions
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            
            results = cursor.fetchall()
            
        conn.close()
        
        return [
            QuizSubmissionResponse(
                submission_id=row[0],
                display_name=row[1],
                top_twin_name=row[2],
                match_score=float(row[3]),
                city=row[4],
                state=row[5],
                created_at=row[6].isoformat()
            )
            for row in results
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_community_stats():
    """Get community statistics"""
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        conn = psycopg2.connect(
            host=db_host,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM quiz_submissions")
            total = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM quiz_submissions 
                WHERE DATE(created_at) = CURRENT_DATE
            """)
            today = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(match_score) FROM quiz_submissions")
            avg_score = cursor.fetchone()[0] or 0
            
        conn.close()
        
        return {
            "total_submissions": total,
            "today_submissions": today,
            "average_match_score": round(float(avg_score), 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
